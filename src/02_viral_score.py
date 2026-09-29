"""
02_viral_score.py
=================
Step 2 — Viral Intelligence & Viral Score Engine
Pipeline: Instagram Indonesia Viral Intelligence & Research Platform

Audits available viral engagement metrics and provides a formal formulation
for Instagram virality potential. Because the current dataset lacks
native interaction metrics (likes, shares, comments, saves, impressions),
the viral score status is explicitly flagged as PARTIAL.

No synthetic engagement figures are generated.

Run:
    python src/02_viral_score.py
    python -m src.02_viral_score
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
CLEAN_CSV = REPO / "output" / "clean_dataset.csv"
TOPICS_CSV = REPO / "output" / "topics_dataset.csv"
OUT_AUDIT_JSON = REPO / "output" / "viral_score_audit.json"

# ---------------------------------------------------------------------------
# Specifications for Instagram Viral Intelligence
# ---------------------------------------------------------------------------
REQUIRED_ENGAGEMENT_FEATURES = [
    "likes_count",
    "comments_count",
    "shares_count",
    "saves_count",
    "views_count",
    "impressions",
    "reach",
    "follower_count",
]

AVAILABLE_DATASET_FEATURES = [
    "username",
    "clean_text",
    "rating",
    "text_length",
    "token_count",
    "url_count",
    "mention_count",
    "hashtag_count",
    "emoji_count",
]


class ViralScoreEngine:
    """Engine for assessing and calculating Instagram Viral Potential.

    Enforces data integrity: If production engagement attributes are missing,
    the engine yields status 'PARTIAL' and documents data gap requirements.
    """

    def __init__(self, data_path: Path | str | None = None) -> None:
        self.data_path = Path(data_path) if data_path else TOPICS_CSV if TOPICS_CSV.exists() else CLEAN_CSV
        self.status = "PARTIAL"

    def audit_features(self, df: pd.DataFrame) -> dict[str, Any]:
        """Audits whether required viral engagement features exist in dataframe."""
        present_required = [f for f in REQUIRED_ENGAGEMENT_FEATURES if f in df.columns]
        missing_required = [f for f in REQUIRED_ENGAGEMENT_FEATURES if f not in df.columns]
        present_available = [f for f in AVAILABLE_DATASET_FEATURES if f in df.columns]

        is_complete = len(missing_required) == 0
        status = "AVAILABLE" if is_complete else "PARTIAL"

        return {
            "status": status,
            "total_records": len(df),
            "required_features_present": present_required,
            "required_features_missing": missing_required,
            "available_structural_features": present_available,
            "formula_definition": (
                "Ideal Viral Score (Normalized): "
                "VS = w1*(likes/reach) + w2*(shares/reach)*2.5 + "
                "w3*(saves/reach)*2.0 + w4*(comments/reach)*1.5 + w5*(velocity_decay)"
            ),
            "proxy_alternative": (
                "Content Virality Propensity Proxy (CVPP): "
                "Combines hashtag intensity, mention resonance, emoji richness, "
                "and sentiment polarity as structural content proxies."
            ),
            "data_limitation_notice": (
                "Native Instagram interaction counts (likes, comments, shares, saves, impressions) "
                "are NOT present in the current review dataset. Viral Score cannot be fully computed "
                "without genuine post-level engagement telemetry."
            ),
        }

    def compute_content_proxy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Computes a structural Content Virality Propensity Proxy (CVPP).

        NOTE: This is NOT a substitute for actual engagement figures. It strictly measures
        content structure signals (hashtag presence, mentions, emoji richness, text volume).
        """
        out = df.copy()

        # Safely extract structural signals
        text_len = out["text_length"].fillna(0).astype(float) if "text_length" in out.columns else out["clean_text"].astype(str).str.len()
        emojis = out["emoji_count"].fillna(0).astype(float) if "emoji_count" in out.columns else 0.0
        hashtags = out["hashtag_count"].fillna(0).astype(float) if "hashtag_count" in out.columns else 0.0
        mentions = out["mention_count"].fillna(0).astype(float) if "mention_count" in out.columns else 0.0

        # Normalize components between 0 and 1
        norm_len = np.clip(text_len / 500.0, 0, 1)
        norm_emoji = np.clip(emojis / 5.0, 0, 1)
        norm_hash = np.clip(hashtags / 10.0, 0, 1)
        norm_mention = np.clip(mentions / 5.0, 0, 1)

        # Weighted composite structural index (0.0 to 1.0)
        out["content_structural_index"] = (
            0.35 * norm_hash +
            0.25 * norm_mention +
            0.20 * norm_emoji +
            0.20 * norm_len
        ).round(4)

        out["viral_score_status"] = "PARTIAL"
        return out


def run(verbose: bool = True) -> dict[str, Any]:
    """Executes the Viral Score audit pipeline."""
    if verbose:
        print("=" * 60)
        print("02_viral_score.py | Viral Score Engine & Feature Audit")
        print("=" * 60)

    engine = ViralScoreEngine()
    if not engine.data_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {engine.data_path}")

    df = pd.read_csv(engine.data_path)
    audit = engine.audit_features(df)

    if verbose:
        print(f"[STATUS]   Viral Score Status: {audit['status']}")
        print(f"[RECORDS]  Evaluated {audit['total_records']:,} records")
        print(f"[MISSING]  Missing Engagement Metrics: {audit['required_features_missing']}")
        print(f"[AVAILABLE] Available Content Signals: {audit['available_structural_features']}")
        print("\n[FORMULATION] Ideal Formula:")
        print(f"  {audit['formula_definition']}")
        print("\n[LIMITATION] Notice:")
        print(f"  {audit['data_limitation_notice']}")

    # Save audit report
    OUT_AUDIT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_AUDIT_JSON, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"\n[SAVE] Audit saved to {OUT_AUDIT_JSON}")
        print("✓ 02_viral_score.py complete (Status: PARTIAL)")

    return audit


if __name__ == "__main__":
    run(verbose=True)
