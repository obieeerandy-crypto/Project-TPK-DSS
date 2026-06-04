"""
DSS Engine: SAW, WP, and TOPSIS implementation for generic datasets.
Provides detailed intermediate calculation steps for education/transparency.
"""

import numpy as np
import pandas as pd

# ── Numeric stability constants ──────────────────────────────────────────────
EPSILON = 1e-10       # General zero-division guard
WP_MIN_VALUE = 1e-5   # Minimum value for WP to avoid log/power issues with ≤0


# ── Shared helper ─────────────────────────────────────────────────────────────
def _impute_criteria(df: pd.DataFrame, kriteria_cols: list[str]) -> pd.DataFrame:
    """
    Returns a copy of df with NaN values in kriteria_cols filled by column mean
    (falls back to 0.0 when the entire column is NaN).
    """
    working = df.copy()
    for col in kriteria_cols:
        working[col] = pd.to_numeric(working[col], errors="coerce")
        if working[col].isnull().any():
            mean_val = working[col].mean()
            working[col] = working[col].fillna(mean_val if pd.notnull(mean_val) else 0.0)
    return working


def run_saw(
    df: pd.DataFrame,
    kriteria_cols: list[str],
    weights: dict[str, float],
    types: dict[str, str],
    nama_col: str,
) -> tuple[pd.DataFrame, dict]:
    """
    Simple Additive Weighting (SAW) Method.
    Returns (results_df, steps_dict).
    """
    working_df = _impute_criteria(df, kriteria_cols)
    matrix = working_df[kriteria_cols].values.astype(float)

    # Normalize weights so they sum to 1
    w_sum = sum(weights.values()) or 1.0
    w_norm = np.array([weights[col] / w_sum for col in kriteria_cols])

    # Step 1: Normalization Matrix
    norm_matrix = np.zeros_like(matrix)
    for j, col in enumerate(kriteria_cols):
        col_data = matrix[:, j]
        if types.get(col, "benefit") == "benefit":
            col_max = col_data.max()
            norm_matrix[:, j] = col_data / col_max if col_max != 0 else 0
        else:
            col_min = col_data.min()
            safe_denom = np.where(col_data == 0, EPSILON, col_data)
            norm_matrix[:, j] = col_min / safe_denom

    # Step 2: Calculate scores
    scores = norm_matrix @ w_norm

    norm_df = pd.DataFrame(norm_matrix, columns=kriteria_cols, index=working_df.index)
    if nama_col not in norm_df.columns:
        norm_df.insert(0, nama_col, working_df[nama_col])

    weighted_matrix = norm_matrix * w_norm
    weighted_df = pd.DataFrame(weighted_matrix, columns=kriteria_cols, index=working_df.index)
    if nama_col not in weighted_df.columns:
        weighted_df.insert(0, nama_col, working_df[nama_col])

    steps = {
        "norm_matrix": norm_df,
        "weighted_matrix": weighted_df,
        "weights_used": {col: weights[col] / w_sum for col in kriteria_cols},
    }

    results = pd.DataFrame({nama_col: working_df[nama_col], "Score": scores})
    return results, steps


def run_wp(
    df: pd.DataFrame,
    kriteria_cols: list[str],
    weights: dict[str, float],
    types: dict[str, str],
    nama_col: str,
) -> tuple[pd.DataFrame, dict]:
    """
    Weighted Product (WP) Method.
    Returns (results_df, steps_dict).
    """
    working_df = _impute_criteria(df, kriteria_cols)
    matrix = working_df[kriteria_cols].values.astype(float)

    # Guard against zero/negative values
    matrix = np.where(matrix <= 0, WP_MIN_VALUE, matrix)

    w_sum = sum(weights.values()) or 1.0
    w_norm = np.array([weights[col] / w_sum for col in kriteria_cols])

    # Adjust sign: positive for benefit, negative for cost
    w_adjusted = np.array([
        w_norm[j] if types.get(col, "benefit") == "benefit" else -w_norm[j]
        for j, col in enumerate(kriteria_cols)
    ])

    # Step 1: S vector
    s_components = matrix ** w_adjusted          # shape (n_alt, n_crit)
    S = s_components.prod(axis=1)

    # Step 2: V vector (relative preference)
    S_sum = S.sum() or EPSILON
    V = S / S_sum

    s_components_df = pd.DataFrame(
        s_components,
        columns=[f"{col}^w" for col in kriteria_cols],
        index=working_df.index,
    )
    if nama_col not in s_components_df.columns:
        s_components_df.insert(0, nama_col, working_df[nama_col])
    s_components_df["S_Score"] = S

    steps = {"s_components": s_components_df, "S_vector": S, "V_vector": V}

    results = pd.DataFrame({nama_col: working_df[nama_col], "Score": V})
    return results, steps


