# Analisis Workload Submittor & Verificator — JSRS

Menguji hipotesis: *apakah deteksi anomali baru juga menguntungkan Submittor & Verificator?*
**Jawaban singkat: belum tentu — tergantung parameter, dan pada skenario median beban justru NAIK.**
Analisis ini sengaja jujur, bukan mencari pembenaran.

> **Label angka:** `(a)` dihitung dari data · `(b)` asumsi parameter · `(c)` belum bisa dihitung.
> **Keterbatasan:** angka akun ≠ jumlah orang aktif (1 orang bisa banyak akun). Volume input
> yang tersedia **hanya energi** (listrik + non-renewable); air/limbah belum ada. Nama divisi
> akun seperti "Poultry Breeding - North" dipetakan ke divisi energi "Poultry Breeding".

---

## 1. Tabel Struktural per Divisi `(a)`

Beban entri per pemeriksa (entri energi/bulan, dialokasikan proporsional ke jumlah SR Admin).

| Divisi | R | S | V | N/bulan | entri/S | entri/V | admin/S | admin/V | V/S | single point |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--:|
| Commercial Poultry | 98 | 25 | 7 | 461 | **18,4** | **65,9** | 3,9 | 14,0 | 0,3 | |
| Aquaculture | 26 | 5 | 2 | 62 | 12,5 | 31,2 | 5,2 | 13,0 | 0,4 | |
| Poultry Breeding | 132 | 30 | 15 | 334 | 11,1 | 22,3 | 4,4 | 8,8 | 0,5 | |
| Poultry Feed | 35 | 9 | 8 | 76 | 8,4 | 9,5 | 3,9 | 4,4 | 0,9 | |
| SBU Grains Trading | 35 | 7 | 5 | 57 | 8,2 | 11,4 | 5,0 | 7,0 | 0,7 | |
| Poultry Processing | 16 | 15 | 3 | 53 | 3,5 | 17,7 | 1,1 | 5,3 | 0,2 | |
| Consumer Foods | 20 | 13 | 18 | 43 | 3,3 | 2,4 | 1,5 | 1,1 | 1,4 | |

**Ketimpangan yang perlu dicatat:**
- **Commercial Poultry:** 1 Verificator menanggung ~66 entri + ~14 SR Admin → titik beban tertinggi.
- **Single point of load (S=1 atau V=1):** Dairy, Swine, SBU Property, Rice Business, Marketing & Sales,
  Dairy and Beef, CORP. Technical Services, Swine-South, Cattle & Poultry Feed-South. Satu orang = satu-satunya pemeriksa.
- Divisi tanpa data energi (Dairy, Swine, Head Office, dll.) → kolom N kosong, ditandai "tak ada data".

---

## 2. Beban Anomali per Bulan `(a)`

Tingkat anomali dari data nyata: **global `a_lama` = 2,1%  vs  `a_baru` = 16,5%** (rumus baru ~8× lebih sensitif).

| Divisi | a_lama | a_baru | anomali/S lama | anomali/S baru | anomali/V baru |
|---|--:|--:|--:|--:|--:|
| Aquaculture | 0,03 | 0,23 | 0,38 | **2,88** | **7,21** |
| Commercial Poultry | 0,01 | 0,12 | 0,18 | 2,26 | 8,08 |
| Poultry Breeding | 0,03 | 0,19 | 0,36 | 2,16 | 4,33 |
| Poultry Feed | 0,02 | 0,18 | 0,17 | 1,55 | 1,74 |

> `a_baru` jauh di atas `a_lama` → lebih banyak entri butuh cek dokumen (kewajiban baru).
> **Inilah risiko utama bagi Submittor/Verificator** dan tidak boleh diabaikan.

---

## 3. Sebelum vs Sesudah (menit/orang/bulan) `(b: median rentang asumsi)`

Parameter asumsi: `t_cek` 2–5, `t_dok` 10–20, `t_tanya` 15–30, `r_lama` 2–4, `r_baru` 0–1 menit/putaran.

| Divisi | Sebelum (S) | Sesudah (S) | Δ median | Δ min | Δ maks |
|---|--:|--:|--:|--:|--:|
| Aquaculture | 72 | 120 | **+48** | −17 | +121 |
| Commercial Poultry | 78 | 122 | **+43** | +1 | +102 |
| Poultry Breeding | 66 | 98 | **+33** | −21 | +87 |
| Cattle & Poultry Feed-South | 44 | 74 | +28 | −5 | +69 |

**Temuan jujur:** pada parameter **median**, beban Submittor **NAIK** di hampir semua divisi berdata.
Penyebab: lonjakan `a_baru` + kewajiban cek dokumen (`t_dok`) lebih besar daripada penghematan
tanya-jawab berjenjang (`r_lama → r_baru`). Rentang Δ min menunjukkan beban bisa **turun** hanya
jika `t_dok` kecil, `r_lama` besar, dan `a_baru` tidak setinggi angka in-sample.

