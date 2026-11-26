"""
jsrs_backtest.py — Menilai keandalan band rumus (robust t-PI & classic)
dibandingkan LCL/UCL milik Excel, memakai data produksi nyata.

Cara kerja (adil, in-sample, meniru cara Excel menghitung band per tahun):
  Untuk TIAP seri (satu baris sumber = satu unit-tahun):
    1. Ambil 12 nilai bulanan.
    2. Hitung band versi kita dari ke-12 nilai itu:
         - robust  : median + MAD terskala
         - classic : mean + std
    3. Bandingkan dengan band Excel (Lower/Upper Control Limit) yang juga in-sample.
    4. Hitung, untuk tiap metode, berapa titik bulanan jatuh DI LUAR band.
    5. Pakai label Excel 'accuracy_check' sebagai acuan "anomali menurut mereka"
       ('OK - With Notes', 'Need to Check' = ditandai; 'OK' = normal).

Metrik yang dihasilkan:
  - Lebar band rata-rata (semakin sempit = semakin ketat, belum tentu lebih baik).
  - Jumlah titik di luar band per metode (kita robust / kita classic / Excel).
  - Kecocokan dengan label Excel: precision/recall/F1 memakai label mereka sebagai
    ground-truth "ditandai". Ini mengukur "seberapa mirip keputusan tiap metode
    dengan penilaian yang sudah berjalan di produksi".
  - Perbandingan langsung: apakah titik yang Excel tandai juga tertangkap band kita.

Catatan kejujuran metodologis:
  Label Excel BUKAN kebenaran mutlak; itu keluaran rumus mereka + catatan manual.
  Jadi "kecocokan tinggi" berarti "mirip perilaku Excel", sedangkan di mana metode
  kita BERBEDA, itu justru kandidat tempat salah satu lebih baik. Laporan memisahkan
  keduanya: kesepakatan, dan ketidaksepakatan (dengan contоh unit).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from jsrs_core import compute_band, BandConfig
from jsrs_loader import load_raw_block, unit_key

import os as _os
def _D(name):
    here = _os.path.dirname(_os.path.abspath(__file__))
    for base in (here, _os.path.join(here, "kiro_file")):
        p = _os.path.join(base, name)
        if _os.path.exists(p):
            return p
    return name



# Label yang dianggap "ditandai" oleh Excel (anomali / perlu perhatian).
FLAGGED_LABELS = {"OK - With Notes", "Need to Check"}
# Label yang berarti tidak ada data (diabaikan saat menghitung kecocokan titik).
NODATA_LABELS = {"-", "No Data", ""}


def _series_rows(res, path, year):
    """Hasilkan (meta, nilai12, label12, excel_lo, excel_hi) per baris sumber."""
    long = res.long
    for rid, grp in long.groupby("row_id", sort=True):
        grp = grp.sort_values("month_idx")
        vals = grp["consumption"].to_numpy(dtype=float)
        labels = grp["accuracy_check"].tolist()
        lo = grp["excel_lower"].iloc[0]
        hi = grp["excel_upper"].iloc[0]
        meta = {d: grp[d].iloc[0] for d in res.dim_cols if d in grp.columns}
        meta["row_id"] = rid
        meta["year"] = year
        yield meta, vals, labels, lo, hi


def _outside(vals: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Mask titik di luar [lo,hi]. NaN -> False (tidak dihitung)."""
    m = np.isfinite(vals)
    out = np.zeros_like(vals, dtype=bool)
    if not np.isfinite(lo) or not np.isfinite(hi):
        return out  # band Excel tak tersedia -> tak ada yang 'di luar'
    out[m] = (vals[m] < lo) | (vals[m] > hi)
    return out


def _band_mask(vals: np.ndarray, method: str, confidence: float) -> tuple[np.ndarray, float, float, float]:
    """Hitung band kita dari 12 nilai (in-sample) dan kembalikan mask di-luar."""
    b = compute_band(vals, BandConfig(method=method, confidence=confidence))
    if not b.valid:
        return np.zeros_like(vals, dtype=bool), np.nan, np.nan, np.nan
    m = np.isfinite(vals)
    out = np.zeros_like(vals, dtype=bool)
    out[m] = (vals[m] < b.lower) | (vals[m] > b.upper)
    return out, b.lower, b.upper, (b.upper - b.lower)


def _prf(pred_flag: np.ndarray, true_flag: np.ndarray) -> tuple[int, int, int, int]:
    """Kembalikan (TP, FP, FN, TN) membandingkan prediksi vs label Excel."""
    tp = int(np.sum(pred_flag & true_flag))
    fp = int(np.sum(pred_flag & ~true_flag))
    fn = int(np.sum(~pred_flag & true_flag))
    tn = int(np.sum(~pred_flag & ~true_flag))
    return tp, fp, fn, tn


