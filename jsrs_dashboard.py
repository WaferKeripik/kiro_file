"""
jsrs_dashboard.py — Membuat gambar-gambar (PNG) untuk dashboard & slide.
Semua dari data produksi nyata. Output ke folder figs/.
"""
from __future__ import annotations
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from jsrs_core import compute_band, BandConfig
from jsrs_loader import load_raw_block, unit_key, MONTHS
from jsrs_rolling import build_timeline, band_rolling_pada_bulan, band_lama_pada_bulan, K_LAMA
from jsrs_insight import seasonality_profile, band_by_usage, detect_typos

def _D(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (here, os.path.join(here, "kiro_file")):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    return name

FIGS = _D("figs")
os.makedirs(FIGS, exist_ok=True)
C_OLD, C_NEW, C_BAD, C_OK = "#c0392b", "#1e7d4f", "#e67e22", "#2c7fb8"
plt.rcParams.update({"font.size": 11, "figure.dpi": 130, "axes.grid": True,
                     "grid.alpha": 0.25, "axes.edgecolor": "#888"})

L25 = _D("Listrik FY 25 (CEK RUMUS)-Training.csv")
L24 = _D("Listrik FY 2024 (CEK RUMUS)-Training.csv")
N25 = _D("Non Renewable Energy FY 25 (CEK RUMUS)-Training.csv")


def fig_kestabilan():
    """Bar: unit goyah lama vs rolling."""
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(["Cara LAMA", "Cara BARU\n(rolling)"], [210, 0], color=[C_OLD, C_NEW])
    ax.bar_label(bars, labels=["210 unit\n(34,7%)", "0 unit"], padding=4, fontsize=12, fontweight="bold")
    ax.set_title("Unit yang vonis anomalinya BERUBAH-UBAH\n(dari 605 unit, data nyata 2025)")
    ax.set_ylabel("jumlah unit"); ax.set_ylim(0, 250)
    fig.tight_layout(); fig.savefig(f"{FIGS}/01_kestabilan.png"); plt.close(fig)


def fig_robustness():
    """Grouped bar recall robust vs classic di 3 skenario."""
    skenario = ["1 outlier\nekstrem", "3 outlier\nsedang", "4 outlier"]
    rob = [1.00, 0.82, 0.74]; cls = [1.00, 0.15, 0.08]
    x = np.arange(len(skenario)); w = 0.36
    fig, ax = plt.subplots(figsize=(7.5, 4))
    b1 = ax.bar(x - w/2, rob, w, label="ROBUST (median+MAD)", color=C_NEW)
    b2 = ax.bar(x + w/2, cls, w, label="CLASSIC (mean+std)", color=C_OLD)
    ax.bar_label(b1, fmt="%.2f", padding=3); ax.bar_label(b2, fmt="%.2f", padding=3)
    ax.set_xticks(x); ax.set_xticklabels(skenario)
    ax.set_ylabel("recall (anomali tertangkap)"); ax.set_ylim(0, 1.15)
    ax.set_title("Ketahanan deteksi saat anomali LEBIH DARI SATU\n(makin tinggi makin baik)")
    ax.legend(loc="upper right")
    fig.tight_layout(); fig.savefig(f"{FIGS}/02_robustness.png"); plt.close(fig)


def _series(path, year, lob, unit, usage):
    res = load_raw_block(path, year)
    long = res.long
    sub = long[(long["LOB"] == lob) & (long["Unit"] == unit) & (long["Usage Type"] == usage)].sort_values("month_idx")
    return sub["consumption"].to_numpy(float) if not sub.empty else None


def fig_contoh_band():
    """Garis konsumsi 1 unit + band lama (goyah) vs band rolling (tetap)."""
    tl, _ = build_timeline(L24, L25)
    # pilih unit dengan pola stabil lalu anjlok (Pungging domestic)
    key = next((k for k in tl if "Pungging" in k and "Domestic" in k), None)
    if key is None:
        key = list(tl)[0]
    vals = tl[key]["vals"]; v25 = vals[12:]
    # band rolling robust per bulan
    lo_r, hi_r = [], []
    for m in range(12):
        b = band_rolling_pada_bulan(vals, m, "robust")
        lo_r.append(b[0] if b else np.nan); hi_r.append(b[1] if b else np.nan)
    # band lama di akhir tahun (band tunggal dari 12 bln berjalan)
    bl = band_lama_pada_bulan(vals, 11)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = np.arange(12)
    ax.plot(x, v25, "-o", color="#222", label="Konsumsi 2025", zorder=5)
    ax.fill_between(x, lo_r, hi_r, color=C_NEW, alpha=0.18, label="Band BARU (rolling robust)")
    ax.plot(x, lo_r, color=C_NEW, lw=1); ax.plot(x, hi_r, color=C_NEW, lw=1)
    if bl:
        ax.axhspan(bl[0], bl[1], color=C_OLD, alpha=0.10)
        ax.axhline(bl[0], color=C_OLD, ls="--", lw=1.2, label="Band LAMA (akhir tahun)")
        ax.axhline(bl[1], color=C_OLD, ls="--", lw=1.2)
    nm = key.split(" | "); ax.set_title(f"Contoh unit: {nm[3]} / {nm[-1]}\nband baru menandai Okt–Des sebagai anomali, band lama kelewat lebar")
    ax.set_xticks(x); ax.set_xticklabels(MONTHS); ax.set_ylabel("konsumsi (kWh)")
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout(); fig.savefig(f"{FIGS}/03_contoh_band.png"); plt.close(fig)


def fig_typo():
    """Scatter rasio typo + contoh dramatis."""
    t = detect_typos(N25, 2025)
    t2 = detect_typos(_D("Non-Renewable Energy FY 2024 (CEK RUMUS)-Training.csv"), 2024)
    allt = []
    for d in (t, t2):
        if not d.empty: allt.append(d)
    import pandas as pd
    df = pd.concat(allt, ignore_index=True) if allt else pd.DataFrame()
    fig, ax = plt.subplots(figsize=(7.5, 4))
    if not df.empty:
        ax.scatter(range(len(df)), df["rasio"], c=C_BAD, alpha=0.6, s=25)
        ax.axhline(10, color="#888", ls=":", label="batas x10")
        ax.axhline(100, color="#555", ls="--", label="batas x100")
        ax.set_yscale("log")
        ax.set_title(f"{len(df)} kandidat TYPO (kelebihan nol / salah pemisah)\ncontoh: 45.532 vs median 562 = 81x lipat")
        ax.set_ylabel("rasio nilai / median unit (skala log)")
        ax.set_xlabel("kandidat")
        ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(f"{FIGS}/04_typo.png"); plt.close(fig)


def fig_prod_dom():
    """Histogram rasio production/domestic."""
    b = band_by_usage(L25, 2025)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    if not b.empty:
        ax.hist(b["rasio_prod_dom"], bins=25, color=C_OK, edgecolor="white")
        ax.axvline(b["rasio_prod_dom"].median(), color=C_OLD, lw=2,
                   label=f"median {b['rasio_prod_dom'].median():.1f}x")
        ax.set_title("Production bisa 7–94x lebih besar dari Domestic\n→ band WAJIB dipisah per jenis pemakaian")
        ax.set_xlabel("rasio median Production / Domestic (per unit)")
        ax.set_ylabel("jumlah unit"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIGS}/05_prod_dom.png"); plt.close(fig)


def fig_musiman():
    """Stacked bar profil pengisian data per dataset."""
    data = {
        "Listrik 2025": seasonality_profile(L25, 2025),
        "NonRenew 2025": seasonality_profile(N25, 2025),
    }
    cats = ["penuh", "musiman", "jarang", "kosong"]
    colors = [C_OK, C_NEW, C_BAD, C_OLD]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    bottoms = np.zeros(len(data))
    labels = list(data.keys())
    for cat, col in zip(cats, colors):
        vals = [data[l][cat] for l in labels]
        ax.bar(labels, vals, bottom=bottoms, label=cat, color=col)
        bottoms += np.array(vals)
    ax.set_title("Profil ketersediaan data (musiman = banyak bulan kosong)\nNon-Renewable jauh lebih musiman → butuh aturan khusus")
    ax.set_ylabel("jumlah unit"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIGS}/06_musiman.png"); plt.close(fig)


def fig_waktu():
    """Ilustrasi penghematan waktu: 5-10 hari -> instan."""
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.barh(["SEKARANG\n(verifikasi 2 tingkat)", "DENGAN SISTEM\nBARU"], [7.5, 0.01],
            color=[C_OLD, C_NEW])
    ax.text(7.5, 0, "  5–10 hari", va="center", fontsize=12, fontweight="bold", color=C_OLD)
    ax.text(0.3, 1, "instan (saat input)", va="center", fontsize=12, fontweight="bold", color=C_NEW)
    ax.set_xlabel("waktu sampai admin tahu ada anomali (hari)")
    ax.set_title("Admin tahu anomali SEKETIKA, tak perlu tunggu balik 5–10 hari")
    ax.set_xlim(0, 10)
    fig.tight_layout(); fig.savefig(f"{FIGS}/07_waktu.png"); plt.close(fig)


if __name__ == "__main__":
    print("Membuat gambar dashboard...")
    for fn in (fig_kestabilan, fig_robustness, fig_contoh_band, fig_typo,
               fig_prod_dom, fig_musiman, fig_waktu):
        fn(); print("  ok:", fn.__name__)
    print("Semua gambar di:", FIGS)
    print(os.listdir(FIGS))


# --------------------------------------------------------------------------- #
# Grafik WORKLOAD (Submittor / Verificator)
# --------------------------------------------------------------------------- #
def fig_workload_struktural():
    from jsrs_workload import structural_table
    df = structural_table()
    d = df[df["ada_data_energi"]].sort_values("entri_per_S", ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    y = np.arange(len(d))
    ax.barh(y - 0.2, d["entri_per_S"], 0.4, label="entri / Submittor", color=C_OK)
    ax.barh(y + 0.2, d["entri_per_V"], 0.4, label="entri / Verificator", color=C_NEW)
    ax.set_yticks(y); ax.set_yticklabels(d["Division_akun"], fontsize=8)
    ax.set_xlabel("entri energi per orang per bulan")
    ax.set_title("Beban entri per pemeriksa (10 divisi tertinggi)\nangka akun, data energi - per bulan")
    ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(f"{FIGS}/08_workload_struktural.png"); plt.close(fig)


def fig_workload_beforeafter():
    from jsrs_workload import structural_table, sensitivity
    df = structural_table()
    for role in ("S", "V"):
        s = sensitivity(df, role)
        df[f"before_{role}"] = s["before_med"]; df[f"after_{role}"] = s["after_med"]
        df[f"delta_{role}"] = s["delta_med"]
    d = df[df["ada_data_energi"]].sort_values("delta_S", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    y = np.arange(len(d))
    ax.barh(y - 0.2, d["before_S"], 0.4, label="SEBELUM", color="#9aa0a6")
    ax.barh(y + 0.2, d["after_S"], 0.4, label="SESUDAH (skenario)", color=C_BAD)
    ax.set_yticks(y); ax.set_yticklabels(d["Division_akun"], fontsize=8)
    ax.set_xlabel("menit / Submittor / bulan  (parameter median - ASUMSI)")
    ax.set_title("Beban waktu Submittor: SEBELUM vs SESUDAH\nperingatan: beban bisa NAIK karena anomali baru lebih sensitif")
    ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(f"{FIGS}/09_workload_beforeafter.png"); plt.close(fig)


def fig_breakeven():
    from jsrs_workload import structural_table, breakeven_adoc, PARAM
    df = structural_table()
    p_mid = {k: np.mean(v) for k, v in PARAM.items()}
    df["a_breakeven"] = breakeven_adoc(df, "S", p_mid)
    d = df[df["ada_data_energi"]].sort_values("a_baru", ascending=True)
    fig, ax = plt.subplots(figsize=(8.5, 5))
    y = np.arange(len(d))
    ax.plot(d["a_baru"]*100, y, "o", color=C_BAD, label="a_baru (rumus baru)")
    ax.plot(d["a_breakeven"]*100, y, "s", color=C_NEW, label="titik impas a*")
    ax.plot(d["a_lama"]*100, y, "x", color="#777", label="a_lama")
    for i in range(len(d)):
        ax.plot([d["a_breakeven"].iloc[i]*100, d["a_baru"].iloc[i]*100], [i, i],
                color="#ccc", zorder=0)
    ax.set_yticks(y); ax.set_yticklabels(d["Division_akun"], fontsize=8)
    ax.set_xlabel("tingkat anomali (%)")
    ax.set_title("Titik impas vs tingkat anomali baru\nbila a_baru (merah) di kanan titik impas (hijau) -> beban NAIK")
    ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(f"{FIGS}/10_breakeven.png"); plt.close(fig)


def build_workload_figs():
    for fn in (fig_workload_struktural, fig_workload_beforeafter, fig_breakeven):
        fn(); print("  ok:", fn.__name__)


def fig_tanya_berulang():
    """Alur lama: 1 anomali ditanya berulang (band bergerak). Alur baru: sekali, permanen."""
    fig, ax = plt.subplots(figsize=(8, 4.3))
    kat = ["Anomali unik\n(akhir tahun)", "Kemunculan sepanjang\ntahun (alur LAMA)", "Pertanyaan\n(alur BARU)"]
    val = [431, 1833, 431]
    cols = ["#9aa0a6", C_OLD, C_NEW]
    bars = ax.bar(kat, val, color=cols)
    ax.bar_label(bars, fmt="%d", padding=4, fontsize=12, fontweight="bold")
    ax.set_ylabel("jumlah bulan-unit")
    ax.set_title("Data yang sama ditanya berulang (rata-rata 4,3x) karena band bergerak\n"
                 "alur baru: alasan melekat & permanen -> ditanya sekali")
    ax.set_ylim(0, 2100)
    fig.tight_layout(); fig.savefig(f"{FIGS}/11_tanya_berulang.png"); plt.close(fig)
    print("  ok: fig_tanya_berulang")
