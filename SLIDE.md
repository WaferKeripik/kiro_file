# SLIDE PRESENTASI — Rumus Deteksi Anomali Baru (JSRS)
> Format: satu `---` = satu slide. Bisa langsung dibuka di Marp / Slidev / reveal.js,
> atau disalin ke PowerPoint. Catatan pembicara ada di blok "🎤".

---

## 1 — Rumus Anomali Baru: Dapat Dipercaya, Akurat, Layak?

**Evaluasi dengan data produksi nyata**
Listrik & Non-Renewable Energy · FY2024 + FY2025 · 605 unit

🎤 Tiga pertanyaan yang akan dijawab dengan angka, bukan opini.

---

## 2 — Proses Bisnis: Di Mana Rumus Ini Dipakai

1. Admin **input angka konsumsi** bulan ini.
2. Sistem cek: angka **di dalam** rentang `[batas bawah, batas atas]`?
3. Keluar vonis otomatis: **NORMAL** atau **ANOMALI**.

➡️ Rentang (band) **harus sudah ada sebelum angka diinput.**

🎤 Jadi kualitas sistem = kualitas band. Band jelek → vonis jelek.

---

## 3 — Masalah Cara Lama (LCL/UCL Sekarang)

Band dihitung dari **data tahun berjalan yang menumpuk**:
- Jan dinilai pakai {Jan}
- Feb dinilai pakai {Jan, Feb}
- Mar dinilai pakai {Jan, Feb, Mar} …

**Akibatnya:**
- Band berubah tiap ada data baru.
- **Vonis bulan lama bisa berubah** walau angkanya tidak berubah.
- Band tercemar angka yang sedang dinilai → sering "buta".

🎤 Inilah sumber frustrasi: "kemarin normal, hari ini tiba-tiba anomali."

---

## 4 — Contoh Nyata Frustrasi (data produksi)

**Unit: RO BR Jatim 2 — nilai April 2025 = 2.040 (TIDAK pernah berubah)**

| Data masuk s/d | Vonis April (cara lama) |
|---|---|
| Apr–Jul | normal |
| **Agu** | **ANOMALI** ⚠️ |
| Sep–Des | ANOMALI |

➡️ Angka sama, vonis berubah hanya karena **bulan lain** masuk.

🎤 Ini membuat hasil tidak bisa dipercaya dan memicu perdebatan tiap bulan.

---

## 5 — Usulan: Band ROLLING dari Data Historis

Band bulan **M** dihitung dari **12 bulan sebelum M**.
Contoh: band **Maret 2025** = Mar 2024 … Feb 2025.

**Kenapa ini menyelesaikan masalah:**
- Band **siap sebelum** admin input.
- Band **tidak** memakai bulan yang dinilai → vonis **tidak bisa berubah** di masa depan.

🎤 "Rolling" = jendela 12 bulan yang bergeser tiap bulan.

---

## 6 — Dua Perbaikan Terpisah

| Perbaikan | Mengatasi | Manfaat |
|---|---|---|
| **Rolling** (historis) | band goyah | **KESTABILAN** vonis |
| **Robust** (median + MAD) | outlier merusak band | **AKURASI** deteksi |

🎤 Dua hal berbeda. Boleh diadopsi bertahap, tapi paling kuat jika keduanya.

---

## 7 — Landasan Teori

| | Lama (classic) | Baru (robust) |
|---|---|---|
| Pusat | rata-rata | **median** |
| Sebaran | standar deviasi | **MAD × 1.4826** |
| Breakdown point | **0%** | **50%** |

- **Breakdown point 50%**: tahan walau ½ data tercemar → tidak terkecoh outlier.
- **1.4826**: menyetarakan MAD dengan σ pada data normal (perbandingan adil).
- Referensi: Rousseeuw & Hubert (arXiv:1707.09752); Hampel Identifier; Rousseeuw–Croux.

🎤 Ini bukan rumus karangan — ini standar statistika robust yang mapan.

---

## 8 — Masking & Swamping (inti kelemahan cara lama)

- **Masking**: outlier menggelembungkan std → anomali lain **lolos** tak terdeteksi.
- **Swamping**: titik normal **salah** ditandai anomali.

➡️ Metode mean/std rentan keduanya. Median/MAD tahan.

🎤 Di data kita, satu unit sering punya beberapa bulan menyimpang — tepat kasus masking.

---

## 9 — BUKTI 1: Kestabilan (data nyata, 605 unit)

| Cara | Unit vonis goyah | Total "berubah pikiran" |
|---|---|---|
| **Lama** | **210 / 605 (34,7%)** | **301 kali** |
| **Rolling** | **0** | **0** |

➡️ **Sepertiga unit** pernah berubah vonis tanpa sebab. Rolling: **nol**.

🎤 Angka tunggal paling kuat untuk manajemen: 34,7% → 0%.

---

## 10 — BUKTI 2: Ketahanan Outlier (simulasi, kritikal disamakan)

| Skenario | Recall ROBUST | Recall CLASSIC |
|---|---|---|
| 1 outlier ekstrem | 1,00 | 1,00 |
| **3 outlier sedang** | **0,82** | **0,15** |
| **4 outlier** | **0,74** | **0,08** |

➡️ Saat anomali >1, cara lama **hampir buta** (8–15%). Robust tetap 74–82%.

🎤 Inilah bukti "akurat": di kasus sulit, selisihnya besar sekali.

---

## 11 — BUKTI 3: Coverage Seri Normal (target ≈95%)

