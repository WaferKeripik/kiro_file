# Kerangka Pitch Deck — Solusi Deteksi Anomali JSRS (Horei AI)

> Status: **kerangka** (bukan teks slide final). Teks lengkap per slide menyusul setelah kerangka disetujui.
> Asumsi: audiens = juri + product owner + manajemen · durasi ~15 menit · ~14 slide utama ·
> kerangka 6 bagian wajib. **North star metric:** *waktu dari input sampai SR Admin tahu anomali*.
>
> Label bukti: `[NYATA]` dari data produksi · `[SIM]` simulasi · `[ASUMSI]` parameter belum diukur ·
> `[RISET]` sumber eksternal (arah, bukan target).

---

## A. Kalimat Masalah (3 opsi)

| Nada | Kalimat |
|---|---|
| Lugas | "Anomali konsumsi energi di JSRS baru diketahui penginput lewat jalur berjenjang yang panjang, dan metode deteksi yang dipakai berubah tiap bulan sehingga vonis anomali tidak stabil." |
| Emosional-operasional | "Saat data yang sama ditanyakan berulang kali sepanjang tahun sementara penginput menunggu berhari-hari untuk tahu ada masalah, energi tim habis di proses — bukan di memperbaiki datanya." |
| Berbasis angka | "Pada 605 unit data produksi, 34,7% vonis anomali berubah tanpa angkanya berubah, dan satu anomali ditanyakan rata-rata 4,3× — masalahnya ada di dua sisi: deteksi dan komunikasi." |

**Rekomendasi: opsi berbasis angka** (judul), lugas (sub-judul), emosional (pembuka lisan).
Alasan: audiens campuran paling cepat yakin oleh fakta `[NYATA]`, dan mengikat kedua pilar sekaligus.

---

## B. Kerangka Slide

