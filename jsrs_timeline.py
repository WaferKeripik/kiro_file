"""
jsrs_timeline.py — Model waktu siklus anomali: alur LAMA vs BARU.

Alur LAMA (end-to-end per anomali), dua tahap berurutan:
  Tahap 1 (deteksi -> unit dapat notif): HO deteksi di QlikSense -> Division PIC cek di
           BI Sustainalytics -> kirim form/email -> diskusi.  ~5-10 hari kerja.
  Tahap 2 (investigasi -> corrective action -> status 'OK with Notes'): di luar sistem
           (email/chat/call), Division PIC <-> Corporate PIC.  ~5-10 hari kerja.
  Total  : ~10-20 hari kerja per anomali.
  Pengganda: karena band LCL/UCL bergerak tiap bulan, anomali bulan yang sama bisa
             dipertanyakan berulang (DIHITUNG dari data: rata-rata 4.3x).

Alur BARU:
  - SR Admin melihat vonis SAAT input dan mengisi alasan saat itu juga (Tahap 1 ~ 0 hari).
  - Jika typo: diperbaiki langsung di JSRS, tanpa lewat Corporate (kedua tahap terpotong).
  - Jika akurat: alasan sudah terlampir -> Tahap 2 menyusut (diskusi minimal) & TIDAK
    berulang karena vonis bulan lama tidak bergerak.

Semua durasi di sini ASUMSI (rentang yang Anda berikan). Pengganda 4.3x DIHITUNG dari data.
"""
from __future__ import annotations
import numpy as np

# ---- Parameter durasi (hari kerja). ASUMSI dari narasi proses bisnis. ----
T1 = (5, 10)   # tahap 1: deteksi -> unit dapat notif
T2 = (5, 10)   # tahap 2: investigasi -> corrective action -> 'OK with Notes'

# ---- Dihitung dari data (lihat jsrs_rolling / analisis pertanyaan berulang). ----
REPEAT_OLD = 4.3      # rata-rata satu anomali dipertanyakan ulang (band bergerak)
ANOM_UNIK = 431       # bulan-unit anomali unik (akhir tahun, data energi FY2025)

# ---- Asumsi proporsi penyebab anomali (untuk ilustrasi; ganti bila ada data). ----
FRAC_TYPO = 0.20      # perkiraan anomali karena salah input (dari 274 kandidat typo)


def old_cycle_days():
    lo = (T1[0] + T2[0]); hi = (T1[1] + T2[1])
    return lo, hi  # per satu putaran, end-to-end


def old_total_per_anomaly():
    """Dengan pengulangan karena band bergerak."""
    lo, hi = old_cycle_days()
    return lo, hi, lo * REPEAT_OLD, hi * REPEAT_OLD


def new_cycle_days():
    """
    Alur baru:
      - Tahap 1 ~ 0 (admin tahu saat input).
      - typo: 0 hari lewat Corporate (perbaiki di JSRS).
      - akurat: Tahap 2 menyusut (alasan terlampir) -> ambil 1-3 hari, TANPA pengulangan.
    """
    t2_new = (1, 3)
    return t2_new


def summary():
    lo, hi = old_cycle_days()
    _, _, lo_rep, hi_rep = old_total_per_anomaly()
    t2n = new_cycle_days()
    print("="*70)
    print("MODEL WAKTU SIKLUS ANOMALI — LAMA vs BARU  (hari kerja)")
    print("="*70)
    print(f"[ASUMSI] Tahap 1 (deteksi->notif ke unit)      : {T1[0]}-{T1[1]} hari")
    print(f"[ASUMSI] Tahap 2 (investigasi->corrective->OKN): {T2[0]}-{T2[1]} hari")
    print(f"[ASUMSI] LAMA, satu putaran end-to-end          : {lo}-{hi} hari")
    print(f"[DATA ] Pengganda pengulangan (band bergerak)   : {REPEAT_OLD}x")
    print(f"[GABUNG] LAMA, efektif per anomali (x{REPEAT_OLD})      : {lo_rep:.0f}-{hi_rep:.0f} hari")
    print()
    print(f"[ASUMSI] BARU, Tahap 1                           : ~0 hari (tahu saat input)")
    print(f"[ASUMSI] BARU, typo -> perbaiki di JSRS          : ~0 hari lewat Corporate")
    print(f"[ASUMSI] BARU, akurat -> Tahap 2 menyusut        : {t2n[0]}-{t2n[1]} hari, TANPA pengulangan")
    print()
    # estimasi penghematan agregat (ilustrasi, energi FY2025)
    typo = int(ANOM_UNIK * FRAC_TYPO)
    akurat = ANOM_UNIK - typo
    old_days = ANOM_UNIK * np.mean([lo, hi]) * REPEAT_OLD
    new_days = typo * 0 + akurat * np.mean(t2n)
    print(f"[ILUSTRASI] {ANOM_UNIK} anomali unik; ~{FRAC_TYPO:.0%} typo ({typo}) + {akurat} akurat")
    print(f"  Total hari-siklus LAMA (approx)  : {old_days:,.0f} hari")
    print(f"  Total hari-siklus BARU (approx)  : {new_days:,.0f} hari")
    print(f"  Penghematan relatif              : {(1-new_days/old_days)*100:.0f}%")
    print("  (ilustrasi; durasi=ASUMSI, jumlah anomali & 4.3x=DATA, %typo=perkiraan)")


if __name__ == "__main__":
    summary()
