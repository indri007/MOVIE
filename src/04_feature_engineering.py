"""
04_feature_engineering.py
=========================
Step 4 — Feature Engineering Suite
Pipeline: Instagram Indonesia Viral Intelligence & Research Platform

Extracts structural, linguistic, lexicon-based, and textual features
from Indonesian Instagram review data to feed tree-based and linear classifiers.

Features engineered:
- Structural & Social: text_length, token_count, emoji_count, hashtag_count,
  mention_count, url_count.
- Stylistic & Expressive: uppercase_count, uppercase_ratio, exclamation_count,
  question_count, digit_count, avg_word_length, lexical_diversity.
- Lexicon Sentiment Signals: pos_word_count, neg_word_count, net_sentiment_score.
- Vectorized Representations: TF-IDF n-grams (1, 2).

Run:
    python src/04_feature_engineering.py
    python -m src.04_feature_engineering
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
INPUT_CSV = REPO / "output" / "topics_dataset.csv"
FALLBACK_CSV = REPO / "output" / "clean_dataset.csv"
OUT_CSV = REPO / "output" / "features_engineered.csv"
OUT_AUDIT_JSON = REPO / "output" / "features_audit.json"

# Indonesian Lexicon for sentiment heuristics
POSITIVE_WORDS = {
    "bagus", "baik", "suka", "mantap", "senang", "cinta", "keren", "puas",
    "terima", "membantu", "hebat", "luar", "biasa", "cepat", "mudah", "ramah",
    "top", "bintang", "bermanfaat", "lengkap", "asik", "nyaman"
}

NEGATIVE_WORDS = {
    "buruk", "kecewa", "kesal", "marah", "lambat", "error", "bug", "gagal",
    "benci", "rusak", "jelek", "lemot", "rugi", "hilang", "parah", "sulit",
    "susah", "mengecewakan", "blokir", "hapus", "sampah", "hang"
}


def extract_linguistic_features(df: pd.DataFrame, text_col: str = "clean_text") -> pd.DataFrame:
    """Extracts linguistic, syntactic, and expressive features from text."""
    out = df.copy()
    texts = out[text_col].fillna("").astype(str)

    # 1. Stylistic counts
    out["char_count"] = texts.str.len()
    out["word_count"] = texts.apply(lambda s: len(s.split()))
    out["avg_word_length"] = np.where(out["word_count"] > 0, out["char_count"] / out["word_count"], 0).round(2)

    # 2. Expressive punctuation
    out["exclamation_count"] = texts.str.count(r"!")
    out["question_count"] = texts.str.count(r"\?")
    out["digit_count"] = texts.str.count(r"\d")

    # 3. Capitalization signals (if original_text available, use that for uppercase)
    orig_col = "original_text" if "original_text" in out.columns else text_col
    orig_texts = out[orig_col].fillna("").astype(str)
    out["uppercase_count"] = orig_texts.apply(lambda s: sum(1 for c in s if c.isupper()))
    out["uppercase_ratio"] = np.where(
        out["char_count"] > 0,
        (out["uppercase_count"] / out["char_count"]).round(4),
        0.0
    )

    # 4. Lexical diversity (Type-Token Ratio)
    def calc_ttr(s: str) -> float:
        words = s.lower().split()
        return round(len(set(words)) / len(words), 4) if words else 0.0

    out["lexical_diversity"] = texts.apply(calc_ttr)

    # 5. Indonesian Sentiment Lexicon Scores
    def score_sentiment(s: str) -> Tuple[int, int, int]:
        tokens = set(re.findall(r"\b\w+\b", s.lower()))
        pos = len(tokens & POSITIVE_WORDS)
        neg = len(tokens & NEGATIVE_WORDS)
        return pos, neg, (pos - neg)

    lex_res = texts.apply(score_sentiment)
    out["pos_word_count"] = [r[0] for r in lex_res]
    out["neg_word_count"] = [r[1] for r in lex_res]
    out["net_sentiment_score"] = [r[2] for r in lex_res]

    return out


def build_tfidf_features(
    texts: pd.Series,
    max_features: int = 3000,
    ngram_range: Tuple[int, int] = (1, 2)
) -> Tuple[Any, np.ndarray, list[str]]:
    """Fits and transforms text series using TfidfVectorizer."""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=2,
        sublinear_tf=True
    )
    X = vectorizer.fit_transform(texts.fillna("").astype(str))
    feature_names = list(vectorizer.get_feature_names_out())
    return vectorizer, X, feature_names


def run(verbose: bool = True) -> dict[str, Any]:
    """Runs the feature engineering pipeline and writes output CSV and audit."""
    if verbose:
        print("=" * 60)
        print("04_feature_engineering.py | Linguistic & Lexicon Feature Suite")
        print("=" * 60)

    in_path = INPUT_CSV if INPUT_CSV.exists() else FALLBACK_CSV
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found at {INPUT_CSV} or {FALLBACK_CSV}")

    df = pd.read_csv(in_path)
    if verbose:
        print(f"[LOAD]  Loaded {len(df):,} records from {in_path.name}")

    # Extract features
    df_feat = extract_linguistic_features(df, text_col="clean_text")

    # Fit TF-IDF sample check
    vec, X_tfidf, tfidf_names = build_tfidf_features(df_feat["clean_text"])
    if verbose:
        print(f"[TFIDF] Vectorized {X_tfidf.shape[0]} samples into {X_tfidf.shape[1]} vocabulary features")

    # Save CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_feat.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    # Prepare audit
    numeric_cols = [
        "char_count", "word_count", "avg_word_length", "exclamation_count",
        "question_count", "digit_count", "uppercase_count", "uppercase_ratio",
        "lexical_diversity", "pos_word_count", "neg_word_count", "net_sentiment_score"
    ]
    summary_stats = df_feat[numeric_cols].describe().round(3).to_dict()

    audit = {
        "status": "AVAILABLE",
        "input_records": len(df_feat),
        "engineered_feature_columns": numeric_cols,
        "tfidf_vocabulary_size": len(tfidf_names),
        "summary_statistics": summary_stats,
        "sample_top_terms": tfidf_names[:20],
        "output_file": str(OUT_CSV),
    }

    with open(OUT_AUDIT_JSON, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"[SAVE]  Features saved to {OUT_CSV.name} ({OUT_CSV.stat().st_size:,} bytes)")
        print(f"[AUDIT] Audit saved to {OUT_AUDIT_JSON.name}")
        print("✓ 04_feature_engineering.py complete")

    return audit


if __name__ == "__main__":
    run(verbose=True)