| Metode | Listrik | Non-Renew |
|---|---|---|
| Excel LCL/UCL | 100% | 100% |
| **Robust** | **95,6%** | **92,3%** |

➡️ Band Excel 100% = terlalu lebar, batas bawah sering **negatif** (mustahil).
Robust pas di ~95%.

🎤 Band yang "selalu bilang normal" bukan pengaman — itu cuma hiasan.

---

## 12 — Kejujuran Metodologis

Label `Accuracy Check` Excel **diturunkan dari LCL/UCL** itu sendiri.
→ Membandingkan ke label itu **memenangkan Excel secara otomatis** (semu).

➡️ Maka evaluasi memakai **ground-truth sintetis** + **coverage netral**,
bukan label Excel.

🎤 Penting disebut agar hasil tidak dituduh bias.

---

## 13 — Unit Baru (belum punya 12 bulan)

- Sejarah ≥ 3 bulan → band rolling dihitung **sebisanya**, sistem tetap memberi vonis.
- Sejarah < 3 bulan → tampilkan **"data historis belum cukup"** (bukan error).

🎤 Proses input tidak pernah mentok; kasus unit baru sudah ditangani.

---

## 14 — Kesimpulan

| Pertanyaan | Jawaban | Bukti |
|---|---|---|
| **Dapat dipercaya?** | ✅ Ya | 0 vonis goyah (vs 301) |
| **Akurat?** | ✅ Ya | 74–82% vs 8–15% anomali majemuk; coverage ~95% |
| **Layak dipakai?** | ✅ Ya | Siap untuk input real-time; unit baru ditangani |

**Rekomendasi: adopsi band ROLLING 12 bulan + ROBUST (median + MAD×1.4826).**

---

## 15 — Langkah Lanjut

1. Terapkan di pipeline input (band dihitung saat data historis masuk).
2. Pantau 1–2 bulan: bandingkan vonis lama vs baru secara paralel.
3. Kalibrasi tingkat kepercayaan (95% default) sesuai toleransi bisnis.

🎤 Reproduksi penuh: `python jsrs_rolling.py`, `jsrs_eval.py`, `jsrs_backtest.py`.

---

## 16 — Masalah Kecepatan: Verifikasi 2 Tingkat (5–10 Hari)

Sekarang: data input → **verifikasi tingkat 1** → **verifikasi tingkat 2** →
baru kembali ke admin. **Butuh 5–10 hari.**

➡️ Kalau ada anomali, admin **baru tahu seminggu kemudian** — terlambat menyelidiki.

**Dengan sistem baru:** vonis muncul **saat input**. Admin langsung investigasi.

🎤 Ini manfaat yang paling terasa untuk operasional harian.

---

## 17 — Band Dipisah: Production vs Domestic

Pada unit yang sama, pemakaian **Production bisa 7–94× lebih besar** dari Domestic.

➡️ Satu band untuk keduanya → pasti salah vonis.

**Aturan:** `Usage Type` jadi bagian kunci → dihitung sebagai **dua seri terpisah**,
band masing-masing.

🎤 Contoh: FeedMill Sragen — Production 912.956 vs Domestic 9.743 (94×).

---

## 18 — Energi Musiman / Event (Banyak Bulan Kosong)

Sebagian unit hanya dipakai musiman/saat event → banyak bulan kosong
(Non-Renewable: 48 musiman, 13 jarang).

**Aturan:**
- Bulan kosong **≠ anomali** (tidak dinilai, bukan dipaksa nol).
- Band hanya dari bulan ber-nilai.
- Minimum **≥3 bulan** sejarah; di bawah itu: "data historis belum cukup".

🎤 Mencegah sistem "menyalakan alarm" hanya karena unit sedang tidak beroperasi.

---

## 19 — BONUS: Deteksi Typo Input Otomatis

**274 kandidat typo** ditemukan di data nyata:
- Kurang 1 nol (÷10): 176 · Kelebihan 1 nol (×10): 94 · Salah pemisah (×100): 4

➡️ Contoh: **45.532** vs median unit **562** = **81×** → jelas typo.

🎤 Sistem menangkap salah ketik SEBELUM masuk verifikasi 5–10 hari. "Wow moment".

---

## 20 — Manfaat untuk Siapa Saja

- **Admin** — tahu anomali seketika, langsung investigasi.
- **Verifikator** — fokus ke yang ditandai; beban 2 tingkat berkurang.
- **Kualitas data** — typo tertangkap dini, laporan lebih bersih.
- **Manajemen energi** — pemborosan/kebocoran cepat terlihat.
- **Audit & keberlanjutan** — jejak anomali terdokumentasi.
- **Perencanaan** — band stabil jadi acuan target.

🎤 Satu perubahan rumus, manfaat lintas fungsi.

---

## 21 — Langkah Demo ke Stakeholder (ringkas)

1. Mulai dari **masalah** (band goyah + tunggu 5–10 hari).
2. Tunjukkan **bukti kestabilan** (210 → 0) & **akurasi** (74–82% vs 8–15%).
3. Sentuh **teori** singkat (breakdown point 50%).
4. Tunjukkan **typo** (45.532 vs 562) sebagai bonus.
5. Tutup dengan **manfaat + rencana uji paralel 1–2 bulan**.

Detail lengkap: **DEMO.md**. Demo live: `python jsrs_rolling.py`, `jsrs_insight.py`.

🎤 PDF siap: **SLIDE_JSRS.pdf**. Dashboard: folder **figs/**.
