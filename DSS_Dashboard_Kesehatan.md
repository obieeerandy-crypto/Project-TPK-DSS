# 🏥 Panduan Lengkap: Dashboard DSS Diagnosis Penyakit Berbasis Gejala
> **Decision Support System · Streamlit · Python · Metode TOPSIS/AHP**

---

## 📋 Daftar Isi

1. [Gambaran Umum Proyek](#-1-gambaran-umum-proyek)
2. [Perancangan Dataset](#-2-perancangan-dataset)
3. [Struktur Folder Proyek](#-3-struktur-folder-proyek)
4. [Arsitektur Sistem & Alur Logika](#-4-arsitektur-sistem--alur-logika)
5. [Formula & Logika DSS (TOPSIS)](#-5-formula--logika-dss-topsis)
6. [Implementasi Kode Lengkap](#-6-implementasi-kode-lengkap)
   - [utils/dss_engine.py](#utidss_enginepy)
   - [utils/data_loader.py](#utilsdata_loaderpy)
   - [pages/1_Eksplorasi_Data.py](#pages1_eksplorasi_datapy)
   - [pages/2_Input_Parameter.py](#pages2_input_parameterpy)
   - [pages/3_Hasil_Rekomendasi.py](#pages3_hasil_rekomendasipy)
   - [app.py (Entry Point)](#apppy-entry-point)
7. [Dataset Contoh (CSV)](#-7-dataset-contoh-csv)
8. [Konfigurasi & Deployment](#-8-konfigurasi--deployment)
9. [Jadwal Eksekusi 3 Minggu](#-9-jadwal-eksekusi-3-minggu)
10. [Checklist Evaluasi Akhir](#-10-checklist-evaluasi-akhir)

---

## 🎯 1. Gambaran Umum Proyek

### Apa yang Dibangun?
Sebuah **Decision Support System (DSS)** berbasis web menggunakan Streamlit yang membantu dokter atau tenaga medis dalam **mendiagnosis kemungkinan penyakit** berdasarkan gejala yang diinputkan pasien, dengan menggunakan metode **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)**.

### Mengapa TOPSIS?
| Kriteria | TOPSIS | AHP | SAW |
|---|---|---|---|
| Kemampuan multi-kriteria | ✅ | ✅ | ✅ |
| Mempertimbangkan solusi ideal positif & negatif | ✅ | ❌ | ❌ |
| Mudah diimplementasi di Python | ✅ | ⚠️ | ✅ |
| Cocok untuk data numerik gejala medis | ✅ | ⚠️ | ✅ |
| Transparansi hasil untuk pengguna awam | ✅ | ❌ | ✅ |

> **Catatan peningkatan:** Proyek ini menggunakan **TOPSIS** sebagai metode utama (bukan sekadar "TPK" generik) karena lebih cocok untuk perbandingan diagnosis medis dengan banyak gejala sebagai kriteria. Bobot kriteria dapat disesuaikan secara interaktif oleh pengguna.

### Stack Teknologi
```
Python 3.10+
├── streamlit>=1.35.0        # Framework UI
├── pandas>=2.0.0            # Manipulasi data
├── numpy>=1.26.0            # Komputasi matriks TOPSIS
├── plotly>=5.18.0           # ⭐ Grafik interaktif (upgrade dari bawaan Streamlit)
└── scikit-learn>=1.4.0      # Normalisasi data (opsional)
```

> **Peningkatan:** Menggunakan **Plotly** alih-alih `st.bar_chart` bawaan agar grafik horizontal bisa diurutkan, diberi label skor, dan lebih informatif untuk presentasi.

---

## 🗄️ 2. Perancangan Dataset

### Skema Dataset (`data/dataset_penyakit.csv`)
Dataset merepresentasikan **matriks keputusan**: setiap baris adalah satu alternatif (penyakit), setiap kolom adalah satu kriteria (gejala/indikator klinis).

| Kolom | Tipe | Deskripsi | Rentang |
|---|---|---|---|
| `id_penyakit` | string | Kode unik penyakit | P001–P010 |
| `nama_penyakit` | string | Nama diagnosis | - |
| `demam` | float | Intensitas demam | 0–10 |
| `batuk` | float | Intensitas batuk | 0–10 |
| `sesak_napas` | float | Tingkat sesak napas | 0–10 |
| `nyeri_kepala` | float | Intensitas nyeri kepala | 0–10 |
| `mual` | float | Tingkat mual | 0–10 |
| `kelelahan` | float | Tingkat kelelahan | 0–10 |
| `nyeri_sendi` | float | Intensitas nyeri sendi | 0–10 |
| `ruam_kulit` | float | Ada/tingkat ruam | 0–10 |
| `kategori` | string | Kelompok penyakit | Infeksi/Kronik/dll |

### Aturan Skoring Gejala
- **0** = Gejala tidak ada / tidak relevan untuk penyakit ini
- **1–3** = Gejala ringan / kadang muncul
- **4–6** = Gejala sedang / sering muncul
- **7–10** = Gejala berat / selalu muncul / sangat khas

---

## 📁 3. Struktur Folder Proyek

```
dss-diagnosis-penyakit/
│
├── app.py                          # 🚀 Entry point utama
├── requirements.txt                # Daftar dependencies
├── .streamlit/
│   └── config.toml                 # Konfigurasi tema Streamlit
│
├── data/
│   ├── dataset_penyakit.csv        # Dataset utama (10 penyakit, 8 gejala)
│   └── deskripsi_penyakit.json     # Penjelasan singkat tiap penyakit
│
├── utils/
│   ├── __init__.py
│   ├── dss_engine.py               # ⚙️ Logika TOPSIS murni
│   └── data_loader.py              # Fungsi load & validasi data
│
└── pages/
    ├── 1_Eksplorasi_Data.py        # Halaman 1
    ├── 2_Input_Parameter.py        # Halaman 2
    └── 3_Hasil_Rekomendasi.py      # Halaman 3
```

---

## 🗺️ 4. Arsitektur Sistem & Alur Logika

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP                            │
│                                                             │
│  ┌──────────────┐    ┌─────────────────────────────────┐   │
│  │   SIDEBAR    │    │         MAIN CONTENT             │   │
│  │              │    │                                  │   │
│  │ 🏠 Beranda   │───▶│  Halaman 1: Eksplorasi Data      │   │
│  │              │    │  • Deskripsi masalah medis       │   │
│  │ 📊 Eksplorasi│    │  • Tabel dataset interaktif      │   │
│  │   Data       │    │  • Grafik distribusi gejala      │   │
│  │              │    │  • Grafik heatmap korelasi ⭐    │   │
│  │ ⚙️ Parameter │───▶│                                  │   │
│  │   & Bobot    │    │  Halaman 2: Input Parameter      │   │
│  │              │    │  • Slider gejala pasien          │   │
│  │ 🎯 Hasil &   │    │  • Slider bobot kepentingan      │   │
│  │   Rekomen-   │    │  • Selectbox skenario            │   │
│  │   dasi       │───▶│  • Preview input real-time ⭐   │   │
│  │              │    │                                  │   │
│  │ ℹ️ Tentang   │    │  Halaman 3: Hasil & Rekomendasi  │   │
│  │   Sistem     │    │  • Metric kartu diagnosis        │   │
│  └──────────────┘    │  • Ranking diagram interaktif    │   │
│                      │  • Detail skor TOPSIS            │   │
│                      │  • Tabel perbandingan lengkap ⭐ │   │
│                      └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   utils/        │
                    │  dss_engine.py  │
                    │                 │
                    │ 1. Normalisasi  │
                    │    Matriks      │
                    │ 2. Bobot ×      │
                    │    Normalisasi  │
                    │ 3. Solusi Ideal │
                    │    + dan -      │
                    │ 4. Jarak D+/D-  │
                    │ 5. Skor TOPSIS  │
                    │    Ci = D-/     │
                    │       (D++D-)   │
                    └─────────────────┘
```

### Alur Data Antar Halaman
```
Session State (st.session_state)
├── gejala_pasien: dict      # Input dari Halaman 2
├── bobot_kriteria: dict     # Bobot dari Halaman 2
├── skenario: str            # Skenario dari Halaman 2
└── hasil_topsis: DataFrame  # Output dari dss_engine, dibaca Halaman 3
```

---

## 📐 5. Formula & Logika DSS (TOPSIS)

### Langkah-langkah TOPSIS

**Step 1: Normalisasi Matriks Keputusan**

$$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}$$

**Step 2: Matriks Keputusan Terbobot**

$$v_{ij} = w_j \times r_{ij}$$

**Step 3: Solusi Ideal Positif (A+) dan Negatif (A-)**

$$A^+ = \{\max(v_{ij})\} \quad A^- = \{\min(v_{ij})\}$$

**Step 4: Jarak ke Solusi Ideal**

$$D_i^+ = \sqrt{\sum_{j=1}^{n}(v_{ij} - A_j^+)^2} \quad D_i^- = \sqrt{\sum_{j=1}^{n}(v_{ij} - A_j^-)^2}$$

**Step 5: Skor TOPSIS (Kedekatan Relatif)**

$$C_i = \frac{D_i^-}{D_i^+ + D_i^-}, \quad 0 \leq C_i \leq 1$$

> Semakin tinggi **Ci**, semakin dekat alternatif ke solusi ideal positif → **diagnosis lebih mungkin cocok**.

---

## 💻 6. Implementasi Kode Lengkap

### `utils/dss_engine.py`

```python
"""
DSS Engine: Implementasi TOPSIS untuk diagnosis penyakit.
Semua fungsi murni (pure functions) — tidak ada side effect.
"""

import numpy as np
import pandas as pd
from typing import Optional


def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Normalisasi matriks keputusan menggunakan metode Euclidean (vektor).
    
    Args:
        matrix: Array 2D (m alternatif × n kriteria)
    
    Returns:
        Matriks ternormalisasi dengan nilai 0–1
    """
    norm_factors = np.sqrt((matrix ** 2).sum(axis=0))
    # Hindari pembagian dengan nol
    norm_factors = np.where(norm_factors == 0, 1e-10, norm_factors)
    return matrix / norm_factors


def apply_weights(normalized_matrix: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Kalikan matriks ternormalisasi dengan bobot kriteria.
    
    Args:
        normalized_matrix: Hasil normalize_matrix()
        weights: Array bobot (harus berjumlah 1.0 setelah normalisasi internal)
    
    Returns:
        Matriks terbobot
    """
    # Normalisasi bobot agar total = 1
    weights_norm = weights / weights.sum()
    return normalized_matrix * weights_norm


def get_ideal_solutions(weighted_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Hitung solusi ideal positif (A+) dan negatif (A-).
    
    Catatan: Semua kriteria diasumsikan benefit (makin tinggi = makin baik).
    Untuk kriteria cost, ubah logika max/min di baris terkait.
    """
    ideal_positive = weighted_matrix.max(axis=0)   # A+: nilai tertinggi tiap kolom
    ideal_negative = weighted_matrix.min(axis=0)   # A-: nilai terendah tiap kolom
    return ideal_positive, ideal_negative


def calculate_distances(
    weighted_matrix: np.ndarray,
    ideal_positive: np.ndarray,
    ideal_negative: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Hitung jarak Euclidean tiap alternatif ke solusi ideal positif dan negatif.
    """
    d_plus = np.sqrt(((weighted_matrix - ideal_positive) ** 2).sum(axis=1))
    d_minus = np.sqrt(((weighted_matrix - ideal_negative) ** 2).sum(axis=1))
    return d_plus, d_minus


def calculate_topsis_score(d_plus: np.ndarray, d_minus: np.ndarray) -> np.ndarray:
    """
    Hitung skor TOPSIS (kedekatan relatif ke solusi ideal).
    Ci = D- / (D+ + D-), range [0, 1]
    """
    denominator = d_plus + d_minus
    denominator = np.where(denominator == 0, 1e-10, denominator)
    return d_minus / denominator


def run_topsis(
    decision_matrix: pd.DataFrame,
    weights: dict[str, float],
    kriteria_cols: list[str],
    nama_col: str = "nama_penyakit",
    scenario_multiplier: float = 1.0
) -> pd.DataFrame:
    """
    Fungsi utama: Jalankan TOPSIS end-to-end.
    
    Args:
        decision_matrix: DataFrame dengan kolom kriteria dan nama alternatif
        weights: Dict {nama_kriteria: nilai_bobot}
        kriteria_cols: List nama kolom yang menjadi kriteria
        nama_col: Nama kolom alternatif (penyakit)
        scenario_multiplier: Pengali untuk simulasi skenario (0.8=pesimis, 1.0=moderat, 1.2=optimis)
    
    Returns:
        DataFrame berisi ranking, nama penyakit, skor TOPSIS, D+, D-
    """
    # Ekstrak matriks numerik
    matrix = decision_matrix[kriteria_cols].values.astype(float)
    
    # Aplikasikan multiplier skenario
    matrix = matrix * scenario_multiplier
    
    # Ekstrak bobot sesuai urutan kriteria
    weight_array = np.array([weights.get(k, 1.0) for k in kriteria_cols])
    
    # Pipeline TOPSIS
    norm_matrix = normalize_matrix(matrix)
    weighted_matrix = apply_weights(norm_matrix, weight_array)
    ideal_pos, ideal_neg = get_ideal_solutions(weighted_matrix)
    d_plus, d_minus = calculate_distances(weighted_matrix, ideal_pos, ideal_neg)
    scores = calculate_topsis_score(d_plus, d_minus)
    
    # Susun hasil
    results = pd.DataFrame({
        "nama_penyakit": decision_matrix[nama_col].values,
        "skor_topsis": scores,
        "jarak_ideal_positif": d_plus,
        "jarak_ideal_negatif": d_minus,
    })
    
    # Urutkan dari skor tertinggi
    results = results.sort_values("skor_topsis", ascending=False).reset_index(drop=True)
    results.index += 1  # Ranking mulai dari 1
    results.index.name = "ranking"
    
    # Tambahkan kolom persentase kesesuaian
    results["kesesuaian_persen"] = (results["skor_topsis"] * 100).round(2)
    
    return results


def match_patient_to_dataset(
    gejala_pasien: dict[str, float],
    dataset: pd.DataFrame,
    kriteria_cols: list[str]
) -> pd.DataFrame:
    """
    ⭐ FITUR TAMBAHAN: Cocokkan gejala pasien dengan dataset penyakit.
    
    Menambahkan baris "Pasien" ke dalam matriks keputusan sehingga TOPSIS
    dapat menghitung penyakit mana yang paling mirip dengan profil gejala pasien.
    
    Strategy: Normalisasi jarak cosine antara vektor gejala pasien
    dan vektor gejala tiap penyakit dalam dataset.
    """
    patient_vector = np.array([gejala_pasien.get(k, 0.0) for k in kriteria_cols])
    
    similarities = []
    for _, row in dataset.iterrows():
        disease_vector = row[kriteria_cols].values.astype(float)
        
        # Cosine Similarity
        dot_product = np.dot(patient_vector, disease_vector)
        norm_patient = np.linalg.norm(patient_vector)
        norm_disease = np.linalg.norm(disease_vector)
        
        if norm_patient == 0 or norm_disease == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (norm_patient * norm_disease)
        
        similarities.append(similarity)
    
    result = dataset.copy()
    result["cosine_similarity"] = similarities
    result = result.sort_values("cosine_similarity", ascending=False).reset_index(drop=True)
    return result
```

---

### `utils/data_loader.py`

```python
"""
Utilitas untuk loading dan validasi dataset.
"""

import pandas as pd
import json
import streamlit as st
from pathlib import Path


KRITERIA_COLS = [
    "demam", "batuk", "sesak_napas", "nyeri_kepala",
    "mual", "kelelahan", "nyeri_sendi", "ruam_kulit"
]

LABEL_GEJALA = {
    "demam": "🌡️ Demam",
    "batuk": "😮‍💨 Batuk",
    "sesak_napas": "🫁 Sesak Napas",
    "nyeri_kepala": "🤕 Nyeri Kepala",
    "mual": "🤢 Mual / Muntah",
    "kelelahan": "😴 Kelelahan",
    "nyeri_sendi": "🦴 Nyeri Sendi",
    "ruam_kulit": "🔴 Ruam Kulit",
}

DEFAULT_WEIGHTS = {k: 1.0 for k in KRITERIA_COLS}

SCENARIO_CONFIG = {
    "Moderat (Standar)": {"multiplier": 1.0, "desc": "Evaluasi standar tanpa penyesuaian"},
    "Optimis (Gejala Ringan)": {"multiplier": 0.85, "desc": "Gejala lebih ringan dari yang dilaporkan"},
    "Pesimis (Gejala Berat)": {"multiplier": 1.15, "desc": "Gejala lebih berat, pertimbangkan diagnosis serius"},
}


@st.cache_data
def load_dataset(filepath: str = "data/dataset_penyakit.csv") -> pd.DataFrame:
    """Load dan cache dataset utama."""
    try:
        df = pd.read_csv(filepath)
        # Validasi kolom wajib
        required_cols = ["id_penyakit", "nama_penyakit"] + KRITERIA_COLS
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.error(f"Kolom tidak ditemukan: {missing}")
            return pd.DataFrame()
        return df
    except FileNotFoundError:
        st.error(f"File dataset tidak ditemukan: {filepath}")
        return pd.DataFrame()


@st.cache_data
def load_descriptions(filepath: str = "data/deskripsi_penyakit.json") -> dict:
    """Load deskripsi penyakit dari JSON."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

---

### `pages/1_Eksplorasi_Data.py`

```python
"""
Halaman 1: Eksplorasi Data & Deskripsi Masalah
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_dataset, KRITERIA_COLS, LABEL_GEJALA

# ─── Konfigurasi Halaman ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Eksplorasi Data | DSS Diagnosis",
    page_icon="🔬",
    layout="wide"
)

# ─── Header ───────────────────────────────────────────────────────────────
st.title("🔬 Eksplorasi Data Medis")
st.markdown("""
**Tujuan Pengambilan Keputusan:**  
Sistem ini membantu tenaga medis mengidentifikasi kemungkinan diagnosis penyakit
berdasarkan profil gejala pasien, menggunakan metode **TOPSIS** (Technique for 
Order of Preference by Similarity to Ideal Solution).

> ⚠️ **Disclaimer:** Sistem ini bersifat pendukung keputusan (*decision support*), 
> bukan pengganti diagnosis dokter. Hasil akhir tetap harus dikonfirmasi 
> oleh tenaga medis berpengalaman.
""")

st.divider()

# ─── Load Data ────────────────────────────────────────────────────────────
df = load_dataset()

if df.empty:
    st.error("Dataset tidak tersedia. Pastikan file `data/dataset_penyakit.csv` ada.")
    st.stop()

# ─── Section 1: Dataset ───────────────────────────────────────────────────
st.header("📋 Dataset Penyakit & Gejala")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyakit", len(df), help="Jumlah alternatif diagnosis")
with col2:
    st.metric("Jumlah Kriteria Gejala", len(KRITERIA_COLS), help="Jumlah parameter evaluasi")
with col3:
    st.metric("Kategori Penyakit", df["kategori"].nunique(), help="Kelompok jenis penyakit")

# Tampilkan dataframe dengan kolom yang di-rename
display_df = df.copy()
rename_map = {k: v for k, v in LABEL_GEJALA.items()}
display_df = display_df.rename(columns=rename_map)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "id_penyakit": st.column_config.TextColumn("ID", width="small"),
        "nama_penyakit": st.column_config.TextColumn("Nama Penyakit", width="medium"),
        "kategori": st.column_config.TextColumn("Kategori", width="small"),
    }
)

st.caption("💡 Klik header kolom untuk mengurutkan. Scroll horizontal untuk melihat semua gejala.")

st.divider()

# ─── Section 2: Visualisasi ───────────────────────────────────────────────
st.header("📊 Analisis Visual")

tab1, tab2, tab3 = st.tabs(["Profil Gejala per Penyakit", "Distribusi Gejala", "Heatmap Korelasi ⭐"])

with tab1:
    selected_disease = st.selectbox(
        "Pilih penyakit untuk melihat profil gejala:",
        options=df["nama_penyakit"].tolist()
    )
    
    disease_data = df[df["nama_penyakit"] == selected_disease][KRITERIA_COLS].iloc[0]
    
    fig = go.Figure(go.Bar(
        x=[LABEL_GEJALA[k] for k in KRITERIA_COLS],
        y=disease_data.values,
        marker_color=["#1e3a5f" if v >= 7 else "#2d6a9f" if v >= 4 else "#a8c8e8"
                      for v in disease_data.values],
        text=[f"{v:.0f}" for v in disease_data.values],
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Profil Gejala: {selected_disease}",
        yaxis_title="Intensitas (0–10)",
        yaxis_range=[0, 12],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        showlegend=False,
    )
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    avg_symptoms = df[KRITERIA_COLS].mean()
    
    fig2 = px.bar(
        x=[LABEL_GEJALA[k] for k in KRITERIA_COLS],
        y=avg_symptoms.values,
        labels={"x": "Gejala", "y": "Rata-rata Intensitas"},
        title="Rata-rata Intensitas Gejala di Seluruh Dataset",
        color=avg_symptoms.values,
        color_continuous_scale=["#a8c8e8", "#1e3a5f"],
    )
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    fig2.update_xaxes(tickangle=-30)
    st.plotly_chart(fig2, use_container_width=True)
    
    # ⭐ Box plot untuk distribusi per gejala
    df_melted = df[["nama_penyakit"] + KRITERIA_COLS].melt(
        id_vars="nama_penyakit",
        var_name="gejala",
        value_name="intensitas"
    )
    df_melted["gejala_label"] = df_melted["gejala"].map(LABEL_GEJALA)
    
    fig3 = px.box(
        df_melted,
        x="gejala_label",
        y="intensitas",
        title="Distribusi Intensitas Gejala (Box Plot)",
        color_discrete_sequence=["#1e3a5f"]
    )
    fig3.update_layout(
        xaxis_tickangle=-30,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    # ⭐ Heatmap korelasi antar gejala
    corr_matrix = df[KRITERIA_COLS].corr()
    labels = [LABEL_GEJALA[k] for k in KRITERIA_COLS]
    
    fig4 = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=labels,
        y=labels,
        colorscale=[[0, "#ffffff"], [0.5, "#6baed6"], [1, "#1e3a5f"]],
        zmin=-1, zmax=1,
        text=corr_matrix.values.round(2),
        texttemplate="%{text}",
        showscale=True,
    ))
    fig4.update_layout(
        title="Heatmap Korelasi Antar Gejala",
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("💡 Nilai mendekati 1 = dua gejala sering muncul bersamaan. Berguna untuk memahami pola penyakit.")
```

---

### `pages/2_Input_Parameter.py`

```python
"""
Halaman 2: Input Gejala Pasien & Bobot Kriteria (Mesin DSS)
"""

import streamlit as st
import plotly.graph_objects as go

from utils.data_loader import (
    load_dataset, KRITERIA_COLS, LABEL_GEJALA,
    DEFAULT_WEIGHTS, SCENARIO_CONFIG
)

st.set_page_config(
    page_title="Input Parameter | DSS Diagnosis",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Input Parameter Diagnostik")
st.markdown("Masukkan gejala pasien dan atur bobot kepentingan tiap gejala untuk mendapatkan rekomendasi diagnosis.")

st.divider()

# ─── Kolom Layout ────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    # ── Section 1: Gejala Pasien ──────────────────────────────────────────
    st.subheader("🩺 Gejala yang Dialami Pasien")
    st.caption("Geser slider sesuai tingkat keparahan gejala (0 = tidak ada, 10 = sangat parah)")
    
    gejala_pasien = {}
    
    # Tampilkan slider dalam 2 sub-kolom untuk efisiensi ruang
    c1, c2 = st.columns(2)
    cols = [c1, c2]
    
    for i, k in enumerate(KRITERIA_COLS):
        with cols[i % 2]:
            gejala_pasien[k] = st.slider(
                label=LABEL_GEJALA[k],
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.get(f"gejala_{k}", 0.0),
                step=0.5,
                key=f"gejala_{k}",
                help=f"Tingkat keparahan: {LABEL_GEJALA[k]}"
            )
    
    st.divider()
    
    # ── Section 2: Bobot Kriteria ─────────────────────────────────────────
    st.subheader("⚖️ Bobot Kepentingan Gejala")
    st.caption("Tentukan seberapa penting tiap gejala dalam proses diagnosis (1–9, skala AHP)")
    
    bobot = {}
    total_bobot = 0
    
    c3, c4 = st.columns(2)
    cols2 = [c3, c4]
    
    for i, k in enumerate(KRITERIA_COLS):
        with cols2[i % 2]:
            bobot[k] = st.slider(
                label=f"Bobot: {LABEL_GEJALA[k]}",
                min_value=1,
                max_value=9,
                value=st.session_state.get(f"bobot_{k}", 5),
                step=1,
                key=f"bobot_{k}",
                help="1=Sangat tidak penting, 9=Sangat penting"
            )
            total_bobot += bobot[k]
    
    # ⭐ Indikator total bobot
    bobot_persen = {k: round(v / total_bobot * 100, 1) for k, v in bobot.items()}
    st.info(f"**Total bobot:** {total_bobot} | **Distribusi:** otomatis dinormalisasi ke 100%")
    
    st.divider()
    
    # ── Section 3: Skenario ───────────────────────────────────────────────
    st.subheader("🎬 Skenario Evaluasi")
    skenario = st.selectbox(
        "Pilih skenario kondisi pasien:",
        options=list(SCENARIO_CONFIG.keys()),
        index=0,
        help="Skenario mempengaruhi bobot intensitas gejala secara keseluruhan"
    )
    st.caption(f"📌 {SCENARIO_CONFIG[skenario]['desc']}")

with col_right:
    # ── Preview Real-time ─────────────────────────────────────────────────
    st.subheader("👁️ Preview Profil Pasien (Real-time)")
    
    # Radar chart untuk profil gejala pasien
    categories = [LABEL_GEJALA[k] for k in KRITERIA_COLS]
    values = [gejala_pasien[k] for k in KRITERIA_COLS]
    values_closed = values + [values[0]]  # Tutup polygon
    categories_closed = categories + [categories[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(30, 58, 95, 0.2)",
        line_color="#1e3a5f",
        name="Profil Pasien"
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=9))
        ),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabel ringkasan
    summary_data = {
        "Gejala": [LABEL_GEJALA[k] for k in KRITERIA_COLS],
        "Intensitas": [f"{gejala_pasien[k]:.1f}/10" for k in KRITERIA_COLS],
        "Bobot (%)": [f"{bobot_persen[k]}%" for k in KRITERIA_COLS],
    }
    st.dataframe(summary_data, use_container_width=True, hide_index=True)
    
    # Highlight gejala dominan
    gejala_dominan = max(gejala_pasien, key=gejala_pasien.get)
    if gejala_pasien[gejala_dominan] > 0:
        st.success(f"**Gejala paling menonjol:** {LABEL_GEJALA[gejala_dominan]} ({gejala_pasien[gejala_dominan]:.1f}/10)")
    else:
        st.warning("⚠️ Belum ada gejala yang diinput.")

# ─── Tombol Proses ───────────────────────────────────────────────────────
st.divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🚀 Proses Diagnosis DSS", type="primary", use_container_width=True):
        # Validasi minimal ada 1 gejala
        if all(v == 0 for v in gejala_pasien.values()):
            st.error("❌ Masukkan minimal satu gejala sebelum memproses.")
        else:
            # Simpan ke session state
            st.session_state["gejala_pasien"] = gejala_pasien
            st.session_state["bobot_kriteria"] = bobot
            st.session_state["skenario"] = skenario
            st.session_state["data_ready"] = True
            st.success("✅ Parameter tersimpan! Buka halaman **Hasil & Rekomendasi** di sidebar.")
            st.balloons()
```

---

### `pages/3_Hasil_Rekomendasi.py`

```python
"""
Halaman 3: Hasil & Rekomendasi Keputusan
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils.data_loader import load_dataset, KRITERIA_COLS, LABEL_GEJALA, SCENARIO_CONFIG
from utils.dss_engine import run_topsis, match_patient_to_dataset

st.set_page_config(
    page_title="Hasil Diagnosis | DSS",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Hasil & Rekomendasi Diagnosis")

# ─── Cek Data ─────────────────────────────────────────────────────────────
if not st.session_state.get("data_ready", False):
    st.warning("⚠️ Belum ada data yang diproses. Silakan isi parameter di halaman **Input Parameter** terlebih dahulu.")
    st.page_link("pages/2_Input_Parameter.py", label="→ Ke Halaman Input Parameter", icon="⚙️")
    st.stop()

# ─── Ambil Data dari Session ──────────────────────────────────────────────
gejala_pasien = st.session_state["gejala_pasien"]
bobot_kriteria = st.session_state["bobot_kriteria"]
skenario = st.session_state["skenario"]
multiplier = SCENARIO_CONFIG[skenario]["multiplier"]

df = load_dataset()

# ─── Jalankan TOPSIS ──────────────────────────────────────────────────────
with st.spinner("Menghitung skor TOPSIS..."):
    hasil_topsis = run_topsis(
        decision_matrix=df,
        weights=bobot_kriteria,
        kriteria_cols=KRITERIA_COLS,
        scenario_multiplier=multiplier
    )
    
    # ⭐ Juga jalankan cosine similarity untuk rekomendasi berbasis gejala pasien
    hasil_cosine = match_patient_to_dataset(
        gejala_pasien=gejala_pasien,
        dataset=df,
        kriteria_cols=KRITERIA_COLS
    )

# ─── Section 1: HEADLINE DIAGNOSIS ───────────────────────────────────────
st.header("🏆 Rekomendasi Utama Sistem")

top_diagnosis = hasil_cosine.iloc[0]["nama_penyakit"]
top_similarity = hasil_cosine.iloc[0]["cosine_similarity"]
second_diagnosis = hasil_cosine.iloc[1]["nama_penyakit"]
second_similarity = hasil_cosine.iloc[1]["cosine_similarity"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="🥇 Diagnosis Teratas",
        value=top_diagnosis,
        delta=f"Kemiripan: {top_similarity:.1%}",
        help="Penyakit dengan profil gejala paling mirip pasien"
    )
with col2:
    st.metric(
        label="🥈 Alternatif Kedua",
        value=second_diagnosis,
        delta=f"Kemiripan: {second_similarity:.1%}",
    )
with col3:
    st.metric(
        label="📊 Skenario",
        value=skenario.split(" ")[0],
        help=SCENARIO_CONFIG[skenario]["desc"]
    )
with col4:
    confidence_level = "Tinggi" if top_similarity > 0.8 else "Sedang" if top_similarity > 0.5 else "Rendah"
    delta_color = "normal" if top_similarity > 0.5 else "inverse"
    st.metric(
        label="🎯 Tingkat Kepercayaan",
        value=confidence_level,
        delta=f"{top_similarity:.1%}",
    )

# ⭐ Card rekomendasi dengan styling
if top_similarity >= 0.75:
    st.success(f"""
    ✅ **Sistem merekomendasikan:** Kemungkinan besar pasien mengalami **{top_diagnosis}**  
    dengan tingkat kemiripan gejala **{top_similarity:.1%}**. 
    Pertimbangkan untuk melakukan pemeriksaan lanjutan terkait kondisi ini.
    """)
elif top_similarity >= 0.50:
    st.warning(f"""
    ⚠️ **Perhatian:** Gejala menunjukkan kemungkinan **{top_diagnosis}**, namun tingkat 
    kemiripan ({top_similarity:.1%}) masih moderat. Pertimbangkan juga alternatif **{second_diagnosis}**.
    Disarankan pemeriksaan laboratorium untuk konfirmasi.
    """)
else:
    st.error(f"""
    🔴 **Gejala tidak spesifik:** Tidak ada diagnosis yang cocok secara signifikan (kemiripan tertinggi: {top_similarity:.1%}).
    Diperlukan pemeriksaan lebih mendalam oleh dokter spesialis.
    """)

st.divider()

# ─── Section 2: RANKING VISUAL ───────────────────────────────────────────
st.header("📊 Peringkat Diagnosis Berdasarkan TOPSIS")

tab1, tab2, tab3 = st.tabs(["Grafik Ranking", "Tabel Detail", "Perbandingan Metode ⭐"])

with tab1:
    # Grafik horizontal bar — diurutkan, diberi label
    fig = go.Figure(go.Bar(
        x=hasil_topsis["skor_topsis"].values,
        y=hasil_topsis["nama_penyakit"].values,
        orientation="h",
        marker_color=[
            "#1e3a5f" if i == 0 else "#2d6a9f" if i == 1 else "#a8c8e8"
            for i in range(len(hasil_topsis))
        ],
        text=[f"{s:.3f}" for s in hasil_topsis["skor_topsis"].values],
        textposition="outside",
    ))
    fig.update_layout(
        title="Skor TOPSIS per Penyakit (lebih tinggi = lebih direkomendasikan)",
        xaxis_title="Skor TOPSIS (0–1)",
        xaxis_range=[0, 1.15],
        height=max(350, len(hasil_topsis) * 40),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    display_hasil = hasil_topsis.copy()
    display_hasil["skor_topsis"] = display_hasil["skor_topsis"].round(4)
    display_hasil["jarak_ideal_positif"] = display_hasil["jarak_ideal_positif"].round(4)
    display_hasil["jarak_ideal_negatif"] = display_hasil["jarak_ideal_negatif"].round(4)
    
    st.dataframe(
        display_hasil,
        use_container_width=True,
        column_config={
            "nama_penyakit": "Nama Penyakit",
            "skor_topsis": st.column_config.ProgressColumn(
                "Skor TOPSIS",
                min_value=0,
                max_value=1,
                format="%.4f",
            ),
            "kesesuaian_persen": st.column_config.NumberColumn(
                "Kesesuaian (%)",
                format="%.2f%%",
            ),
            "jarak_ideal_positif": "Jarak D+",
            "jarak_ideal_negatif": "Jarak D-",
        }
    )

with tab3:
    # ⭐ Perbandingan skor TOPSIS vs Cosine Similarity
    merged = hasil_topsis.merge(
        hasil_cosine[["nama_penyakit", "cosine_similarity"]],
        on="nama_penyakit"
    )
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="TOPSIS Score",
        x=merged["nama_penyakit"],
        y=merged["skor_topsis"],
        marker_color="#1e3a5f"
    ))
    fig2.add_trace(go.Bar(
        name="Cosine Similarity",
        x=merged["nama_penyakit"],
        y=merged["cosine_similarity"],
        marker_color="#2d9f6a"
    ))
    fig2.update_layout(
        barmode="group",
        title="Perbandingan: Skor TOPSIS vs Kemiripan Kosinus dengan Gejala Pasien",
        yaxis_title="Skor",
        xaxis_tickangle=-30,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.caption("""
    **TOPSIS Score:** Ranking berbasis bobot kriteria dan solusi ideal dari seluruh dataset.  
    **Cosine Similarity:** Kemiripan langsung antara profil gejala pasien dan tiap penyakit.  
    Kedua metode memberikan perspektif yang saling melengkapi.
    """)

st.divider()

# ─── Section 3: DETAIL GEJALA PASIEN ─────────────────────────────────────
with st.expander("🔍 Lihat Detail Input Gejala Pasien", expanded=False):
    gejala_df = pd.DataFrame({
        "Gejala": [LABEL_GEJALA[k] for k in KRITERIA_COLS],
        "Intensitas Pasien": [gejala_pasien[k] for k in KRITERIA_COLS],
        "Bobot Kriteria": [bobot_kriteria[k] for k in KRITERIA_COLS],
    })
    st.dataframe(gejala_df, use_container_width=True, hide_index=True)

# ─── Tombol Ekspor ────────────────────────────────────────────────────────
st.subheader("💾 Ekspor Hasil")
csv_export = hasil_topsis.to_csv(index=True).encode("utf-8")
st.download_button(
    label="⬇️ Unduh Hasil sebagai CSV",
    data=csv_export,
    file_name="hasil_diagnosis_dss.csv",
    mime="text/csv",
    help="Unduh tabel lengkap hasil diagnosis untuk dokumentasi"
)
```

---

### `app.py` (Entry Point)

```python
"""
Entry point aplikasi DSS Diagnosis Penyakit.
Berisi halaman beranda dan konfigurasi sidebar.
"""

import streamlit as st

st.set_page_config(
    page_title="DSS Diagnosis Penyakit",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "DSS Diagnosis Penyakit · Metode TOPSIS · Streamlit"
    }
)

# ─── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=DSS+Medis", use_column_width=True)
    st.markdown("### 🧭 Navigasi")
    st.markdown("""
    1. 🔬 **Eksplorasi Data** — Lihat dataset & grafik
    2. ⚙️ **Input Parameter** — Masukkan gejala & bobot
    3. 🎯 **Hasil Diagnosis** — Lihat rekomendasi
    """)
    
    st.divider()
    st.markdown("### ℹ️ Tentang Sistem")
    st.markdown("""
    **Metode:** TOPSIS + Cosine Similarity  
    **Dataset:** 10 penyakit, 8 kriteria gejala  
    **Versi:** 1.0.0  
    """)
    
    if st.session_state.get("data_ready"):
        st.success("✅ Data siap dianalisis")
    else:
        st.info("💡 Mulai dari halaman **Input Parameter**")

# ─── Halaman Beranda ──────────────────────────────────────────────────────
st.title("🏥 Dashboard DSS Diagnosis Penyakit")
st.markdown("""
### Sistem Pendukung Keputusan Medis

Selamat datang di **Dashboard Decision Support System** untuk membantu 
proses diagnosis penyakit berdasarkan gejala klinis pasien.

---

#### 🚀 Cara Penggunaan:

| Langkah | Halaman | Aksi |
|---------|---------|------|
| 1 | 🔬 Eksplorasi Data | Pahami dataset dan pola gejala |
| 2 | ⚙️ Input Parameter | Masukkan gejala pasien & bobot kepentingan |
| 3 | 🎯 Hasil Diagnosis | Lihat rekomendasi dan ranking diagnosis |

---

#### ⚠️ Disclaimer Penting

> Sistem ini merupakan **alat bantu keputusan** yang dirancang untuk mendukung,  
> bukan menggantikan, penilaian klinis tenaga medis profesional.  
> Selalu konfirmasi hasil dengan pemeriksaan fisik dan laboratorium.

---
""")

col1, col2 = st.columns(2)
with col1:
    st.info("""
    **📊 Metode Utama: TOPSIS**  
    Mengevaluasi semua alternatif diagnosis berdasarkan jarak ke solusi ideal 
    positif dan negatif, mempertimbangkan bobot tiap gejala.
    """)
with col2:
    st.info("""
    **🔍 Metode Pendukung: Cosine Similarity**  
    Mengukur kemiripan langsung antara profil gejala pasien dengan 
    profil gejala tiap penyakit dalam basis data.
    """)
```

---

## 📄 7. Dataset Contoh (CSV)

Simpan sebagai `data/dataset_penyakit.csv`:

```csv
id_penyakit,nama_penyakit,demam,batuk,sesak_napas,nyeri_kepala,mual,kelelahan,nyeri_sendi,ruam_kulit,kategori
P001,COVID-19,8,8,7,6,5,8,4,3,Infeksi Virus
P002,Influenza,8,7,4,8,5,8,6,2,Infeksi Virus
P003,DBD (Dengue),9,2,3,8,7,9,8,7,Infeksi Virus
P004,Malaria,9,2,4,8,8,9,7,2,Infeksi Parasit
P005,Pneumonia,7,8,9,5,4,7,2,1,Infeksi Bakteri
P006,TBC (Tuberkulosis),6,9,6,4,4,8,3,2,Infeksi Bakteri
P007,Tifoid (Typhus),8,3,2,7,8,8,5,3,Infeksi Bakteri
P008,Hepatitis A,7,2,2,6,9,8,4,4,Infeksi Virus
P009,Chikungunya,7,2,2,7,5,7,9,6,Infeksi Virus
P010,ISPA,5,8,5,6,3,5,2,2,Infeksi Saluran Napas
```

---

## ⚙️ 8. Konfigurasi & Deployment

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1e3a5f"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f4f8"
textColor = "#1a1a2e"
font = "sans serif"

[server]
maxUploadSize = 10
headless = true

[browser]
gatherUsageStats = false
```

### `requirements.txt`

```txt
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.18.0
scikit-learn>=1.4.0
```

### Langkah Deploy ke Streamlit Community Cloud

```bash
# 1. Push ke GitHub
git init
git add .
git commit -m "feat: initial DSS dashboard"
git remote add origin https://github.com/USERNAME/dss-diagnosis.git
git push -u origin main

# 2. Buka https://share.streamlit.io
# 3. Klik "New app" → Connect GitHub repo
# 4. Set:
#    - Repository: USERNAME/dss-diagnosis
#    - Branch: main  
#    - Main file path: app.py
# 5. Klik "Deploy" → tunggu ~2 menit → link siap dibagikan!
```

---

## 📅 9. Jadwal Eksekusi 3 Minggu

```
MINGGU 1: Fondasi Data & Logika
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hari 1–2  │ Riset & kumpulkan data penyakit-gejala
Hari 3    │ Bersihkan & format dataset_penyakit.csv
Hari 4–5  │ Tulis & uji fungsi di utils/dss_engine.py
Hari 6–7  │ Unit test: cek output TOPSIS di Jupyter Notebook

MINGGU 2: Pengembangan Streamlit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hari 8–9  │ Buat app.py + utils/data_loader.py
Hari 10   │ Bangun Halaman 1 (Eksplorasi Data)
Hari 11   │ Bangun Halaman 2 (Input Parameter + Radar Chart)
Hari 12   │ Bangun Halaman 3 (Hasil + Ranking + Ekspor)
Hari 13–14│ Integrasi: sambungkan session_state antar halaman

MINGGU 3: Finalisasi & Deployment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hari 15–16│ Uji berbagai kombinasi input & edge cases
Hari 17   │ Perbaiki teks penjelasan & tooltip
Hari 18   │ Tambahkan fitur ekspor CSV
Hari 19   │ Konfigurasi tema & rapikan tampilan
Hari 20   │ Deploy ke Streamlit Community Cloud
Hari 21   │ Final check & latihan presentasi
```

---

## ✅ 10. Checklist Evaluasi Akhir

### Fungsionalitas
- [ ] Dataset ter-load tanpa error
- [ ] Slider gejala mempengaruhi grafik radar real-time
- [ ] Normalisasi bobot otomatis berjalan benar (total ≠ 100, tapi dinormalisasi)
- [ ] Skenario (Optimis/Moderat/Pesimis) mengubah skor TOPSIS
- [ ] Ranking berubah saat bobot diubah (logika keputusan responsif)
- [ ] Tombol "Proses" menyimpan data ke session state
- [ ] Halaman 3 tidak error jika diakses tanpa proses Halaman 2 terlebih dahulu
- [ ] Fitur ekspor CSV berfungsi

### Kualitas Visual
- [ ] Tema warna konsisten (navy blue + white + abu-abu)
- [ ] Grafik Plotly interaktif (hover, zoom)
- [ ] Heatmap korelasi terbaca jelas
- [ ] Radar chart profil pasien update real-time
- [ ] `st.metric` terlihat jelas di bagian atas Halaman 3
- [ ] `st.success` / `st.warning` / `st.error` muncul sesuai kondisi

### Presentasi
- [ ] Disclaimer medis tertulis di Halaman 1 dan Halaman 3
- [ ] Penjelasan metode TOPSIS ada tapi tidak terlalu teknis
- [ ] Link deploy bisa diakses dari perangkat lain (uji di HP)
- [ ] Waktu loading < 3 detik untuk input rata-rata

---

> **💡 Tips Presentasi:**  
> Saat demo, gunakan skenario "Pesimis" dengan input demam 9, batuk 8, sesak napas 7 untuk memperlihatkan rekomendasi COVID-19 atau Pneumonia — ini yang paling dramatis dan mudah dipahami penguji.

---

*Dibuat untuk keperluan akademik · DSS Berbasis TOPSIS · Streamlit · Python*
