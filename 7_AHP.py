"""
AHP (Analytic Hierarchy Process) Page.
Pairwise comparison matrix input, consistency ratio check, and weight derivation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui_components import inject_custom_css, render_header

st.set_page_config(
    page_title="AHP - DSS Dashboard",
    page_icon="🔺",
    layout="wide"
)

inject_custom_css()
render_header(
    "🔺 AHP — Analytic Hierarchy Process",
    "Tentukan bobot kriteria melalui perbandingan berpasangan (pairwise comparison) dengan uji konsistensi."
)

# ── Saaty Scale Reference ──────────────────────────────────────────────────────
SAATY_SCALE = {
    1: "Sama pentingnya",
    2: "Di antara 1 dan 3",
    3: "Sedikit lebih penting",
    4: "Di antara 3 dan 5",
    5: "Lebih penting",
    6: "Di antara 5 dan 7",
    7: "Sangat lebih penting",
    8: "Di antara 7 dan 9",
    9: "Mutlak lebih penting",
}

# Random Index table (Saaty, 1980) — index by n (1-indexed, so RI[n] = RI for n criteria)
RI_TABLE = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

# ── Theory Expander ────────────────────────────────────────────────────────────
with st.expander("📚 Landasan Teori — AHP", expanded=False):
    st.markdown("""
    **AHP (Analytic Hierarchy Process)** dikembangkan oleh Thomas L. Saaty (1980).
    Metode ini menstrukturkan masalah keputusan kompleks menjadi hierarki, lalu menentukan
    bobot kriteria melalui **perbandingan berpasangan** menggunakan **Skala Saaty (1–9)**.
    """)

    st.markdown("#### Skala Perbandingan Saaty")
    saaty_df = pd.DataFrame(list(SAATY_SCALE.items()), columns=["Nilai", "Keterangan"])
    st.dataframe(saaty_df, use_container_width=True, hide_index=True)

    st.markdown("#### Langkah-langkah AHP")
    st.markdown("""
    1. **Bangun Matriks Perbandingan Berpasangan (A)**
    2. **Normalisasi Matriks** — bagi setiap elemen dengan jumlah kolomnya
    3. **Hitung Bobot Prioritas (w)** — rata-rata setiap baris dari matriks ternormalisasi
    4. **Hitung λ_max** — eigenvalue maksimum
    5. **Hitung Consistency Index (CI)**
    6. **Hitung Consistency Ratio (CR)** — jika CR ≤ 0.10, matriks konsisten
    """)

    st.markdown("#### Rumus Kunci")
    st.latex(r"\lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{(A \cdot w)_i}{w_i}")
    st.latex(r"CI = \frac{\lambda_{max} - n}{n - 1}")
    st.latex(r"CR = \frac{CI}{RI}")
    st.markdown("Di mana **RI** adalah Random Index dari tabel Saaty berdasarkan jumlah kriteria n.")

    st.markdown("#### Tabel Random Index (RI) Saaty")
    ri_df = pd.DataFrame({"n": list(RI_TABLE.keys()), "RI": list(RI_TABLE.values())})
    st.dataframe(ri_df.T, use_container_width=True)

# ── Setup ──────────────────────────────────────────────────────────────────────
st.markdown("### ⚙️ Konfigurasi Kriteria AHP")

use_from_dataset = st.checkbox(
    "Gunakan kriteria dari dataset yang sudah dikonfigurasi",
    value=True,
    help="Jika dicentang, kriteria diambil dari halaman Upload Data."
)

if use_from_dataset and st.session_state.get("kriteria_cols"):
    kriteria_cols = st.session_state["kriteria_cols"]
    st.info(f"Menggunakan {len(kriteria_cols)} kriteria dari dataset: **{', '.join(kriteria_cols)}**")
else:
    n_crit = st.number_input("Jumlah Kriteria", min_value=2, max_value=10, value=4, step=1)
    kriteria_cols = []
    cols_input = st.columns(min(int(n_crit), 5))
    for i in range(int(n_crit)):
        with cols_input[i % 5]:
            name = st.text_input(f"Kriteria {i+1}", value=f"C{i+1}", key=f"ahp_crit_{i}")
            kriteria_cols.append(name)

n = len(kriteria_cols)

# ── Pairwise Comparison Matrix Input ──────────────────────────────────────────
st.markdown("### 📊 Matriks Perbandingan Berpasangan")
st.markdown(
    "Isi nilai perbandingan **baris terhadap kolom** menggunakan Skala Saaty (1–9). "
    "Nilai diagonal otomatis = 1. Nilai di bawah diagonal = kebalikan (1/nilai)."
)
st.caption("💡 Contoh: Jika C1 **sedikit lebih penting** dari C2, isi sel (C1, C2) = 3")

# Build upper-triangle inputs
matrix = np.ones((n, n))

st.markdown("**Isi bagian segitiga atas (upper triangle):**")
for i in range(n):
    row_cols = st.columns(n)
    for j in range(n):
        if i == j:
            row_cols[j].markdown(
                f"<div style='text-align:center; padding:8px; color:#b388ff; font-weight:bold'>1</div>",
                unsafe_allow_html=True
            )
        elif j > i:
            val = row_cols[j].number_input(
                f"{kriteria_cols[i]} vs {kriteria_cols[j]}",
                min_value=1.0/9.0, max_value=9.0,
                value=1.0, step=0.5,
                format="%.2f",
                key=f"ahp_{i}_{j}",
                label_visibility="collapsed",
                help=f"Seberapa penting {kriteria_cols[i]} dibanding {kriteria_cols[j]}?"
            )
            matrix[i][j] = val
            matrix[j][i] = 1.0 / val
        else:
            row_cols[j].markdown(
                f"<div style='text-align:center; padding:8px; color:#666'>1/{matrix[j][i]:.2f}</div>",
                unsafe_allow_html=True
            )

# Show column labels
st.markdown("**Keterangan kolom (kiri→kanan):** " + " | ".join([f"**{c}**" for c in kriteria_cols]))

# ── Compute AHP ────────────────────────────────────────────────────────────────
if st.button("🔺 Hitung AHP & Uji Konsistensi"):
    # Step 1: Column sums
    col_sums = matrix.sum(axis=0)

    # Step 2: Normalize
    norm_matrix = matrix / col_sums

    # Step 3: Priority weights (row averages)
    weights = norm_matrix.mean(axis=1)

    # Step 4: Weighted sum vector
    weighted_sum = matrix @ weights

    # Step 5: Lambda max
    lambda_vec = weighted_sum / weights
    lambda_max = lambda_vec.mean()

    # Step 6: CI
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0

    # Step 7: CR
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0.0

    st.session_state["ahp_results"] = {
        "matrix": matrix,
        "col_sums": col_sums,
        "norm_matrix": norm_matrix,
        "weights": weights,
        "weighted_sum": weighted_sum,
        "lambda_vec": lambda_vec,
        "lambda_max": lambda_max,
        "ci": ci,
        "ri": ri,
        "cr": cr,
        "kriteria_cols": kriteria_cols,
        "n": n,
    }
    st.success("✅ Perhitungan AHP selesai!")

# ── Display Results ────────────────────────────────────────────────────────────
if "ahp_results" in st.session_state:
    res = st.session_state["ahp_results"]
    crits = res["kriteria_cols"]
    n_res = res["n"]

    st.markdown("---")
    st.markdown("### 📋 Hasil AHP")

    # Consistency check banner
    cr_val = res["cr"]
    if cr_val <= 0.10:
        st.success(f"✅ **Matriks KONSISTEN** — CR = {cr_val:.4f} ≤ 0.10. Bobot dapat diterima.")
    else:
        st.error(f"❌ **Matriks TIDAK KONSISTEN** — CR = {cr_val:.4f} > 0.10. Revisi perbandingan diperlukan.")

    # KPI row
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    col_k1.metric("λ_max", f"{res['lambda_max']:.4f}")
    col_k2.metric("CI (Consistency Index)", f"{res['ci']:.4f}")
    col_k3.metric("RI (Random Index)", f"{res['ri']:.2f}")
    col_k4.metric("CR (Consistency Ratio)", f"{cr_val:.4f}", delta="OK ✅" if cr_val <= 0.10 else "Revisi ❌")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Matriks & Normalisasi",
        "⚖️ Bobot Prioritas",
        "🔍 Uji Konsistensi Detail",
        "📈 Visualisasi Bobot"
    ])

    with tab1:
        st.markdown("#### Matriks Perbandingan Berpasangan (A)")
        mat_df = pd.DataFrame(res["matrix"], index=crits, columns=crits).round(4)
        st.dataframe(mat_df, use_container_width=True)

        st.markdown("#### Jumlah Kolom")
        colsum_df = pd.DataFrame([res["col_sums"].round(4)], columns=crits, index=["Jumlah Kolom"])
        st.dataframe(colsum_df, use_container_width=True)

        st.markdown("#### Matriks Ternormalisasi")
        norm_df = pd.DataFrame(res["norm_matrix"], index=crits, columns=crits).round(4)
        st.dataframe(norm_df, use_container_width=True)

    with tab2:
        st.markdown("#### Bobot Prioritas (Priority Weights)")
        st.markdown("Bobot diperoleh dari rata-rata setiap baris matriks ternormalisasi.")
        weight_df = pd.DataFrame({
            "Kriteria": crits,
            "Bobot (w)": res["weights"].round(4),
            "Bobot (%)": (res["weights"] * 100).round(2),
        }).sort_values("Bobot (w)", ascending=False)
        weight_df["Rank"] = range(1, len(weight_df) + 1)
        st.dataframe(weight_df, use_container_width=True, hide_index=True)

        # Option to apply weights to DSS
        if st.button("📥 Terapkan Bobot AHP ke Analisis DSS"):
            if st.session_state.get("kriteria_cols"):
                ahp_weights = {crits[i]: float(res["weights"][i]) for i in range(n_res)}
                # Only apply for criteria that exist in the current DSS config
                current_crits = st.session_state["kriteria_cols"]
                new_weights = {}
                for c in current_crits:
                    new_weights[c] = ahp_weights.get(c, 1.0)
                st.session_state["weights"] = new_weights
                st.success("✅ Bobot AHP berhasil diterapkan ke konfigurasi DSS! Jalankan ulang analisis di halaman Analisis DSS.")
            else:
                st.warning("Tidak ada dataset yang dikonfigurasi. Upload data terlebih dahulu.")

    with tab3:
        st.markdown("#### Detail Perhitungan Konsistensi")
        st.latex(r"\lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{(A \cdot w)_i}{w_i}")

        consistency_df = pd.DataFrame({
            "Kriteria": crits,
            "Bobot (w_i)": res["weights"].round(4),
            "Weighted Sum (Aw)_i": res["weighted_sum"].round(4),
            "λ_i = (Aw)_i / w_i": res["lambda_vec"].round(4),
        })
        st.dataframe(consistency_df, use_container_width=True, hide_index=True)

        st.markdown(f"""
        **Ringkasan:**
        - λ_max = {res['lambda_max']:.4f}
        - n = {n_res}
        - CI = (λ_max − n) / (n − 1) = ({res['lambda_max']:.4f} − {n_res}) / ({n_res} − 1) = **{res['ci']:.4f}**
        - RI (n={n_res}) = **{res['ri']}**
        - CR = CI / RI = {res['ci']:.4f} / {res['ri']} = **{cr_val:.4f}**
        - Kesimpulan: {"✅ Konsisten (CR ≤ 0.10)" if cr_val <= 0.10 else "❌ Tidak Konsisten (CR > 0.10) — revisi perbandingan"}
        """)

    with tab4:
        st.markdown("#### Grafik Bobot Prioritas Kriteria")
        weight_plot_df = pd.DataFrame({"Kriteria": crits, "Bobot": res["weights"]}).sort_values("Bobot", ascending=True)
        fig_bar = px.bar(
            weight_plot_df, x="Bobot", y="Kriteria", orientation="h",
            title="Bobot Prioritas AHP per Kriteria",
            template="plotly_dark",
            color="Bobot",
            color_continuous_scale="Purples",
            text=weight_plot_df["Bobot"].round(4),
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### Pie Chart Distribusi Bobot")
        fig_pie = px.pie(
            values=res["weights"],
            names=crits,
            title="Distribusi Bobot Prioritas AHP",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Purples_r,
        )
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#fafafa"))
        st.plotly_chart(fig_pie, use_container_width=True)
