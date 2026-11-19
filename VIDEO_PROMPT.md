# Prompt Motion Graphic Video — NEW Anomaly Detection (Tim Horei, JSRS)

> Dipakai untuk: generator video AI (Sora / Runway / Veo / Kling) **atau** brief untuk motion designer.
> Sumber konten: `PITCH_DECK.md`. Semua angka berlabel bukti; jaga kejujuran.
>
> **Penamaan (penting):** "Horei" = nama **tim proyek**, bukan nama produk, dan **bukan AI** — ini sebuah
> solusi/metode, bukan kecerdasan buatan. Nama solusi sementara: **"NEW anomaly detection"**.
> **Hindari kata "vonis".** Gunakan: "status", "hasil penilaian", "ditandai normal / perlu dicek".

---

## 0. CATATAN SUMBER ANGKA (baca dulu — agar konsisten di layar)

Ada **dua sumber data berbeda**; jangan dicampur:

- **Data energi** = gabungan dua jenis: **Listrik** + **Non-Renewable Energy** (FY2024 & FY2025).
  Air/limbah **belum** termasuk.
- **Data akun** = daftar pengguna per peran, mencakup **31 divisi** (lebih banyak dari data energi).

Angka kunci & asalnya:

| Angka | Arti | Dari mana |
|---|---|---|
| **605 unit** | seri yang cocok 2024↔2025 **pada data Listrik saja** | `jsrs_rolling.build_timeline` (Listrik) `[NYATA]` |
| (577 unit) | pasangan pada Non-Renewable (jangan dicampur ke 605) | idem `[NYATA]` |
| **210 (34,7%) / 301 kali** | unit yang status-nya sempat berubah & total perubahan | basis **605 unit Listrik** `[NYATA]` TEMUAN §3.1 |
| **16 divisi** | divisi unik **pada data energi** | loader `[NYATA]` |
| **9 divisi** | divisi dengan **1 Submittor ATAU 1 Verificator** | dihitung dari **data akun 31 divisi** `[NYATA]` |
| **431 → 1.833 · 4,3×** | kemunculan anomali berulang | data energi (Listrik+NonRenew) `[NYATA]` WORKLOAD §6b |
| **11 rata-rata / 66 puncak** | entri per Verificator/bulan | data energi `[NYATA]` RISET §A |
| **274 kandidat typo** | dugaan salah input (belum divalidasi) | data energi `[NYATA-kandidat]` |

> **Perlu dipastikan sebelum tayang** (jangan tampilkan sebagai angka pasti):
> - **Corporate** sebenarnya tim kecil **~3–4 orang** yang mengolah data (angka akun 641 ≠ jumlah orang).
> - **Submittor & Verificator:** dasarnya **1 Submittor + 1 Verificator** per divisi, tapi ada divisi di mana
>   **1 orang memegang 2 peran** → angka akun ≠ jumlah orang aktif.
> - Bila ragu, tampilkan sebagai "sekitar" atau beri label `[perlu dikonfirmasi]`.

---

## 1. SPESIFIKASI TEKNIS

| Item | Nilai |
|---|---|
| Rasio | 16:9 (YouTube landscape) |
| Resolusi | 1920×1080 (1080p), 4K bila memungkinkan |
| Durasi | maksimal **5:00** menit |
| Frame rate | 30 fps |
| Gaya | profesional, minimalis, motion graphic 2D |
| Audio | voice-over Indonesia tenang + musik ambient-corporate lembut |

---

## 2. ARAHAN GAYA VISUAL (GLOBAL)

- **Nada warna: calm / soft.**
  - Dasar: off-white `#F5F3EF` / soft grey `#ECEFF1`
  - Aksen tenang: sage-teal `#4C8C84`, deep navy `#1A2A4A`
  - Aksen "perlu dicek" (hangat, tak mencolok): muted terracotta `#C77B5A`
  - Hijau "stabil/selesai": `#1E7D4F`
