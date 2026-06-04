"""
Keputusan di Bawah Risiko (Decision Under Risk).
Implements EMV, EOL, EVPI with payoff/probability table input.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui_components import inject_custom_css, render_header

st.set_page_config(
    page_title="Keputusan Risiko - DSS Dashboard",
    page_icon="🎯",
    layout="wide"
)

inject_custom_css()
render_header(
    "🎯 Keputusan di Bawah Risiko",
    "Analisis keputusan ketika probabilitas setiap kondisi alam diketahui — EMV, EOL, dan EVPI."
)

# ── Theory Expander ────────────────────────────────────────────────────────────
with st.expander("📚 Landasan Teori — Keputusan di Bawah Risiko", expanded=False):
    st.markdown("""
    Dalam kondisi **risiko (risk)**, probabilitas terjadinya setiap kondisi alam (*state of nature*)
    **diketahui** atau dapat diestimasi. Tiga konsep utama:

    | Konsep | Deskripsi |
    |---|---|
    | **EMV** (Expected Monetary Value) | Nilai harapan tertimbang dari setiap alternatif |
    | **EOL** (Expected Opportunity Loss) | Nilai harapan kerugian peluang (penyesalan) |
    | **EVPI** (Expected Value of Perfect Information) | Nilai maksimum yang layak dibayar untuk informasi sempurna |
    """)

    st.markdown("#### Rumus EMV")
    st.latex(r"EMV_i = \sum_{j=1}^{n} P(S_j) \cdot x_{ij}")
    st.markdown("Pilih alternatif dengan **EMV terbesar**.")

    st.markdown("#### Rumus EOL (Opportunity Loss)")
    st.latex(r"OL_{ij} = \max_k(x_{kj}) - x_{ij}")
    st.latex(r"EOL_i = \sum_{j=1}^{n} P(S_j) \cdot OL_{ij}")
    st.markdown("Pilih alternatif dengan **EOL terkecil**.")

    st.markdown("#### Rumus EVPI")
    st.latex(r"EVwPI = \sum_{j=1}^{n} P(S_j) \cdot \max_k(x_{kj})")
    st.latex(r"EVPI = EVwPI - \max_i(EMV_i)")
    st.markdown("""
    - **EVwPI** = Expected Value *with* Perfect Information
    - **EVPI** = nilai maksimum yang rasional untuk dibayar demi mendapatkan informasi sempurna
    - Hubungan: **EVPI = min(EOL)**
    """)

# ── Input Section ──────────────────────────────────────────────────────────────
st.markdown("### 📝 Input Tabel Payoff & Probabilitas")

col_setup1, col_setup2 = st.columns(2)
with col_setup1:
    n_alt = st.number_input("Jumlah Alternatif", min_value=2, max_value=10, value=3, step=1)
with col_setup2:
    n_state = st.number_input("Jumlah Kondisi Alam (State of Nature)", min_value=2, max_value=8, value=3, step=1)

st.markdown("#### Beri Nama Alternatif dan Kondisi Alam")
col_names1, col_names2 = st.columns(2)

with col_names1:
    alt_names = []
    for i in range(int(n_alt)):
        name = st.text_input(f"Nama Alternatif {i+1}", value=f"A{i+1}", key=f"risk_alt_{i}")
        alt_names.append(name)

with col_names2:
    state_names = []
    for j in range(int(n_state)):
        name = st.text_input(f"Nama Kondisi Alam {j+1}", value=f"S{j+1}", key=f"risk_state_{j}")
        state_names.append(name)

# ── Probability Input ──────────────────────────────────────────────────────────
st.markdown("#### Probabilitas Kondisi Alam")
st.caption("Total probabilitas harus = 1.0")

prob_cols = st.columns(int(n_state))
probs = []
for j in range(int(n_state)):
    default_p = round(1.0 / n_state, 4)
    p = prob_cols[j].number_input(
        f"P({state_names[j]})",
        min_value=0.0, max_value=1.0,
        value=default_p, step=0.01, format="%.4f",
        key=f"prob_{j}"
    )
    probs.append(p)

prob_sum = sum(probs)
if abs(prob_sum - 1.0) > 0.001:
    st.warning(f"⚠️ Total probabilitas = {prob_sum:.4f} (harus = 1.0). Sistem akan menormalisasi otomatis saat perhitungan.")
else:
    st.success(f"✅ Total probabilitas = {prob_sum:.4f}")

# ── Payoff Table Input ─────────────────────────────────────────────────────────
st.markdown("#### Isi Nilai Payoff")

default_data = {}
for j, sname in enumerate(state_names):
    default_data[sname] = [float((i + 1) * 20 - j * 8) for i in range(int(n_alt))]

default_df = pd.DataFrame(default_data, index=alt_names)
default_df.index.name = "Alternatif"

edited_df = st.data_editor(
    default_df,
    use_container_width=True,
    num_rows="fixed",
    key="risk_payoff_editor"
)

# ── Compute ────────────────────────────────────────────────────────────────────
if st.button("🎯 Hitung EMV, EOL, dan EVPI"):
    payoff = edited_df.values.astype(float)
    alts = edited_df.index.tolist()
    states = edited_df.columns.tolist()

    # Normalize probabilities
    p = np.array(probs, dtype=float)
    p_sum = p.sum()
    if p_sum > 0:
        p = p / p_sum

    # 1. EMV
    emv = payoff @ p

    # 2. Opportunity Loss matrix
    col_max = payoff.max(axis=0)
    ol_matrix = col_max - payoff

    # 3. EOL
    eol = ol_matrix @ p

    # 4. EVwPI
    evwpi = (col_max * p).sum()

    # 5. EVPI
    evpi = evwpi - emv.max()

    st.session_state["risk_results"] = {
        "payoff": payoff,
        "alts": alts,
        "states": states,
        "probs": p,
        "emv": emv,
        "ol_matrix": ol_matrix,
        "eol": eol,
        "evwpi": evwpi,
        "evpi": evpi,
        "col_max": col_max,
    }
    st.success("✅ Perhitungan selesai!")

# ── Display Results ────────────────────────────────────────────────────────────
if "risk_results" in st.session_state:
    res = st.session_state["risk_results"]
    alts = res["alts"]
    states = res["states"]
    p = res["probs"]

    st.markdown("---")
    st.markdown("### 🏆 Ringkasan Hasil")

    best_emv_idx = np.argmax(res["emv"])
    best_eol_idx = np.argmin(res["eol"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Alternatif Terbaik (EMV)", alts[best_emv_idx], f"EMV = {res['emv'][best_emv_idx]:.4f}")
    col2.metric("Alternatif Terbaik (EOL)", alts[best_eol_idx], f"EOL = {res['eol'][best_eol_idx]:.4f}")
    col3.metric("EVwPI", f"{res['evwpi']:.4f}", help="Expected Value with Perfect Information")
    col4.metric("EVPI", f"{res['evpi']:.4f}", help="Nilai maksimum yang layak dibayar untuk informasi sempurna")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Tabel Payoff",
        "💰 EMV",
        "📉 EOL",
        "🔮 EVPI",
        "📈 Visualisasi"
    ])

    with tab1:
        st.markdown("#### Tabel Payoff dengan Probabilitas")
        payoff_display = pd.DataFrame(res["payoff"], index=alts, columns=states)
        payoff_display.index.name = "Alternatif"

        prob_row = pd.DataFrame([p], columns=states, index=["Probabilitas P(Sj)"])
        st.markdown("**Probabilitas:**")
        st.dataframe(prob_row.round(4), use_container_width=True)
        st.markdown("**Tabel Payoff:**")
        st.dataframe(payoff_display, use_container_width=True)

    with tab2:
        st.markdown("#### EMV — Expected Monetary Value")
        st.latex(r"EMV_i = \sum_{j=1}^{n} P(S_j) \cdot x_{ij}")

        # Show calculation detail
        emv_detail = pd.DataFrame(res["payoff"], index=alts, columns=states)
        emv_detail.index.name = "Alternatif"
        for j, s in enumerate(states):
            emv_detail[f"×P({s})={p[j]:.3f}"] = (res["payoff"][:, j] * p[j]).round(4)

        emv_df = pd.DataFrame({
            "Alternatif": alts,
            "EMV": res["emv"].round(4),
        })
        emv_df["Rank"] = emv_df["EMV"].rank(ascending=False, method="min").astype(int)
        emv_df["Terpilih?"] = ["✅ TERPILIH" if i == best_emv_idx else "" for i in range(len(alts))]
        st.dataframe(emv_df, use_container_width=True, hide_index=True)

        st.markdown("**Detail Perhitungan (Payoff × Probabilitas):**")
        detail_rows = []
        for i, alt in enumerate(alts):
            row = {"Alternatif": alt}
            total = 0
            for j, s in enumerate(states):
                contrib = res["payoff"][i, j] * p[j]
                row[f"{s} ({p[j]:.3f})"] = f"{res['payoff'][i,j]:.2f} × {p[j]:.3f} = {contrib:.4f}"
                total += contrib
            row["EMV"] = round(total, 4)
            detail_rows.append(row)
        st.dataframe(pd.DataFrame(detail_rows), use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("#### EOL — Expected Opportunity Loss")
        st.latex(r"OL_{ij} = \max_k(x_{kj}) - x_{ij}")
        st.latex(r"EOL_i = \sum_{j=1}^{n} P(S_j) \cdot OL_{ij}")

        st.markdown("**Matriks Opportunity Loss (OL):**")
        ol_display = pd.DataFrame(res["ol_matrix"], index=alts, columns=states).round(4)
        ol_display.index.name = "Alternatif"
        st.dataframe(ol_display, use_container_width=True)

        eol_df = pd.DataFrame({
            "Alternatif": alts,
            "EOL": res["eol"].round(4),
        })
        eol_df["Rank"] = eol_df["EOL"].rank(ascending=True, method="min").astype(int)
        eol_df["Terpilih?"] = ["✅ TERPILIH" if i == best_eol_idx else "" for i in range(len(alts))]
        st.markdown("**Nilai EOL per Alternatif (pilih yang terkecil):**")
        st.dataframe(eol_df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("#### EVPI — Expected Value of Perfect Information")
        st.latex(r"EVwPI = \sum_{j=1}^{n} P(S_j) \cdot \max_k(x_{kj})")
        st.latex(r"EVPI = EVwPI - \max_i(EMV_i)")

        evwpi_detail = pd.DataFrame({
            "Kondisi Alam": states,
            "Probabilitas P(Sj)": p.round(4),
            "Payoff Terbaik max_k(x_kj)": res["col_max"].round(4),
            "Kontribusi P(Sj) × max": (p * res["col_max"]).round(4),
        })
        st.dataframe(evwpi_detail, use_container_width=True, hide_index=True)

        st.markdown(f"""
        **Ringkasan EVPI:**
        - EVwPI = Σ P(Sj) × max_k(x_kj) = **{res['evwpi']:.4f}**
        - max EMV = EMV({alts[best_emv_idx]}) = **{res['emv'][best_emv_idx]:.4f}**
        - **EVPI = {res['evwpi']:.4f} − {res['emv'][best_emv_idx]:.4f} = {res['evpi']:.4f}**

        > Interpretasi: Pengambil keputusan **tidak perlu membayar lebih dari {res['evpi']:.4f}**
        > untuk mendapatkan informasi sempurna tentang kondisi alam yang akan terjadi.

        > Verifikasi: EVPI = min(EOL) = **{res['eol'].min():.4f}** ✅
        """)

    with tab5:
        st.markdown("#### Visualisasi Perbandingan EMV")
        emv_plot = pd.DataFrame({"Alternatif": alts, "EMV": res["emv"]})
        fig_emv = px.bar(
            emv_plot, x="Alternatif", y="EMV",
            title="Perbandingan EMV Antar Alternatif",
            template="plotly_dark",
            color="EMV",
            color_continuous_scale="Purples",
            text=emv_plot["EMV"].round(3),
        )
        fig_emv.add_hline(
            y=res["evwpi"], line_dash="dash", line_color="#b388ff",
            annotation_text=f"EVwPI = {res['evwpi']:.3f}"
        )
        fig_emv.update_traces(textposition="outside")
        fig_emv.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
        st.plotly_chart(fig_emv, use_container_width=True)

        st.markdown("#### Perbandingan EMV vs EOL")
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(name="EMV", x=alts, y=res["emv"], marker_color="#8a2be2"))
        fig_dual.add_trace(go.Bar(name="EOL", x=alts, y=res["eol"], marker_color="#a5b4fc"))
        fig_dual.update_layout(
            barmode="group",
            title="EMV vs EOL per Alternatif",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#fafafa"),
        )
        st.plotly_chart(fig_dual, use_container_width=True)

        st.markdown("#### Distribusi Payoff per Kondisi Alam")
        payoff_melt = pd.DataFrame(res["payoff"], index=alts, columns=states).reset_index()
        payoff_melt = payoff_melt.melt(id_vars="Alternatif", var_name="Kondisi Alam", value_name="Payoff")
        fig_grouped = px.bar(
            payoff_melt, x="Kondisi Alam", y="Payoff", color="Alternatif",
            barmode="group",
            title="Payoff per Kondisi Alam",
            template="plotly_dark",
        )
        fig_grouped.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
        st.plotly_chart(fig_grouped, use_container_width=True)
