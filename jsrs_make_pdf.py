"""
jsrs_make_pdf.py — Membuat slide presentasi PDF (landscape) dari temuan + grafik.
Tanpa dependensi sistem: pakai fpdf2 murni Python.
Output: SLIDE_JSRS.pdf
"""
from __future__ import annotations
import os
from fpdf import FPDF

def _D(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (here, os.path.join(here, "kiro_file")):
        p = os.path.join(base, name)
        if os.path.exists(p) or True:
            if os.path.exists(os.path.join(base, name)):
                return os.path.join(base, name)
    return os.path.join(here, name)

FIGS = _D("figs")

_REPL = {"\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
         "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u2022": "-",
         "\u2192": "->", "\u2265": ">=", "\u2264": "<=", "\u00d7": "x"}
def _s(t):
    if not isinstance(t, str):
        return t
    for k, v in _REPL.items():
        t = t.replace(k, v)
    return t

NAVY = (26, 42, 74); GREEN = (30, 125, 79); RED = (192, 57, 43)
GREY = (90, 90, 90); LIGHT = (238, 242, 248); DARK = (33, 37, 41)

class Slides(FPDF):
    def header(self): pass
    def footer(self):
        self.set_y(-12); self.set_font("Helvetica", "", 8); self.set_text_color(*GREY)
        self.cell(0, 8, f"JSRS - Evaluasi Rumus Deteksi Anomali   |   halaman {self.page_no()}",
                  align="C")

def new(pdf):
    pdf.add_page()

def title_slide(pdf, title, subtitle, lines):
    new(pdf)
    pdf.set_fill_color(*NAVY); pdf.rect(0, 0, 297, 210, "F")
    W = 297 - 2 * pdf.l_margin
    pdf.set_y(55); pdf.set_font("Helvetica", "B", 30); pdf.set_text_color(255, 255, 255)
    pdf.set_x(pdf.l_margin); pdf.multi_cell(W, 13, title, align="C")
    pdf.ln(2); pdf.set_font("Helvetica", "", 15); pdf.set_text_color(170, 200, 230)
    pdf.set_x(pdf.l_margin); pdf.multi_cell(W, 9, subtitle, align="C")
    pdf.ln(8); pdf.set_font("Helvetica", "", 12); pdf.set_text_color(220, 230, 240)
    for l in lines:
        if l.strip() == "":
            pdf.ln(8)
        else:
            pdf.set_x(pdf.l_margin); pdf.multi_cell(W, 8, l, align="C")

def head(pdf, title, kicker=None):
    new(pdf)
    pdf.set_fill_color(*NAVY); pdf.rect(0, 0, 297, 26, "F")
    if kicker:
        pdf.set_xy(12, 4); pdf.set_font("Helvetica", "B", 9); pdf.set_text_color(150, 190, 230)
        pdf.cell(0, 5, kicker.upper())
    pdf.set_xy(12, 10); pdf.set_font("Helvetica", "B", 17); pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, title)
    pdf.set_xy(12, 32); pdf.set_text_color(*DARK)

def bullets(pdf, items, size=12, lh=8, x=16):
    pdf.set_font("Helvetica", "", size)
    for it in items:
        bold = it.startswith("*")
        txt = it[1:] if bold else it
        pdf.set_x(x)
        pdf.set_font("Helvetica", "B" if bold else "", size)
        pdf.set_text_color(*(GREEN if bold else DARK))
        pdf.multi_cell(297 - x - pdf.r_margin, lh, ("-  " if not bold else ">> ") + txt)
    pdf.set_text_color(*DARK)

def image_slide(pdf, title, img, caption, kicker=None):
    head(pdf, title, kicker)
    p = os.path.join(FIGS, img)
    if os.path.exists(p):
        pdf.image(p, x=40, y=34, w=217)
    pdf.set_xy(12, 176); pdf.set_font("Helvetica", "I", 11); pdf.set_text_color(*GREY)
    pdf.multi_cell(297 - 24, 6, caption, align="C")
    pdf.set_text_color(*DARK)

def two_col(pdf, left_title, left, right_title, right):
    y0 = 34
    pdf.set_xy(14, y0); pdf.set_font("Helvetica", "B", 13); pdf.set_text_color(*RED)
    pdf.cell(135, 8, left_title)
    pdf.set_xy(155, y0); pdf.set_text_color(*GREEN); pdf.cell(130, 8, right_title)
    pdf.set_text_color(*DARK)
    pdf.set_xy(14, y0 + 10); pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(135, 7, left)
    pdf.set_xy(155, y0 + 10)
    pdf.multi_cell(130, 7, right)