- **Tipografi:** sans-serif geometris bersih (Inter / Poppins / Satoshi). Judul tebal, body ringan.
- **Gerak:** easing halus, transisi fade/slide pelan, angka **count-up**, garis **draw-on**, banyak ruang kosong.
- **Motif signature:** garis rentang (band) yang **bergeser tiap bulan** (masalah) → berubah mulus jadi band
  **terkunci stabil** (solusi). Pakai motif ini berulang.
- **Hindari:** kata "vonis"; stok foto ramai; warna neon; 3D berlebihan; teks padat; menyebut "AI".

---

## 3. STRUKTUR & NASKAH PER SEGMEN

> Format: **[waktu] Judul · Voice-over (ID) · Visual · Teks layar.** Nada tenang, menghargai proses lama.

### SEG 1 — Hook (0:00–0:30)
- **VO:** "Bayangkan sebuah angka yang tidak berubah. Bulan lalu ditandai normal. Bulan ini tiba-tiba perlu dicek. Padahal angkanya sama."
- **Visual:** satu titik data; band rentang di belakangnya **bergeser** naik-turun tiap bulan sehingga titik yang sama berpindah dari dalam ke luar.
- **Teks:** "Angka sama. Statusnya berubah." → **34,7%** (count-up).

### SEG 2 — Dua pilar masalah (0:30–1:05)
- **VO:** "Masalahnya ada di dua sisi. Pertama, deteksi: rentang kendali dihitung ulang tiap bulan, jadi statusnya bergeser. Kedua, komunikasi: satu anomali bisa ditanyakan berulang sebelum sampai ke penginput."
- **Visual:** layar terbelah. Kiri: grafik band goyah ("Deteksi"). Kanan: rantai berjenjang memanjang ("Komunikasi").
- **Teks:** "Dua pilar: Deteksi · Komunikasi" · badge "data produksi nyata".

### SEG 3 — Ini nyata, bukan prediksi (1:05–1:40)
- **VO:** "Ini bukan simulasi. Dari enam ratus lima unit listrik pada data produksi, dua ratus sepuluh pernah berubah status tanpa angkanya berubah — tiga ratus satu kali."
- **Visual:** grid 605 titik; 210 menyala terracotta; counter "301" count-up. Zoom ke satu unit: garis datar di 2.040, label "April: normal → Agustus: perlu dicek" tanpa titiknya bergerak.
- **Teks:** "605 unit listrik · 210 berubah · 301 kali" · stempel "[DATA NYATA]".
- **Catatan:** sebut **"605 unit listrik"** — jangan tampilkan sebagai total semua jenis energi.

### SEG 4 — Magnitude: beban & biaya berulang (1:40–2:25)
- **VO:** "Bebannya tidak merata. Rata-rata sekitar sebelas entri per pemeriksa tiap bulan — tapi di satu divisi mencapai enam puluh enam. Dan karena rentang terus bergeser, data yang sama ditanyakan rata-rata empat koma tiga kali."
- **Visual:** bar halus 11 vs 66; lalu animasi 431 titik menggandakan diri jadi 1.833.
- **Teks:** "≈11 rata-rata · 66 puncak" → "431 → 1.833 · 4,3×" · catatan kecil "data energi: listrik + non-renewable; air/limbah belum dihitung".

### SEG 5 — Siapa yang terdampak (2:25–2:50)
- **VO:** "Beberapa peran terlibat: SR Admin yang menginput, Submittor dan Verificator yang memeriksa, dan tim Corporate yang mengolah data — melewati dua sistem sebelum penginput tahu."
- **Visual:** alur minimalis SR Admin → Submittor → Verificator → Corporate, dengan HO & Division PIC di jalur.
- **Teks:** "Beberapa peran · 2 sistem · 1 jalur panjang".
- **Catatan jujur:** jangan pajang angka orang yang belum pasti. Corporate = **tim kecil ~3–4 orang** `[perlu dikonfirmasi]`;
  Submittor/Verificator dasarnya 1+1 per divisi, sebagian **1 orang 2 peran** `[perlu dikonfirmasi]`.
  Angka akun (mis. 499/192/135/641) hanya tampil bila diberi label "jumlah akun, bukan jumlah orang".

