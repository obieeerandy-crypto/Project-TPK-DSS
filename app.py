"""
Universal Decision Support System (DSS) Dashboard.
Main landing page initializing session states and showing a premium, interactive overview.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from ui_components import inject_custom_css, render_header, kpi_card
from data_loader import load_csv, auto_detect_columns

# Page Configuration
st.set_page_config(
    page_title="Universal DSS Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "dataset" not in st.session_state:
    # Load default dataset (heart_disease_uci.csv)
    default_path = Path(__file__).resolve().parent / "heart_disease_uci.csv"
    if default_path.exists():
        st.session_state["dataset"] = pd.read_csv(default_path)
        st.session_state["dataset_name"] = "heart_disease_uci.csv (Default)"
    else:
        st.session_state["dataset"] = pd.DataFrame()
        st.session_state["dataset_name"] = "Tidak ada"

if "nama_col" not in st.session_state:
    st.session_state["nama_col"] = "id" if not st.session_state["dataset"].empty and "id" in st.session_state["dataset"].columns else ""

if "kriteria_cols" not in st.session_state:
    if not st.session_state["dataset"].empty:
        # Default criteria cols for heart disease
        cols = [c for c in ["age", "trestbps", "chol", "thalch", "oldpeak", "ca"] if c in st.session_state["dataset"].columns]
        st.session_state["kriteria_cols"] = cols
    else:
        st.session_state["kriteria_cols"] = []

if "weights" not in st.session_state:
    if "kriteria_cols" in st.session_state:
        st.session_state["weights"] = {col: 1.0 for col in st.session_state["kriteria_cols"]}
    else:
        st.session_state["weights"] = {}

if "types" not in st.session_state:
    if "kriteria_cols" in st.session_state:
        st.session_state["types"] = {col: "benefit" for col in st.session_state["kriteria_cols"]}
        # Default cost types for heart disease (e.g., age, oldpeak should be cost for low disease risk, or benefit depending on perspective. Let's make all default benefit first)
    else:
        st.session_state["types"] = {}

# Inject Premium CSS Styling
inject_custom_css()

# Header
render_header(
    "🎯 Universal Decision Support System (DSS) Dashboard",
    "Solusi analisis pengambilan keputusan multi-kriteria berbasis metode SAW, WP, dan TOPSIS."
)

# Content Grid
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(
        """
        <div class="glass-card">
            <h3>🚀 Tentang Dashboard DSS</h3>
            <p>
                Dashboard ini dirancang untuk menyelesaikan masalah <b>Multi-Criteria Decision Making (MCDM)</b> secara dinamis. Anda dapat mengunggah dataset CSV Anda sendiri, mengonfigurasi krit[...]
            </p>
            <p>
                Sistem ini mendukung perbandingan langsung antara 3 metode pengambilan keputusan klasik yang populer:
            </p>
            <ul>
                <li><b>SAW (Simple Additive Weighting):</b> Metode penjumlahan terbobot dari rating kinerja pada setiap alternatif untuk semua kriteria.</li>
                <li><b>WP (Weighted Product):</b> Metode perkalian terbobot untuk menghubungkan rating kriteria, di mana rating harus dipangkatkan terlebih dahulu dengan bobot kriteria.</li>
                <li><b>TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution):</b> Mengevaluasi alternatif berdasarkan jarak terdekat dari solusi ideal positif dan terjauh dari[...]</li>
            </ul>
            <p>Ditambah modul teori lengkap untuk mata kuliah <b>Teori Pengambilan Keputusan</b>:</p>
            <ul>
                <li><b>AHP (Analytic Hierarchy Process):</b> Penentuan bobot kriteria melalui perbandingan berpasangan dengan uji konsistensi (CR).</li>
                <li><b>Keputusan di Bawah Ketidakpastian:</b> Maximin, Maximax, Hurwicz, Laplace, Minimax Regret.</li>
                <li><b>Keputusan di Bawah Risiko:</b> EMV, EOL, EVPI dengan tabel payoff dan probabilitas.</li>
                <li><b>Korelasi Peringkat Spearman:</b> Uji konsistensi antar metode SAW, WP, dan TOPSIS.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-card">
            <h3>🧭 Alur Penggunaan</h3>
            <table style="width:100%; border-collapse: collapse; margin-top:10px;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <th style="text-align:left; padding:8px; color:#a5b4fc;">Langkah</th>
                    <th style="text-align:left; padding:8px; color:#a5b4fc;">Halaman</th>
                    <th style="text-align:left; padding:8px; color:#a5b4fc;">Deskripsi</th>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">1</td>
                    <td style="padding:8px;">📁 Upload Data</td>
                    <td style="padding:8px;">Unggah dataset CSV Anda dan konfigurasikan kolom alternatif serta kriteria.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">2</td>
                    <td style="padding:8px;">📊 Eksplorasi Data</td>
                    <td style="padding:8px;">Eksplorasi data interaktif (tabel, statistik, visualisasi grafik korelatif).</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">3</td>
                    <td style="padding:8px;">⚙️ Analisis DSS</td>
                    <td style="padding:8px;">Set bobot preferensi (weights) & jenis kriteria (benefit/cost) serta lakukan analisis sensitivitas.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">4</td>
                    <td style="padding:8px;">🏆 Hasil Rekomendasi</td>
                    <td style="padding:8px;">Lihat ranking akhir, matriks perbandingan, visualisasi, perhitungan step-by-step, dan korelasi Spearman.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">5</td>
                    <td style="padding:8px;">📚 Teori & Metodologi</td>
                    <td style="padding:8px;">Rumus lengkap SAW, WP, TOPSIS, ELECTRE, AHP, Ketidakpastian, Risiko, dan Korelasi Peringkat.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">6</td>
                    <td style="padding:8px;">🎲 Keputusan Ketidakpastian</td>
                    <td style="padding:8px;">Analisis Maximin, Maximax, Hurwicz, Laplace, Minimax Regret dengan tabel payoff kustom.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">7</td>
                    <td style="padding:8px;">🔺 AHP</td>
                    <td style="padding:8px;">Pairwise comparison matrix, uji konsistensi (CR), dan derivasi bobot prioritas.</td>
                </tr>
                <tr>
                    <td style="padding:8px; font-weight:bold; color:#b388ff;">8</td>
                    <td style="padding:8px;">🎯 Keputusan Risiko</td>
                    <td style="padding:8px;">Analisis EMV, EOL, dan EVPI dengan tabel payoff dan probabilitas kondisi alam.</td>
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center;">
            <h3>📊 Status Konfigurasi</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render KPI Cards in Column Right
    kpi_card(
        "Dataset Aktif", 
        st.session_state["dataset_name"],
        icon="📁"
    )
    kpi_card(
        "Jumlah Kriteria", 
        f"{len(st.session_state['kriteria_cols'])} Kriteria",
        icon="⚙️"
    )
    if not st.session_state["dataset"].empty:
        kpi_card(
            "Alternatif Terdeteksi", 
            f"{len(st.session_state['dataset'])} Baris",
            icon="🏆"
        )

# Sidebar Info
with st.sidebar:
    st.markdown("### 🎯 DSS Engine Multi-Metode")
    st.info(
        f"**Dataset saat ini:**\n`{st.session_state['dataset_name']}`"
    )
    st.divider()
    st.markdown(
        """
        **💡 Keunggulan Dashboard ini:**
        - **Dinamis & Universal:** Menerima input CSV apapun.
        - **Multi-Metode MCDM:** SAW, WP, TOPSIS, AHP.
        - **Teori Keputusan Lengkap:** Ketidakpastian & Risiko (EMV, EOL, EVPI).
        - **Analisis Sensitivitas:** Lihat perubahan bobot secara interaktif.
        - **Korelasi Spearman:** Uji konsistensi antar metode.
        - **Transparan:** Menampilkan semua rumus dan matriks perhitungan step-by-step.
        """
    )