def run_backtest(path: str, year: int, confidence: float = 0.95) -> dict:
    res = load_raw_block(path, year)

    detail_rows = []
    # akumulator untuk confusion matrix tiap metode (vs label Excel)
    acc = {m: np.zeros(4, dtype=int) for m in ("robust", "classic", "excel")}
    width_sum = {m: 0.0 for m in ("robust", "classic", "excel")}
    width_cnt = {m: 0 for m in ("robust", "classic", "excel")}
    out_count = {m: 0 for m in ("robust", "classic", "excel")}

    for meta, vals, labels, elo, ehi in _series_rows(res, path, year):
        valid_pt = np.isfinite(vals)
        # label 'ditandai' Excel per titik; titik tanpa data tidak dinilai
        true_flag = np.array([(l in FLAGGED_LABELS) for l in labels], dtype=bool)
        scorable = valid_pt & np.array([(l not in NODATA_LABELS) for l in labels], dtype=bool)

        # band kita
        rob_out, rlo, rhi, rwid = _band_mask(vals, "robust", confidence)
        cls_out, clo, chi, cwid = _band_mask(vals, "classic", confidence)
        # band excel
        exc_out = _outside(vals, elo, ehi)

        for name, mask, wid, lo, hi in (
            ("robust", rob_out, rwid, rlo, rhi),
            ("classic", cls_out, cwid, clo, chi),
            ("excel", exc_out, (ehi - elo) if (np.isfinite(elo) and np.isfinite(ehi)) else np.nan, elo, ehi),
        ):
            # confusion vs label Excel, hanya pada titik yang bisa dinilai
            tp, fp, fn, tn = _prf(mask & scorable, true_flag & scorable)
            acc[name] += np.array([tp, fp, fn, tn])
            out_count[name] += int(np.sum(mask & valid_pt))
            if np.isfinite(wid):
                width_sum[name] += wid
                width_cnt[name] += 1

        detail_rows.append({
            **meta,
            "n_valid": int(valid_pt.sum()),
            "n_flagged_excel": int((true_flag & scorable).sum()),
            "out_robust": int(np.sum(rob_out & valid_pt)),
            "out_classic": int(np.sum(cls_out & valid_pt)),
            "out_excel": int(np.sum(exc_out & valid_pt)),
            "robust_lo": rlo, "robust_hi": rhi,
            "classic_lo": clo, "classic_hi": chi,
            "excel_lo": elo, "excel_hi": ehi,
        })

    detail = pd.DataFrame(detail_rows)

    def metrics(name):
        tp, fp, fn, tn = acc[name]
        prec = tp / (tp + fp) if (tp + fp) else float("nan")
        rec = tp / (tp + fn) if (tp + fn) else float("nan")
        f1 = (2 * prec * rec / (prec + rec)) if (prec and rec and prec + rec) else float("nan")
        mean_w = (width_sum[name] / width_cnt[name]) if width_cnt[name] else float("nan")
        return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=prec, recall=rec, f1=f1,
                    points_outside=out_count[name], mean_band_width=mean_w)

    summary = {m: metrics(m) for m in ("robust", "classic", "excel")}
    return {"summary": summary, "detail": detail, "is_nonrenewable": res.is_nonrenewable, "year": year}


def _fmt(v, nd=3):
    if isinstance(v, float):
        if np.isnan(v):
            return "n/a"
        return f"{v:,.{nd}f}"
    return str(v)


def print_summary(label: str, result: dict) -> None:
    s = result["summary"]
    print(f"\n=== {label} (year {result['year']}) ===")
    print(f"{'metode':<10}{'F1':>8}{'precision':>11}{'recall':>9}{'#diluar':>9}{'lebar_band_rata2':>20}")
    for m in ("excel", "robust", "classic"):
        d = s[m]
        print(f"{m:<10}{_fmt(d['f1']):>8}{_fmt(d['precision']):>11}{_fmt(d['recall']):>9}"
              f"{d['points_outside']:>9}{_fmt(d['mean_band_width'],1):>20}")
    print("  (F1/precision/recall = kecocokan dengan label 'ditandai' Excel)")


if __name__ == "__main__":
    files = [
        ("Listrik FY2025", _D("Listrik FY 25 (CEK RUMUS)-Training.csv"), 2025),
        ("Listrik FY2024", _D("Listrik FY 2024 (CEK RUMUS)-Training.csv"), 2024),
        ("NonRenew FY2025", _D("Non Renewable Energy FY 25 (CEK RUMUS)-Training.csv"), 2025),
        ("NonRenew FY2024", _D("Non-Renewable Energy FY 2024 (CEK RUMUS)-Training.csv"), 2024),
    ]
    all_detail = []
    for label, path, yr in files:
        res = run_backtest(path, yr)
        print_summary(label, res)
        d = res["detail"]
        d.insert(0, "dataset", label)
        all_detail.append(d)
    out = pd.concat(all_detail, ignore_index=True)
    out.to_csv("backtest_detail.csv"), index=False)
    print(f"\nDetail per unit disimpan: backtest_detail.csv ({len(out)} baris)")
