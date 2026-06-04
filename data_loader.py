"""
Data Loader: Utilities for uploading, parsing, caching, and preprocessing datasets.
Handles dynamic column detection and missing values imputation.
"""

import pandas as pd
import numpy as np
import streamlit as st


def load_csv(file_path: str) -> pd.DataFrame:
    """Loads a CSV from a file path into a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {str(e)}")
        return pd.DataFrame()


def auto_detect_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Auto-detects columns:
    1. Alternative candidates: object/category columns, or columns whose name
       contains id/nama/name/label keywords. Falls back to all columns only if
       nothing else is found.
    2. Criteria candidates: numerical columns (float/int) only.
    """
    if df.empty:
        return [], []

    # Criteria: strictly numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Alternative candidates: categorical/string columns first
    string_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Also prioritise columns whose name looks like an identifier
    id_like_cols = [
        col for col in df.columns
        if any(kw in col.lower() for kw in ["id", "nama", "name", "label", "alternatif", "alternative"])
    ]

    # Merge without duplicates, keeping priority order; do NOT fall back to all columns
    alternative_candidates = list(dict.fromkeys(id_like_cols + string_cols))

    # Last resort: if nothing found, expose all columns so the app doesn't break
    if not alternative_candidates:
        alternative_candidates = df.columns.tolist()

    return alternative_candidates, numerical_cols


def preprocess_dataset(
    df: pd.DataFrame,
    kriteria_cols: list[str],
    impute_method: str = "Mean"
) -> pd.DataFrame:
    """
    Cleans and prepares dataset:
    - Fills missing values (NaNs) in the selected criteria columns using Mean/Median/Zero.
    """
    clean_df = df.copy()
    
    for col in kriteria_cols:
        if col in clean_df.columns:
            # Coerce to numeric
            clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")
            
            # Impute missing values
            if clean_df[col].isnull().any():
                if impute_method == "Mean":
                    val = clean_df[col].mean()
                elif impute_method == "Median":
                    val = clean_df[col].median()
                else:
                    val = 0.0
                clean_df[col] = clean_df[col].fillna(val)
                
    return clean_df
