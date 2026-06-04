"""
Results and Recommendations Page.
Displays ranking comparisons, step-by-step intermediate calculation matrices,
and interactive sensitivity analysis with Plotly line graphs.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import inject_custom_css, render_header, kpi_card
from utils.dss_engine import run_sensitivity_analysis

st.set_page_config(
    page_title="Hasil Rekomendasi - DSS Dashboard",
    page_icon="🏆",
    layout="wide"
)

inject_custom_css()
render_header(
    "🏆 Hasil Perankingan & Analisis Rekomendasi",
    "Lihat ranking alternatif terbaik dan pelajari proses perhitungan secara transparan.",
)

# ── Retrieve data and results ─────────────────────────────────────────────────
df = st.session_state.get("dataset", pd.DataFrame())
kriteria_cols = st.session_state.get("kriteria_cols", [])
nama_col = st.session_state.get("nama_col", "")
analisis_dijalankan = st.session_state.get("analisis_dijalankan", False)

if df.empty or not analisis_dijalankan:
    st.info(
        "💡 Silakan lakukan konfigurasi parameter dan tekan tombol "
        "**Jalankan Analisis Keputusan** terlebih dahulu di halaman **Analisis DSS**."
    )
    st.stop()

results_df = st.session_state["dss_results"]
steps = st.session_state["dss_steps"]
weights = st.session_state["weights"]
types = st.session_state["types"]

# ── KPI cards ─────────────────────────────────────────────────────────────────
st.markdown("### 🥇 Alternatif Terbaik per Metode")

top_saw = results_df.sort_values("SAW Score", ascending=False).iloc[0]
top_wp = results_df.sort_values("WP Score", ascending=False).iloc[0]
top_topsis = results_df.sort_values("TOPSIS Score", ascending=False).iloc[0]
top_konsensus = results_df.sort_values("Konsensus Rank").iloc[0]

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    kpi_card(label=f"Terbaik SAW ({top_saw['SAW Score']:.4f})", value=str(top_saw[nama_col]), icon="📊")
with col_kpi2:
    kpi_card(label=f"Terbaik WP ({top_wp['WP Score']:.4f})", value=str(top_wp[nama_col]), icon="🌀")
with col_kpi3:
    kpi_card(label=f"Terbaik TOPSIS ({top_topsis['TOPSIS Score']:.4f})", value=str(top_topsis[nama_col]), icon="⭐")
with col_kpi4:
    kpi_card(label=f"Konsensus Borda (Rank #{top_konsensus['Konsensus Rank']})", value=str(top_konsensus[nama_col]), icon="🏆")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_ranks, tab_steps, tab_sensitivity, tab_rank_corr = st.tabs([
    "🏆 Tabel Peringkat & Perbandingan",
    "⚙️ Detail Perhitungan Step-by-step",
    "📈 Analisis Sensitivitas Bobot",
    "📐 Korelasi Peringkat Spearman",
])

# ── Tab 1: Rankings ───────────────────────────────────────────────────────────
with tab_ranks:
    st.markdown("#### Perbandingan Hasil Akhir & Peringkat")
    st.markdown(
        "Kolom **Konsensus Rank** menggunakan metode Borda (rata-rata peringkat dari ketiga metode) "
        "untuk membantu memilih alternatif terbaik ketika SAW, WP, dan TOPSIS tidak sepakat."
    )

    display_cols = [
        nama_col,
        "SAW Score", "SAW Rank",
        "WP Score", "WP Rank",
        "TOPSIS Score", "TOPSIS Rank",
        "Borda Avg Rank", "Konsensus Rank",
    ]
    display_cols = [c for c in display_cols if c in results_df.columns]

    show_all = st.checkbox("Tampilkan semua baris", value=False)
    display_df = results_df[display_cols].sort_values("Konsensus Rank")
    st.dataframe(
        display_df if show_all else display_df.head(20),
        use_container_width=True,
        hide_index=True,
    )
    if not show_all and len(display_df) > 20:
        st.caption(f"Menampilkan 20 dari {len(display_df)} baris. Centang 'Tampilkan semua baris' untuk melihat seluruh data.")

    # CSV export
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Unduh Hasil sebagai CSV",
        data=csv_data,
        file_name="hasil_dss.csv",
        mime="text/csv",
    )

    # Bar chart — top 10 by consensus
    st.markdown("#### Grafik Perbandingan 10 Alternatif Teratas (Konsensus Borda)")
    top_10 = results_df.sort_values("Konsensus Rank").head(10)
    melted_df = top_10.melt(
        id_vars=[nama_col],
        value_vars=["SAW Score", "WP Score", "TOPSIS Score"],
        var_name="Metode",
        value_name="Skor",
    )
    fig_compare = px.bar(
        melted_df,
        x=nama_col,
        y="Skor",
        color="Metode",
        barmode="group",
        title="Skor Alternatif Teratas Berdasarkan Metode",
        template="plotly_dark",
    )
    fig_compare.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fafafa"),
    )
    st.plotly_chart(fig_compare, use_container_width=True)

# ── Tab 2: Step-by-step ───────────────────────────────────────────────────────
with tab_steps:
    st.markdown("#### Transparansi Langkah Perhitungan")
    st.markdown("Lihat hasil perhitungan dari masing-masing metode di bawah ini:")

    method_choice = st.radio("Pilih Metode untuk Detail Langkah:", ["TOPSIS", "SAW", "WP"], horizontal=True)
    show_all_steps = st.checkbox("Tampilkan semua baris matriks", value=False, key="steps_show_all")
    _n = None if show_all_steps else 10

    if method_choice == "TOPSIS":
        st.markdown("##### 1. Matriks Ternormalisasi Vektor (R)")
        st.dataframe(steps["topsis"]["norm_matrix"].head(_n), use_container_width=True)

        st.markdown("##### 2. Matriks Ternormalisasi Terbobot (V)")
        st.dataframe(steps["topsis"]["weighted_matrix"].head(_n), use_container_width=True)

        st.markdown("##### 3. Solusi Ideal Positif ($A^+$) & Negatif ($A^-$)")
        ideal_df = pd.DataFrame(
            [steps["topsis"]["ideal_positive"], steps["topsis"]["ideal_negative"]],
            columns=kriteria_cols,
            index=["Solusi Ideal Positif (A+)", "Solusi Ideal Negatif (A-)"],
        )
        st.dataframe(ideal_df, use_container_width=True)

        st.markdown("##### 4. Jarak Euclidean & Nilai Preferensi Akhir")
        topsis_summary = (
            results_df[[nama_col, "TOPSIS Score", "TOPSIS Rank", "D_plus", "D_minus"]]
            .rename(columns={
                "D_plus": "Jarak ke A+ (D+)",
                "D_minus": "Jarak ke A- (D-)",
                "TOPSIS Score": "Nilai Closeness (C)",
            })
            .sort_values("TOPSIS Rank")
        )
        st.dataframe(topsis_summary.head(_n), use_container_width=True, hide_index=True)

    elif method_choice == "SAW":
        st.markdown("##### 1. Matriks Ternormalisasi Skalar (R)")
        st.dataframe(steps["saw"]["norm_matrix"].head(_n), use_container_width=True)

        st.markdown("##### 2. Matriks Ternormalisasi Terbobot")
        st.dataframe(steps["saw"]["weighted_matrix"].head(_n), use_container_width=True)

    elif method_choice == "WP":
        st.markdown("##### 1. Matriks Pangkat Nilai Kriteria ($X_{ij}^{W_j}$)")
        st.dataframe(steps["wp"]["s_components"].head(_n), use_container_width=True)

        st.markdown("##### 2. Vektor S dan Vektor V (Skor Akhir)")
        wp_summary = results_df[[nama_col, "WP Score", "WP Rank"]].copy()
        wp_summary["Vector S"] = steps["wp"]["S_vector"]
        st.dataframe(wp_summary.sort_values("WP Rank").head(_n), use_container_width=True, hide_index=True)

# ── Tab 3: Sensitivity ────────────────────────────────────────────────────────
with tab_sensitivity:
    st.markdown("#### Analisis Sensitivitas Bobot Kriteria")
    st.markdown(
        "Analisis sensitivitas mengevaluasi seberapa sensitif ranking keputusan "
        "terhadap perubahan bobot kriteria tertentu. Jika perubahan bobot minor mengubah ranking teratas "
        "secara drastis, keputusan tersebut dinilai sensitif/tidak stabil."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        target_criterion = st.selectbox("Pilih Kriteria yang Ingin Diuji:", options=kriteria_cols)
    with col2:
        sensitivity_method = st.selectbox("Pilih Metode DSS:", options=["topsis", "saw", "wp"])
    with col3:
        sens_range_pct = st.slider(
            "Rentang Perubahan Bobot (±%)",
            min_value=10, max_value=50, value=20, step=10,
        )

    # Build steps list from the chosen range
    r = sens_range_pct / 100
    sens_steps = [-r, -r / 2, 0.0, r / 2, r]

    sens_df = run_sensitivity_analysis(
        df,
        kriteria_cols,
        weights,
        types,
        nama_col,
        target_criterion=target_criterion,
        method=sensitivity_method,
        steps=sens_steps,
    )

    # Use the stable numeric column to find the baseline top-5
    original_top_5 = (
        sens_df[sens_df["weight_change_pct"] == 0.0]
        .sort_values("Rank")["Alternatif"]
        .head(5)
        .tolist()
    )
    filtered_sens_df = sens_df[sens_df["Alternatif"].isin(original_top_5)]

    fig_sens = px.line(
        filtered_sens_df,
        x="Weight Change %",
        y="Score",
        color="Alternatif",
        hover_data=["Rank", "New Weight"],
        title=f"Sensitivitas Skor 5 Alternatif Teratas — Bobot {target_criterion} (±{sens_range_pct}%)",
        markers=True,
        template="plotly_dark",
    )
    fig_sens.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fafafa"),
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("##### Tabel Perubahan Peringkat")
    pivot = filtered_sens_df.pivot(index="Alternatif", columns="Weight Change %", values="Rank")
    st.dataframe(pivot, use_container_width=True)

# ── Tab 4: Rank Correlation ───────────────────────────────────────────────────
with tab_rank_corr:
    import numpy as np
    import plotly.express as px

    st.markdown("#### Korelasi Peringkat Spearman Antar Metode DSS")
    st.markdown(
        "Mengukur seberapa konsisten SAW, WP, dan TOPSIS dalam menghasilkan urutan yang sama. "
        "Nilai mendekati 1.0 berarti kedua metode sangat sepakat."
    )
    st.latex(r"r_s = 1 - \frac{6 \sum_{i=1}^{n} d_i^2}{n(n^2 - 1)}")

    saw_r = results_df["SAW Rank"].values
    wp_r = results_df["WP Rank"].values
    topsis_r = results_df["TOPSIS Rank"].values
    n_alts = len(saw_r)

    def spearman_corr(r1, r2):
        d2 = (r1.astype(float) - r2.astype(float)) ** 2
        return 1 - 6 * d2.sum() / (n_alts * (n_alts ** 2 - 1))

    rs_saw_wp = spearman_corr(saw_r, wp_r)
    rs_saw_topsis = spearman_corr(saw_r, topsis_r)
    rs_wp_topsis = spearman_corr(wp_r, topsis_r)
    avg_corr = (rs_saw_wp + rs_saw_topsis + rs_wp_topsis) / 3

    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    col_c1.metric("SAW vs WP", f"{rs_saw_wp:.4f}")
    col_c2.metric("SAW vs TOPSIS", f"{rs_saw_topsis:.4f}")
    col_c3.metric("WP vs TOPSIS", f"{rs_wp_topsis:.4f}")
    col_c4.metric("Rata-rata Korelasi", f"{avg_corr:.4f}")

    if avg_corr >= 0.9:
        st.success(f"✅ Rata-rata korelasi = {avg_corr:.4f} — Ketiga metode **sangat konsisten**. Konsensus Borda dapat dipercaya.")
    elif avg_corr >= 0.7:
        st.warning(f"⚠️ Rata-rata korelasi = {avg_corr:.4f} — Konsistensi **sedang**. Perhatikan perbedaan ranking antar metode.")
    else:
        st.error(f"❌ Rata-rata korelasi = {avg_corr:.4f} — Konsistensi **rendah**. Hasil ketiga metode berbeda signifikan.")

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

    # Scatter plot: SAW rank vs TOPSIS rank
    st.markdown("#### Scatter Plot Peringkat SAW vs TOPSIS")
    scatter_df = results_df[[nama_col, "SAW Rank", "WP Rank", "TOPSIS Rank"]].copy()
    fig_scatter = px.scatter(
        scatter_df, x="SAW Rank", y="TOPSIS Rank",
        hover_name=nama_col,
        title=f"Perbandingan Peringkat SAW vs TOPSIS (rₛ = {rs_saw_topsis:.4f})",
        template="plotly_dark",
        trendline="ols",
        trendline_color_override="#b388ff",
    )
    fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Rank difference table
    st.markdown("#### Tabel Selisih Peringkat (d_i)")
    diff_df = results_df[[nama_col, "SAW Rank", "WP Rank", "TOPSIS Rank", "Konsensus Rank"]].copy()
    diff_df["|SAW-WP|"] = (diff_df["SAW Rank"] - diff_df["WP Rank"]).abs()
    diff_df["|SAW-TOPSIS|"] = (diff_df["SAW Rank"] - diff_df["TOPSIS Rank"]).abs()
    diff_df["|WP-TOPSIS|"] = (diff_df["WP Rank"] - diff_df["TOPSIS Rank"]).abs()
    diff_df["Max Selisih"] = diff_df[["|SAW-WP|", "|SAW-TOPSIS|", "|WP-TOPSIS|"]].max(axis=1)
    diff_df = diff_df.sort_values("Konsensus Rank")
    st.dataframe(diff_df, use_container_width=True, hide_index=True)
