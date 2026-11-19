# Prompt Motion Graphic Video — Solusi Deteksi Anomali JSRS (Horei AI)

> Dipakai untuk: generator video AI (Sora / Runway / Veo / Kling) **atau** brief untuk motion designer.
> Sumber konten: `PITCH_DECK.md`. Semua angka sudah berlabel bukti; jaga kejujuran (jangan melebih-lebihkan).

---

## 1. SPESIFIKASI TEKNIS

| Item | Nilai |
|---|---|
| Rasio | 16:9 (YouTube landscape) |
| Resolusi | 1920×1080 (1080p), 4K bila memungkinkan |
| Durasi | maksimal **5:00** menit |
| Frame rate | 30 fps |
| Gaya | profesional, minimalis, motion graphic 2D (flat + subtle depth) |
| Audio | voice-over tenang + musik latar ambient-corporate lembut |

---

## 2. ARAHAN GAYA VISUAL (GLOBAL)

- **Nada warna: calm / soft.** Palet:
  - Dasar: off-white `#F5F3EF` / soft grey `#ECEFF1`
  - Aksen utama (tenang/positif): sage-teal `#4C8C84`, deep navy `#1A2A4A`
  - Aksen masalah (hangat, tak mencolok): muted terracotta `#C77B5A`
  - Hijau "baru/berhasil": `#1E7D4F`
- **Tipografi:** sans-serif geometris bersih (mis. Inter / Poppins / Satoshi). Judul tebal, body ringan.
- **Prinsip gerak:** easing halus (ease-in-out), transisi *fade/slide* pelan, jangan ada kedipan keras.
  Angka selalu **count-up** (animasi naik dari 0). Garis "digambar" (draw-on). Banyak ruang kosong (negative space).
- **Motif berulang:** garis band/rentang yang "bergerak-goyah" (masalah) vs garis band "terkunci stabil" (solusi) —
  jadikan ini visual signature sepanjang video.
- **Hindari:** stok foto ramai, warna neon, transisi 3D berlebihan, teks padat. Satu ide besar per layar.

---

## 3. STRUKTUR & NASKAH PER SEGMEN

> Format tiap segmen: **[waktu] Judul · Voice-over (ID) · Visual · Teks di layar.**
> VO ditulis tenang, berwibawa, tempo sedang. Angka diikuti label ringan bila perlu.

### SEG 1 — Hook (0:00–0:30)
- **VO:** "Bayangkan sebuah angka yang tidak berubah. Bulan lalu dianggap normal. Bulan ini tiba-tiba dianggap anomali. Padahal angkanya sama."
- **Visual:** satu titik data di garis waktu. Band rentang di belakangnya **bergeser** naik-turun tiap bulan, membuat titik yang sama berpindah dari "dalam" ke "luar". Latar off-white, garis sage-teal.
- **Teks:** "Angka sama. Vonis berubah." → lalu muncul **34,7%** (count-up).
- **Catatan:** ini pembuka emosional; belum sebut solusi.

### SEG 2 — Masalah: dua pilar (0:30–1:05)
- **VO:** "Di JSRS, masalahnya ada di dua sisi. Pertama, deteksi: rentang kendali dihitung ulang tiap bulan, jadi vonis bergeser. Kedua, komunikasi: satu anomali bisa ditanyakan berulang kali sebelum sampai ke penginput."
- **Visual:** layar terbelah dua. Kiri: ikon grafik dengan band goyah ("Deteksi"). Kanan: rantai email/orang berjenjang yang memanjang ("Komunikasi"). Keduanya terhubung ke satu ikon "data".
- **Teks:** "Dua pilar: Deteksi · Komunikasi" · badge kecil "data produksi nyata".

### SEG 3 — Ini nyata, bukan prediksi (1:05–1:40)
- **VO:** "Ini bukan simulasi. Pada 605 unit data produksi, 210 di antaranya pernah berubah vonis tanpa angkanya berubah — tiga ratus satu kali."
- **Visual:** grid 605 titik kecil; 210 menyala muted-terracotta satu per satu; counter "301 kali" count-up. Lalu zoom ke satu unit (RO BR Jatim 2): garis konsumsi datar di 2.040, label "April: normal → Agustus: anomali" muncul tanpa titiknya bergerak.
- **Teks:** "605 unit · 210 berubah · 301 kali" · stempel "[DATA NYATA]".

### SEG 4 — Magnitude: beban & biaya tersembunyi (1:40–2:25)
- **VO:** "Bebannya tidak merata. Rata-rata sebelas entri per verifikator tiap bulan — tapi di satu divisi mencapai enam puluh enam. Dan karena rentang terus bergeser, data yang sama ditanyakan rata-rata empat koma tiga kali."
- **Visual:** bar chart halus naik: rata-rata 11 vs puncak 66 (Commercial Poultry). Transisi ke animasi "satu anomali → menggandakan diri 4,3×" (431 titik berubah jadi 1.833).
- **Teks:** "11 rata-rata · 66 puncak" → "431 → 1.833 kemunculan · 4,3×" · catatan kecil "baru energi; air/limbah belum dihitung".

### SEG 5 — Siapa yang terdampak (2:25–2:50)
- **VO:** "Lima peran terlibat: SR Admin yang menginput, Submittor dan Verificator yang memeriksa, Corporate yang mengolah — melewati dua sistem sebelum penginput tahu."
- **Visual:** peta alur minimalis: SR Admin → Submittor → Verificator → Corporate, dengan HO & Division PIC di jalur. Angka akun muncul lembut di tiap ikon (499 / 192 / 135 / 641).
- **Teks:** "5 peran · 2 sistem · 1 jalur panjang".

