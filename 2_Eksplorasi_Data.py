"""
Interactive Data Exploration (EDA) Page.
Provides data summary, missing value analysis, and Plotly visualisations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from utils.ui_components import inject_custom_css, render_header

st.set_page_config(
    page_title="Eksplorasi Data - DSS Dashboard",
    page_icon="📊",
    layout="wide"
)

inject_custom_css()
render_header("📊 Eksplorasi & Analisis Data", "Pahami karakteristik, sebaran, dan korelasi antar kriteria keputusan.")

# Retrieve configurations from session state
df = st.session_state.get("dataset", pd.DataFrame())
kriteria_cols = st.session_state.get("kriteria_cols", [])
nama_col = st.session_state.get("nama_col", "")

if df.empty:
    st.info("💡 Silakan unggah atau simpan konfigurasi data terlebih dahulu di halaman **Upload Data**.")
    st.stop()

# Basic statistics
st.markdown("### 📈 Ringkasan Statistik Kriteria")
st.dataframe(df[kriteria_cols].describe(), use_container_width=True)

# Missing values info
missing_counts = df[kriteria_cols].isnull().sum()
if missing_counts.sum() > 0:
    st.warning(f"⚠️ Ditemukan nilai kosong (NaN) di beberapa kriteria: \n" + 
               ", ".join([f"{k}: {v}" for k, v in missing_counts.items() if v > 0]))
else:
    st.success("✅ Dataset bersih, tidak ditemukan nilai kosong pada kriteria terpilih.")

# Plotly Visualizations Section
st.markdown("### 🎨 Visualisasi Distribusi dan Korelasi")

tab1, tab2, tab3 = st.tabs(["📊 Distribusi Kriteria", "📈 Hubungan Dua Kriteria (Scatter)", "🌡️ Korelasi Matrix Heatmap"])

with tab1:
    st.markdown("#### Distribusi Kriteria")
    selected_dist_col = st.selectbox("Pilih Kriteria untuk Distribusi:", options=kriteria_cols)
    
    # Histogram
    fig_hist = px.histogram(
        df, 
        x=selected_dist_col, 
        marginal="box",
        title=f"Distribusi Nilai {selected_dist_col}",
        template="plotly_dark",
        color_discrete_sequence=["#8a2be2"]
    )
    fig_hist.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fafafa")
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with tab2:
    st.markdown("#### Scatter Plot Korelasi antar Kriteria")
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Pilih Kriteria Sumbu X:", options=kriteria_cols, index=0)
    with col2:
        y_axis = st.selectbox("Pilih Kriteria Sumbu Y:", options=kriteria_cols, index=min(1, len(kriteria_cols)-1))
        
    color_by = st.selectbox("Warna Berdasarkan Kolom:", options=["None"] + [c for c in df.columns if c != x_axis and c != y_axis])
    
    fig_scatter = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color=None if color_by == "None" else color_by,
        hover_name=nama_col if nama_col else None,
        title=f"Scatter Plot: {x_axis} vs {y_axis}",
        template="plotly_dark"
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fafafa")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.markdown("#### Heatmap Korelasi Pearson")
    if len(kriteria_cols) >= 2:
        corr_matrix = df[kriteria_cols].corr()
        
        # Plotly Annotated Heatmap
        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="Purples",
            title="Korelasi Linear Pearson antar Kriteria",
            template="plotly_dark"
        )
        fig_heat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#fafafa")
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Pilih minimal 2 kriteria untuk menampilkan heatmap korelasi.")