def kpi_row(pdf, y, items):
    """items: list of (big, small). 3 kartu."""
    w = 88; gap = 7; x = 14
    for big, small, col in items:
        pdf.set_fill_color(*LIGHT); pdf.rect(x, y, w, 34, "F")
        pdf.set_xy(x, y + 5); pdf.set_font("Helvetica", "B", 22); pdf.set_text_color(*col)
        pdf.cell(w, 12, big, align="C")
        pdf.set_xy(x, y + 20); pdf.set_font("Helvetica", "", 10); pdf.set_text_color(*DARK)
        pdf.multi_cell(w, 5, small, align="C")
        x += w + gap


def build():
    pdf = Slides(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(False)
    # auto-sanitasi semua teks ke latin-1 (hindari error em-dash dsb.)
    _cell, _mcell = pdf.cell, pdf.multi_cell
    def cell(w, h=0, text="", *a, **k): return _cell(w, h, _s(text), *a, **k)
    def mcell(w, h=0, text="", *a, **k): return _mcell(w, h, _s(text), *a, **k)
    pdf.cell = cell; pdf.multi_cell = mcell

    # 1 cover
    title_slide(pdf, "Rumus Deteksi Anomali Baru",
                "Rolling Band + Statistik Robust (Median / MAD)",
                ["Evaluasi dengan data produksi nyata",
                 "Listrik & Non-Renewable Energy  -  FY2024 + FY2025  -  605 unit",
                 "", "Pertanyaan: dapat dipercaya? akurat? layak dipakai?"])

    # 2 ringkasan KPI
    head(pdf, "Ringkasan Eksekutif", "tiga angka kunci")
    kpi_row(pdf, 40, [("210 -> 0", "unit yang vonisnya goyah\n(lama vs baru)", RED),
                      ("74-82%", "anomali majemuk tertangkap\n(vs 8-15% cara lama)", GREEN),
                      ("5-10 hari -> instan", "admin tahu anomali\nsaat input", NAVY)])
    pdf.set_xy(12, 90); bullets(pdf, [
        "*Dapat dipercaya: vonis stabil, tidak berubah gara-gara data bulan berikutnya.",
        "*Akurat: tahan terhadap banyak outlier; band pas ~95% pada data normal.",
        "*Layak: cocok untuk input real-time; bonus deteksi typo input otomatis.",
    ], size=12, lh=9)

    # 3 proses bisnis + masalah waktu
    head(pdf, "Proses Bisnis & Masalah Saat Ini", "kenapa ini penting")
    bullets(pdf, [
        "Admin input angka konsumsi -> sistem cek posisi terhadap rentang (band) -> vonis NORMAL / ANOMALI.",
        "Masalah 1 (verifikasi lama): data harus lewat 2 TINGKAT verifikasi, butuh 5-10 HARI kembali ke admin.",
        "  Akibat: kalau ada anomali, admin baru tahu seminggu kemudian - terlambat menyelidiki.",
        "Masalah 2 (band goyah): rumus lama hitung band dari data tahun berjalan yang menumpuk,",
        "  sehingga vonis sebuah bulan bisa BERUBAH saat data bulan lain masuk (padahal angkanya tetap).",
        "*Solusi: band rolling dari sejarah -> vonis instan saat input + stabil selamanya.",
    ], size=11.5, lh=8.5)

    # 4 waktu figure
    image_slide(pdf, "Dampak Kecepatan untuk Admin", "07_waktu.png",
                "Tanpa menunggu siklus verifikasi 5-10 hari, admin bisa langsung menyelidiki dugaan anomali.",
                "manfaat utama")

    # 5 cara lama vs baru
    head(pdf, "Akar Masalah: Band Lama Dihitung dari Data yang Sedang Dinilai", "konsep")
    two_col(pdf, "CARA LAMA (tahun berjalan menumpuk)",
            "Jan dinilai dari {Jan}\n"
            "Feb dinilai dari {Jan, Feb}\n"
            "Mar dinilai dari {Jan, Feb, Mar}\n...\n\n"
            "-> band berubah tiap bulan\n"
            "-> vonis bulan lama ikut berubah\n"
            "-> band tercemar angka yang dinilai",
            "CARA BARU (rolling, historis)",
            "Band bulan M dari 12 bulan SEBELUM M\n"
            "Contoh band Mar-2025 = Mar-2024..Feb-2025\n\n\n"
            "-> band siap SEBELUM admin input\n"
            "-> vonis instan & tidak berubah\n"
            "-> tidak memakai bulan yang dinilai")

    # 6 kestabilan figure
    image_slide(pdf, "Bukti 1 — Kestabilan Vonis", "01_kestabilan.png",
                "Dari 605 unit, cara lama 'berubah pikiran' pada 210 unit (301 kali). Cara baru: nol, secara desain.",
                "dapat dipercaya")

    # 7 contoh band
    image_slide(pdf, "Contoh Nyata Satu Unit", "03_contoh_band.png",
                "Band rolling robust menandai bulan anjlok (Okt-Des) sebagai anomali; band lama terlalu lebar sehingga lolos.",
                "ilustrasi")

    # 8 robustness figure
    image_slide(pdf, "Bukti 2 — Ketahanan terhadap Outlier", "02_robustness.png",
                "Saat satu unit punya >1 anomali (umum di data nyata), cara lama hampir buta (8-15%); robust tetap 74-82%.",
                "akurat")

    # 9 teori
    head(pdf, "Landasan Teori (bukan rumus karangan)", "dasar ilmiah")
    bullets(pdf, [
        "*Median & MAD punya 'breakdown point' 50%: tahan walau separuh data tercemar outlier.",
        "Mean & std punya breakdown point 0%: satu outlier saja sudah merusak band.",
        "Konstanta 1.4826 menyetarakan MAD dengan standar deviasi pada data normal (perbandingan adil).",
        "Masking: outlier menggelembungkan std -> anomali lain lolos. Swamping: titik normal salah ditandai.",
        "Rujukan: Rousseeuw & Hubert, 'Anomaly Detection by Robust Statistics' (arXiv:1707.09752);",
        "  Hampel Identifier (MAD-based); estimator skala Rousseeuw-Croux.",
    ], size=11.5, lh=8.5)
    pdf.set_xy(12, 150); pdf.set_font("Helvetica", "I", 10); pdf.set_text_color(*GREY)
    pdf.multi_cell(297 - 24, 6, "Catatan: sumber dirangkum ulang & diparafrasekan untuk mematuhi lisensi.")
    pdf.set_text_color(*DARK)

    # 10 production vs domestic
    image_slide(pdf, "Band Dipisah: Production vs Domestic", "05_prod_dom.png",
                "Pemakaian Production bisa 7-94x lebih besar dari Domestic pada unit yang sama. Satu band untuk keduanya pasti salah.",
                "cara membagi band")
    head(pdf, "Cara Membagi Band per Jenis Pemakaian", "aturan")
    bullets(pdf, [
        "Kunci band = Division + LOB + Unit + Jenis Energi (+ Energy Source) + JENIS PEMAKAIAN.",
        "*Production dan Domestic dihitung sebagai dua seri TERPISAH, masing-masing band sendiri.",
        "Alasan: skalanya beda jauh (median rasio ~7-9x, ekstrem s/d 94x) -> digabung menghasilkan band palsu.",
        "Implementasi sudah demikian di loader: 'Usage Type' bagian dari kunci unit.",
    ], size=12, lh=9)

    # 11 musiman
    image_slide(pdf, "Energi Musiman / Event (banyak bulan kosong)", "06_musiman.png",
                "Non-Renewable banyak yang musiman (48 unit) atau jarang (13). Band harus sadar pola ini agar tidak salah vonis.",
                "kasus khusus")
    head(pdf, "Aturan untuk Data Musiman / Kosong", "kasus khusus")
    bullets(pdf, [
        "Bulan KOSONG (tidak ada pemakaian) != anomali. Diperlakukan 'tidak dinilai', bukan nol paksa.",
        "Band dihitung hanya dari bulan yang benar-benar ada pemakaian (nilai valid).",
        "*Syarat minimum: >=3 bulan historis. Di bawah itu tampilkan 'data historis belum cukup'.",
        "Unit baru / musiman: gunakan jendela sebisanya; sistem tetap memberi jawaban, tidak error.",
        "Opsi lanjut: band musiman (bandingkan bulan vs bulan yang sama tahun lalu) bila pola kuat.",
    ], size=11.5, lh=8.5)

    # 12 typo
    image_slide(pdf, "Bonus: Deteksi TYPO Input Otomatis", "04_typo.png",
                "274 kandidat typo ditemukan: kelebihan/kurang nol & salah pemisah ribuan. Contoh: 45.532 vs median 562 (81x).",
                "akurat - temuan baru")
    head(pdf, "Jenis Typo yang Tertangkap", "kualitas data")
    bullets(pdf, [
        "*Kelebihan 1 nol (x10): 94 kasus  -  mis. 2.000 ditulis 20.000.",
        "*Kurang 1 nol (/10): 176 kasus  -  mis. 500 ditulis 50.",
        "*Salah pemisah ribuan/desimal (x100): 4 kasus  -  mis. 5,62 jadi 562.",
        "Deteksi pakai rasio nilai terhadap median robust unit (median tahan outlier).",
        "Manfaat: menangkap kesalahan input manusia SEBELUM masuk verifikasi 2 tingkat.",
    ], size=12, lh=9)

    # 13 manfaat
    head(pdf, "Informasi Ini Bermanfaat untuk Apa Saja", "nilai bisnis")
    bullets(pdf, [
        "*Admin: tahu seketika saat input, langsung investigasi (tak tunggu 5-10 hari).",
        "*Verifikator: fokus hanya pada yang ditandai -> beban kerja 2 tingkat jauh berkurang.",
        "*Kualitas data: typo (titik-koma/nol) tertangkap dini, laporan energi lebih bersih.",
        "*Manajemen energi: pola turun/naik tak wajar cepat terlihat (potensi kebocoran/pemborosan).",
        "*Audit & keberlanjutan: jejak anomali terdokumentasi, angka lebih bisa dipertanggungjawabkan.",
        "*Perencanaan: band stabil jadi acuan target konsumsi per unit.",
    ], size=12, lh=9)

    # 14 kesimpulan
    head(pdf, "Kesimpulan", "putusan")
    kpi_row(pdf, 40, [("DIPERCAYA", "vonis stabil\n0 perubahan (vs 301)", GREEN),
                      ("AKURAT", "74-82% deteksi\ncoverage ~95%", GREEN),
                      ("LAYAK", "real-time + deteksi typo\nunit baru tertangani", GREEN)])
    pdf.set_xy(12, 92); bullets(pdf, [
        "*Rekomendasi: adopsi band ROLLING 12 bulan + estimator ROBUST (median + MAD x 1.4826),",
        "  dipisah per jenis pemakaian (Production / Domestic), dengan aturan khusus data musiman.",
        "Langkah aman: jalankan paralel 1-2 bulan (lama vs baru) sebelum switch penuh.",
    ], size=12, lh=9)

    # 15a biaya tersembunyi: pertanyaan berulang
    image_slide(pdf, "Biaya Tersembunyi Alur Lama: Pertanyaan Berulang", "11_tanya_berulang.png",
                "Band bergerak tiap bulan -> data sama ditanya ulang (rata-rata 4,3x). Alasan disimpan di notepad pribadi, jadi hilang & ditanya lagi.",
                "workload - temuan kunci")
    head(pdf, "Kenapa Alur Baru Memangkas Beban Lintas-Bulan", "temuan kunci")
    bullets(pdf, [
        "Alur LAMA: band LCL/UCL dihitung ulang tiap bulan -> status anomali bulan lama BERGERAK.",
        "  -> data yang sama ditanyakan berulang (rata-rata 4,3x; ~1.400 tanya ulang/tahun).",
        "  -> tiap siklus tanya-jawab 5-10 hari, berjenjang Corporate -> Verificator -> Submittor -> Admin.",
        "  -> alasan disimpan di notepad pribadi Corporate (tercecer, ditanya lagi sampai akhir tahun).",
        "*Alur BARU: SR Admin isi alasan saat input -> melekat pada data, terlihat semua pihak.",
        "*Karena band rolling TIDAK menggeser vonis bulan lama, satu alasan berlaku PERMANEN -> tak ditanya ulang.",
        "Inilah penghematan terbesar bagi Submittor & Verificator (tak tertangkap di model satu-bulan).",
    ], size=11, lh=8)

    # 15a2 timeline siklus anomali
    image_slide(pdf, "Timeline Siklus Anomali: Deteksi -> 'OK with Notes'", "12_timeline.png",
                "Alur lama 2 tahap (10-20 hari/putaran) x pengulangan 4,3x = 43-86 hari/anomali. Alur baru: 1-3 hari (akurat) atau ~0 (typo, perbaiki di JSRS).",
                "workload - kecepatan proses")
    head(pdf, "Dua Tahap Proses Saat Ini (di luar sistem)", "rincian alur")
    bullets(pdf, [
        "Tahap 1 (deteksi -> unit dapat notif): HO QlikSense -> Division PIC cek BI -> email Corporate -> diskusi. ~5-10 hari.",
        "  Jika datanya SALAH (typo): Division PIC cukup perbaiki di JSRS, tanpa ke Corporate.",
        "Tahap 2 (investigasi -> corrective -> 'OK with Notes'): di luar sistem, Division PIC <-> Corporate. ~5-10 hari.",
        "*Alur baru: Tahap 1 ~ 0 (admin tahu saat input); typo terpotong; Tahap 2 menyusut (alasan terlampir); tanpa pengulangan.",
        "Catatan: durasi hari = ASUMSI dari narasi proses; jumlah anomali & pengganda 4,3x = DIHITUNG dari data.",
    ], size=11, lh=8)

    # 15b workload — struktural & risiko
    image_slide(pdf, "Beban Submittor & Verificator (struktural)", "08_workload_struktural.png",
                "Beban antar-divisi sudah timpang: Commercial Poultry ~18 entri/Submittor & ~66 entri/Verificator per bulan (data energi).",
                "workload - apa adanya")
    image_slide(pdf, "Risiko: Beban Bisa NAIK (jujur)", "09_workload_beforeafter.png",
                "Rumus baru menandai ~8x lebih banyak anomali (2,1% -> 16,5%). Cek dokumen jadi wajib -> beban cek bisa bertambah (skenario, asumsi).",
                "workload - risiko")
    image_slide(pdf, "Titik Impas Beban", "10_breakeven.png",
                "Submittor untung hanya bila a_baru < titik impas. Saat ini mayoritas di atasnya -> perlu cek dokumen efisien / kalibrasi ambang.",
                "workload - syarat untung")
    head(pdf, "Workload: Kesimpulan Jujur", "nilai bagi pemeriksa")
    bullets(pdf, [
        "Per-bulan: cek dokumen bisa NAIK (median +30-50 mnt/orang/bln di divisi padat) karena anomali baru lebih sensitif.",
        "*Lintas-bulan: beban TURUN karena pertanyaan berulang hilang (alur lama: 1 anomali ditanya 4,3x).",
        "*Bersih: penghematan dari hilangnya tanya ulang lintas-bulan menutup kenaikan cek dokumen per-bulan.",
        "Manfaat jelas juga di ADMIN & CORPORATE (tahu saat input, alasan melekat permanen).",
        "Syarat optimal: cek dokumen ringkas/sampling + sediakan FIELD ALASAN di sistem (ganti notepad).",
        "Catatan: waktu per-entri ASUMSI; pertanyaan berulang 4,3x DIHITUNG dari data.",
    ], size=11, lh=8)

    # 15 langkah demo
    head(pdf, "Langkah Demo ke Stakeholder", "panduan presentasi")
    bullets(pdf, [
        "1. Buka dengan MASALAH: tunjukkan satu unit yang vonisnya berubah-ubah (slide contoh).",
        "2. Tanyakan ke audiens: 'bisa dipercaya kalau vonis berubah sendiri?' - bangun urgensi.",
        "3. Tunjukkan BUKTI 1 (kestabilan 210->0) lalu BUKTI 2 (deteksi 74-82% vs 8-15%).",
        "4. Hubungkan ke TEORI singkat (breakdown point 50%) agar kredibel, jangan lama-lama.",
        "5. Tunjukkan BONUS typo (angka 45.532 vs 562) - ini biasanya 'wow moment'.",
        "6. Tutup dengan MANFAAT & kecepatan (5-10 hari -> instan) + rencana uji paralel.",
        "7. Siapkan file: SLIDE_JSRS.pdf, dashboard (figs/), dan demo live 'python jsrs_rolling.py'.",
    ], size=11.5, lh=8.5)

    out = _D("SLIDE_JSRS.pdf")
    # pastikan tersimpan di root sandbox juga
    pdf.output(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SLIDE_JSRS.pdf"))
    print("PDF dibuat: SLIDE_JSRS.pdf (15 slide)")

if __name__ == "__main__":
    build()
