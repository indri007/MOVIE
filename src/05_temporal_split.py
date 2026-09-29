"""
05_temporal_split.py
====================
Step 5 — Temporal Validation & Split Engine
Pipeline: Instagram Indonesia Viral Intelligence & Research Platform

Audits dataset for temporal timestamps (e.g., created_at, post_timestamp, date).
Adheres strictly to the research rule:
- Checks actual dataset columns.
- If timestamp metadata is absent:
    Status: MISSING / PARTIAL
- Never invents synthetic or simulated dates.
- Documents exact data requirements needed for chronological walk-forward validation
  and forecasting toward 2027.
- Provides a transparent fallback train/test split (stratified by rating) while
  explicitly flagging that it is cross-sectional, NOT temporal.

Run:
    python src/05_temporal_split.py
    python -m src.05_temporal_split
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
INPUT_CSV = REPO / "output" / "features_engineered.csv"
FALLBACK_CSV = REPO / "output" / "topics_dataset.csv"
OUT_AUDIT_JSON = REPO / "output" / "temporal_split_audit.json"

POSSIBLE_DATE_COLS = [
    "timestamp", "created_at", "date", "post_date", "review_date",
    "published_at", "time", "datetime", "crawl_timestamp"
]


class TemporalSplitEngine:
    """Evaluates temporal availability and provides split strategies."""

    def __init__(self, data_path: Path | str | None = None) -> None:
        self.data_path = Path(data_path) if data_path else INPUT_CSV if INPUT_CSV.exists() else FALLBACK_CSV

    def audit_temporal_metadata(self, df: pd.DataFrame) -> dict[str, Any]:
        """Audits whether temporal columns are present in the dataset."""
        matched_cols = [c for c in df.columns if c.lower() in POSSIBLE_DATE_COLS]

        if not matched_cols:
            status = "MISSING"
            explanation = (
                "Dataset does NOT contain genuine post timestamps or date metadata. "
                "Per research guidelines, synthetic timestamps are strictly prohibited. "
                "Temporal split status is marked as MISSING."
            )
        else:
            status = "AVAILABLE"
            explanation = f"Temporal columns detected: {matched_cols}"

        return {
            "temporal_status": status,
            "detected_temporal_columns": matched_cols,
            "checked_candidate_columns": POSSIBLE_DATE_COLS,
            "explanation": explanation,
            "required_metadata_for_2027_forecasting": [
                "post_timestamp (ISO 8601 UTC timestamp)",
                "crawl_timestamp (Data ingestion time)",
                "account_creation_date (User tenure)",
                "engagement_delta_t (Time elapsed between post and metric snapshot)",
            ],
            "fallback_strategy": "Stratified cross-sectional split (preserving rating distribution)",
        }

    def execute_split(
        self,
        df: pd.DataFrame,
        target_col: str = "rating",
        test_size: float = 0.20,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
        """Performs stratified fallback split with comprehensive metadata."""
        audit = self.audit_temporal_metadata(df)

        if audit["temporal_status"] == "AVAILABLE":
            date_col = audit["detected_temporal_columns"][0]
            df_sorted = df.sort_values(by=date_col).reset_index(drop=True)
            split_idx = int(len(df_sorted) * (1 - test_size))
            train_df = df_sorted.iloc[:split_idx].copy()
            test_df = df_sorted.iloc[split_idx:].copy()
            split_type = "chronological_walk_forward"
        else:
            # Fallback cross-sectional split
            stratify_col = df[target_col] if target_col in df.columns and df[target_col].nunique() > 1 else None
            train_df, test_df = train_test_split(
                df,
                test_size=test_size,
                random_state=random_state,
                stratify=stratify_col
            )
            split_type = "stratified_cross_sectional_fallback"

        split_summary = {
            "split_type": split_type,
            "temporal_status": audit["temporal_status"],
            "total_records": len(df),
            "train_records": len(train_df),
            "test_records": len(test_df),
            "test_ratio": test_size,
            "target_distribution_train": (
                train_df[target_col].value_counts().sort_index().to_dict()
                if target_col in train_df.columns else {}
            ),
            "target_distribution_test": (
                test_df[target_col].value_counts().sort_index().to_dict()
                if target_col in test_df.columns else {}
            ),
        }
        return train_df, test_df, split_summary


def run(verbose: bool = True) -> dict[str, Any]:
    """Executes the temporal audit and fallback split validation."""
    if verbose:
        print("=" * 60)
        print("05_temporal_split.py | Temporal Split & Validation Audit")
        print("=" * 60)

    engine = TemporalSplitEngine()
    if not engine.data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {engine.data_path}")

    df = pd.read_csv(engine.data_path)
    audit = engine.audit_temporal_metadata(df)
    train_df, test_df, split_info = engine.execute_split(df)

    combined_report = {
        **audit,
        "split_execution": split_info,
    }

    if verbose:
        print(f"[STATUS]     Temporal Status: {audit['temporal_status']}")
        print(f"[EXPLAIN]    {audit['explanation']}")
        print(f"[SPLIT TYPE] {split_info['split_type']}")
        print(f"[SPLIT SIZE] Train: {split_info['train_records']:,} | Test: {split_info['test_records']:,}")
        print("\nTarget Distribution in Train Set:")
        for k, v in split_info["target_distribution_train"].items():
            print(f"  Rating {k}: {v:4d}")

    OUT_AUDIT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_AUDIT_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_report, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"\n[SAVE] Audit saved to {OUT_AUDIT_JSON.name}")
        print("✓ 05_temporal_split.py complete")

    return combined_report


if __name__ == "__main__":
    run(verbose=True)
