# Kerangka Pitch Deck — NEW Anomaly Detection (Tim Horei, JSRS)

> Status: **kerangka** (bukan teks slide final). Teks lengkap per slide menyusul setelah kerangka disetujui.
> Asumsi: audiens = juri + product owner + manajemen · durasi ~15 menit · ~14 slide utama · kerangka 6 bagian wajib.
> **North star metric:** *waktu dari input sampai SR Admin tahu status anomali*.
>
> **Penamaan:** "Horei" = nama **tim proyek** (bukan produk, **bukan AI**). Nama solusi sementara:
> **"NEW anomaly detection"**. Hindari kata "vonis" → pakai "status / hasil penilaian / ditandai".
>
> Label bukti: `[NYATA]` dari data produksi · `[SIM]` simulasi · `[ASUMSI]` parameter belum diukur ·
> `[RISET]` sumber eksternal (arah, bukan target) · `[perlu dikonfirmasi]` angka belum final.

---

## 0. DASAR ANGKA (sudah diverifikasi ulang dari data mentah)

**Dua sumber data berbeda — jangan dicampur:**
- **Data energi** = **Listrik + Non-Renewable Energy** (FY2024 & FY2025). Air/limbah belum termasuk.
- **Data akun** = pengguna per peran, mencakup **31 divisi**.

**Definisi "unit" (DIPAKAI KONSISTEN): satu LOKASI FISIK** (kolom `Unit`), **tidak** dipecah per
Production/Domestic. Pemisahan Production vs Domestic tetap dipakai **hanya saat menghitung band**
(karena skalanya beda 7–94×), bukan saat menghitung jumlah unit.

| Angka | Nilai | Dari mana |
|---|--:|---|
| Lokasi fisik unik — Listrik 2025 | **334** | kolom `Unit` `[NYATA]` |
| Lokasi fisik unik — Non-Renewable 2025 | 282 | `[NYATA]` |
| Lokasi fisik gabungan (4 file) | 340 | `[NYATA]` |
| **Lokasi Listrik berpasangan 2024↔2025** | **334** | basis analisis kestabilan `[NYATA]` |
| Lokasi Non-Renewable berpasangan | 276 | `[NYATA]` |
| **Divisi di data energi** | **16** | `[NYATA]` |
| **Divisi di data akun** | **31** | `[NYATA]` |
| Divisi akun yang **punya** data energi | 16 | 3 lainnya tergabung via North/South |
| Divisi akun **tanpa** data energi | 12 | belum/tidak input energi `[NYATA]` |
| Divisi single point (S=1 atau V=1) | **9** | dari data akun 31 divisi `[NYATA]` |
| Akun SR Admin / Submittor / Verificator / Corporate | 499 / 192 / 135 / 641 | **jumlah akun, bukan orang** `[NYATA]` |

**Perlu dikonfirmasi sebelum tayang (jangan tampil sebagai angka orang):**
- Corporate sebenarnya tim kecil **~3–4 orang** pengolah data (641 = akun).
- Submittor/Verificator dasarnya 1+1 per divisi; sebagian **1 orang memegang 2 peran**.

---

## A. Kalimat Masalah (3 opsi)

| Nada | Kalimat |
|---|---|
| Lugas | "Status anomali di JSRS baru diketahui penginput lewat jalur berjenjang yang panjang, dan metode deteksi yang dipakai berubah tiap bulan sehingga hasil penilaian tidak stabil." |
| Emosional-operasional | "Saat data yang sama ditanyakan berulang sepanjang tahun sementara penginput menunggu berhari-hari untuk tahu ada masalah, energi tim habis di proses — bukan di memperbaiki datanya." |
| Berbasis angka | "Dari 334 lokasi listrik pada data produksi, 128 (38%) pernah berubah status tanpa angkanya berubah, dan satu anomali ditanyakan rata-rata 4,3× — masalahnya di dua sisi: deteksi dan komunikasi." |

**Rekomendasi: opsi berbasis angka** (judul), lugas (sub-judul), emosional (pembuka lisan).

---

## B. Kerangka Slide

