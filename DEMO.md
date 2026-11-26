# Panduan Demo ke Stakeholder — Rumus Deteksi Anomali Baru

Durasi target: **15–20 menit**. Tujuan: stakeholder setuju bahwa rumus baru
**dapat dipercaya, akurat, dan layak dipakai**, lalu menyetujui uji paralel.

## Persiapan (sebelum ruangan)
1. Buka **SLIDE_JSRS.pdf** (layar utama).
2. Siapkan terminal untuk demo live:
   ```bash
   python3 -m venv .venv && .venv/bin/pip install numpy pandas scipy matplotlib fpdf2
   .venv/bin/python jsrs_rolling.py      # bukti kestabilan 210 -> 0
   .venv/bin/python jsrs_insight.py      # typo, musiman, production vs domestic
   ```
3. Buka folder **figs/** bila ingin menampilkan grafik satu per satu.

## Alur presentasi (ikuti urutan slide)

| Menit | Slide | Yang dilakukan |
|---|---|---|
| 0–2 | 1–3 | Buka dengan MASALAH: data lewat 2 tingkat verifikasi, 5–10 hari baru balik. |
| 2–4 | 4–5 | Tunjukkan contoh unit yang vonisnya **berubah-ubah** (April normal→anomali). Tanya audiens: "bisa dipercaya?" |
| 4–8 | 6–8 | BUKTI 1 kestabilan (**210 → 0**), lalu BUKTI 2 deteksi (**74–82% vs 8–15%**). |
| 8–10 | 9 | TEORI singkat: breakdown point 50%, MAD×1.4826. Jangan lama — cukup kredibilitas. |
| 10–13 | 10–11 | Production vs Domestic (beda s/d 94×) & aturan data musiman. |
| 13–15 | 12 | **Wow moment**: typo 45.532 vs 562 (81×) — sistem menangkapnya otomatis. |
| 15–18 | 13–14 | MANFAAT (admin, verifikator, audit) + kesimpulan 3 kriteria. |
| 18–20 | 15 | Rencana: uji paralel 1–2 bulan, lalu rollout. Minta persetujuan. |

## Pesan kunci (hafalkan 3 ini)
1. **"210 unit berubah vonis jadi 0."** — kepercayaan.
2. **"Saat anomali lebih dari satu, cara lama hanya menangkap 8–15%; cara baru 74–82%."** — akurasi.
3. **"Admin tahu saat input, bukan 5–10 hari kemudian."** — nilai bisnis.

## Antisipasi pertanyaan
- *"Kenapa bukan rumus lama saja?"* → band lama dihitung dari data yang sedang dinilai, jadi goyah dan buta. Tunjukkan slide 5.
- *"Robust ini mengada-ada?"* → standar statistika mapan (Rousseeuw/Hubert, Hampel). Slide 9.
- *"Bagaimana unit baru / musiman?"* → fallback ≥3 bulan; bulan kosong tidak dihukum. Slide 11.
- *"Bukti adil?"* → kami TIDAK memakai label Excel (itu tautologi); pakai ground-truth sintetis + coverage. Slide 12 catatan.

## Setelah demo
- Bagikan `SLIDE_JSRS.pdf` + `TEMUAN.md`.
- Sepakati 2 hal teknis: faktor band lama (±2σ/±3σ?) dan arah jendela rolling (murni historis / termasuk bulan berjalan).
- Jadwalkan uji paralel.
