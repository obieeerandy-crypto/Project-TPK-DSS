"""
Keputusan di Bawah Ketidakpastian (Decision Under Uncertainty).
Implements Maximin, Maximax, Hurwicz, Laplace, and Minimax Regret criteria.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui_components import inject_custom_css, render_header

st.set_page_config(
    page_title="Keputusan Ketidakpastian - DSS Dashboard",
    page_icon="🎲",
    layout="wide"
)

inject_custom_css()
render_header(
    "🎲 Keputusan di Bawah Ketidakpastian",
    "Analisis keputusan ketika probabilitas kejadian tidak diketahui — Maximin, Maximax, Hurwicz, Laplace, Minimax Regret."
)

# ── Theory Expander ────────────────────────────────────────────────────────────
with st.expander("📚 Landasan Teori — Keputusan di Bawah Ketidakpastian", expanded=False):
    st.markdown("""
    Dalam kondisi **ketidakpastian (uncertainty)**, pengambil keputusan tidak mengetahui probabilitas
    terjadinya setiap kondisi alam (*state of nature*). Lima kriteria klasik digunakan:

    | Kriteria | Filosofi | Tipe Pengambil Keputusan |
    |---|---|---|
    | **Maximin** | Pilih alternatif dengan *payoff minimum terbesar* | Pesimis / Risk-averse |
    | **Maximax** | Pilih alternatif dengan *payoff maksimum terbesar* | Optimis / Risk-seeking |
    | **Hurwicz** | Kombinasi optimisme-pesimisme dengan koefisien α | Moderat |
    | **Laplace** | Asumsikan semua kondisi sama-sama mungkin (equal probability) | Netral |
    | **Minimax Regret** | Minimasi penyesalan (*opportunity loss*) terbesar | Penyesal |
    """)

    st.markdown("#### Rumus Hurwicz")
    st.latex(r"H_i = \alpha \cdot \max_j(x_{ij}) + (1 - \alpha) \cdot \min_j(x_{ij})")
    st.markdown("Di mana α ∈ [0,1] adalah koefisien optimisme. α=1 → Maximax; α=0 → Maximin.")

    st.markdown("#### Rumus Laplace")
    st.latex(r"\bar{x}_i = \frac{1}{n} \sum_{j=1}^{n} x_{ij}")

    st.markdown("#### Rumus Minimax Regret")
    st.latex(r"r_{ij} = \max_k(x_{kj}) - x_{ij}")
    st.markdown("Kemudian pilih alternatif dengan nilai **maksimum regret terkecil**.")

# ── Input Section ──────────────────────────────────────────────────────────────
st.markdown("### 📝 Input Tabel Payoff")
st.markdown(
    "Masukkan **tabel payoff** (nilai hasil/keuntungan) untuk setiap kombinasi alternatif dan kondisi alam. "
    "Nilai positif = keuntungan, nilai negatif = kerugian."
)

col_setup1, col_setup2 = st.columns(2)
with col_setup1:
    n_alt = st.number_input("Jumlah Alternatif (Keputusan)", min_value=2, max_value=10, value=3, step=1)
with col_setup2:
    n_state = st.number_input("Jumlah Kondisi Alam (State of Nature)", min_value=2, max_value=8, value=3, step=1)

st.markdown("#### Beri Nama Alternatif dan Kondisi Alam")
col_names1, col_names2 = st.columns(2)

with col_names1:
    alt_names = []
    for i in range(int(n_alt)):
        name = st.text_input(f"Nama Alternatif {i+1}", value=f"A{i+1}", key=f"alt_name_{i}")
        alt_names.append(name)

with col_names2:
    state_names = []
    for j in range(int(n_state)):
        name = st.text_input(f"Nama Kondisi Alam {j+1}", value=f"S{j+1}", key=f"state_name_{j}")
        state_names.append(name)

st.markdown("#### Isi Nilai Payoff")
st.caption("Isi setiap sel dengan nilai payoff (keuntungan/kerugian) untuk kombinasi alternatif × kondisi alam.")

# Build editable payoff table using st.data_editor
default_data = {}
for j, sname in enumerate(state_names):
    default_data[sname] = [float((i + 1) * 10 - j * 5) for i in range(int(n_alt))]

default_df = pd.DataFrame(default_data, index=alt_names)
default_df.index.name = "Alternatif"

edited_df = st.data_editor(
    default_df,
    use_container_width=True,
    num_rows="fixed",
    key="payoff_editor"
)

# ── Hurwicz alpha ──────────────────────────────────────────────────────────────
st.markdown("---")
alpha = st.slider(
    "Koefisien Optimisme Hurwicz (α)",
    min_value=0.0, max_value=1.0, value=0.5, step=0.05,
    help="α=1.0 → sangat optimis (Maximax); α=0.0 → sangat pesimis (Maximin)"
)

# ── Compute ────────────────────────────────────────────────────────────────────
if st.button("🔍 Hitung Semua Kriteria Ketidakpastian"):
    payoff = edited_df.values.astype(float)
    alts = edited_df.index.tolist()
    states = edited_df.columns.tolist()

    # 1. Maximin
    row_min = payoff.min(axis=1)
    maximin_idx = np.argmax(row_min)

    # 2. Maximax
    row_max = payoff.max(axis=1)
    maximax_idx = np.argmax(row_max)

    # 3. Hurwicz
    hurwicz = alpha * row_max + (1 - alpha) * row_min
    hurwicz_idx = np.argmax(hurwicz)

    # 4. Laplace
    laplace = payoff.mean(axis=1)
    laplace_idx = np.argmax(laplace)

    # 5. Minimax Regret
    col_max = payoff.max(axis=0)
    regret_matrix = col_max - payoff
    max_regret = regret_matrix.max(axis=1)
    minimax_idx = np.argmin(max_regret)

    # ── Store results ──────────────────────────────────────────────────────────
    st.session_state["uncertainty_results"] = {
        "payoff": payoff,
        "alts": alts,
        "states": states,
        "row_min": row_min,
        "row_max": row_max,
        "hurwicz": hurwicz,
        "laplace": laplace,
        "regret_matrix": regret_matrix,
        "max_regret": max_regret,
        "maximin_idx": maximin_idx,
        "maximax_idx": maximax_idx,
        "hurwicz_idx": hurwicz_idx,
        "laplace_idx": laplace_idx,
        "minimax_idx": minimax_idx,
        "alpha": alpha,
    }
    st.success("✅ Perhitungan selesai! Lihat hasil di bawah.")

# ── Display Results ────────────────────────────────────────────────────────────
if "uncertainty_results" in st.session_state:
    res = st.session_state["uncertainty_results"]
    alts = res["alts"]
    states = res["states"]
    payoff = res["payoff"]

    st.markdown("---")
    st.markdown("### 🏆 Ringkasan Keputusan Terbaik per Kriteria")

    col1, col2, col3, col4, col5 = st.columns(5)
    def winner_card(col, icon, label, alt_name, score):
        col.markdown(
            f"""<div class="kpi-card">
                <div style="font-size:1.5rem">{icon}</div>
                <div class="kpi-val" style="font-size:1.2rem">{alt_name}</div>
                <div class="kpi-label">{label}</div>
                <div style="color:#b388ff; font-size:0.9rem; margin-top:4px">Skor: {score:.3f}</div>
            </div>""",
            unsafe_allow_html=True
        )

    winner_card(col1, "🛡️", "Maximin (Pesimis)", alts[res["maximin_idx"]], res["row_min"][res["maximin_idx"]])
    winner_card(col2, "🚀", "Maximax (Optimis)", alts[res["maximax_idx"]], res["row_max"][res["maximax_idx"]])
    winner_card(col3, "⚖️", f"Hurwicz (α={res['alpha']})", alts[res["hurwicz_idx"]], res["hurwicz"][res["hurwicz_idx"]])
    winner_card(col4, "📊", "Laplace (Equal Prob)", alts[res["laplace_idx"]], res["laplace"][res["laplace_idx"]])
    winner_card(col5, "😌", "Minimax Regret", alts[res["minimax_idx"]], res["max_regret"][res["minimax_idx"]])

    # ── Tabs for detail ────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Tabel Payoff",
        "🛡️ Maximin & Maximax",
        "⚖️ Hurwicz",
        "📊 Laplace",
        "😌 Minimax Regret",
        "📈 Visualisasi"
    ])

    with tab1:
        st.markdown("#### Tabel Payoff Asli")
        payoff_display = pd.DataFrame(payoff, index=alts, columns=states)
        payoff_display.index.name = "Alternatif"
        st.dataframe(payoff_display.style.highlight_max(axis=0, color="#2d1b4e").highlight_min(axis=0, color="#1a2e1a"), use_container_width=True)

    with tab2:
        st.markdown("#### Maximin — Kriteria Pesimis")
        st.markdown("Pilih nilai minimum dari setiap baris, lalu ambil yang terbesar.")
        maximin_df = pd.DataFrame({
            "Alternatif": alts,
            "Min Payoff (Worst Case)": res["row_min"],
        })
        maximin_df["Terpilih?"] = ["✅ TERPILIH" if i == res["maximin_idx"] else "" for i in range(len(alts))]
        st.dataframe(maximin_df, use_container_width=True, hide_index=True)

        st.markdown("#### Maximax — Kriteria Optimis")
        st.markdown("Pilih nilai maksimum dari setiap baris, lalu ambil yang terbesar.")
        maximax_df = pd.DataFrame({
            "Alternatif": alts,
            "Max Payoff (Best Case)": res["row_max"],
        })
        maximax_df["Terpilih?"] = ["✅ TERPILIH" if i == res["maximax_idx"] else "" for i in range(len(alts))]
        st.dataframe(maximax_df, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown(f"#### Hurwicz — Koefisien Optimisme α = {res['alpha']}")
        st.latex(r"H_i = \alpha \cdot \max_j(x_{ij}) + (1 - \alpha) \cdot \min_j(x_{ij})")
        hurwicz_df = pd.DataFrame({
            "Alternatif": alts,
            "Max Payoff": res["row_max"],
            "Min Payoff": res["row_min"],
            f"Hurwicz (α={res['alpha']})": res["hurwicz"].round(4),
        })
        hurwicz_df["Terpilih?"] = ["✅ TERPILIH" if i == res["hurwicz_idx"] else "" for i in range(len(alts))]
        st.dataframe(hurwicz_df, use_container_width=True, hide_index=True)

        # Alpha sensitivity
        st.markdown("##### Sensitivitas Keputusan terhadap Nilai α")
        alpha_range = np.linspace(0, 1, 21)
        sens_data = []
        for a in alpha_range:
            h = a * res["row_max"] + (1 - a) * res["row_min"]
            for i, alt in enumerate(alts):
                sens_data.append({"α": round(a, 2), "Alternatif": alt, "Hurwicz Score": round(h[i], 4)})
        sens_df = pd.DataFrame(sens_data)
        fig_hurwicz = px.line(
            sens_df, x="α", y="Hurwicz Score", color="Alternatif",
            title="Perubahan Skor Hurwicz terhadap Koefisien Optimisme (α)",
            markers=True, template="plotly_dark"
        )
        fig_hurwicz.add_vline(x=res["alpha"], line_dash="dash", line_color="#b388ff",
                              annotation_text=f"α saat ini = {res['alpha']}")
        fig_hurwicz.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
        st.plotly_chart(fig_hurwicz, use_container_width=True)

    with tab4:
        st.markdown("#### Laplace — Prinsip Insufficient Reason")
        st.markdown("Asumsikan semua kondisi alam memiliki probabilitas yang sama: P(Sj) = 1/n")
        st.latex(r"\bar{x}_i = \frac{1}{n} \sum_{j=1}^{n} x_{ij}")
        laplace_df = pd.DataFrame({
            "Alternatif": alts,
            "Rata-rata Payoff (Laplace)": res["laplace"].round(4),
        })
        laplace_df["Terpilih?"] = ["✅ TERPILIH" if i == res["laplace_idx"] else "" for i in range(len(alts))]
        st.dataframe(laplace_df, use_container_width=True, hide_index=True)

    with tab5:
        st.markdown("#### Minimax Regret — Matriks Penyesalan (Opportunity Loss)")
        st.latex(r"r_{ij} = \max_k(x_{kj}) - x_{ij}")
        regret_display = pd.DataFrame(res["regret_matrix"], index=alts, columns=states)
        regret_display.index.name = "Alternatif"
        st.markdown("**Matriks Regret:**")
        st.dataframe(regret_display, use_container_width=True)

        minimax_df = pd.DataFrame({
            "Alternatif": alts,
            "Max Regret": res["max_regret"].round(4),
        })
        minimax_df["Terpilih?"] = ["✅ TERPILIH" if i == res["minimax_idx"] else "" for i in range(len(alts))]
        st.markdown("**Pilih alternatif dengan Max Regret terkecil:**")
        st.dataframe(minimax_df, use_container_width=True, hide_index=True)

    with tab6:
        st.markdown("#### Perbandingan Skor Semua Kriteria")

        # Normalize scores for comparison (min-max)
        def safe_norm(arr):
            mn, mx = arr.min(), arr.max()
            if mx == mn:
                return np.ones_like(arr) * 0.5
            return (arr - mn) / (mx - mn)

        # For minimax regret, lower is better — invert
        regret_norm = 1 - safe_norm(res["max_regret"])

        comparison_df = pd.DataFrame({
            "Alternatif": alts,
            "Maximin": safe_norm(res["row_min"]),
            "Maximax": safe_norm(res["row_max"]),
            f"Hurwicz(α={res['alpha']})": safe_norm(res["hurwicz"]),
            "Laplace": safe_norm(res["laplace"]),
            "Minimax Regret (inv)": regret_norm,
        })

        melted = comparison_df.melt(id_vars="Alternatif", var_name="Kriteria", value_name="Skor Ternormalisasi")
        fig_bar = px.bar(
            melted, x="Alternatif", y="Skor Ternormalisasi", color="Kriteria",
            barmode="group",
            title="Perbandingan Skor Ternormalisasi Semua Kriteria Ketidakpastian",
            template="plotly_dark"
        )
        fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
        st.plotly_chart(fig_bar, use_container_width=True)

        # Radar chart
        st.markdown("#### Radar Chart — Profil Alternatif")
        categories = ["Maximin", "Maximax", f"Hurwicz(α={res['alpha']})", "Laplace", "Minimax Regret (inv)"]
        fig_radar = go.Figure()
        for i, alt in enumerate(alts):
            vals = [
                safe_norm(res["row_min"])[i],
                safe_norm(res["row_max"])[i],
                safe_norm(res["hurwicz"])[i],
                safe_norm(res["laplace"])[i],
                regret_norm[i],
            ]
            vals_closed = vals + [vals[0]]
            cats_closed = categories + [categories[0]]
            fig_radar.add_trace(go.Scatterpolar(r=vals_closed, theta=cats_closed, fill="toself", name=alt))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#fafafa"),
            title="Radar Chart Profil Alternatif"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Summary table
        st.markdown("#### Tabel Rekap Keputusan")
        summary = pd.DataFrame({
            "Kriteria": ["Maximin", "Maximax", f"Hurwicz (α={res['alpha']})", "Laplace", "Minimax Regret"],
            "Filosofi": ["Pesimis", "Optimis", "Moderat", "Netral", "Penyesal"],
            "Alternatif Terpilih": [
                alts[res["maximin_idx"]],
                alts[res["maximax_idx"]],
                alts[res["hurwicz_idx"]],
                alts[res["laplace_idx"]],
                alts[res["minimax_idx"]],
            ],
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)