### SEG 6 — Latar & tujuan (2:50–3:15)
- **VO:** "Akar penyebabnya: rentang yang bergantung pada data bulan berjalan, dan alasan anomali yang dicatat di luar sistem. Tujuan kami sederhana — status yang stabil, diketahui saat input, dengan pemeriksaan yang terfokus."
- **Visual:** notepad kertas (alasan tercecer) memudar → kartu digital "alasan tersimpan di sistem". Tiga ikon: stabil / saat input / fokus.
- **Teks:** "Stabil · Saat input · Terfokus".

### SEG 7 — Solusi: cara lama vs baru (less technical) (3:15–3:55)
- **VO:** "Kami mengganti cara perhitungan lama dengan rentang yang mengikuti dua belas bulan terakhir dan lebih tahan terhadap angka yang melonjak. Hasilnya, rentang tidak lagi bergeser tiap bulan, dan lebih jarang salah menandai."
- **Visual:** motif signature — band "goyah" berubah mulus jadi band "terkunci stabil". Tambahkan ilustrasi sederhana:
  saat ada beberapa lonjakan sekaligus, cara lama "ikut melebar lalu kehilangan jejak", cara baru "tetap pada pola wajar".
  (Hindari istilah teknis seperti recall/outlier/MAD di layar; simpan untuk Q&A.)
- **Teks:** "Rentang mengikuti 12 bulan terakhir · lebih stabil · lebih fokus".

### SEG 8 — PUNCAK: kecepatan (swimlane) (3:55–4:25)
- **VO:** "Dampak terbesarnya di sini. Dulu, informasi anomali menempuh jalur berhari-hari. Kini, SR Admin tahu saat menginput — dan langsung bisa menuliskan alasannya."
- **Visual:** **swimlane sebelum/sesudah**. Atas "LAMA": titik bergerak lambat lewat banyak tahap (label 10–20 hari, `[asumsi]`). Bawah "BARU": titik langsung menyala hijau di titik input (~instan).
- **Teks:** "Berhari-hari → saat input" · label halus "[asumsi durasi]".
- **Catatan:** klimaks. Beri swell musik lembut.

### SEG 9 — Yang sudah dikerjakan (timeline ke belakang) (4:25–4:45)
- **VO:** "Sejauh ini, kami telah menguji cara baru ini pada data produksi, membandingkannya dengan cara lama, menemukan dugaan kesalahan input, dan menganalisis beban kerja pemeriksa."
- **Visual:** timeline **mundur ke belakang** (bukan rencana): milestone yang sudah dicapai, ditandai tercentang
  lembut — "uji data nyata → perbandingan lama/baru → temuan typo → analisis workload".
- **Teks:** "Yang sudah dikerjakan" (bukan "rencana").

### SEG 10 — Risiko, mitigasi & rekomendasi (4:45–5:00)
- **VO:** "Kami jujur soal risikonya. Karena lebih banyak data ditandai, beban cek bisa bertambah; sebagian dugaan masih perlu divalidasi; dan data air serta limbah belum dihitung. Sebagai rekomendasi untuk tim yang melanjutkan: mulai dari pilot singkat, sediakan tempat alasan di sistem, dan validasi oleh ahli."
- **Visual:** dua kolom tenang — kiri "Risiko", kanan "Mitigasi/Rekomendasi" (lihat §4). Nada kalem, tidak defensif.
  Tutup dengan motif band stabil + wordmark kecil **"NEW anomaly detection — Tim Horei"**, fade ke off-white.
- **Teks:** "Risiko dikenali · Mitigasi · Rekomendasi (untuk tim penerus)".
- **Catatan:** proyek akan **di-handover**; rekomendasi bersifat saran, **bukan komitmen tanggal**.

---

## 4. RISIKO & MITIGASI (perluasan untuk SEG 10 / appendix)

