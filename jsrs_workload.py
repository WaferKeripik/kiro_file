"""
jsrs_workload.py — Analisis beban kerja Submittor & Verificator (JSRS).

Menjawab: apakah fitur deteksi anomali baru juga menguntungkan Submittor & Verificator,
bukan hanya Admin & Corporate?

Tiga jenis angka DIPISAHKAN dengan jelas:
  (a) DIHITUNG DARI DATA  : volume input N(d,m), tingkat anomali a_lama/a_baru,
                            jumlah akun R/S/V, jumlah unit U.
  (b) ASUMSI PARAMETER    : t_cek, t_dok, t_tanya, r_lama, r_baru, k_ringan
                            -> dijalankan sebagai RENTANG sensitivitas, diberi label.
  (c) BELUM BISA DIHITUNG  : waktu nyata per entri (tidak ada datanya) -> lihat (b).

Keterbatasan penting:
  - Angka akun != jumlah orang aktif (1 orang bisa banyak akun; sebagian akun nonaktif).
  - Volume input yang tersedia HANYA energi (listrik + non-renewable). Air/limbah belum ada.
  - Nama divisi data akun (mis. 'Poultry Breeding - North') dipetakan ke divisi energi
    ('Poultry Breeding') saat mencocokkan; divisi tanpa data energi ditandai 'tak ada data'.
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# PARAMETER (ubah di sini). Semua waktu dalam MENIT. Ini ASUMSI, bukan fakta.
# --------------------------------------------------------------------------- #
PARAM = {
    "t_cek":   (2.0, 5.0),    # menit cek 1 entri biasa
    "t_dok":   (10.0, 20.0),  # menit cek dokumen pendukung 1 entri anomali (kewajiban BARU)
    "t_tanya": (15.0, 30.0),  # menit 1 putaran tanya-jawab alasan anomali
    "r_lama":  (2.0, 4.0),    # putaran tanya-jawab per anomali, alur lama (berjenjang)
    "r_baru":  (0.0, 1.0),    # putaran tanya-jawab per anomali, alur baru (alasan terlampir)
    "k_ringan": (1.0, 1.0),   # faktor cek entri non-anomali pada alur baru
}

# --------------------------------------------------------------------------- #
# (a) DATA AKUN per divisi — dari lampiran pengguna
# --------------------------------------------------------------------------- #
AKUN = """Aquaculture,26,5,2
CORP. TECHNICAL SERVICES,1,1,1
Cattle and Poultry Feed - South,4,1,3
Commercial Broiler,4,2,2
Commercial Poultry,98,25,7
Consumer Foods,20,13,18
Corporate Shared Services,5,3,3
Dairy,7,1,1
Dairy and Beef,1,1,1
Head Office,11,7,6
Marketing & Sales,1,1,1
Poultry Breeding,132,30,15
Poultry Breeding - North,6,7,3
Poultry Breeding - South,6,7,4
Poultry Feed,35,9,8
Poultry Feed - North,6,5,2
Poultry Processing,16,15,3
Rice Business,1,1,1
SBU AHLE,24,21,19
SBU Aqua Processing,9,4,3
SBU Beef,9,8,4
SBU Consumer Go Direct,5,2,2
SBU Duck & Ulu Chicken,4,4,4
SBU EPI,5,3,3
SBU Grains Trading,35,7,5
SBU Plantation,6,2,2
SBU Property,4,1,2
SBU Transportation,8,2,3
Swine,1,1,2
Swine - North,4,2,2
Swine - South,5,1,3"""

# Pemetaan sub-divisi akun -> divisi pada data energi.
DIV_MAP = {
    "Poultry Breeding - North": "Poultry Breeding",
    "Poultry Breeding - South": "Poultry Breeding",
    "Poultry Feed - North": "Poultry Feed",
    "Cattle and Poultry Feed - South": "Poultry Feed",
    # sisanya cocok apa adanya; divisi tanpa data energi akan 'tak ada data'
}


def load_accounts():
    rows = [r.split(",") for r in AKUN.strip().splitlines()]
    df = pd.DataFrame(rows, columns=["Division_akun", "R", "S", "V"])
    for c in ("R", "S", "V"):
        df[c] = df[c].astype(int)
    df["Division_energi"] = df["Division_akun"].map(lambda d: DIV_MAP.get(d, d))
    return df


def _D(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (here, os.path.join(here, "kiro_file")):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    return name


def load_volume_and_anomaly():
    """
    (a) Hitung dari data energi nyata:
        N (entri/bulan), U (unit), a_lama, a_baru — per divisi energi.
    """
    from jsrs_loader import load_raw_block
    from jsrs_rolling import build_timeline, band_rolling_pada_bulan, band_lama_pada_bulan

    # volume & unit
    vol = {}
    for fn in ("Listrik FY 25 (CEK RUMUS)-Training.csv",
               "Non Renewable Energy FY 25 (CEK RUMUS)-Training.csv"):
        res = load_raw_block(_D(fn), 2025)
        long = res.long
        valid = long[np.isfinite(long["consumption"])]
        for div, g in valid.groupby("Division"):
            e = vol.setdefault(div, [0.0, 0])
            e[0] += len(g) / 12.0
            e[1] += g["row_id"].nunique()

    # anomali
    agg = {}
    pairs = [("Listrik FY 2024 (CEK RUMUS)-Training.csv", "Listrik FY 25 (CEK RUMUS)-Training.csv"),
             ("Non-Renewable Energy FY 2024 (CEK RUMUS)-Training.csv", "Non Renewable Energy FY 25 (CEK RUMUS)-Training.csv")]
    for p24, p25 in pairs:
        tl, _ = build_timeline(_D(p24), _D(p25))
        for key, d in tl.items():
            div = key.split(" | ")[1]
            vals = d["vals"]
            a = agg.setdefault(div, [0, 0, 0])
            for m in range(12):
                v = vals[12 + m]
                if not np.isfinite(v):
                    continue
                a[0] += 1
                bl = band_lama_pada_bulan(vals, m)
                if bl and (v < bl[0] or v > bl[1]):
                    a[1] += 1
                br = band_rolling_pada_bulan(vals, m, "robust")
                if br and (v < br[0] or v > br[1]):
                    a[2] += 1

    rows = []
    for div in set(vol) | set(agg):
        n, u = vol.get(div, [0.0, 0])
        ev, al, ab = agg.get(div, [0, 0, 0])
        rows.append({
            "Division_energi": div,
            "N": n, "U": u,
            "a_lama": (al / ev) if ev else np.nan,
            "a_baru": (ab / ev) if ev else np.nan,
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# TABEL STRUKTURAL
# --------------------------------------------------------------------------- #
def structural_table():
    acc = load_accounts()
    data = load_volume_and_anomaly()
    # agregasi N & U ke divisi energi, lalu bagikan ke akun lewat mapping
    df = acc.merge(data, on="Division_energi", how="left")

    # Jika beberapa divisi akun memetakan ke 1 divisi energi, N dibagi proporsional
    # terhadap jumlah SR Admin (pendekatan wajar: unit tersebar mengikuti admin).
    df["R_div_energi"] = df.groupby("Division_energi")["R"].transform("sum")
    share = np.where(df["R_div_energi"] > 0, df["R"] / df["R_div_energi"], np.nan)
    df["N_alok"] = df["N"] * share      # entri/bulan dialokasikan ke baris akun ini
    df["U_alok"] = df["U"] * share

    def safe(a, b):
        return np.where(b > 0, a / b, np.nan)

    df["entri_per_S"] = safe(df["N_alok"], df["S"])
    df["entri_per_V"] = safe(df["N_alok"], df["V"])
    df["unit_per_S"] = safe(df["U_alok"], df["S"])
    df["unit_per_V"] = safe(df["U_alok"], df["V"])
    df["admin_per_S"] = safe(df["R"], df["S"])
    df["admin_per_V"] = safe(df["R"], df["V"])
    df["V_per_S"] = safe(df["V"], df["S"])
    df["single_point"] = (df["S"] == 1) | (df["V"] == 1)
    df["ada_data_energi"] = df["N"].notna() & (df["N"] > 0)
    return df


# --------------------------------------------------------------------------- #
# MODEL SEBELUM vs SESUDAH (per orang per bulan)
# --------------------------------------------------------------------------- #
def workload_time(df, role="S", scenario="lama", p=None):
    """Waktu/orang/bulan (menit). role 'S' atau 'V'. p = dict nilai parameter tunggal."""
    cnt = df[role].to_numpy(float)
    N = df["N_alok"].to_numpy(float)
    a_lama = df["a_lama"].to_numpy(float)
    a_baru = df["a_baru"].to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        if scenario == "lama":
            t = (N / cnt) * p["t_cek"] + (N * a_lama / cnt) * p["r_lama"] * p["t_tanya"]
        else:
            t = ((N * (1 - a_baru) / cnt) * p["t_cek"] * p["k_ringan"]
                 + (N * a_baru / cnt) * (p["t_cek"] + p["t_dok"])
                 + (N * a_baru / cnt) * p["r_baru"] * p["t_tanya"])
    return t


def sensitivity(df, role="S"):
    """Jalankan kombinasi batas rentang parameter -> min/median/max selisih."""
    import itertools
    keys = list(PARAM)
    combos = list(itertools.product(*[PARAM[k] for k in keys]))
    before, after = [], []
    for combo in combos:
        p = dict(zip(keys, combo))
        before.append(workload_time(df, role, "lama", p))
        after.append(workload_time(df, role, "baru", p))
    before = np.array(before); after = np.array(after)
    delta = after - before
    allnan = np.all(np.isnan(before), axis=0)
    def safemed(a, fn):
        out = np.full(a.shape[1], np.nan)
        m = ~allnan
        if m.any():
            out[m] = fn(a[:, m], axis=0)
        return out
    return {
        "before_med": safemed(before, np.nanmedian),
        "after_med": safemed(after, np.nanmedian),
        "delta_med": safemed(delta, np.nanmedian),
        "delta_min": safemed(delta, np.nanmin),
        "delta_max": safemed(delta, np.nanmax),
    }


def breakeven_adoc(df, role="S", p_mid=None):
    """
    Titik impas: nilai a_baru di mana Waktu_sesudah = Waktu_sebelum (parameter mid).
    Turunan: t_sebelum = (N/c)tcek + (N*a_lama/c)*r_lama*ttanya
             t_sesudah(a) = (N/c)*tcek + (N*a/c)*(tdok + r_baru*ttanya)   [k_ringan=1]
    (bagian tcek untuk entri anomali diserap: (1-a)tcek + a*tcek = tcek)
    => break-even a* = a_lama * r_lama * ttanya / (tdok + r_baru*ttanya)
    """
    r_lama = p_mid["r_lama"]; ttanya = p_mid["t_tanya"]
    tdok = p_mid["t_dok"]; r_baru = p_mid["r_baru"]
    denom = tdok + r_baru * ttanya
    a_star = df["a_lama"].to_numpy(float) * r_lama * ttanya / denom
    return a_star


if __name__ == "__main__":
    pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30)
    df = structural_table()

    print("="*90)
    print("CATATAN: (a)=dihitung dari data  (b)=asumsi parameter  (c)=belum bisa dihitung")
    print("Angka akun != orang aktif. Volume input HANYA energi (listrik+non-renewable).")
    print("="*90)

    # --- 1. STRUKTURAL ---
    print("\n[1] TABEL STRUKTURAL per divisi akun (a) — urut beban entri/Submittor:")
    cols = ["Division_akun", "R", "S", "V", "N_alok", "U_alok",
            "entri_per_S", "entri_per_V", "admin_per_S", "admin_per_V", "V_per_S", "single_point"]
    show = df[cols].sort_values("entri_per_S", ascending=False)
    print(show.to_string(index=False, float_format=lambda x: f"{x:,.1f}"))

    print("\n  Divisi timpang (single point: S=1 atau V=1):")
    sp = df[df["single_point"]][["Division_akun", "S", "V", "N_alok"]]
    print(sp.to_string(index=False, float_format=lambda x: f"{x:,.1f}"))

    # --- 2. BEBAN ANOMALI ---
    print("\n[2] BEBAN ANOMALI per bulan (a) — entri anomali per orang:")
    df["anom_S_lama"] = df["N_alok"] * df["a_lama"] / df["S"]
    df["anom_S_baru"] = df["N_alok"] * df["a_baru"] / df["S"]
    df["anom_V_lama"] = df["N_alok"] * df["a_lama"] / df["V"]
    df["anom_V_baru"] = df["N_alok"] * df["a_baru"] / df["V"]
    b = df[df["ada_data_energi"]][["Division_akun", "a_lama", "a_baru",
         "anom_S_lama", "anom_S_baru", "anom_V_lama", "anom_V_baru"]].sort_values("anom_S_baru", ascending=False)
    print(b.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    # --- 3. SEBELUM vs SESUDAH (sensitivitas) ---
    for role, nm in (("S", "SUBMITTOR"), ("V", "VERIFICATOR")):
        s = sensitivity(df, role)
        df[f"before_{role}"] = s["before_med"]
        df[f"after_{role}"] = s["after_med"]
        df[f"delta_{role}"] = s["delta_med"]
        df[f"delta_{role}_min"] = s["delta_min"]
        df[f"delta_{role}_max"] = s["delta_max"]
    print("\n[3] SEBELUM vs SESUDAH — menit/orang/bulan (b: median rentang asumsi):")
    cc = ["Division_akun", "before_S", "after_S", "delta_S", "delta_S_min", "delta_S_max"]
    print(df[df["ada_data_energi"]][cc].sort_values("delta_S", ascending=False)
          .to_string(index=False, float_format=lambda x: f"{x:,.0f}"))

    # --- 4. TITIK IMPAS ---
    p_mid = {k: np.mean(v) for k, v in PARAM.items()}
    df["a_breakeven"] = breakeven_adoc(df, "S", p_mid)
    df["untung_S"] = df["delta_S"] < 0
    print("\n[4] TITIK IMPAS a_baru* (b) — jika a_baru < a* maka Submittor diuntungkan:")
    be = df[df["ada_data_energi"]][["Division_akun", "a_lama", "a_baru", "a_breakeven", "untung_S"]]
    print(be.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    n_ok = int((df[df["ada_data_energi"]]["delta_S"] < 0).sum())
    n_tot = int(df["ada_data_energi"].sum())
    print(f"\n  Submittor diuntungkan (delta<0, parameter median): {n_ok}/{n_tot} divisi berdata.")
    n_okv = int((df[df["ada_data_energi"]]["delta_V"] < 0).sum())
    print(f"  Verificator diuntungkan: {n_okv}/{n_tot} divisi berdata.")

    df.to_csv("workload_divisi.csv", index=False)
    print("\nDisimpan: workload_divisi.csv")
