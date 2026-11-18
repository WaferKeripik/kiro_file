# Evaluasi Rumus Deteksi Anomali JSRS — Ringkasan Temuan

Dokumen ini menjawab tiga pertanyaan: **apakah rumus baru dapat dipercaya, akurat, dan layak dipakai?**
Semua angka diambil dari data produksi nyata (Listrik & Non-Renewable Energy, FY2024 + FY2025).

---

## 1. Konteks & Proses Bisnis

Sistem dipakai saat **admin menginput angka konsumsi bulanan**. Sistem langsung memvonis
angka itu **anomali / normal** berdasarkan posisinya terhadap rentang kendali (band)
`[Lower Control Limit, Upper Control Limit]`.

**Masalah cara lama (LCL/UCL sekarang):**
Band dihitung dari data **tahun berjalan yang menumpuk** — Januari dari {Jan}, Februari
dari {Jan, Feb}, Maret dari {Jan, Feb, Mar}, dst. Akibatnya:

- Rentang **berubah tiap kali ada data bulan baru**.
- **Vonis sebuah bulan bisa berubah di kemudian hari** walau angkanya tidak berubah
  (contoh: April dinilai "normal" 4 bulan, lalu mendadak "anomali" setelah Agustus masuk).
- Band tercemar oleh angka yang sedang dinilai → hampir selalu bilang "normal" (buta).

**Usulan:** band **rolling** dari data historis. Band bulan M dihitung dari 12 bulan
**sebelum** M (mis. band Mar-2025 = Mar-2024 … Feb-2025). Band sudah tersedia **sebelum**
admin input, dan tidak memakai bulan yang sedang dinilai → **vonis stabil**.

---

## 2. Landasan Teori

| Konsep | Rumus lama (classic) | Rumus baru (robust) |
|---|---|---|
| Pusat | rata-rata (mean) | median |
| Sebaran | standar deviasi (std) | MAD (Median Absolute Deviation) × 1.4826 |
| Breakdown point | **0%** (1 outlier merusak) | **50%** (tahan hingga ½ data tercemar) |

- **Breakdown point 50%** pada median & MAD: estimator tidak terdistorsi oleh nilai
  ekstrem yang justru ingin kita deteksi — inilah yang memperbaiki *masking*
  (Rousseeuw & Hubert, *Anomaly Detection by Robust Statistics*, arXiv:1707.09752;
  Hampel identifier).
- **Konstanta 1.4826** = `1 / Φ⁻¹(0.75)` membuat MAD konsisten dengan σ pada data
  normal, sehingga band robust & classic sebanding (PLOS ONE S1; Rousseeuw–Croux).
- **Masking**: outlier menggelembungkan std sampai anomali lain tak terdeteksi.
  **Swamping**: titik normal salah ditandai. Keduanya adalah kelemahan metode
  berbasis mean/std (arXiv:1707.09752).

Rumus band: `pusat ± t_crit × sebaran`, dengan `t_crit` nilai kritis distribusi-t
(derajat bebas = n−1). Disamakan antar metode agar perbandingan adil.

---

## 3. Hasil Uji

### 3.1 Kestabilan vonis — data nyata 2025 (605 unit berpasangan 2024→2025)

| Cara | Unit yang vonisnya goyah | Total "berubah pikiran" |
|---|---|---|
| **Lama** (band tahun-berjalan) | **210 / 605 (34.7%)** | **301 kali** |
| **Rolling** (band historis) | **0** | **0** (mustahil berubah secara desain) |

> Sepertiga unit pernah berubah vonis **tanpa angkanya berubah**. Rolling menghilangkan
> ini sepenuhnya karena band tidak pernah memakai data bulan yang dinilai.

**Contoh nyata (RO BR Jatim 2, For Domestic Use):**
Nilai April-2025 = 2.040 (tetap). Cara lama: "normal" (s/d Jul) → **"anomali"** (begitu
Agustus masuk). Cara baru rolling-robust: band `[2.658 … 3.212]` → **"anomali" sejak awal, tetap**.

### 3.2 Ketahanan terhadap outlier — simulasi ground-truth (nilai kritis disamakan)

| Skenario | Recall robust | Recall classic |
|---|---|---|
| 1 outlier ekstrem (5–9σ) | 1.000 | 1.000 |
| **3 outlier sedang (3–5σ)** | **0.820** | **0.154** |
| **4 outlier (3–6σ)** | **0.743** | **0.079** |

> Begitu ada **lebih dari satu** anomali dalam satu unit (pola umum di data produksi),
> classic/Excel hampir buta (8–15%) akibat *masking*. Robust tetap menangkap 74–82%.

### 3.3 Coverage pada seri stabil nyata (target ≈ 95%)

| Metode | Coverage (Listrik) | Coverage (Non-Renew) |
|---|---|---|
| Excel LCL/UCL | 100% | 100% |
| Classic | 100% | 100% |
| **Robust** | **95.6%** | **92.3%** |

> Band Excel memuat 100% titik "normal" → terlalu lebar, jarang menandai apa pun
> (batas bawahnya sering **negatif**, mustahil untuk konsumsi energi). Robust pas di ~95%.

### 3.4 Catatan kejujuran metodologis

Label `Accuracy Check` Excel **diturunkan langsung dari LCL/UCL** (0 titik di luar band
yang berlabel "OK"). Maka membandingkan metode terhadap label itu memenangkan Excel secara
**tautologis** (precision 1.0 semu). Evaluasi di atas sengaja memakai ground-truth sintetis
dan coverage netral, bukan label Excel.

---

## 4. Kesimpulan

| Kriteria | Putusan |
|---|---|
| **Dapat dipercaya?** | Ya. Vonis stabil — 0 perubahan vs 301 pada cara lama. |
| **Akurat?** | Ya. Menangkap 74–82% anomali majemuk vs 8–15% cara lama; coverage ~95%. |
| **Layak dipakai?** | Ya. Cocok untuk proses input real-time; band siap sebelum input. |

**Rekomendasi:** adopsi **band rolling 12 bulan + estimator robust (median + MAD×1.4826)**.
Untuk unit baru (<12 bulan sejarah): pakai jendela sebisanya bila ≥3 bulan; di bawah itu
tampilkan "data historis belum cukup".

---

## 5. Reproduksi

```bash
python3 -m venv .venv && .venv/bin/pip install numpy pandas scipy
.venv/bin/python jsrs_rolling.py   # perbandingan 3 cara (hasil utama)
.venv/bin/python jsrs_eval.py      # robustness, coverage, ketidaksepakatan
.venv/bin/python jsrs_backtest.py  # vs label Excel (+ catatan tautologi)
```

File: `jsrs_core.py` (band), `jsrs_loader.py` (baca CSV), `jsrs_rolling.py`,
`jsrs_eval.py`, `jsrs_backtest.py`.

*Sumber dirangkum ulang untuk mematuhi lisensi. Konten diparafrasekan.*
