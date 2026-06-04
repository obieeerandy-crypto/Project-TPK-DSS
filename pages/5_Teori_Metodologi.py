"""
Teori dan Metodologi Page.
Provides educational overview and LaTeX mathematical formulas.
"""

import streamlit as st
import pandas as pd
from utils.ui_components import inject_custom_css, render_header

st.set_page_config(
    page_title="Teori & Metodologi - DSS Dashboard",
    page_icon="📚",
    layout="wide"
)

inject_custom_css()
render_header(
    "📚 Teori & Metodologi Pengambilan Keputusan",
    "Landasan matematis lengkap: SAW, WP, TOPSIS, ELECTRE, AHP, Ketidakpastian, Risiko."
)

tab_saw, tab_wp, tab_topsis = st.tabs([
    "📊 SAW",
    "🌀 WP",
    "⭐ TOPSIS",
])

# SAW Tab
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
    **2. Menghitung Nilai Preferensi Akhir ($V_i$)**
    """)
    st.latex(r"V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}")

# WP Tab
with tab_wp:
    st.markdown("### Weighted Product (WP)")
    st.markdown("""
    Metode WP menggunakan perkalian untuk menghubungkan rating kriteria, di mana rating setiap
    kriteria harus dipangkatkan terlebih dahulu dengan bobot kepentingan kriteria yang bersangkutan.

    #### Langkah-langkah Perhitungan:

    **1. Normalisasi Bobot Kriteria ($w_j$)**
    """)
    st.latex(r"w_j = \frac{W_j}{\sum_{k=1}^{n} W_k}")
    st.markdown("**2. Menghitung Nilai Vektor S:**")
    st.latex(r"S_i = \prod_{j=1}^{n} (x_{ij})^{w_j}")
    st.markdown("**3. Menghitung Nilai Vektor V (Skor Relatif):**")
    st.latex(r"V_i = \frac{S_i}{\sum_{k=1}^{m} S_k}")

# TOPSIS Tab
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
    st.markdown("**3. Jarak Euclidean:**")
    st.latex(r"D_i^+ = \sqrt{\sum_{j=1}^{n} (v_{ij} - v_j^+)^2}")
    st.latex(r"D_i^- = \sqrt{\sum_{j=1}^{n} (v_{ij} - v_j^-)^2}")
    st.markdown("**4. Nilai Preferensi / Kedekatan Relatif ($C_i$):**")
    st.latex(r"C_i = \frac{D_i^-}{D_i^+ + D_i^-}")
