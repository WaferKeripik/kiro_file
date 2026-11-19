"""
jsrs_eval.py — Perbandingan NETRAL keandalan band: robust t-PI vs classic vs Excel LCL/UCL.

Mengapa modul ini ada:
  Label 'Accuracy Check' Excel ternyata diturunkan dari LCL/UCL itu sendiri
  (titik di luar band -> selalu 'With Notes'; dibuktikan di analisis terpisah).
  Maka memakai label Excel sebagai "kebenaran" membuat Excel menang otomatis
  (precision 1.0 yang tautologis). Modul ini menilai tanpa memakai label Excel.

Tiga sudut penilaian:

  A. ROBUSTNESS (ground truth sintetis).
     Kita tahu cara Excel menghitung band dari data: band = mean/median +/- k*spread,
     in-sample. Kelemahan klasik metode non-robust: satu-dua outlier ekstrem
     menggelembungkan std sehingga anomali LAIN tak terdeteksi (masking), atau
     menggeser pusat sehingga titik normal tertandai (swamping).
     Kita suntik outlier terkendali ke seri stabil sintetis dan ukur deteksi.

  B. COVERAGE pada seri stabil nyata.
     Ambil seri yang labelnya semua 'OK' (dianggap normal oleh produksi).
     Band yang baik seharusnya memuat ~confidence (mis. 95%) titik — tidak
     terlalu lebar (melewatkan semua) atau terlalu sempit (menandai yang normal).

  C. KETIDAKSEPAKATAN nyata.
     Tunjukkan seri di mana robust menandai titik yang Excel/classic lewatkan,
     atau sebaliknya — supaya bisa dinilai manusia mana yang benar.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from jsrs_core import compute_band, BandConfig
from jsrs_loader import load_raw_block

import os as _os
def _D(name):
    here = _os.path.dirname(_os.path.abspath(__file__))
    for base in (here, _os.path.join(here, "kiro_file")):
        p = _os.path.join(base, name)
        if _os.path.exists(p):
            return p
    return name



# --------------------------------------------------------------------------- #
# A. Robustness dengan ground-truth sintetis
# --------------------------------------------------------------------------- #
def robustness_sim(n_series=4000, n_months=12, confidence=0.95, seed=7):
    """
    Bangun seri stabil (normal) lalu suntik 1 outlier nyata pada sebagian seri.
    Ukur, untuk tiap metode band in-sample:
      - detect  : outlier yang benar tertangkap (recall terhadap outlier sintetis)
      - false   : titik normal yang salah ditandai (per seri bersih)
    'excel-like' = classic (mean +/- z*std) karena LCL/UCL bergaya simetris sekitar
    rata-rata; kita bandingkan robust vs gaya itu memakai nilai kritis sama.
    """
    rng = np.random.default_rng(seed)
    z = 1.959963985  # ~95% dua sisi, dipakai sama untuk semua agar adil

    res = {"robust": {"tp": 0, "fn": 0, "fp": 0, "clean_pts": 0, "outl": 0},
           "classic": {"tp": 0, "fn": 0, "fp": 0, "clean_pts": 0, "outl": 0}}

    for i in range(n_series):
        mu = rng.uniform(50, 5000)
        sigma = mu * rng.uniform(0.03, 0.15)   # variasi bulanan wajar 3-15%
        x = rng.normal(mu, sigma, n_months)

        inject = (i % 2 == 0)  # separuh seri diberi 1 outlier
        truth = np.zeros(n_months, dtype=bool)
        if inject:
            j = rng.integers(0, n_months)
            # outlier jelas: 5-9 sigma dari mean sejati
            x[j] = mu + rng.choice([-1, 1]) * rng.uniform(5, 9) * sigma
            truth[j] = True

        for method in ("robust", "classic"):
            b = compute_band(x, BandConfig(method=method, confidence=confidence, t_df=10**9))
            # paksa z-sama via t_df besar -> t_crit ~ z, perbandingan adil
            lo, hi = b.lower, b.upper
            outside = (x < lo) | (x > hi)
            # titik outlier sintetis
            res[method]["tp"] += int(np.sum(outside & truth))
            res[method]["fn"] += int(np.sum(~outside & truth))
            res[method]["outl"] += int(truth.sum())
            # titik normal (bukan outlier sintetis) yang salah ditandai
            res[method]["fp"] += int(np.sum(outside & ~truth))
            res[method]["clean_pts"] += int(np.sum(~truth))

    rows = []
    for m in ("robust", "classic"):
        d = res[m]
        recall = d["tp"] / d["outl"] if d["outl"] else float("nan")
        far = d["fp"] / d["clean_pts"] if d["clean_pts"] else float("nan")  # false alarm rate
        rows.append({"method": m, "outlier_recall": recall,
                     "false_alarm_rate": far,
                     "outliers_total": d["outl"], "clean_points": d["clean_pts"]})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# B. Coverage pada seri stabil nyata
# --------------------------------------------------------------------------- #
def coverage_on_stable(path, year, confidence=0.95, min_mean=1.0):
    """
    Pada seri NYATA yang semua bulannya berlabel 'OK' (dianggap normal produksi),
    ukur fraksi titik yang berada DI DALAM band tiap metode. Idealnya ~confidence.
    Seri konstan / hampir nol dilewati (band tak bermakna).
    """
    res = load_raw_block(path, year)
    long = res.long
    agg = {m: {"inside": 0, "total": 0} for m in ("robust", "classic", "excel")}
    n_series = 0
    for _, grp in long.groupby("row_id"):
        grp = grp.sort_values("month_idx")
        if not (grp["accuracy_check"] == "OK").all():
            continue
        vals = grp["consumption"].to_numpy(float)
        vals = vals[np.isfinite(vals)]
        if vals.size < 6 or np.nanmean(vals) < min_mean or np.allclose(vals, vals[0]):
            continue
        n_series += 1
        elo = grp["excel_lower"].iloc[0]; ehi = grp["excel_upper"].iloc[0]
        for m in ("robust", "classic"):
            b = compute_band(vals, BandConfig(method=m, confidence=confidence))
            if b.valid:
                inside = int(np.sum((vals >= b.lower) & (vals <= b.upper)))
                agg[m]["inside"] += inside
                agg[m]["total"] += vals.size
        if np.isfinite(elo) and np.isfinite(ehi):
            inside = int(np.sum((vals >= elo) & (vals <= ehi)))
            agg["excel"]["inside"] += inside
            agg["excel"]["total"] += vals.size

    rows = []
    for m in ("excel", "robust", "classic"):
        t = agg[m]["total"]
        cov = agg[m]["inside"] / t if t else float("nan")
        rows.append({"method": m, "coverage": cov, "points": t})
    return pd.DataFrame(rows), n_series


# --------------------------------------------------------------------------- #
# C. Ketidaksepakatan nyata (contoh untuk dinilai manusia)
# --------------------------------------------------------------------------- #
def disagreements(path, year, confidence=0.95, top=12):
    """
    Cari seri di mana band robust dan band Excel memberi keputusan BERBEDA pada
    jumlah titik terbanyak. Kembalikan ringkasan untuk ditinjau manusia.
    """
    res = load_raw_block(path, year)
    long = res.long
    rows = []
    for _, grp in long.groupby("row_id"):
        grp = grp.sort_values("month_idx")
        vals = grp["consumption"].to_numpy(float)
        finite = np.isfinite(vals)
        if finite.sum() < 6:
            continue
        elo = grp["excel_lower"].iloc[0]; ehi = grp["excel_upper"].iloc[0]
        if not (np.isfinite(elo) and np.isfinite(ehi)):
            continue
        br = compute_band(vals, BandConfig(method="robust", confidence=confidence))
        if not br.valid:
            continue
        rob_out = finite & ((vals < br.lower) | (vals > br.upper))
        exc_out = finite & ((vals < elo) | (vals > ehi))
        diff = int(np.sum(rob_out != exc_out))
        if diff == 0:
            continue
        name = " | ".join(str(grp[c].iloc[0]) for c in res.dim_cols if c in grp.columns)
        rows.append({
            "unit": name,
            "rob_only": int(np.sum(rob_out & ~exc_out)),   # robust tandai, Excel tidak
            "exc_only": int(np.sum(exc_out & ~rob_out)),   # Excel tandai, robust tidak
            "robust_band": f"[{br.lower:,.0f}, {br.upper:,.0f}]",
            "excel_band": f"[{elo:,.0f}, {ehi:,.0f}]",
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["total_diff"] = df["rob_only"] + df["exc_only"]
    return df.sort_values("total_diff", ascending=False).head(top).reset_index(drop=True)


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    pd.set_option("display.max_columns", 20)

    print("A. ROBUSTNESS (ground-truth sintetis; nilai kritis disamakan)")
    print("   outlier_recall tinggi + false_alarm_rate rendah = lebih baik")
    print(robustness_sim().to_string(index=False))

    print("\nB. COVERAGE pada seri stabil NYATA (target ~0.95)")
    for label, path, yr in [
        ("Listrik FY2025", _D("Listrik FY 25 (CEK RUMUS)-Training.csv"), 2025),
        ("NonRenew FY2025", _D("Non Renewable Energy FY 25 (CEK RUMUS)-Training.csv"), 2025),
    ]:
        cov, n = coverage_on_stable(path, yr)
        print(f"\n   {label}  (seri stabil terpakai: {n})")
        print(cov.to_string(index=False))

    print("\nC. KETIDAKSEPAKATAN robust vs Excel (Listrik FY2025, 12 teratas)")
    dis = disagreements(_D("Listrik FY 25 (CEK RUMUS)-Training.csv"), 2025)
    print(dis.to_string(index=False) if not dis.empty else "  (tak ada)")