### SEG 6 — Latar & tujuan (2:50–3:15)
- **VO:** "Akar penyebabnya: rentang yang bergantung pada data bulan berjalan, dan alasan anomali yang tercatat di luar sistem. Tujuan kami sederhana — vonis yang stabil, diketahui saat input, dengan beban yang terfokus."
- **Visual:** notepad kertas (alasan tercecer) memudar → berganti kartu digital "alasan tersimpan di sistem". Tiga ikon tujuan muncul: stabil / instan / fokus.
- **Teks:** "Stabil · Saat input · Terfokus".

### SEG 7 — Solusi: rumus lama vs baru (3:15–3:55)
- **VO:** "Kami mengganti perhitungan lama dengan rentang rolling dua belas bulan dan statistik robust — median dan MAD. Hasilnya: rentang yang dikunci dari sejarah, tidak lagi bergeser, dan tahan terhadap lonjakan ganda."
- **Visual:** motif signature kembali — band "goyah" (kiri) berubah mulus jadi band "terkunci stabil" (kanan). Lalu dua garis recall: robust tetap tinggi, classic anjlok saat outlier bertambah (dari tabel `[SIM]`). Tampilkan "coverage ~95%".
- **Teks:** "Rolling 12 bulan + robust (median/MAD)" · badge kecil "breakdown point 50% — teori".

### SEG 8 — PUNCAK: kecepatan (swimlane) (3:55–4:25)
- **VO:** "Dampak terbesarnya ada di sini. Dulu, informasi anomali menempuh jalur berhari-hari. Kini, SR Admin tahu di detik yang sama saat menginput — dan langsung bisa menuliskan alasannya."
- **Visual:** **swimlane sebelum/sesudah**. Baris atas "LAMA": titik bergerak lambat melewati banyak tahap (label 10–20 hari, `[ASUMSI]`). Baris bawah "BARU": titik langsung menyala hijau di titik input (label ~instan). Kontras waktu dibuat dramatis namun tenang.
- **Teks:** "Berhari-hari → di detik yang sama" · label halus "[asumsi durasi]".
- **Catatan:** ini klimaks emosional. Beri jeda musik sejenak lalu naik.

### SEG 9 — Jujur: risiko & rencana (4:25–4:45)
- **VO:** "Kami jujur: karena lebih banyak data ditandai, beban cek bisa bertambah. Maka kami rencanakan pilot satu sampai dua bulan, cek dokumen ringkas, dan validasi ahli sebelum diterapkan penuh."
- **Visual:** timbangan seimbang (risiko ⇄ mitigasi); checklist pilot tercentang lembut. Nada tetap kalem, tidak defensif.
- **Teks:** "Risiko dikenali · Pilot · Validasi".

### SEG 10 — Penutup / ask (4:45–5:00)
- **VO:** "Dari deteksi yang stabil hari ini, menuju pemantauan yang lebih cerdas ke depan. Kami meminta restu untuk memulai pilot."
- **Visual:** motif band stabil menyatu jadi logo/wordmark "Horei AI — JSRS". Fade ke off-white bersih.
- **Teks:** "Horei AI · JSRS" → "Mulai dari pilot." (CTA).

---

## 4. CATATAN PRODUKSI

- **Durasi total:** ~5:00. Jika melebihi, pangkas SEG 5 dan SEG 6 (bukan SEG 3 & 8 — itu inti).
- **Label bukti di layar:** tampilkan kecil & tidak mengganggu (`[data nyata]`, `[asumsi]`, `[simulasi]`,
  `[riset]`). Angka `[NYATA]` boleh ditonjolkan; `[ASUMSI]`/`[SIM]` jangan tampil seolah fakta keras.
- **Konsistensi angka (dari PITCH_DECK.md):** 605 unit · 210 (34,7%) · 301 kali · 11 rata-rata / 66 puncak ·
  431→1.833 · 4,3× · 274 kandidat typo · coverage ~95% · 2,1%→16,5% · akun 499/192/135/641.
- **Musik:** ambient corporate, BPM rendah, tanpa drop tajam; swell lembut di SEG 8.
- **Aksesibilitas:** sediakan subtitle (SRT) dari naskah VO; kontras teks minimal 4.5:1.
- **Nada:** menghargai proses yang berjalan; hindari kata "salah/buruk/buta".

---

## 5. PROMPT RINGKAS (untuk generator video AI, 1 paragraf)

> Professional minimalist 2D motion graphic explainer, 16:9, 1080p, calm soft color palette
> (off-white #F5F3EF, sage-teal #4C8C84, deep navy #1A2A4A, muted terracotta accents, success green #1E7D4F),
> clean geometric sans-serif typography, generous negative space, smooth ease-in-out transitions,
> count-up number animations, draw-on line charts. Recurring motif: a "wobbling" control-band that shifts
> every month (problem) transforming into a "locked, stable" band (solution). Ambient corporate background
> music, calm Indonesian voice-over. Topic: an energy-data anomaly-detection solution (JSRS/Horei AI) that
> makes anomaly verdicts stable and instant at data entry. Tone: trustworthy, honest, understated.
> Avoid neon colors, busy stock footage, heavy 3D. ~5 minutes, 10 segments per the shot list.
