"""
Teori dan Metodologi Page.
Provides educational overview and LaTeX mathematical formulas for SAW, WP, TOPSIS,
ELECTRE, AHP, Decision Under Uncertainty, Decision Under Risk, and Rank Correlation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.ui_components import inject_custom_css, render_header

st.set_page_config(
    page_title="Teori & Metodologi - DSS Dashboard",
    page_icon="📚",
    layout="wide"
)

inject_custom_css()
render_header(
    "📚 Teori & Metodologi Pengambilan Keputusan",
    "Landasan matematis lengkap: SAW, WP, TOPSIS, ELECTRE, AHP, Ketidakpastian, Risiko, dan Korelasi Peringkat."
)

tab_saw, tab_wp, tab_topsis, tab_electre, tab_ahp, tab_uncertainty, tab_risk, tab_rank_corr = st.tabs([
    "📊 SAW",
    "🌀 WP",
    "⭐ TOPSIS",
    "🔷 ELECTRE",
    "🔺 AHP",
    "🎲 Ketidakpastian",
    "🎯 Risiko",
    "📐 Korelasi Peringkat",
])

# ── SAW ────────────────────────────────────────────────────────────────────────
with tab_saw:
    st.markdown("### Simple Additive Weighting (SAW)")
    st.markdown("""
    Metode SAW sering dikenal dengan istilah metode penjumlahan terbobot. Konsep dasar metode SAW
    adalah mencari penjumlahan terbobot dari rating kinerja pada setiap alternatif pada semua kriteria.

    #### Langkah-langkah Perhitungan:

    **1. Normalisasi Matriks Keputusan ($R$)**

    Untuk kriteria **Benefit** (Makin besar makin baik):
    """)
    st.latex(r"r_{ij} = \frac{x_{ij}}{\max_{k}(x_{kj})}")
    st.markdown("Untuk kriteria **Cost** (Makin kecil makin baik):")
    st.latex(r"r_{ij} = \frac{\min_{k}(x_{kj})}{x_{ij}}")
    st.markdown("""
    Di mana:
    - $r_{ij}$ adalah nilai rating kinerja ternormalisasi.
    - $x_{ij}$ adalah nilai rating kinerja dari alternatif $A_i$ pada kriteria $C_j$.

    **2. Menghitung Nilai Preferensi Akhir ($V_i$)**
    """)
    st.latex(r"V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}")
    st.markdown("Nilai $V_i$ yang lebih besar mengindikasikan bahwa alternatif $A_i$ lebih terpilih.")

# ── WP ─────────────────────────────────────────────────────────────────────────
with tab_wp:
    st.markdown("### Weighted Product (WP)")
    st.markdown("""
    Metode WP menggunakan perkalian untuk menghubungkan rating kriteria, di mana rating setiap
    kriteria harus dipangkatkan terlebih dahulu dengan bobot kepentingan kriteria yang bersangkutan.

    #### Langkah-langkah Perhitungan:

    **1. Normalisasi Bobot Kriteria ($w_j$)**
    """)
    st.latex(r"w_j = \frac{W_j}{\sum_{k=1}^{n} W_k}")
    st.markdown("Pangkat bernilai positif untuk kriteria **Benefit** dan negatif untuk kriteria **Cost**.")
    st.markdown("**2. Menghitung Nilai Vektor S:**")
    st.latex(r"S_i = \prod_{j=1}^{n} (x_{ij})^{w_j}")
    st.markdown("**3. Menghitung Nilai Vektor V (Skor Relatif):**")
    st.latex(r"V_i = \frac{S_i}{\sum_{k=1}^{m} S_k}")

# ── TOPSIS ─────────────────────────────────────────────────────────────────────
with tab_topsis:
    st.markdown("### TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)")
    st.markdown("""
    TOPSIS didasarkan pada konsep bahwa alternatif yang terpilih tidak hanya memiliki jarak terpendek
    dari solusi ideal positif, tetapi juga memiliki jarak terpanjang dari solusi ideal negatif.

    #### Langkah-langkah Perhitungan:

    **1. Normalisasi Matriks (Vektor):**
    """)
    st.latex(r"r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^{m} (x_{kj})^2}}")
    st.markdown("**2. Matriks Ternormalisasi Terbobot:**")
    st.latex(r"v_{ij} = w_j \cdot r_{ij}")
    st.markdown("**3. Solusi Ideal Positif ($A^+$) dan Negatif ($A^-$):**")
    st.latex(r"A^+ = (v_1^+, v_2^+, \dots, v_n^+)")
    st.latex(r"A^- = (v_1^-, v_2^-, \dots, v_n^-)")
    st.markdown("**4. Jarak Euclidean:**")
    st.latex(r"D_i^+ = \sqrt{\sum_{j=1}^{n} (v_{ij} - v_j^+)^2}")
    st.latex(r"D_i^- = \sqrt{\sum_{j=1}^{n} (v_{ij} - v_j^-)^2}")
    st.markdown("**5. Nilai Preferensi / Kedekatan Relatif ($C_i$):**")
    st.latex(r"C_i = \frac{D_i^-}{D_i^+ + D_i^-}")
    st.markdown("Alternatif dengan $C_i$ tertinggi merupakan alternatif yang paling direkomendasikan.")

# ── ELECTRE ────────────────────────────────────────────────────────────────────
with tab_electre:
    st.markdown("### ELECTRE (Elimination and Choice Expressing Reality)")
    st.markdown(r"""
    ELECTRE adalah metode **outranking** yang dikembangkan oleh Bernard Roy (1968). Berbeda dengan
    SAW/WP/TOPSIS yang menghasilkan skor tunggal, ELECTRE menentukan apakah satu alternatif
    **mendominasi (outranks)** alternatif lain berdasarkan **concordance** dan **discordance**.

    #### Konsep Dasar
    Alternatif $A_k$ dikatakan *outrank* $A_l$ jika:
    - **Concordance**: Sebagian besar bobot kriteria mendukung $A_k \geq A_l$
    - **Discordance**: Tidak ada kriteria yang terlalu jauh lebih baik untuk $A_l$

    #### Langkah-langkah ELECTRE I:

    **1. Normalisasi Matriks (Vektor):**
    """)
    st.latex(r"r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^{m} x_{kj}^2}}")

    st.markdown("**2. Matriks Ternormalisasi Terbobot:**")
    st.latex(r"v_{ij} = w_j \cdot r_{ij}")

    st.markdown("**3. Concordance Set ($C_{kl}$) dan Discordance Set ($D_{kl}$):**")
    st.markdown(r"""
    Untuk setiap pasang alternatif $(A_k, A_l)$:
    - **Concordance Set**: $C_{kl} = \{j \mid v_{kj} \geq v_{lj}\}$ — kriteria di mana $A_k$ tidak lebih buruk dari $A_l$
    - **Discordance Set**: $D_{kl} = \{j \mid v_{kj} < v_{lj}\}$ — kriteria di mana $A_k$ lebih buruk dari $A_l$
    """)

    st.markdown("**4. Indeks Concordance ($c_{kl}$):**")
    st.latex(r"c_{kl} = \frac{\sum_{j \in C_{kl}} w_j}{\sum_{j=1}^{n} w_j}")
    st.markdown("Nilai $c_{kl}$ ∈ [0,1]. Semakin tinggi → $A_k$ semakin mendominasi $A_l$.")

    st.markdown("**5. Indeks Discordance ($d_{kl}$):**")
    st.latex(r"d_{kl} = \frac{\max_{j \in D_{kl}} |v_{kj} - v_{lj}|}{\max_{j} |v_{kj} - v_{lj}|}")
    st.markdown("Nilai $d_{kl}$ ∈ [0,1]. Semakin rendah → $A_k$ semakin mendominasi $A_l$.")

    st.markdown("**6. Matriks Dominansi (Aggregate Dominance):**")
    st.markdown("""
    $A_k$ *outranks* $A_l$ jika:
    - $c_{kl} \\geq \\bar{c}$ (threshold concordance), **DAN**
    - $d_{kl} \\leq \\bar{d}$ (threshold discordance)

    Di mana $\\bar{c}$ dan $\\bar{d}$ adalah rata-rata dari seluruh nilai concordance/discordance.
    """)
    st.latex(r"\bar{c} = \frac{1}{m(m-1)} \sum_{k \neq l} c_{kl}")
    st.latex(r"\bar{d} = \frac{1}{m(m-1)} \sum_{k \neq l} d_{kl}")

    st.markdown("**7. Eliminasi Alternatif:**")
    st.markdown("""
    Alternatif yang paling banyak di-*outrank* oleh alternatif lain dieliminasi.
    Alternatif yang tidak di-*outrank* oleh siapapun masuk ke **core** (set solusi terbaik).
    """)

    st.markdown("#### Perbandingan ELECTRE vs TOPSIS")
    comparison_data = {
        "Aspek": ["Tipe Metode", "Output", "Penanganan Inkomparabilitas", "Kompleksitas", "Cocok untuk"],
        "ELECTRE": ["Outranking", "Set dominansi / eliminasi", "Ya (bisa tidak ada pemenang)", "Tinggi", "Banyak alternatif, kriteria konflik"],
        "TOPSIS": ["Scoring/Ranking", "Skor tunggal per alternatif", "Tidak", "Sedang", "Perbandingan langsung semua alternatif"],
    }
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

    st.info("💡 Implementasi interaktif ELECTRE tersedia di halaman **Analisis DSS** (akan segera ditambahkan). Halaman ini menampilkan teori lengkapnya.")

# ── AHP ────────────────────────────────────────────────────────────────────────
with tab_ahp:
    st.markdown("### AHP — Analytic Hierarchy Process")
    st.markdown("""
    AHP dikembangkan oleh Thomas L. Saaty (1980). Metode ini menstrukturkan masalah keputusan
    kompleks menjadi hierarki, lalu menentukan bobot kriteria melalui **perbandingan berpasangan**
    menggunakan **Skala Saaty (1–9)**.

    #### Skala Perbandingan Saaty
    """)
    saaty_data = {
        "Nilai": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Keterangan": [
            "Sama pentingnya", "Di antara 1 dan 3", "Sedikit lebih penting",
            "Di antara 3 dan 5", "Lebih penting", "Di antara 5 dan 7",
            "Sangat lebih penting", "Di antara 7 dan 9", "Mutlak lebih penting"
        ]
    }
    st.dataframe(pd.DataFrame(saaty_data), use_container_width=True, hide_index=True)

    st.markdown("#### Langkah-langkah AHP:")
    st.markdown("**1. Normalisasi Matriks Perbandingan:**")
    st.latex(r"\bar{a}_{ij} = \frac{a_{ij}}{\sum_{k=1}^{n} a_{kj}}")
    st.markdown("**2. Bobot Prioritas (rata-rata baris):**")
    st.latex(r"w_i = \frac{1}{n} \sum_{j=1}^{n} \bar{a}_{ij}")
    st.markdown("**3. Eigenvalue Maksimum:**")
    st.latex(r"\lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{(A \cdot w)_i}{w_i}")
    st.markdown("**4. Consistency Index (CI):**")
    st.latex(r"CI = \frac{\lambda_{max} - n}{n - 1}")
    st.markdown("**5. Consistency Ratio (CR):**")
    st.latex(r"CR = \frac{CI}{RI}")
    st.markdown("Jika **CR ≤ 0.10**, matriks dianggap konsisten dan bobot dapat diterima.")

    st.markdown("#### Tabel Random Index (RI) Saaty")
    ri_data = {"n": [1,2,3,4,5,6,7,8,9,10], "RI": [0.00,0.00,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1.49]}
    st.dataframe(pd.DataFrame(ri_data).T, use_container_width=True)

    st.markdown("#### Hierarki AHP")
    st.markdown("""
    ```
    TUJUAN (Goal)
    ├── Kriteria 1 (C1)  ─── bobot w1
    ├── Kriteria 2 (C2)  ─── bobot w2
    └── Kriteria n (Cn)  ─── bobot wn
         ├── Alternatif A1
         ├── Alternatif A2
         └── Alternatif Am
    ```
    """)

# ── Uncertainty ────────────────────────────────────────────────────────────────
with tab_uncertainty:
    st.markdown("### Keputusan di Bawah Ketidakpastian")
    st.markdown("""
    Dalam kondisi **ketidakpastian**, probabilitas kondisi alam **tidak diketahui**.
    Lima kriteria klasik digunakan:

    | Kriteria | Filosofi | Tipe Pengambil Keputusan |
    |---|---|---|
    | **Maximin** | Pilih worst-case terbaik | Pesimis / Risk-averse |
    | **Maximax** | Pilih best-case terbaik | Optimis / Risk-seeking |
    | **Hurwicz** | Kombinasi optimisme-pesimisme | Moderat |
    | **Laplace** | Semua kondisi sama-sama mungkin | Netral |
    | **Minimax Regret** | Minimasi penyesalan terbesar | Penyesal |
    """)

    st.markdown("#### Maximin (Wald Criterion)")
    st.latex(r"\text{Pilih } A_i^* = \arg\max_i \left[ \min_j (x_{ij}) \right]")

    st.markdown("#### Maximax")
    st.latex(r"\text{Pilih } A_i^* = \arg\max_i \left[ \max_j (x_{ij}) \right]")

    st.markdown("#### Hurwicz")
    st.latex(r"H_i = \alpha \cdot \max_j(x_{ij}) + (1 - \alpha) \cdot \min_j(x_{ij})")
    st.markdown("α ∈ [0,1] adalah koefisien optimisme. α=1 → Maximax; α=0 → Maximin.")

    st.markdown("#### Laplace (Insufficient Reason)")
    st.latex(r"\bar{x}_i = \frac{1}{n} \sum_{j=1}^{n} x_{ij}")

    st.markdown("#### Minimax Regret (Savage Criterion)")
    st.latex(r"r_{ij} = \max_k(x_{kj}) - x_{ij}")
    st.latex(r"\text{Pilih } A_i^* = \arg\min_i \left[ \max_j (r_{ij}) \right]")

    st.info("💡 Gunakan halaman **Keputusan Ketidakpastian** untuk analisis interaktif dengan tabel payoff kustom.")

# ── Risk ───────────────────────────────────────────────────────────────────────
with tab_risk:
    st.markdown("### Keputusan di Bawah Risiko")
    st.markdown("""
    Dalam kondisi **risiko**, probabilitas kondisi alam **diketahui** atau dapat diestimasi.
    Tiga konsep utama:
    """)

    st.markdown("#### EMV — Expected Monetary Value")
    st.latex(r"EMV_i = \sum_{j=1}^{n} P(S_j) \cdot x_{ij}")
    st.markdown("Pilih alternatif dengan **EMV terbesar**.")

    st.markdown("#### EOL — Expected Opportunity Loss")
    st.latex(r"OL_{ij} = \max_k(x_{kj}) - x_{ij}")
    st.latex(r"EOL_i = \sum_{j=1}^{n} P(S_j) \cdot OL_{ij}")
    st.markdown("Pilih alternatif dengan **EOL terkecil**.")

    st.markdown("#### EVPI — Expected Value of Perfect Information")
    st.latex(r"EVwPI = \sum_{j=1}^{n} P(S_j) \cdot \max_k(x_{kj})")
    st.latex(r"EVPI = EVwPI - \max_i(EMV_i)")
    st.markdown("""
    - **EVwPI** = Expected Value *with* Perfect Information
    - **EVPI** = nilai maksimum yang rasional untuk dibayar demi informasi sempurna
    - Hubungan penting: **EVPI = min(EOL)**
    """)

    st.markdown("#### Pohon Keputusan (Decision Tree)")
    st.markdown("""
    Pohon keputusan adalah representasi visual dari masalah keputusan di bawah risiko:
    ```
    [Keputusan] ──── Alternatif A1 ──── [Peluang] ──── S1 (P=0.3) → Payoff 100
                                                   └──── S2 (P=0.7) → Payoff  40
                └─── Alternatif A2 ──── [Peluang] ──── S1 (P=0.3) → Payoff  80
                                                   └──── S2 (P=0.7) → Payoff  60
    ```
    EMV(A1) = 0.3×100 + 0.7×40 = 58
    EMV(A2) = 0.3×80  + 0.7×60 = 66 ← Terpilih
    """)

    st.info("💡 Gunakan halaman **Keputusan Risiko** untuk analisis interaktif EMV, EOL, dan EVPI.")

# ── Rank Correlation ───────────────────────────────────────────────────────────
with tab_rank_corr:
    st.markdown("### Korelasi Peringkat — Spearman & Kendall")
    st.markdown("""
    Korelasi peringkat mengukur seberapa **konsisten** dua metode DSS dalam menghasilkan urutan
    alternatif yang sama. Ini penting untuk mengevaluasi **keandalan konsensus** antar metode.
    """)

    st.markdown("#### Korelasi Spearman ($r_s$)")
    st.latex(r"r_s = 1 - \frac{6 \sum_{i=1}^{n} d_i^2}{n(n^2 - 1)}")
    st.markdown("""
    Di mana $d_i = \\text{Rank}_1(i) - \\text{Rank}_2(i)$ adalah selisih peringkat alternatif ke-$i$
    antara dua metode. Nilai $r_s$ ∈ [-1, 1]:
    - $r_s = 1$ → peringkat identik
    - $r_s = 0$ → tidak ada korelasi
    - $r_s = -1$ → peringkat terbalik sempurna
    """)

    st.markdown("#### Korelasi Kendall ($\\tau$)")
    st.latex(r"\tau = \frac{C - D}{\frac{1}{2} n(n-1)}")
    st.markdown("""
    Di mana:
    - $C$ = jumlah pasangan **concordant** (urutan sama di kedua metode)
    - $D$ = jumlah pasangan **discordant** (urutan berbeda)
    """)

    st.markdown("#### Interpretasi Nilai Korelasi")
    interp_data = {
        "Rentang |r|": ["0.90 – 1.00", "0.70 – 0.89", "0.50 – 0.69", "0.30 – 0.49", "0.00 – 0.29"],
        "Interpretasi": ["Sangat kuat", "Kuat", "Sedang", "Lemah", "Sangat lemah / tidak ada"],
    }
    st.dataframe(pd.DataFrame(interp_data), use_container_width=True, hide_index=True)

    st.markdown("#### Aplikasi dalam DSS")
    st.markdown("""
    Setelah menjalankan SAW, WP, dan TOPSIS, kita dapat menghitung korelasi Spearman antar
    peringkat ketiga metode untuk menilai konsistensi:

    - **SAW vs WP**, **SAW vs TOPSIS**, **WP vs TOPSIS**
    - Jika semua $r_s > 0.9$ → ketiga metode sangat konsisten → keputusan stabil
    - Jika ada $r_s < 0.7$ → ada ketidaksepakatan signifikan → perlu analisis lebih lanjut
    """)

    # Interactive demo with current DSS results
    if st.session_state.get("analisis_dijalankan") and st.session_state.get("dss_results") is not None:
        st.markdown("---")
        st.markdown("#### 📊 Korelasi Peringkat dari Hasil DSS Saat Ini")
        results_df = st.session_state["dss_results"]

        if all(c in results_df.columns for c in ["SAW Rank", "WP Rank", "TOPSIS Rank"]):
            saw_r = results_df["SAW Rank"].values
            wp_r = results_df["WP Rank"].values
            topsis_r = results_df["TOPSIS Rank"].values
            n_alts = len(saw_r)

            def spearman(r1, r2):
                d2 = (r1 - r2) ** 2
                return 1 - 6 * d2.sum() / (n_alts * (n_alts**2 - 1))

            rs_saw_wp = spearman(saw_r, wp_r)
            rs_saw_topsis = spearman(saw_r, topsis_r)
            rs_wp_topsis = spearman(wp_r, topsis_r)

            col1, col2, col3 = st.columns(3)
            col1.metric("Spearman SAW vs WP", f"{rs_saw_wp:.4f}")
            col2.metric("Spearman SAW vs TOPSIS", f"{rs_saw_topsis:.4f}")
            col3.metric("Spearman WP vs TOPSIS", f"{rs_wp_topsis:.4f}")

            # Heatmap
            corr_matrix = np.array([
                [1.0, rs_saw_wp, rs_saw_topsis],
                [rs_saw_wp, 1.0, rs_wp_topsis],
                [rs_saw_topsis, rs_wp_topsis, 1.0],
            ])
            fig_heat = px.imshow(
                corr_matrix,
                x=["SAW", "WP", "TOPSIS"],
                y=["SAW", "WP", "TOPSIS"],
                text_auto=".4f",
                color_continuous_scale="Purples",
                title="Heatmap Korelasi Spearman Antar Metode DSS",
                template="plotly_dark",
                zmin=-1, zmax=1,
            )
            fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
            st.plotly_chart(fig_heat, use_container_width=True)

            avg_corr = (rs_saw_wp + rs_saw_topsis + rs_wp_topsis) / 3
            if avg_corr >= 0.9:
                st.success(f"✅ Rata-rata korelasi = {avg_corr:.4f} — Ketiga metode **sangat konsisten**. Konsensus Borda dapat dipercaya.")
            elif avg_corr >= 0.7:
                st.warning(f"⚠️ Rata-rata korelasi = {avg_corr:.4f} — Konsistensi **sedang**. Perhatikan perbedaan ranking antar metode.")
            else:
                st.error(f"❌ Rata-rata korelasi = {avg_corr:.4f} — Konsistensi **rendah**. Hasil ketiga metode berbeda signifikan.")
    else:
        st.info("💡 Jalankan analisis DSS terlebih dahulu (halaman Analisis DSS) untuk melihat korelasi peringkat dari hasil aktual.")
