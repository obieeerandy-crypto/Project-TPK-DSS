"""
Upload Data Page.
Allows users to upload custom CSV files and configure the alternative and criteria columns.
"""

import streamlit as st
import pandas as pd
from utils.ui_components import inject_custom_css, render_header
from utils.data_loader import auto_detect_columns, preprocess_dataset

st.set_page_config(
    page_title="Upload Data - DSS Dashboard",
    page_icon="📁",
    layout="wide"
)

inject_custom_css()
render_header("📁 Upload & Konfigurasi Dataset", "Unggah dataset CSV kustom Anda atau sesuaikan dengan data bawaan.")

# Sidebar Info
with st.sidebar:
    st.markdown("### ℹ️ Petunjuk Unggah")
    st.markdown(
        """
        1. **Format File:** Wajib berupa CSV (.csv).
        2. **Kolom Identitas:** Pilih kolom yang merepresentasikan nama/ID alternatif unik (misal: ID, Nama, Kode).
        3. **Kolom Kriteria:** Harus berupa kolom dengan nilai angka (numerik) agar dapat dihitung dengan metode DSS.
        4. **Data Hilang:** Jika ada nilai kosong (NaN), sistem akan mengisinya otomatis menggunakan metode imputasi yang dipilih.
        """
    )

# File uploader
uploaded_file = st.file_uploader("Unggah file CSV baru", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"🎉 Berhasil mengunggah file: **{uploaded_file.name}**")
        st.session_state["dataset"] = df
        st.session_state["dataset_name"] = uploaded_file.name
        # Mark results as stale whenever a new file is uploaded
        st.session_state["analisis_dijalankan"] = False
    except Exception as e:
        st.error(f"Gagal membaca file: {str(e)}")

# Display current configuration status
df = st.session_state["dataset"]

if not df.empty:
    st.markdown("### ⚙️ Konfigurasi Kolom & Kriteria")
    
    alt_candidates, crit_candidates = auto_detect_columns(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_alt = st.session_state.get("nama_col", "")
        if default_alt not in alt_candidates:
            default_alt = alt_candidates[0] if alt_candidates else ""
            
        nama_col = st.selectbox(
            "Pilih Kolom Alternatif (Nama / ID):",
            options=alt_candidates,
            index=alt_candidates.index(default_alt) if default_alt in alt_candidates else 0,
            help="Kolom ini akan digunakan sebagai label identitas alternatif dalam perankingan."
        )
        
    with col2:
        impute_method = st.selectbox(
            "Metode Penanganan Nilai Kosong (NaN Imputation):",
            options=["Mean", "Median", "Zero"],
            help="Nilai kosong pada kolom kriteria akan diisi otomatis dengan nilai statistik terpilih."
        )
        
    st.markdown("#### Pilih Kolom Kriteria (Wajib Numerik):")
    
    saved_crit = st.session_state.get("kriteria_cols", [])
    default_select = [c for c in saved_crit if c in crit_candidates]
    if not default_select and crit_candidates:
        default_select = crit_candidates[:min(5, len(crit_candidates))]
        
    kriteria_cols = st.multiselect(
        "Pilih kriteria keputusan:",
        options=crit_candidates,
        default=default_select,
        help="Hanya kolom angka yang didukung untuk perhitungan."
    )
    
    if len(kriteria_cols) < 2:
        st.warning("⚠️ Mohon pilih minimal 2 kriteria untuk melakukan analisis keputusan multi-kriteria.")
    else:
        if st.button("Simpan & Terapkan Konfigurasi"):
            st.session_state["nama_col"] = nama_col
            st.session_state["kriteria_cols"] = kriteria_cols
            
            saved_weights = st.session_state.get("weights", {})
            saved_types = st.session_state.get("types", {})
            
            new_weights = {col: saved_weights.get(col, 1.0) for col in kriteria_cols}
            new_types = {col: saved_types.get(col, "benefit") for col in kriteria_cols}
                
            st.session_state["weights"] = new_weights
            st.session_state["types"] = new_types
            st.session_state["dataset"] = preprocess_dataset(df, kriteria_cols, impute_method)
            # Mark results as stale after reconfiguration
            st.session_state["analisis_dijalankan"] = False
            
            st.success("✅ Konfigurasi disimpan! Silakan lanjut ke halaman **Eksplorasi Data** atau **Analisis DSS**.")
            st.rerun()

    st.markdown("### 📋 Preview Dataset Mentah")
    st.dataframe(df.head(10), use_container_width=True)
    st.info(f"Menampilkan 10 baris pertama dari total {len(df)} baris data.")
else:
    st.info("💡 Unggah file CSV di atas untuk memulai.")