| No | Bagian | Judul slide (pesan) | Pesan utama | Bukti/angka (+label + sumber) | Visual | Status |
|--|--|--|--|--|--|--|
| 1 | cover | Horei AI: deteksi anomali yang stabil & langsung di titik input | Pembuka + north star | North star: waktu input→SR Admin tahu | Judul + angka hidup | Siap |
| 2 | Masalah | Masalahnya ada di dua sisi: deteksi yang bergeser & komunikasi berjenjang | Dua pilar | 34,7% vonis berubah `[NYATA]` TEMUAN §3.1; ditanya 4,3× `[NYATA]` WORKLOAD §6b | Diagram 2 pilar | Siap |
| 3 | Masalah | Ini bukan prediksi — ini terjadi pada data produksi nyata | Magnitude + urgensi | 605 unit, 210 berubah, 301 kali `[NYATA]`; contoh RO BR Jatim 2 `[NYATA]` | `01_kestabilan.png` + contoh unit | Siap |
| 4 | Masalah | Satu Verificator bisa menanggung 66 entri/bulan — dan itu baru energi | Magnitude beban | 7,2/Submittor, 11/Verificator; Commercial Poultry 66; 9 divisi single point `[NYATA]` RISET §A | `13_rasio_beban.png` | Siap |
| 5 | Masalah | Sebagian anomali hanya salah ketik — & data sama ditanya 4,3× | Typo + pertanyaan berulang | 274 kandidat typo `[NYATA]` TEMUAN §6.1; 431→1.833 `[NYATA]` WORKLOAD §6b | `04_typo.png` + `11_tanya_berulang.png` | Siap |
| 6 | Masalah | Lima peran, dua sistem, jalur panjang sebelum penginput tahu | Peta pemangku kepentingan | SR Admin 499, Submittor 192, Verificator 135, Corporate 641 `[NYATA]`; +HO, Division PIC | Peta stakeholder + alur | Siap |
| 7 | Latar belakang | Kenapa kami mengambil masalah ini sekarang | Pemicu: band bergeser + alasan tercecer di notepad | Band dihitung ulang tiap bulan; belum ada tempat simpan alasan `[NYATA]` WORKLOAD §6b | Timeline "mengapa sekarang" | Siap |
| 8 | Tujuan | Vonis stabil, diketahui saat input, beban terfokus | 3 tujuan terukur | Target coverage ~95%; vonis tak berubah; alasan melekat | 3 ikon tujuan | Siap |
| 9 | Solusi | Dari band yang bergeser ke band yang dikunci dari sejarah | Rumus lama vs baru | Coverage 100% vs 95,6/92,3% `[NYATA]`; 2,1%→16,5% `[NYATA]` TEMUAN §3.3; breakdown 50% vs 0% teori/`[SIM]` | `03_contoh_band.png` + `02_robustness.png` | Siap |
| 10 | Solusi | Penginput tahu di detik yang sama, bukan berhari-hari kemudian | Kecepatan info (swimlane) | Lama 10–20 hari/siklus ×4,3 `[ASUMSI]`+`[NYATA]`; baru 1–3 hari `[ASUMSI]` WORKLOAD §6c | Swimlane sebelum/sesudah `12_timeline.png` | Siap |
| 11 | Demo aplikasi | Begini tampilannya saat SR Admin menginput angka anomali | Vonis + field alasan di layar input | — (demo langsung) | Screen recording / mockup | **Butuh mockup/demo** |
| 12 | Timeline | Peta pengerjaan: yang sudah siap vs yang akan dijaga | Status jujur | Pantau paralel 1–2 bln; band non-minus; musiman; Prod/Dom 7–94× `[NYATA]` RISET §5.8 | Gantt/milestone | **Butuh tanggal milestone** |
| 13 | Penutup (risiko) | Jujur: beban pemeriksa bisa naik — ini cara kami menjaganya | Risiko + mitigasi | +28…+48 mnt/Submittor `[ASUMSI]` WORKLOAD §5.9; mitigasi SOP ringkas, sampling, kalibrasi | Tabel risiko→mitigasi | Siap |
| 14 | Penutup (ask) | Yang kami minta: restu pilot 1–2 bulan + 3 data kunci | Keputusan yang diminta | KPI pilot; daftar data (bagian E) | Kotak "the ask" | Siap |

**Appendix (cadangan Q&A):**
- A1 Teori breakdown point 50% & konstanta 1,4826 (TEMUAN §2)
- A2 Definisi coverage & recall (TEMUAN §3.3, §3.2)
- A3 Rolling vs robust: dua perbaikan terpisah (SLIDE.md slide 6)
- A4 Cara hitung 1.833 & 4,3× (WORKLOAD §6b, `jsrs_rolling.py`)
- A5 Model beban pemeriksa + titik impas (WORKLOAD §3–4)
- A6 Pembanding industri `[RISET]` + peta jalan IoT (RISET §B–C)

---

## C. Saran Tambahan (yang diadopsi)

| # | Ide | Putusan | Alasan |
|--|--|--|--|
| 1 | North star metric | Masuk (slide 1 & 10) | Mudah diingat, mengikat dua pilar |
| 2 | Biaya tersembunyi (1.833 / 4,3×) | Masuk (slide 5) | Angka `[NYATA]` paling berdampak |
| 3 | Risiko & mitigasi | Masuk (slide 13) | Membangun kepercayaan |
| 4 | Pilot + KPI | Masuk (slide 14) | Inti "the ask" |
| 5 | "Mengapa sekarang" | Gabung ke slide 7 | Tak ada tenggat regulasi (tak boleh dikarang) |
| 6 | Langkah berikutnya | Masuk (slide 14) | — |
| 7 | Peta jalan IoT | Appendix/penutup singkat | Visi, bukan klaim |
| 8 | North star sebagai angka hidup di cover | Masuk | Melekatkan metric sejak awal |

---

## D. Kesenjangan Data (urut dampak)

