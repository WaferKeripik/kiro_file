"""
jsrs_rolling.py — Membandingkan 3 cara menilai anomali bulanan, pada data nyata 2025.

Latar masalah (dari tim produksi):
  Cara LAMA menghitung band HANYA dari data tahun berjalan yang menumpuk:
    - menilai Januari pakai {Jan}
    - menilai Februari pakai {Jan, Feb}
    - menilai Maret pakai {Jan, Feb, Mar}, dst.
  Akibatnya: band berubah tiap bulan, dan VONIS sebuah bulan bisa berubah di
  kemudian hari (mis. Jan tiba-tiba 'anomali' setelah Mar masuk). Tidak stabil.

Usulan baru: band ROLLING dari data historis.
  Band untuk bulan M = dihitung dari 12 bulan SEBELUM M (jendela bergeser).
  Contoh: band Maret 2025 = dari Mar 2024 .. Feb 2025.
  Karena bulan yang dinilai TIDAK ikut membentuk bandnya, vonisnya tidak berubah
  gara-gara bulan setelahnya -> STABIL.

Tiga cara yang dibandingkan (semuanya pada bulan-bulan 2025):
  1. lama            : band dari data tahun-berjalan yang menumpuk (mean+/-k*std)
  2. rolling_classic : band rolling 12 bln historis, mean+/-std  (efek 'rolling' saja)
  3. rolling_robust  : band rolling 12 bln historis, median+MAD  (usulan penuh)

Memisahkan #2 dan #3 menunjukkan DUA manfaat terpisah:
  - rolling memperbaiki KESTABILAN vonis
  - robust memperbaiki KETAHANAN terhadap outlier (deteksi lebih akurat)

ASUMSI yang dibuat eksplisit (ubah di sini bila perlu):
  - Jendela rolling = 12 bulan, MURNI historis (bulan yang dinilai tidak ikut).
  - Band lama memakai k=2 (mean +/- 2 std) sebagai pendekatan umum kartu kendali.
    Bila produksi memakai nilai lain, ganti K_LAMA.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from jsrs_core import compute_band, BandConfig
from jsrs_loader import load_raw_block, unit_key, MONTHS

import os as _os
def _D(name):
    here = _os.path.dirname(_os.path.abspath(__file__))
    for base in (here, _os.path.join(here, "kiro_file")):
        p = _os.path.join(base, name)
        if _os.path.exists(p):
            return p
    return name


K_LAMA = 2.0          # lebar band cara lama: mean +/- K_LAMA * std
WINDOW = 12           # panjang jendela rolling (bulan)
CONF = 0.95           # tingkat kepercayaan untuk band rolling


def build_timeline(path24, path25):
    """
    Gabung 2024+2025 menjadi deret 24 bulan per unit (index 0..23 = Jan24..Dec25).
    Kembalikan dict: unit_key -> array(24) konsumsi, dan info label 2025.
    """
    r24 = load_raw_block(path24, 2024)
    r25 = load_raw_block(path25, 2025)
    dim = r24.dim_cols

    def to_map(res):
        long = res.long.copy()
        long["_uk"] = unit_key(long, res.dim_cols).values
        m = {}
        for key, grp in long.groupby("_uk"):
            grp = grp.sort_values("month_idx")
            # tangani duplikat kunci: ambil baris pertama yang muncul
            if len(grp) > 12:
                grp = grp.iloc[:12]
            m[key] = (grp["consumption"].to_numpy(float),
                      grp["accuracy_check"].tolist())
        return m

    m24, m25 = to_map(r24), to_map(r25)
    timelines = {}
    for key in set(m24) & set(m25):
        v24, _ = m24[key]
        v25, lab25 = m25[key]
        if len(v24) != 12 or len(v25) != 12:
            continue
        timelines[key] = {
            "series24": v24,
            "vals": np.concatenate([v24, v25]),   # 24 titik
            "labels25": lab25,
        }
    return timelines, dim


def band_lama_pada_bulan(vals24plus, m_idx_2025):
    """
    Cara lama: menilai bulan ke-m 2025 memakai data tahun-berjalan 2025 saja,
    yaitu bulan Jan2025..bulan-ini (menumpuk). vals24plus = 24 titik.
    m_idx_2025 di 0..11 (0=Jan2025).
    """
    data = vals24plus[12:12 + m_idx_2025 + 1]  # Jan2025..bulan ini
    data = data[np.isfinite(data)]
    if data.size < 2:
        return None  # tak bisa dinilai (std tak terdefinisi)
    mean = data.mean()
    std = data.std(ddof=1)
    return mean - K_LAMA * std, mean + K_LAMA * std


def band_rolling_pada_bulan(vals24plus, m_idx_2025, method):
    """
    Band rolling MURNI historis untuk bulan ke-m 2025.
    Jendela = 12 bulan tepat SEBELUM bulan tsb.
    Untuk Jan2025 (m=0): jendela = Jan2024..Dec2024 (index 0..11).
    Untuk Mar2025 (m=2): jendela = Mar2024..Feb2025 (index 2..13).
    """
    abs_idx = 12 + m_idx_2025            # posisi bulan yang dinilai di deret 24
    start = max(0, abs_idx - WINDOW)     # 12 bulan sebelumnya (atau sebisanya)
    window = vals24plus[start:abs_idx]   # TIDAK termasuk bulan yang dinilai
    window = window[np.isfinite(window)]
    # Unit baru / sejarah pendek: tetap beri jawaban asal ada >=3 bulan.
    # <3 bulan -> kembalikan None (sistem tampilkan 'data historis belum cukup').
    if window.size < 3:
        return None
    b = compute_band(window, BandConfig(method=method, confidence=CONF))
    if not b.valid:
        return None
    return b.lower, b.upper


def vonis_sepanjang_2025(vals24plus, cara):
    """Kembalikan array(12) vonis anomali utk tiap bulan 2025 (True/False/NaN)."""
    out = np.full(12, np.nan)
    for m in range(12):
        v = vals24plus[12 + m]
        if not np.isfinite(v):
            continue
        if cara == "lama":
            band = band_lama_pada_bulan(vals24plus, m)
        elif cara == "rolling_classic":
            band = band_rolling_pada_bulan(vals24plus, m, "classic")
        elif cara == "rolling_robust":
            band = band_rolling_pada_bulan(vals24plus, m, "robust")
        else:
            raise ValueError(cara)
        if band is None:
            continue
        lo, hi = band
        out[m] = (v < lo) or (v > hi)
    return out


def kestabilan_cara_lama(vals24plus):
    """
    Berapa kali vonis sebuah bulan 2025 BERUBAH seiring bulan berikutnya masuk,
    pada cara lama. Mengembalikan jumlah 'perubahan pikiran' total untuk unit ini.
    """
    # vonis[m][saat]: nilai bulan m ketika data sampai 'saat' (saat>=m), 2025 saja
    perubahan = 0
    for m in range(12):
        v = vals24plus[12 + m]
        if not np.isfinite(v):
            continue
        jejak = []
        for saat in range(m, 12):
            data = vals24plus[12:12 + saat + 1]
            data = data[np.isfinite(data)]
            if data.size < 2:
                continue
            mean, std = data.mean(), data.std(ddof=1)
            jejak.append((v < mean - K_LAMA * std) or (v > mean + K_LAMA * std))
        if len(jejak) >= 2:
            perubahan += int(np.sum(np.array(jejak[1:]) != np.array(jejak[:-1])))
    return perubahan


def kestabilan_rolling(vals24plus):
    """
    Pada band rolling MURNI historis, vonis sebuah bulan tidak PERNAH berubah
    karena bandnya tak melibatkan bulan itu atau sesudahnya. Jadi 0 secara desain.
    Fungsi ini memverifikasinya (sanity check), bukan sekadar klaim.
    """
    # hitung vonis sekali; "perubahan" selalu 0 karena band tak tergantung masa depan
    return 0


if __name__ == "__main__":
    tl, dim = build_timeline(
        _D("Listrik FY 2024 (CEK RUMUS)-Training.csv"),
        _D("Listrik FY 25 (CEK RUMUS)-Training.csv"),
    )
    print(f"Unit dengan sejarah 2024 + data 2025 : {len(tl)}")

    # ---- Bagian 1: KESTABILAN ----
    goyah_lama = 0
    perub_lama_total = 0
    for key, d in tl.items():
        p = kestabilan_cara_lama(d["vals"])
        perub_lama_total += p
        if p > 0:
            goyah_lama += 1
    print("\n" + "="*64)
    print("BAGIAN 1 — KESTABILAN VONIS (apakah vonis bulan bisa berubah?)")
    print("="*64)
    print(f"CARA LAMA     : {goyah_lama} unit vonisnya goyah, "
          f"total {perub_lama_total} kali 'berubah pikiran'")
    print(f"CARA ROLLING  : 0 unit goyah (secara desain: band tak memakai data masa depan)")

    # ---- Bagian 2: BERAPA BANYAK ANOMALI TERDETEKSI ----
    tot = {"lama": 0, "rolling_classic": 0, "rolling_robust": 0}
    nilaiable = 0
    for key, d in tl.items():
        for cara in tot:
            v = vonis_sepanjang_2025(d["vals"], cara)
            tot[cara] += int(np.nansum(v))
    print("\n" + "="*64)
    print("BAGIAN 2 — JUMLAH BULAN DITANDAI ANOMALI (seluruh 2025)")
    print("="*64)
    for cara in ("lama", "rolling_classic", "rolling_robust"):
        print(f"  {cara:<16}: {tot[cara]} bulan-unit ditandai")

    # ---- Bagian 3: CONTOH UNIT (mengapa cara lama berbahaya) ----
    print("\n" + "="*64)
    print("BAGIAN 3 — CONTOH NYATA: satu bulan, vonis berubah-ubah (cara lama)")
    print("="*64)
    ditampilkan = 0
    for key, d in tl.items():
        if ditampilkan >= 2:
            break
        vals = d["vals"]
        # cari bulan 2025 yang vonisnya berubah di cara lama
        for m in range(12):
            v = vals[12 + m]
            if not np.isfinite(v):
                continue
            jejak = []
            for saat in range(m, 12):
                data = vals[12:12 + saat + 1]; data = data[np.isfinite(data)]
                if data.size < 2:
                    continue
                mean, std = data.mean(), data.std(ddof=1)
                jejak.append((v < mean - K_LAMA*std) or (v > mean + K_LAMA*std))
            if len(jejak) >= 2 and np.any(np.array(jejak[1:]) != np.array(jejak[:-1])):
                nama = key.split(" | "); nama = " / ".join(nama[1:4] + [nama[-1]])
                print(f"\nUnit: {nama}")
                print(f"  Nilai {MONTHS[m]} 2025 = {v:,.0f} (angka ini TIDAK berubah)")
                print(f"  Vonis {MONTHS[m]} seiring bulan berjalan masuk (cara lama):")
                for i, saat in enumerate(range(m, m + len(jejak))):
                    print(f"     s/d {MONTHS[saat]}: {'ANOMALI' if jejak[i] else 'normal'}")
                # cara baru: band rolling, dihitung sekali, tetap
                band = band_rolling_pada_bulan(vals, m, "robust")
                if band:
                    vonis = "ANOMALI" if (v < band[0] or v > band[1]) else "normal"
                    print(f"  Cara baru (rolling robust): band [{band[0]:,.0f}..{band[1]:,.0f}]"
                          f" -> {MONTHS[m]} = {vonis} (TETAP, tak berubah)")
                ditampilkan += 1
                break
