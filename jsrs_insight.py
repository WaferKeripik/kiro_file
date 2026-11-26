"""
jsrs_insight.py — Analisis lanjutan untuk 3 aspek nyata:
  1. Deteksi TYPO input (titik-koma tertukar / kelebihan nol) — anomali buatan manusia.
  2. Energi MUSIMAN / event (banyak bulan kosong) — jangan salah vonis.
  3. Pemisahan band per JENIS PEMAKAIAN (Production vs Domestic).

Dipakai oleh slide & dashboard. Semua angka dari data produksi nyata.
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
from jsrs_core import compute_band, BandConfig
from jsrs_loader import load_raw_block, unit_key

def _D(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (here, os.path.join(here, "kiro_file")):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    return name

FILES = [
    ("Listrik FY2025", "Listrik FY 25 (CEK RUMUS)-Training.csv", 2025),
    ("Listrik FY2024", "Listrik FY 2024 (CEK RUMUS)-Training.csv", 2024),
    ("NonRenew FY2025", "Non Renewable Energy FY 25 (CEK RUMUS)-Training.csv", 2025),
    ("NonRenew FY2024", "Non-Renewable Energy FY 2024 (CEK RUMUS)-Training.csv", 2024),
]


# --------------------------------------------------------------------------- #
# 1. DETEKSI TYPO (kelebihan nol / salah pemisah ribuan-desimal)
# --------------------------------------------------------------------------- #
def detect_typos(path, year, factor=8.0):
    """
    Typo khas input energi:
      - kelebihan 1 nol  -> nilai ~10x median
      - kurang 1 nol     -> nilai ~1/10 median
      - titik/koma tertukar (mis. 1.234 jadi 1234) -> lompatan ~10x/100x/1000x

    Heuristik: untuk tiap unit, bandingkan tiap bulan terhadap MEDIAN robust unit.
    Jika rasio nilai/median (atau kebalikannya) >= `factor` DAN titik lain stabil,
    tandai sebagai 'kandidat typo' dengan dugaan pola (x10, x100, /10).
    """
    res = load_raw_block(path, year)
    rows = []
    for _, grp in res.long.groupby("row_id"):
        grp = grp.sort_values("month_idx")
        v = grp["consumption"].to_numpy(float)
        finite = v[np.isfinite(v)]
        if finite.size < 6:
            continue
        med = np.median(finite[finite > 0]) if np.any(finite > 0) else 0.0
        if med <= 0:
            continue
        for i, x in enumerate(v):
            if not np.isfinite(x) or x <= 0:
                continue
            ratio = x / med
            pola = None
            if 8 <= ratio < 20:
                pola = "kelebihan 1 nol (x10)"
            elif 80 <= ratio < 200:
                pola = "x100 (salah pemisah ribuan)"
            elif 800 <= ratio < 2000:
                pola = "x1000"
            elif 0.05 < ratio <= 0.125:
                pola = "kurang 1 nol (/10)"
            if pola:
                rows.append({
                    "unit": " | ".join(str(grp[c].iloc[0]) for c in res.dim_cols if c in grp.columns),
                    "bulan": grp["month"].iloc[i],
                    "nilai": x, "median_unit": med, "rasio": ratio, "dugaan": pola,
                })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 2. POLA MUSIMAN / BANYAK KOSONG
# --------------------------------------------------------------------------- #
def seasonality_profile(path, year):
    """
    Klasifikasi tiap unit berdasar jumlah bulan terisi:
      - 'penuh'    : 10-12 bulan ada data
      - 'musiman'  : 3-9 bulan ada data (produksi musiman / event)
      - 'jarang'   : 1-2 bulan (hampir tidak dipakai)
      - 'kosong'   : 0 bulan
    Band hanya layak dihitung untuk 'penuh' dan sebagian 'musiman' (>=3 titik).
    """
    res = load_raw_block(path, year)
    counts = {"penuh": 0, "musiman": 0, "jarang": 0, "kosong": 0}
    for _, grp in res.long.groupby("row_id"):
        n = int(np.isfinite(grp["consumption"].to_numpy(float)).sum())
        if n == 0:
            counts["kosong"] += 1
        elif n <= 2:
            counts["jarang"] += 1
        elif n <= 9:
            counts["musiman"] += 1
        else:
            counts["penuh"] += 1
    return counts


# --------------------------------------------------------------------------- #
# 3. BAND TERPISAH PER JENIS PEMAKAIAN (Production vs Domestic)
# --------------------------------------------------------------------------- #
def band_by_usage(path, year, confidence=0.95):
    """
    Bukti bahwa Production dan Domestic HARUS punya band terpisah:
    untuk unit yang punya KEDUA jenis, bandingkan skala (median) keduanya.
    Jika rasio median jauh dari 1, menyatukan band akan salah total.
    """
    res = load_raw_block(path, year)
    long = res.long
    # kunci unit tanpa Usage Type
    base_dims = [c for c in res.dim_cols if c != "Usage Type"]
    long = long.copy()
    long["_base"] = long[base_dims].astype(str).agg(" | ".join, axis=1)
    rows = []
    for base, grp in long.groupby("_base"):
        usages = grp["Usage Type"].unique()
        if not ({"For Production Use", "For Domestic Use"} <= set(usages)):
            continue
        med = {}
        for u in ("For Production Use", "For Domestic Use"):
            vv = grp[grp["Usage Type"] == u]["consumption"].to_numpy(float)
            vv = vv[np.isfinite(vv) & (vv > 0)]
            if vv.size >= 3:
                med[u] = float(np.median(vv))
        if len(med) == 2 and med["For Domestic Use"] > 0:
            rows.append({
                "unit": base,
                "median_production": med["For Production Use"],
                "median_domestic": med["For Domestic Use"],
                "rasio_prod_dom": med["For Production Use"] / med["For Domestic Use"],
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 170); pd.set_option("display.max_columns", 20)

    print("="*70, "\n1. KANDIDAT TYPO (kelebihan nol / salah pemisah)\n", "="*70, sep="")
    all_typo = []
    for label, fn, yr in FILES:
        t = detect_typos(_D(fn), yr)
        if not t.empty:
            t.insert(0, "dataset", label)
            all_typo.append(t)
    typo = pd.concat(all_typo, ignore_index=True) if all_typo else pd.DataFrame()
    if not typo.empty:
        print(f"Total kandidat typo: {len(typo)}")
        print(typo["dugaan"].value_counts().to_string())
        print("\nContoh (10 teratas berdasar rasio):")
        print(typo.sort_values("rasio", ascending=False)
              .head(10)[["dataset","unit","bulan","nilai","median_unit","rasio","dugaan"]].to_string(index=False))
        typo.to_csv(_D("typo_candidates.csv"), index=False)
        print(f"\nDisimpan: typo_candidates.csv")

    print("\n", "="*70, "\n2. PROFIL MUSIMAN / BANYAK KOSONG\n", "="*70, sep="")
    for label, fn, yr in FILES:
        c = seasonality_profile(_D(fn), yr)
        tot = sum(c.values())
        print(f"{label:<16}: penuh={c['penuh']}  musiman={c['musiman']}  "
              f"jarang={c['jarang']}  kosong={c['kosong']}  (total {tot})")

    print("\n", "="*70, "\n3. PRODUCTION vs DOMESTIC — perlu band terpisah?\n", "="*70, sep="")
    for label, fn, yr in FILES[:1] + FILES[2:3]:
        b = band_by_usage(_D(fn), yr)
        if b.empty:
            continue
        print(f"\n{label}: {len(b)} unit punya kedua jenis pemakaian")
        print(f"  Rasio median Production/Domestic — median: {b['rasio_prod_dom'].median():.1f}x, "
              f"maks: {b['rasio_prod_dom'].max():.0f}x")
        print("  Contoh 5 unit dengan selisih terbesar:")
        print(b.sort_values("rasio_prod_dom", ascending=False)
              .head(5).to_string(index=False))
