# Rasio Beban Pemeriksa & Riset Kasus Industri — JSRS

Dokumen ini menjawab dua hal:
1. **Rasio jumlah Submittor/Verificator terhadap data yang harus dicek tiap bulan** — dan apa
   yang bisa diperoleh bila deteksi anomali dilakukan dengan rumus yang proper.
2. **Kasus nyata perusahaan lain** (deteksi anomali energi → otomasi → IoT/real-time) sebagai
   pembanding arah.

> Label angka: `(a)` dihitung dari data JSRS · `(b)` asumsi · `(riset)` dari sumber eksternal.
> Konten sumber eksternal diparafrasekan untuk mematuhi lisensi; tautan disertakan.

---

## A. Rasio Beban Pemeriksa vs Volume Data `(a)`

Dihitung dari data energi nyata (listrik + non-renewable, per bulan, divisi berdata):

| Ukuran | Nilai |
|---|--:|
| Total entri energi per bulan | **≈ 1.224** |
| Total akun Submittor (divisi berdata) | 170 |
| Total akun Verificator (divisi berdata) | 111 |
| **Rata-rata entri / Submittor / bulan** | **≈ 7,2** |
| **Rata-rata entri / Verificator / bulan** | **≈ 11,0** |

Terlihat ringan **secara rata-rata**, tetapi **sangat timpang** antar-divisi:

| Divisi | entri / Verificator / bulan | jumlah Verificator |
|---|--:|--:|
| Commercial Poultry | **66** | 7 |
| Aquaculture | **31** | 2 |
| Poultry Breeding | 22 | 15 |
| Poultry Processing | 18 | 3 |

**Catatan penting:** angka di atas **baru energi**. JSRS juga mencakup air, limbah, dll., sehingga
beban nyata **lebih tinggi**. Jadi rasio sebenarnya kemungkinan jauh di atas 7–11 entri/bulan.

### Apa yang berubah dengan rumus proper?

Tanpa deteksi yang baik, pemeriksa harus menyisir **semua** entri secara manual. Dengan rumus
rolling + robust, pekerjaan bergeser dari "cek semua" menjadi "**cek yang ditandai**":

- Rumus baru menandai **16,5%** entri `(a)`. Artinya pemeriksa idealnya fokus pada ~1 dari 6 entri,
  bukan seluruhnya — **asal** cek dokumen dibuat ringkas (lihat WORKLOAD.md §3–4).
- Yang paling menghemat: **hilangnya pertanyaan berulang** (band lama menanyakan anomali sama
  rata-rata **4,3×** `(a)`), dan **deteksi typo dini** (274 kandidat) yang memotong siklus 10–20 hari.

> Kesimpulan rasio: beban **terkonsentrasi di segelintir divisi** dan **diperberat oleh proses
> berulang**, bukan oleh volume mentah. Rumus proper menyerang dua sumber beban itu langsung.

---

## B. Kasus Nyata Perusahaan Lain `(riset)`

Pola yang konsisten di industri: **deteksi dini berbasis data → kurangi kerja manual → lanjut ke
pemantauan real-time/IoT.** Beberapa hasil terukur yang dilaporkan:

| Sumber | Konteks | Hasil yang dilaporkan |
|---|---|---|
| Industrial IoT monitoring (uvik.net) | platform energi industri | rekonsiliasi meter manual **turun ~76%**; alert gangguan **~42% lebih dini**; data dari batch 30 menit → **< 60 detik** |
| SMT re-inspection, MDPI Applied Sciences | lini produksi elektronik | volume **review manual turun >98%** pada tingkat deteksi cacat yang auditable |
| Forrester 2024 (dirangkum zigpoll) | respons insiden energi | otomasi → **MTTR −40%**, penanganan tiket manual **−50%** |
| Operator gas midstream (zigpoll) | SCADA + alert otomatis | **downtime tak terjadwal −30%** setelah beralih dari tinjauan log manual ke deteksi instan |
| Rule-based energy DSS, MDPI Applied Sciences | smart factory | sistem memisahkan **skor anomali** untuk menandai hari operasi tak biasa & memprioritaskan inspeksi |

**Benang merahnya** sama dengan arah JSRS: memindahkan manusia dari "memeriksa semuanya & bertanya
berulang" ke "menindak yang ditandai sistem". Besaran persentasenya berbeda tiap industri, tetapi
arah manfaatnya konsisten.

Sumber:
- Industrial Energy IoT Monitoring — https://uvik.net/case-studies/industrial-energy-iot-monitoring-platform-python/
- Automated SMT Re-Inspection, MDPI — https://www.mdpi.com/2076-3417/16/20/10068
- Incident Response Automation (merangkum Forrester 2024) — https://www.zigpoll.com/content/incident-response-planning-strategy-guide-executive-automation
- Production-Aware Energy DSS, MDPI — https://www.mdpi.com/2076-3417/16/17/8601
- IoT + AI Energy Management, MDPI Energies — https://www.mdpi.com/1996-1073/18/7/1706

*Angka dari sumber adalah hasil pada konteks masing-masing, bukan janji hasil identik untuk JSRS.*

---

## C. Peta Jalan: dari Deteksi ke IoT / Real-time

Rumus baru adalah **fondasi**. Setelah deteksi andal & stabil, langkah lanjut yang lazim di industri:

1. **Sekarang → deteksi proper (rolling + robust).** Vonis saat input, alasan melekat, typo tertangkap.
2. **Integrasi alur:** field alasan di sistem (ganti notepad), dashboard anomali untuk Corporate.
3. **Semi-otomasi:** aturan prioritas — anomali berisiko tinggi wajib dokumen, risiko rendah sampling.
4. **IoT / smart metering (opsional, jangka menengah):** data meter mengalir otomatis → anomali
   terdeteksi mendekati real-time (industri lain: dari batch menit → detik), input manual berkurang,
   sumber typo hilang di hulu.
5. **Prediktif:** dari "mendeteksi penyimpangan" ke "memperkirakan pemborosan/kebocoran" sebelum terjadi.

> JSRS tidak harus langsung ke IoT. Nilai terbesar jangka pendek ada di langkah 1–2 (murah, cepat,
> berbasis data yang sudah ada). IoT menjadi masuk akal setelah proses deteksi matang.

---

## D. Keterbatasan
- Rasio beban `(a)` baru mencakup **energi**; air/limbah belum dihitung → beban nyata lebih tinggi.
- Angka akun ≠ orang aktif.
- Angka kasus industri `(riset)` berasal dari konteks perusahaan lain; dicantumkan sebagai
  **pembanding arah**, bukan target yang dijamin untuk JSRS.
