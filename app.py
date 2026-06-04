"""
Universal Decision Support System (DSS) Dashboard.
Main landing page initializing session states and showing a premium, interactive overview.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================================
# UI COMPONENTS
# ============================================================================

def inject_custom_css():
    """Injects premium styling and glassmorphism elements."""
    st.markdown(
        """
        <style>
        .glass-card {
            background: rgba(31, 38, 53, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 24px;
            margin-bottom: 20px;
            color: #fafafa;
        }
        
        .kpi-card {
            flex: 1;
            min-width: 200px;
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(31, 38, 53, 0.8) 100%);
            border: 1px solid rgba(138, 43, 226, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        
        .kpi-val {
            font-size: 2rem;
            font-weight: 700;
            color: #b388ff;
            margin-bottom: 4px;
        }
        
        .kpi-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #a5b4fc;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #8a2be2 0%, #4a0e4e 100%);
            color: white;
            border: none;
            padding: 8px 24px;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
            background: linear-gradient(135deg, #a044ff 0%, #6a11cb 100%);
            color: white;
        }
        
        .dataframe {
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            background-color: #1f2635 !important;
            color: #fafafa !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, icon: str = "🎯"):
    """Renders a single KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
            <div class="kpi-val">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_header(title: str, subtitle: str):
    """Renders a standard premium header."""
    st.markdown(
        f"""
        <div style="margin-bottom: 30px;">
            <h1 style="color: #fafafa; font-size: 2.5rem; margin-bottom: 8px; font-weight: 800; background: linear-gradient(to right, #ffffff, #b388ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
            <p style="color: #a5b4fc; font-size: 1.1rem; margin-top: 0;">{subtitle}</p>
            <hr style="border-color: rgba(138, 43, 226, 0.2); margin-top: 20px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Universal DSS Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "dataset" not in st.session_state:
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
    else:
        st.session_state["types"] = {}

# Inject CSS
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
                Dashboard ini dirancang untuk menyelesaikan masalah <b>Multi-Criteria Decision Making (MCDM)</b> secara dinamis. Anda dapat mengunggah dataset CSV Anda sendiri, mengonfigurasi kriteria keputusan, dan membandingkan hasil dari tiga metode MCDM yang berbeda.
            </p>
            <p>
                Sistem ini mendukung perbandingan langsung antara 3 metode pengambilan keputusan klasik yang populer:
            </p>
            <ul>
                <li><b>SAW (Simple Additive Weighting):</b> Metode penjumlahan terbobot dari rating kinerja pada setiap alternatif untuk semua kriteria.</li>
                <li><b>WP (Weighted Product):</b> Metode perkalian terbobot untuk menghubungkan rating kriteria, di mana rating harus dipangkatkan terlebih dahulu dengan bobot kriteria.</li>
                <li><b>TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution):</b> Mengevaluasi alternatif berdasarkan jarak terdekat dari solusi ideal positif dan terjauh dari solusi ideal negatif.</li>
            </ul>
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
        - **Multi-Metode MCDM:** SAW, WP, TOPSIS.
        - **Transparan:** Menampilkan semua rumus dan matriks perhitungan step-by-step.
        """
    )
