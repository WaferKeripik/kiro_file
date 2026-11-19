"""
jsrs_core.py — Fungsi inti perhitungan band (batas bawah/atas) untuk JSRS.

Tujuan modul ini:
  - Murni (pure): tidak membaca file, tidak bergantung pada bentuk data apa pun.
    Masukannya cukup array angka 1 dimensi; keluarannya sebuah Band.
  - Dua metode band dalam satu antarmuka yang sama supaya bisa dibandingkan adil:
      * "robust"  -> pusat = median, sebaran = MAD (Median Absolute Deviation)
      * "classic" -> pusat = mean,   sebaran = std  (standar deviasi sampel)
  - Setiap aturan tambahan dibuat sebagai flag yang bisa dimatikan/dinyalakan,
    sehingga efek tiap aturan bisa diukur terpisah saat backtest.

Lima perbaikan terhadap versi sebelumnya (dirangkum di setiap titik terkait):
  1. Konstanta MAD->sigma = 1.4826 (sebelumnya salah/hilang).
  2. Derajat kebebasan (df) untuk nilai kritis t bisa dikonfigurasi.
  3. MAD floor yang benar: floor = max(MAD, floor_frac * |median|).
  4. Aturan hard-drop 10% dijadikan OPSIONAL (default mati).
  5. Tingkat kepercayaan (confidence) disamakan antar metode via satu sumber
     nilai kritis, agar perbandingan robust vs classic adil.

Catatan: scipy dipakai hanya untuk nilai kritis t bila tersedia. Bila tidak,
modul tetap berjalan dengan tabel fallback (lihat _t_critical).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np

# Perbaikan #1: konstanta konsistensi MAD -> estimasi sigma untuk sebaran normal.
# 1 / Phi^{-1}(0.75) ~= 1.482602218505602. Dengan ini, MAD_scaled ~ sigma
# ketika data mendekati normal, sehingga robust dan classic sebanding.
MAD_TO_SIGMA: float = 1.482602218505602


# --------------------------------------------------------------------------- #
# Konfigurasi
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class BandConfig:
    """Parameter perhitungan band. Semua aturan tambahan berupa flag."""

    method: str = "robust"            # "robust" | "classic"
    confidence: float = 0.95          # tingkat kepercayaan dua sisi (0<c<1)

    # Perbaikan #2: df untuk nilai kritis t.
    #   None -> df diturunkan dari ukuran sampel (n - 1), minimal 1.
    #   int  -> df tetap (dipaksa), berguna untuk membandingkan metode secara adil.
    t_df: Optional[int] = None

    # Perbaikan #5: paksa df sama untuk kedua metode agar nilai kritis identik.
    # Jika True, kedua metode memakai df dari classic (n-1) kecuali t_df diset.
    equalize_confidence: bool = True

    # Perbaikan #3: MAD floor. floor_frac dipakai sebagai fraksi dari |median|.
    # Sebaran efektif = max(scale, floor_frac * |center|). 0 berarti tanpa floor.
    floor_frac: float = 0.0

    # Perbaikan #4: aturan hard-drop. Jika True, buang `hard_drop_frac` bagian
    # ekor terbesar (berdasarkan |x - center|) sebelum menghitung sebaran.
    # Default MATI agar tidak diam-diam mengubah hasil.
    hard_drop_enabled: bool = False
    hard_drop_frac: float = 0.10      # 10% bila diaktifkan

    # Batas minimal jumlah titik valid untuk menghasilkan band.
    min_points: int = 2

    def validate(self) -> None:
        if self.method not in ("robust", "classic"):
            raise ValueError(f"method tidak dikenal: {self.method!r}")
        if not (0.0 < self.confidence < 1.0):
            raise ValueError("confidence harus di antara 0 dan 1 (eksklusif)")
        if self.t_df is not None and self.t_df < 1:
            raise ValueError("t_df harus >= 1 bila diisi")
        if self.floor_frac < 0.0:
            raise ValueError("floor_frac tidak boleh negatif")
        if not (0.0 <= self.hard_drop_frac < 0.5):
            raise ValueError("hard_drop_frac harus di [0, 0.5)")
        if self.min_points < 1:
            raise ValueError("min_points harus >= 1")


@dataclass(frozen=True)
class Band:
    """Hasil perhitungan band untuk satu kumpulan nilai."""

    center: float
    scale: float          # sebaran efektif setelah floor/drop (skala sigma)
    lower: float
    upper: float
    n: int                # jumlah titik valid yang dipakai
    n_dropped: int        # jumlah titik dibuang oleh hard-drop
    t_crit: float         # nilai kritis t yang dipakai
    method: str
    confidence: float
    valid: bool           # True bila band dapat dihitung

    def contains(self, x: float) -> bool:
        """Apakah nilai x berada di dalam band (inklusif)."""
        if not self.valid:
            return False
        return self.lower <= x <= self.upper

    def as_dict(self) -> dict:
        return {
            "center": self.center,
            "scale": self.scale,
            "lower": self.lower,
            "upper": self.upper,
            "n": self.n,
            "n_dropped": self.n_dropped,
            "t_crit": self.t_crit,
            "method": self.method,
            "confidence": self.confidence,
            "valid": self.valid,
        }


# --------------------------------------------------------------------------- #
# Utilitas internal
# --------------------------------------------------------------------------- #
def _clean(values: Sequence[float]) -> np.ndarray:
    """Ubah ke array float dan buang NaN/inf."""
    arr = np.asarray(values, dtype=float).ravel()
    return arr[np.isfinite(arr)]


def _t_critical(confidence: float, df: int) -> float:
    """
    Nilai kritis t dua sisi untuk tingkat kepercayaan `confidence`.
    Memakai scipy bila ada; jika tidak, memakai tabel fallback + aproksimasi.
    """
    alpha = 1.0 - confidence
    q = 1.0 - alpha / 2.0  # kuantil dua sisi
    try:
        from scipy.stats import t as _t  # impor lokal agar modul tetap jalan tanpa scipy
        return float(_t.ppf(q, df))
    except Exception:
        # Fallback: tabel t untuk confidence umum, lalu pakai nilai z untuk df besar.
        _Z = {0.90: 1.6448536, 0.95: 1.9599640, 0.975: 2.2414027, 0.99: 2.5758293}
        z = _Z.get(round(confidence, 3), 1.9599640)
        if df >= 1000:
            return z
        # Koreksi Peizer-Pratt sederhana agar sedikit lebih besar dari z pada df kecil.
        return z * (1.0 + (z * z + 1.0) / (4.0 * df))


def _scale_robust(x: np.ndarray, center: float) -> float:
    """MAD terskala menjadi estimasi sigma (perbaikan #1)."""
    mad = float(np.median(np.abs(x - center)))
    return MAD_TO_SIGMA * mad


def _scale_classic(x: np.ndarray) -> float:
    """Standar deviasi sampel (ddof=1)."""
    if x.size < 2:
        return 0.0
    return float(np.std(x, ddof=1))


def _apply_hard_drop(x: np.ndarray, center: float, frac: float) -> tuple[np.ndarray, int]:
    """
    Perbaikan #4: buang `frac` bagian titik terjauh dari center (berdasarkan
    jarak absolut). Mengembalikan (array_tersisa, jumlah_dibuang).
    """
    n = x.size
    k = int(np.floor(frac * n))
    if k <= 0:
        return x, 0
    order = np.argsort(np.abs(x - center))  # dekat -> jauh
    keep = order[: n - k]
    return x[np.sort(keep)], k


# --------------------------------------------------------------------------- #
# API utama
# --------------------------------------------------------------------------- #
def compute_band(values: Sequence[float], config: BandConfig = BandConfig()) -> Band:
    """
    Hitung band dari sekumpulan nilai historis.

    Alur:
      1. Bersihkan data (buang NaN/inf).
      2. Tentukan center (median untuk robust, mean untuk classic).
      3. (opsional) hard-drop titik ekor terjauh.
      4. Hitung sebaran (MAD terskala atau std), terapkan floor.
      5. Tentukan df dan nilai kritis t (disamakan antar metode bila diminta).
      6. lower/upper = center -/+ t_crit * scale.
    """
    config.validate()
    x = _clean(values)
    n = x.size

    if n < config.min_points:
        return Band(
            center=float(np.median(x)) if n else float("nan"),
            scale=0.0, lower=float("nan"), upper=float("nan"),
            n=n, n_dropped=0, t_crit=float("nan"),
            method=config.method, confidence=config.confidence, valid=False,
        )

    # Langkah 2: center sesuai metode.
    if config.method == "robust":
        center = float(np.median(x))
    else:
        center = float(np.mean(x))

    # Langkah 3: hard-drop opsional (perbaikan #4).
    n_dropped = 0
    if config.hard_drop_enabled and config.hard_drop_frac > 0.0:
        x_used, n_dropped = _apply_hard_drop(x, center, config.hard_drop_frac)
        # Hitung ulang center pada data tersisa supaya konsisten.
        center = float(np.median(x_used)) if config.method == "robust" else float(np.mean(x_used))
    else:
        x_used = x

    # Langkah 4: sebaran + floor (perbaikan #3).
    if config.method == "robust":
        scale = _scale_robust(x_used, center)
    else:
        scale = _scale_classic(x_used)

    if config.floor_frac > 0.0:
        scale = max(scale, config.floor_frac * abs(center))

    # Langkah 5: df + nilai kritis t (perbaikan #2 dan #5).
    if config.t_df is not None:
        df = config.t_df
    else:
        # df alami = n_efektif - 1. Saat equalize_confidence, pakai df berbasis
        # ukuran sampel yang sama untuk kedua metode (perbaikan #5).
        n_eff = x_used.size
        df = max(1, n_eff - 1)

    t_crit = _t_critical(config.confidence, df)

    lower = center - t_crit * scale
    upper = center + t_crit * scale

    return Band(
        center=center, scale=scale, lower=lower, upper=upper,
        n=x_used.size, n_dropped=n_dropped, t_crit=t_crit,
        method=config.method, confidence=config.confidence, valid=True,
    )


def band_robust(values: Sequence[float], confidence: float = 0.95, **kwargs) -> Band:
    """Pintasan: band metode robust (median + MAD)."""
    return compute_band(values, BandConfig(method="robust", confidence=confidence, **kwargs))


def band_classic(values: Sequence[float], confidence: float = 0.95, **kwargs) -> Band:
    """Pintasan: band metode classic (mean + std)."""
    return compute_band(values, BandConfig(method="classic", confidence=confidence, **kwargs))


if __name__ == "__main__":
    # Contoh cepat & pemeriksaan mandiri (tanpa file data).
    rng = np.random.default_rng(0)
    base = rng.normal(100.0, 5.0, size=24)
    data = np.concatenate([base, [180.0]])  # satu outlier

    rb = band_robust(data)
    cl = band_classic(data)
    print("ROBUST :", {k: round(v, 3) if isinstance(v, float) else v for k, v in rb.as_dict().items()})
    print("CLASSIC:", {k: round(v, 3) if isinstance(v, float) else v for k, v in cl.as_dict().items()})
    print("outlier 180 di band robust? ", rb.contains(180.0))
    print("outlier 180 di band classic?", cl.contains(180.0))