| # | Gap | Kenapa penting | Cara mendapatkan |
|--|--|--|--|
| 1 | Validasi expert atas entri yang hanya ditandai rumus baru | Menutup klaim "anomali terlewat" | Sampel 50–100 entri `baru-only` → Division PIC nilai benar/salah |
| 2 | Waktu nyata `t_cek`/`t_dok`/`t_tanya` | Ganti `[ASUMSI]` di model beban | Time-tracking 2 minggu di divisi percontohan |
| 3 | Volume air/limbah | Beban sebenarnya > angka energi | Ekstrak modul JSRS lain |
| 4 | Akun aktif (vs jumlah akun) | Rasio beban lebih akurat | Query login terakhir / status akun |
| 5 | % typo tervalidasi | Ubah "kandidat" → fakta | Division PIC konfirmasi 274 kandidat |

---

## E. Sepuluh Pertanyaan Sulit + Jawaban Jujur

1. **16,5% vs 2,1% = banyak anomali terlewat?** Belum bisa diklaim; butuh validasi expert (gap #1). Yang pasti: band lama memuat 100% titik normal `[NYATA]` & buta anomali majemuk di `[SIM]`.
2. **Beban pemeriksa naik?** Ya, per bulan +28…48 mnt `[ASUMSI]`; kami akui. Diimbangi hilangnya pertanyaan berulang 4,3× + SOP/sampling.
3. **43–86 hari = tunggu satu anomali?** Bukan — penjumlahan siklus karena data sama ditanya berulang. Satu siklus 10–20 hari `[ASUMSI]`.
4. **Typo sudah pasti?** Masih **kandidat** (274) sampai divalidasi.
5. **Kenapa median/MAD, bukan perbaiki rumus lama?** Breakdown point 50% vs 0% — tahan outlier majemuk (teori + `[SIM]`).
6. **Data cuma energi?** Benar; air/limbah belum masuk → beban nyata lebih tinggi. Masuk gap.
7. **Unit baru (belum 12 bulan)?** Fallback ≥3 bulan; di bawah itu "data belum cukup". Belum penuh (akan dijaga).
8. **Band minus / musiman salah vonis?** Temuan nyata (Prod/Dom 7–94×, musiman); penanganan akan dilakukan — transparan.
9. **Angka akun = orang?** Bukan; satu orang bisa banyak akun. Perlu data akun aktif.
10. **Kasus industri = jaminan?** Tidak; `[RISET]` hanya arah, konteks beda, sebagian sumber vendor — perlu verifikasi.

---

## F. Alur Naratif

Mulai dari kejutan terukur (34,7% vonis berubah tanpa data berubah) → tegaskan "ini nyata, bukan prediksi".
Bangun magnitude (1 Verificator 66 entri, typo, pertanyaan berulang 4,3×) → tunjukkan siapa yang terdampak
(5 peran + HO/PIC) agar manusiawi → jelaskan kenapa sekarang (band bergeser + alasan tercecer di notepad) →
nyatakan tujuan. **Puncak emosional di slide 10**: swimlane "berhari-hari → di detik yang sama". Disusul demo
yang mengkonkretkan, lalu timeline jujur (siap vs dijaga), risiko+mitigasi (kepercayaan), dan ask yang jelas
(restu pilot + 3 data kunci). Puncak sengaja di solusi/kecepatan, bukan di masalah.

---

## G. Catatan Kejujuran (ringkas)

- "Anomali terlewat" **belum** diklaim sebagai fakta (butuh ground truth).
- Typo = **kandidat**. Waktu = **asumsi**. 43–86 hari = **penjumlahan siklus**, bukan lama tunggu.
- Manfaat untuk pemeriksa **belum pasti** (beban bisa naik) → ditampilkan sebagai risiko termitigasi.
- Nada menghargai proses & pemilik LCL/UCL saat ini.
- Angka akun ≠ orang aktif; volume baru energi.
