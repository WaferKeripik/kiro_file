"""
jsrs_loader.py — Pembaca data JSRS berbentuk "wide" (bulan tersebar ke samping).

Struktur sumber (hasil ekspor Excel "CEK RUMUS"):
  - Dua baris header pertama memberi tahun dan bulan untuk tiap pasang kolom.
  - Baris header ketiga memberi nama kolom nyata.
  - Tiap unit = satu baris. 12 bulan (Jan..Dec), masing-masing 2 kolom:
    "Total Consumption" dan "Accuracy Check".
  - Kolom dimensi:
      Electricity          : Country, Division, LOB, Unit, SR Category, Usage Type
      Non Renewable Energy : + Energy Sources (di antara SR Category dan Usage Type)
  - Ada kolom batas yang sudah dihitung Excel:
      "Lower Control Limit", "Upper Control Limit"
  - Kolom terakhir: "Total Anomaly".

Modul ini mengubah data wide menjadi "long" (satu baris per unit-bulan) yang jauh
lebih mudah dipakai untuk backtest band. Semua angka dibersihkan dari pemisah ribuan
(",") dan tanda "-"/kosong menjadi NaN.

Tidak ada ketergantungan pada isi data tertentu: cukup arahkan ke file CSV yang
strukturnya seperti di atas.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Nama kolom dimensi untuk kedua jenis tabel.
DIM_ELECTRICITY = ["Country", "Division", "LOB", "Unit", "SR Category", "Usage Type"]
DIM_NONRENEW = ["Country", "Division", "LOB", "Unit", "SR Category",
                "Energy Sources", "Usage Type"]


def _to_number(x) -> float:
    """Ubah teks angka gaya Excel ('1,234.56', '-', '') menjadi float/NaN."""
    if x is None:
        return np.nan
    s = str(x).strip()
    if s in ("", "-", "nan", "NaN", "None"):
        return np.nan
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return np.nan


@dataclass(frozen=True)
class LoadResult:
    long: pd.DataFrame      # satu baris per (unit, bulan)
    wide: pd.DataFrame      # bentuk lebar yang sudah dibersihkan
    dim_cols: list          # kolom kunci unit
    is_nonrenewable: bool


def _detect_kind(header_cols: list[str]) -> bool:
    """True bila tabel Non Renewable Energy (punya kolom 'Energy Sources')."""
    return "Energy Sources" in header_cols


def load_wide_csv(path: str, year: Optional[int] = None) -> LoadResult:
    """
    Baca satu file CSV berstruktur wide JSRS.

    Asumsi: file sudah dirapikan sehingga baris header nyata (yang memuat
    'Total Consumption') ada, dan dua baris 'Year'/'Month' di atasnya sudah
    DIBUANG. Jika belum, pakai load_raw_block() yang menangani tiga baris header.
    """
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return _finalize(df, year)


def load_raw_block(path: str, year: Optional[int] = None) -> LoadResult:
    """
    Baca CSV mentah yang masih memuat dua baris atas (Year, Month) sebelum
    baris header nyata.

    Pendekatan tangguh: kita TIDAK memakai baris header apa adanya (kolomnya bisa
    bergeser / kekurangan sel). Sebaliknya kita:
      1. cari baris header nyata (mengandung 'Country' dan 'Total Consumption');
      2. tentukan jumlah kolom dimensi dari header itu (posisi 'Lower Control Limit');
      3. bangun ulang nama kolom secara posisional:
         [dim...] + [Lower, Upper] + 12x[Total Consumption, Accuracy Check] + [Total Anomaly]
      4. potong tiap baris data ke lebar tepat itu (buang sel kosong di ekor).
    """
    raw = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    header_idx = None
    for i in range(min(6, len(raw))):
        row = [c.strip() for c in raw.iloc[i].tolist()]
        if "Country" in row and "Total Consumption" in row:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Baris header nyata (berisi 'Country' & 'Total Consumption') tidak ditemukan.")

    header = [c.strip() for c in raw.iloc[header_idx].tolist()]
    # Kolom dimensi = semua kolom sebelum 'Lower Control Limit'.
    try:
        low_pos = header.index("Lower Control Limit")
    except ValueError as exc:
        raise ValueError("Kolom 'Lower Control Limit' tidak ditemukan di header.") from exc
    dim_names = [h for h in header[:low_pos] if h != ""]

    # Nama kolom posisional yang pasti benar.
    built = list(dim_names) + ["Lower Control Limit", "Upper Control Limit"]
    for _ in range(12):
        built += ["Total Consumption", "Accuracy Check"]
    built += ["Total Anomaly"]
    width = len(built)
    built = _dedupe(built)

    body = raw.iloc[header_idx + 1:].reset_index(drop=True)
    # Potong/padding tiap baris agar tepat selebar `width`.
    fixed = []
    for _, r in body.iterrows():
        vals = r.tolist()[:width]
        if len(vals) < width:
            vals += [""] * (width - len(vals))
        fixed.append(vals)
    out = pd.DataFrame(fixed, columns=built)
    return _finalize(out, year)


def _dedupe(names: list[str]) -> list[str]:
    """Beri akhiran .1, .2, ... pada nama kolom yang berulang (Total Consumption dst)."""
    seen: dict[str, int] = {}
    out = []
    for n in names:
        if n in seen:
            seen[n] += 1
            out.append(f"{n}.{seen[n]}")
        else:
            seen[n] = 0
            out.append(n)
    return out


def _finalize(df: pd.DataFrame, year: Optional[int]) -> LoadResult:
    cols = list(df.columns)
    is_nr = _detect_kind(cols)
    # Dim = kolom sebelum 'Lower Control Limit', apa pun jenis tabelnya.
    ref = DIM_NONRENEW if is_nr else DIM_ELECTRICITY
    dim_cols = [c for c in ref if c in cols]

    # Kolom "Total Consumption" berulang 12x -> Total Consumption, .1, ... .11
    cons_cols = [c for c in cols if c == "Total Consumption" or c.startswith("Total Consumption.")]
    chk_cols = [c for c in cols if c == "Accuracy Check" or c.startswith("Accuracy Check.")]
    if len(cons_cols) < 12 or len(chk_cols) < 12:
        raise ValueError(f"Diharapkan 12 kolom bulanan; dapat cons={len(cons_cols)} chk={len(chk_cols)}")
    cons_cols, chk_cols = cons_cols[:12], chk_cols[:12]

    # Bersihkan batas kontrol & bangun long-form.
    lower = df["Lower Control Limit"].map(_to_number).to_numpy()
    upper = df["Upper Control Limit"].map(_to_number).to_numpy()

    records = []
    for ridx in range(len(df)):
        key = {d: df.iloc[ridx][d] for d in dim_cols if d in df.columns}
        for m_i, (cc, kc) in enumerate(zip(cons_cols, chk_cols)):
            records.append({
                "row_id": ridx,  # tiap baris sumber = satu seri (tangani duplikat kunci)
                **key,
                "month": MONTHS[m_i],
                "month_idx": m_i + 1,
                "year": year,
                "consumption": _to_number(df.iloc[ridx][cc]),
                "accuracy_check": str(df.iloc[ridx][kc]).strip(),
                "excel_lower": lower[ridx],
                "excel_upper": upper[ridx],
            })
    long = pd.DataFrame.from_records(records)

    # wide yang sudah bersih (numerik) untuk pemeriksaan cepat.
    wide = df.copy()
    for c in cons_cols + ["Lower Control Limit", "Upper Control Limit"]:
        wide[c] = wide[c].map(_to_number)

    return LoadResult(long=long, wide=wide, dim_cols=dim_cols, is_nonrenewable=is_nr)


def unit_key(df_long: pd.DataFrame, dim_cols: list[str]) -> pd.Series:
    """Gabungkan kolom dimensi menjadi satu kunci unit string."""
    keys = [c for c in dim_cols if c in df_long.columns]
    return df_long[keys].astype(str).agg(" | ".join, axis=1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Pakai: python jsrs_loader.py <file.csv> [year]")
        raise SystemExit(1)
    res = load_raw_block(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
    print("Jenis :", "Non-Renewable" if res.is_nonrenewable else "Electricity")
    print("Dim   :", res.dim_cols)
    print("Unit  :", res.long.pipe(unit_key, res.dim_cols).nunique(), "unit unik")
    print("Baris long:", len(res.long))
    print(res.long.head(6).to_string())