| # | Risiko | Dampak | Mitigasi / Rekomendasi |
|--|--|--|--|
| 1 | Beban pemeriksa **naik** (lebih banyak ditandai: 2,1% → 16,5%) | Submittor/Verificator keberatan | SOP cek dokumen ringkas; **sampling** anomali risiko rendah; ukur ulang setelah 2–3 bulan `[ASUMSI waktu]` |
| 2 | Dugaan anomali & typo **belum divalidasi** | Klaim "anomali terlewat" belum sahih | Validasi ahli pada sampel entri yang hanya ditandai cara baru (gap data #1) |
| 3 | Data **hanya energi** (listrik + non-renewable) | Beban/temuan sebenarnya lebih besar | Masukkan air & limbah pada iterasi berikut |
| 4 | **Angka orang belum pasti** (akun ≠ orang; 1 orang 2 peran; Corporate ~3–4) | Rasio beban bisa salah | Konfirmasi akun aktif & pemetaan peran ke orang |
| 5 | **Unit baru / musiman** (sejarah <12 bulan) | Rentang tak bisa dihitung penuh | Aturan fallback ≥3 bulan; "data belum cukup" bila kurang (belum diimplementasi penuh) |
| 6 | **Production vs Domestic** beda 7–94× | Satu rentang → salah tanda | Pisahkan rentang per jenis pemakaian (temuan, belum diterapkan) |
| 7 | **Band bisa bernilai minus** pada pola tertentu | Batas bawah tak masuk akal | Aturan band non-negatif (akan dijaga) |
| 8 | Parameter waktu masih **asumsi** | Estimasi penghematan belum pasti | Time-tracking nyata di 1–2 divisi percontohan |
| 9 | **Handover** ke tim lain | Pengetahuan bisa hilang | Dokumentasi (repo ini) + sesi serah terima; rekomendasi, bukan tenggat |
| 10 | Sebagian pembanding industri dari **sumber vendor** | Ekspektasi berlebih | Perlakukan `[RISET]` sebagai arah, bukan target; verifikasi mandiri |

---

## 5. CATATAN PRODUKSI

- **Durasi ~5:00.** Jika lebih, pangkas SEG 5 atau SEG 6 (jangan SEG 3 & 8).
- **Label bukti di layar** kecil & tidak mengganggu: `[data nyata]`, `[asumsi]`, `[simulasi]`, `[riset]`,
  `[perlu dikonfirmasi]`. Angka `[NYATA]` boleh ditonjolkan; sisanya jangan seolah fakta keras.
- **Larangan kata:** "vonis", "AI", "buruk/salah/buta".
- **Konsistensi angka:** 605 **unit listrik** (bukan total) · 210 (34,7%) · 301 · ≈11/66 · 431→1.833 · 4,3× ·
  274 kandidat typo · 2,1%→16,5% · 9 divisi (dari data akun 31 divisi) · 16 divisi (data energi).
- **Musik:** ambient corporate BPM rendah; swell lembut di SEG 8.
- **Subtitle (SRT)** dari VO; kontras teks ≥ 4.5:1.

---

## 6. PROMPT RINGKAS (untuk generator video AI, 1 paragraf)

> Professional minimalist 2D motion-graphic explainer, 16:9, 1080p, calm soft palette
> (off-white #F5F3EF, sage-teal #4C8C84, deep navy #1A2A4A, muted terracotta, success green #1E7D4F),
> clean geometric sans-serif, generous negative space, smooth ease-in-out, count-up numbers, draw-on charts.
> Recurring motif: a monthly-shifting control band (problem) morphing into a locked, stable band (solution).
> Calm Indonesian voice-over, ambient corporate music. Topic: an energy-data anomaly-detection solution for
> an internal sustainability system — making status stable and known at the moment of data entry. It is a
> method/solution, **not an AI product**; team name "Horei", working name "NEW anomaly detection".
> Avoid the word "verdict/vonis", neon colors, busy stock footage, heavy 3D. ~5 minutes, 10 segments per the
> shot list; end on risks, mitigations, and recommendations for a successor team (no fixed future timeline).