| No | Bagian | Judul slide (pesan) | Pesan utama | Bukti/angka (+label + sumber) | Visual | Status |
|--|--|--|--|--|--|--|
| 1 | cover | NEW anomaly detection: status stabil & langsung di titik input | Pembuka + north star | North star: waktu input→SR Admin tahu | Judul + angka hidup | Siap |
| 2 | Masalah | Masalahnya ada di dua sisi: deteksi yang bergeser & komunikasi berjenjang | Dua pilar | 38% lokasi berubah status `[NYATA]` TEMUAN §3.1; ditanya 4,3× `[NYATA]` WORKLOAD §6b | Diagram 2 pilar | Siap |
| 3 | Masalah | Ini bukan prediksi — ini terjadi pada data produksi nyata | Magnitude + urgensi | 334 lokasi listrik, 128 berubah (38%) `[NYATA]`; contoh RO BR Jatim 2 `[NYATA]` | `01_kestabilan.png` + contoh unit | **Perbarui grafik ke 334/128** |
| 4 | Masalah | Satu Verificator bisa menanggung puluhan entri/bulan — dan itu baru energi | Magnitude beban | rata-rata & puncak entri/Verificator `[NYATA]` RISET §A; 9 divisi single point `[NYATA]` | `13_rasio_beban.png` | **Perbarui angka akun lengkap** |
| 5 | Masalah | Sebagian anomali hanya salah ketik — & data sama ditanya 4,3× | Typo + pertanyaan berulang | 274 kandidat typo `[NYATA]` TEMUAN §6.1; 431→1.833 `[NYATA]` WORKLOAD §6b | `04_typo.png` + `11_tanya_berulang.png` | Siap |
| 6 | Masalah | Beberapa peran, dua sistem, jalur panjang sebelum penginput tahu | Peta pemangku kepentingan | akun 499/192/135/~3–4 Corporate `[NYATA]`+`[perlu dikonfirmasi]`; +HO, Division PIC | Peta stakeholder + alur | Siap |
| 7 | Latar belakang | Kenapa kami mengambil masalah ini sekarang | Pemicu: band bergeser + alasan tercecer di catatan terpisah | Band dihitung ulang tiap bulan; belum ada tempat simpan alasan `[NYATA]` WORKLOAD §6b | Timeline "mengapa sekarang" | Siap |
| 8 | Tujuan | Status stabil, diketahui saat input, pemeriksaan terfokus | 3 tujuan terukur | Target coverage ~95%; status tak berubah; alasan melekat | 3 ikon tujuan | Siap |
| 9 | Solusi | Dari rentang yang bergeser ke rentang yang dikunci dari sejarah | Cara lama vs baru (less technical) | Coverage 100% vs ~95% `[NYATA]`; lebih tahan lonjakan ganda `[SIM]` | `03_contoh_band.png` + `02_robustness.png` | Siap |
| 10 | Solusi | Penginput tahu di saat input, bukan berhari-hari kemudian | Kecepatan info (swimlane) | Lama 10–20 hari/siklus ×4,3 `[ASUMSI]`+`[NYATA]`; baru ~instan `[ASUMSI]` WORKLOAD §6c | Swimlane sebelum/sesudah `12_timeline.png` | Siap |
| 11 | Demo aplikasi | Begini tampilannya saat SR Admin menginput angka anomali | Status + field alasan di layar input | — (demo langsung) | Screen recording / mockup | **Butuh mockup/demo** |
| 12 | Timeline | Yang sudah dikerjakan (ke belakang) | Perjalanan kerja yang sudah dilakukan | uji data nyata → banding lama/baru → temuan typo → analisis beban | Timeline mundur | Siap |
| 13 | Penutup (risiko) | Jujur: beban pemeriksa bisa naik — ini cara menjaganya | Risiko + mitigasi | +28…+48 mnt/Submittor `[ASUMSI]` WORKLOAD §5.9; mitigasi SOP ringkas, sampling | Tabel risiko→mitigasi | **Perbarui penyebut akun** |
| 14 | Penutup (rekomendasi) | Rekomendasi ke depan | Saran, bukan komitmen tanggal | pilot 1–2 bln; field alasan; validasi ahli | Kotak rekomendasi | Siap |

**Appendix (Q&A):** A1 teori breakdown 50% & 1,4826 · A2 definisi coverage/recall · A3 rolling vs robust ·
A4 cara hitung 1.833 & 4,3× · A5 model beban + titik impas · A6 pembanding industri `[RISET]`.

---

## C. Saran Tambahan (yang diadopsi)

