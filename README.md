# Universal DSS Dashboard

Sistem Pendukung Keputusan (DSS) berbasis web untuk analisis **Multi-Criteria Decision Making (MCDM)** secara dinamis. Mendukung dataset CSV apapun dan membandingkan tiga metode klasik secara bersamaan: **SAW**, **WP**, dan **TOPSIS**.

## Menjalankan Aplikasi

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka browser di `http://localhost:8501`

## Struktur Proyek

```
├── app.py                        # Halaman beranda & inisialisasi session state
├── pages/
│   ├── 1_Upload_Data.py          # Upload CSV & konfigurasi kolom alternatif/kriteria
│   ├── 2_Eksplorasi_Data.py      # Statistik deskriptif, distribusi, heatmap korelasi
│   ├── 3_Analisis_DSS.py         # Pengaturan bobot & jenis kriteria, jalankan analisis
│   ├── 4_Hasil_Rekomendasi.py    # Ranking, konsensus Borda, step-by-step, sensitivitas
│   └── 5_Teori_Metodologi.py     # Landasan matematis SAW, WP, TOPSIS (LaTeX)
├── utils/
│   ├── dss_engine.py             # Implementasi SAW, WP, TOPSIS, analisis sensitivitas
│   ├── data_loader.py            # Load & preprocessing dataset
│   └── ui_components.py         # CSS, KPI cards, header
├── data/
│   ├── dataset_penyakit.csv      # Contoh dataset penyakit
│   └── deskripsi_penyakit.json
└── heart_disease_uci.csv         # Dataset default (UCI Heart Disease)
```

## Alur Penggunaan

1. **Upload Data** — Unggah CSV kustom atau gunakan dataset bawaan. Pilih kolom alternatif dan kriteria numerik, lalu klik **Simpan & Terapkan Konfigurasi**.
2. **Eksplorasi Data** — Lihat statistik deskriptif, distribusi per kriteria, scatter plot, dan heatmap korelasi Pearson.
3. **Analisis DSS** — Atur bobot kepentingan (slider) dan jenis kriteria (Benefit/Cost) untuk setiap kriteria, lalu klik **Jalankan Analisis Keputusan**.
4. **Hasil Rekomendasi** — Lihat ranking dari ketiga metode, kolom **Konsensus Rank** (Borda), matriks perhitungan step-by-step, unduh hasil CSV, dan jalankan analisis sensitivitas bobot interaktif.
5. **Teori & Metodologi** — Pelajari rumus matematis lengkap SAW, WP, dan TOPSIS.

## Fitur Utama

- **Universal:** Menerima dataset CSV apapun, bukan hanya data kesehatan.
- **Multi-Metode:** SAW, WP, dan TOPSIS dijalankan sekaligus untuk perbandingan.
- **Konsensus Borda:** Kolom peringkat konsensus otomatis ketika ketiga metode tidak sepakat.
- **Analisis Sensitivitas:** Uji stabilitas keputusan dengan mengubah bobot kriteria ±10–50%.
- **Transparan:** Semua matriks perhitungan intermediate ditampilkan step-by-step.
- **Export CSV:** Unduh tabel hasil perankingan langsung dari halaman Hasil Rekomendasi.

## Disclaimer

Sistem ini adalah alat bantu pengambilan keputusan. Keputusan akhir tetap berada di tangan pengguna.