def run_topsis(
    df: pd.DataFrame,
    kriteria_cols: list[str],
    weights: dict[str, float],
    types: dict[str, str],
    nama_col: str,
) -> tuple[pd.DataFrame, dict]:
    """
    Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS).
    Returns (results_df, steps_dict).
    """
    working_df = _impute_criteria(df, kriteria_cols)
    matrix = working_df[kriteria_cols].values.astype(float)

    w_sum = sum(weights.values()) or 1.0
    w_norm = np.array([weights[col] / w_sum for col in kriteria_cols])

    # Step 1: Vector normalization
    norm_factors = np.sqrt((matrix ** 2).sum(axis=0))
    norm_factors = np.where(norm_factors == 0, EPSILON, norm_factors)
    norm_matrix = matrix / norm_factors

    norm_df = pd.DataFrame(norm_matrix, columns=kriteria_cols, index=working_df.index)
    if nama_col not in norm_df.columns:
        norm_df.insert(0, nama_col, working_df[nama_col])

    # Step 2: Weighted matrix
    weighted_matrix = norm_matrix * w_norm
    weighted_df = pd.DataFrame(weighted_matrix, columns=kriteria_cols, index=working_df.index)
    if nama_col not in weighted_df.columns:
        weighted_df.insert(0, nama_col, working_df[nama_col])

    # Step 3: Ideal positive (A+) and negative (A-)
    ideal_positive = np.array([
        weighted_matrix[:, j].max() if types.get(col, "benefit") == "benefit"
        else weighted_matrix[:, j].min()
        for j, col in enumerate(kriteria_cols)
    ])
    ideal_negative = np.array([
        weighted_matrix[:, j].min() if types.get(col, "benefit") == "benefit"
        else weighted_matrix[:, j].max()
        for j, col in enumerate(kriteria_cols)
    ])

    # Step 4: Euclidean distances
    d_plus = np.sqrt(((weighted_matrix - ideal_positive) ** 2).sum(axis=1))
    d_minus = np.sqrt(((weighted_matrix - ideal_negative) ** 2).sum(axis=1))

    # Step 5: Closeness coefficient
    denom = np.where(d_plus + d_minus == 0, EPSILON, d_plus + d_minus)
    scores = d_minus / denom

    steps = {
        "norm_matrix": norm_df,
        "weighted_matrix": weighted_df,
        "ideal_positive": ideal_positive,
        "ideal_negative": ideal_negative,
        "d_plus": d_plus,
        "d_minus": d_minus,
    }

    results = pd.DataFrame({
        nama_col: working_df[nama_col],
        "Score": scores,
        "D_plus": d_plus,
        "D_minus": d_minus,
    })
    return results, steps


def run_all_methods(
    df: pd.DataFrame,
    kriteria_cols: list[str],
    weights: dict[str, float],
    types: dict[str, str],
    nama_col: str,
) -> tuple[pd.DataFrame, dict]:
    """Runs SAW, WP, and TOPSIS, and merges results into a single comparison DataFrame.
    Also computes a Borda consensus rank (average of the three method ranks).
    """
    saw_res, saw_steps = run_saw(df, kriteria_cols, weights, types, nama_col)
    wp_res, wp_steps = run_wp(df, kriteria_cols, weights, types, nama_col)
    topsis_res, topsis_steps = run_topsis(df, kriteria_cols, weights, types, nama_col)

    saw_res = saw_res.rename(columns={"Score": "SAW Score"})
    wp_res = wp_res.rename(columns={"Score": "WP Score"})
    topsis_res = topsis_res.rename(columns={"Score": "TOPSIS Score"})

    for col, frame in [("SAW Score", saw_res), ("WP Score", wp_res), ("TOPSIS Score", topsis_res)]:
        frame[col] = frame[col].fillna(0.0)

    saw_res["SAW Rank"] = saw_res["SAW Score"].rank(ascending=False, method="min").astype(int)
    wp_res["WP Rank"] = wp_res["WP Score"].rank(ascending=False, method="min").astype(int)
    topsis_res["TOPSIS Rank"] = topsis_res["TOPSIS Score"].rank(ascending=False, method="min").astype(int)

    merged = saw_res.merge(wp_res, on=nama_col).merge(
        topsis_res[[nama_col, "TOPSIS Score", "TOPSIS Rank", "D_plus", "D_minus"]],
        on=nama_col,
    )

    # Borda consensus: average rank across the three methods (lower = better)
    merged["Borda Avg Rank"] = (
        (merged["SAW Rank"] + merged["WP Rank"] + merged["TOPSIS Rank"]) / 3
    ).round(2)
    merged["Konsensus Rank"] = merged["Borda Avg Rank"].rank(method="min").astype(int)

    steps = {"saw": saw_steps, "wp": wp_steps, "topsis": topsis_steps}
    return merged, steps


def run_sensitivity_analysis(
    df: pd.DataFrame,
    kriteria_cols: list[str],
    weights: dict[str, float],
    types: dict[str, str],
    nama_col: str,
    target_criterion: str,
    method: str = "topsis",
    steps: list[float] | None = None,
) -> pd.DataFrame:
    """
    Analyzes how the ranking of the top alternatives changes when the weight of one
    criterion is varied by certain percentages (steps), keeping others constant.

    steps: list of fractional changes, e.g. [-0.2, -0.1, 0.0, 0.1, 0.2].
           Defaults to ±20 % in 10 % increments.
    The baseline (0 % change) row is tagged with weight_change_pct == 0 so callers
    can filter it reliably without relying on a formatted string.
    """
    if steps is None:
        steps = [-0.2, -0.1, 0.0, 0.1, 0.2]

    sensitivity_results = []
    base_weight = weights[target_criterion]

    for step in steps:
        new_w = max(0.0, base_weight * (1.0 + step))
        temp_weights = weights.copy()
        temp_weights[target_criterion] = new_w

        if method.lower() == "saw":
            res, _ = run_saw(df, kriteria_cols, temp_weights, types, nama_col)
        elif method.lower() == "wp":
            res, _ = run_wp(df, kriteria_cols, temp_weights, types, nama_col)
        else:
            res, _ = run_topsis(df, kriteria_cols, temp_weights, types, nama_col)

        res["Rank"] = res["Score"].rank(ascending=False, method="min").astype(int)

        for _, row in res.iterrows():
            sensitivity_results.append({
                "Alternatif": row[nama_col],
                "weight_change_pct": step,                      # numeric, stable for filtering
                "Weight Change %": f"{int(step * 100):+}%",    # display label
                "New Weight": round(new_w, 3),
                "Score": round(row["Score"], 4),
                "Rank": row["Rank"],
            })

    return pd.DataFrame(sensitivity_results)