| # | Ide | Putusan | Alasan |
|--|--|--|--|
| 1 | North star metric | Masuk (slide 1 & 10) | Mudah diingat, mengikat dua pilar |
| 2 | Biaya tersembunyi (1.833 / 4,3×) | Masuk (slide 5) | Angka `[NYATA]` paling berdampak |
| 3 | Risiko & mitigasi | Masuk (slide 13) | Membangun kepercayaan |
| 4 | Pilot + KPI | Masuk (slide 14, sbg rekomendasi) | — |
| 5 | "Mengapa sekarang" | Gabung ke slide 7 | Tak ada tenggat regulasi (tak dikarang) |
| 6 | Peta jalan IoT | Appendix singkat | Visi, bukan klaim |
| 7 | North star sebagai angka hidup di cover | Masuk | Melekatkan metric sejak awal |

---

## D. Kesenjangan Data (urut dampak)

| # | Gap | Kenapa penting | Cara mendapatkan |
|--|--|--|--|
| 1 | Validasi ahli atas entri yang hanya ditandai cara baru | Menutup klaim "anomali terlewat" | Sampel 50–100 entri → Division PIC nilai benar/salah |
| 2 | Waktu nyata `t_cek`/`t_dok`/`t_tanya` | Ganti `[ASUMSI]` di model beban | Time-tracking 2 minggu di divisi percontohan |
| 3 | Volume air/limbah | Beban sebenarnya > angka energi | Ekstrak modul JSRS lain |
| 4 | Jumlah **orang** (vs akun); Corporate ~3–4; 1 orang 2 peran | Rasio beban akurat | Konfirmasi ke pemilik sistem |
| 5 | 12 divisi akun tanpa data energi | Pastikan bukan beda penamaan | Cek apakah input via nama lain / belum input |
| 6 | % typo tervalidasi | Ubah "kandidat" → fakta | Division PIC konfirmasi 274 kandidat |

---

## E. Sepuluh Pertanyaan Sulit + Jawaban Jujur

1. **Banyak anomali terlewat cara lama?** Belum bisa diklaim; butuh validasi ahli (gap #1). Yang pasti: band lama memuat 100% titik normal `[NYATA]` & buta anomali majemuk di `[SIM]`.
2. **Beban pemeriksa naik?** Ya, per bulan +28…48 mnt `[ASUMSI]`; kami akui. Diimbangi hilangnya pertanyaan berulang 4,3× + SOP/sampling.
3. **43–86 hari = tunggu satu anomali?** Bukan — penjumlahan siklus karena data sama ditanya berulang. Satu siklus 10–20 hari `[ASUMSI]`.
4. **Typo sudah pasti?** Masih **kandidat** (274) sampai divalidasi.
5. **Kenapa median/MAD?** Tahan terhadap lonjakan ganda (breakdown point 50% vs 0%; teori + `[SIM]`).
6. **Data cuma energi?** Benar; air/limbah belum masuk → beban nyata lebih tinggi.
7. **Kenapa unit ~300, bukan 600?** 1 unit = 1 lokasi fisik. Angka sebelumnya memecah per Production/Domestic; kini dihitung sebagai satu lokasi.
8. **Unit baru / musiman?** Fallback ≥3 bulan; di bawah itu "data belum cukup" (belum penuh).
9. **Angka akun = orang?** Bukan; satu orang bisa banyak akun / dua peran.
10. **Kasus industri = jaminan?** Tidak; `[RISET]` hanya arah, konteks beda — perlu verifikasi.

---

## F. Alur Naratif

Mulai dari kejutan terukur (38% lokasi berubah status tanpa data berubah) → tegaskan "ini nyata, bukan prediksi".
Bangun magnitude (beban timpang, typo, pertanyaan berulang 4,3×) → tunjukkan siapa yang terdampak (peran + HO/PIC)
→ jelaskan kenapa sekarang (band bergeser + alasan tercecer) → nyatakan tujuan. **Puncak emosional di slide 10**:
swimlane "berhari-hari → saat input". Disusul demo, lalu timeline mundur (yang sudah dikerjakan), risiko+mitigasi
(kepercayaan), dan rekomendasi ke depan. Puncak sengaja di solusi/kecepatan, bukan di masalah.

---

## G. Catatan Kejujuran

- Definisi unit = **lokasi fisik** (tidak dikali Prod/Dom). Band tetap dihitung per Prod/Dom.
- "Anomali terlewat" belum diklaim fakta (butuh ground truth). Typo = kandidat. Waktu = asumsi.
- 43–86 hari = penjumlahan siklus, bukan lama tunggu satu anomali.
- Manfaat untuk pemeriksa belum pasti (beban bisa naik) → ditampilkan sebagai risiko termitigasi.
- Angka akun ≠ orang aktif; volume baru energi. Nada menghargai proses & pemilik sistem saat ini.