---

## 4. Titik Impas `(b)`

`a*` = `a_lama × r_lama × t_tanya / (t_dok + r_baru × t_tanya)` (parameter mid).
Jika **`a_baru < a*`** → Submittor diuntungkan.

| Divisi | a_lama | a_baru | a* (impas) | Untung? |
|---|--:|--:|--:|:--:|
| SBU Aqua Processing | 0,054 | 0,192 | 0,140 | tidak |
| Poultry Processing | 0,037 | 0,208 | 0,095 | tidak |
| Poultry Breeding | 0,032 | 0,194 | 0,083 | tidak |
| SBU Property | 0,083 | 0,083 | 0,214 | **ya** |
| Commercial Poultry | 0,010 | 0,123 | 0,025 | tidak |

**Ringkasan:** pada parameter median, **Submittor diuntungkan hanya 1/20 divisi**; Verificator **1/20**.
Agar menguntungkan mayoritas, `a_baru` operasional harus turun ke kisaran **2,5–14%** (tergantung divisi),
ATAU `t_dok` ditekan (cek dokumen ringkas / sampling), ATAU `r_lama` saat ini memang tinggi (≥3 putaran).

---

## 5. Cara Membaca & Menjalankan

```bash
.venv/bin/python jsrs_workload.py     # semua tabel di atas -> workload_divisi.csv
python -c "import jsrs_dashboard as d; d.build_workload_figs()"  # grafik 08-10
```
Ubah asumsi di `PARAM` (atas file `jsrs_workload.py`). Grafik: `figs/08–10`.

---

## 6. Temuan Utama untuk Manajemen

1. **Secara struktural, beban sudah timpang** — Commercial Poultry & Aquaculture paling berat;
   banyak divisi bergantung pada **satu** pemeriksa (risiko operasional, terlepas dari rumus).
2. **Rumus baru menandai ~8× lebih banyak anomali** (2,1% → 16,5%). Tanpa penyesuaian, ini
   **menambah** beban Submittor/Verificator, bukan mengurangi — diperkirakan +30–50 mnt/orang/bulan
   di divisi padat (skenario median, asumsi).
3. **Manfaat nyata ada di sisi Admin & Corporate** (tahu anomali saat input, tak tunggu 5–10 hari).
   Agar Submittor/Verificator ikut untung, perlu: cek dokumen ringkas, atau kalibrasi ambang anomali,
   atau sampling dokumen untuk anomali berisiko rendah.
4. **Alasan terlampir sejak input memang memangkas tanya-jawab berjenjang** (`r_lama → r_baru`),
   tetapi penghematan ini belum cukup menutup biaya cek dokumen pada tingkat `a_baru` saat ini.
5. **Titik impas jelas:** jika tingkat anomali operasional bisa ditekan ke <~10% dan cek dokumen
   dibuat efisien, mayoritas divisi menjadi netral–untung.

---

## 7. Ringkasan 1 Slide

**Judul:** Dampak Fitur Anomali Baru ke Beban Submittor & Verificator

- Beban antar-divisi **sudah timpang** (Commercial Poultry: 1 Verificator ≈ 66 entri/bulan).
- Rumus baru lebih sensitif (**2,1% → 16,5%**) → tanpa penyesuaian, beban cek **naik**.
- Manfaat terbesar di **Admin & Corporate**; Submittor/Verificator untung **hanya jika** cek dokumen efisien / ambang dikalibrasi.
- **Rekomendasi:** uji paralel + tetapkan SOP cek dokumen ringkas sebelum rollout.

(Grafik utama: `figs/09_workload_beforeafter.png` atau `figs/10_breakeven.png`.)

---

## 8. Keterbatasan & Data yang Masih Dibutuhkan

- **`(c)` Parameter waktu** (`t_cek`, `t_dok`, `t_tanya`, `r_lama`, `r_baru`) belum ada → dipakai rentang asumsi.
  Minta data nyata dari 1–2 divisi percontohan untuk mengganti asumsi.
- **Volume input hanya energi.** Air/limbah/jenis lain belum masuk → beban sebenarnya lebih tinggi.
- **Angka akun ≠ orang aktif.** Perlu data akun aktif & siapa benar-benar memeriksa.
- **`a_baru` in-sample** (tahun pertama rolling). Setelah berjalan stabil, `a_baru` operasional
  kemungkinan **lebih rendah**; perlu diukur ulang setelah 2–3 bulan.
- **Distribusi unit antar sub-divisi** (North/South) diperkirakan proporsional ke SR Admin;
  idealnya pakai pemetaan unit→divisi yang sebenarnya.
