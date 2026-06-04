"""
DSS Analysis Configuration Page.
Sets weights, criteria types (Benefit/Cost), and initiates calculations.
"""

import streamlit as st
import pandas as pd
from utils.ui_components import inject_custom_css, render_header
from utils.dss_engine import run_all_methods

st.set_page_config(
    page_title="Analisis DSS - DSS Dashboard",
    page_icon="⚙️",
    layout="wide"
)

inject_custom_css()
render_header("⚙️ Konfigurasi Parameter & Bobot DSS", "Atur bobot kriteria dan jenis kriteria untuk menghitung peringkat terbaik.")

# Load session state variables
df = st.session_state.get("dataset", pd.DataFrame())
kriteria_cols = st.session_state.get("kriteria_cols", [])
nama_col = st.session_state.get("nama_col", "")

if df.empty or not kriteria_cols:
    st.info("💡 Silakan konfigurasikan dataset terlebih dahulu di halaman **Upload Data**.")
    st.stop()

st.markdown("### 🛠️ Pengaturan Parameter Kriteria")
st.markdown("Tentukan kepentingan relatif (bobot) dan pengaruh (Benefit vs Cost) untuk setiap kriteria:")

# Create configuration inputs
weights = st.session_state.get("weights", {c: 1.0 for c in kriteria_cols})
types = st.session_state.get("types", {c: "benefit" for c in kriteria_cols})

col_params_container = st.container()

with col_params_container:
    # Build a table-like form using streamlit columns
    col_hdr1, col_hdr2, col_hdr3 = st.columns([2, 2, 2])
    with col_hdr1:
        st.markdown("**Kriteria**")
    with col_hdr2:
        st.markdown("**Bobot Kepentingan (Weight)**")
    with col_hdr3:
        st.markdown("**Jenis Kriteria**")

    st.divider()

    updated_weights = {}
    updated_types = {}

    for col in kriteria_cols:
        col_c1, col_c2, col_c3 = st.columns([2, 2, 2])
        
        with col_c1:
            st.markdown(f"**{col}**")
            
        with col_c2:
            # Slider or Number input for weights
            val = weights.get(col, 1.0)
            weight_val = st.slider(
                f"Bobot {col}",
                min_value=0.1,
                max_value=10.0,
                value=float(val),
                step=0.1,
                label_visibility="collapsed"
            )
            updated_weights[col] = weight_val
            
        with col_c3:
            # Selectbox for type
            t_val = types.get(col, "benefit")
            type_val = st.selectbox(
                f"Jenis {col}",
                options=["benefit", "cost"],
                index=0 if t_val == "benefit" else 1,
                format_func=lambda x: "📈 Benefit (Makin besar makin baik)" if x == "benefit" else "📉 Cost (Makin kecil makin baik)",
                label_visibility="collapsed"
            )
            updated_types[col] = type_val

st.markdown("---")

# Save configurations in session state
st.session_state["weights"] = updated_weights
st.session_state["types"] = updated_types

# Sum of weights indicator
w_sum = sum(updated_weights.values())
st.markdown(f"💡 **Jumlah Total Bobot:** `{w_sum:.2f}` (Sistem akan otomatis menormalisasi bobot sehingga totalnya bernilai 1.0 atau 100% saat perhitungan dijalankan).")

st.markdown("### 🚀 Jalankan Perhitungan")
st.markdown("Klik tombol di bawah ini untuk menjalankan perhitungan DSS (SAW, WP, TOPSIS) secara bersamaan.")

# Warn if a previous result exists but config has changed since it was run
if st.session_state.get("analisis_dijalankan") is False:
    st.warning("⚠️ Konfigurasi dataset atau kriteria telah berubah. Jalankan ulang analisis untuk memperbarui hasil.")

if st.button("Jalankan Analisis Keputusan"):
    with st.spinner("Menghitung model keputusan..."):
        # Run calculations
        results_df, steps_dict = run_all_methods(
            df,
            kriteria_cols,
            updated_weights,
            updated_types,
            nama_col
        )
        
        # Save results in session state
        st.session_state["dss_results"] = results_df
        st.session_state["dss_steps"] = steps_dict
        st.session_state["analisis_dijalankan"] = True
        
        st.success("🎉 Analisis Keputusan berhasil diselesaikan! Buka halaman **Hasil Rekomendasi** untuk melihat peringkat.")
        
        # Guide user to page 4
        st.info("💡 Hasil perankingan sudah siap. Silakan klik **Hasil Rekomendasi** di panel navigasi.")
