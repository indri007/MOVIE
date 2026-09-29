# Instagram Indonesia 2027: Viral Intelligence & Research Platform

> **Tagline:** *From Instagram Data to Explainable Trend Intelligence.*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost%20%7C%20LightGBM-brightgreen.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainability-SHAP-orange.svg)](https://shap.readthedocs.io/)

---

## 📌 Executive Summary

**Instagram Indonesia 2027** is an empirical research and artificial intelligence analytics platform engineered to decipher content dynamics, user polarity, and viral propagation tendencies within the Indonesian social ecosystem. Combining natural language processing (IndoBERT/TF-IDF), gradient boosted decision tree ensembles (XGBoost, LightGBM, Random Forest), game-theoretic model interpretability (SHAP TreeExplainer), and econometric forecasting specifications, the platform transforms raw social data into an auditable intelligence system.

A foundational principle of this project is **uncompromising scientific and data integrity**:
* Zero fabrication of synthetic data points or engagement metrics.
* Module states are tracked transparently as `AVAILABLE`, `PARTIAL`, or `MISSING`.
* All benchmark numbers reflect authentic audit artifacts.

---

## 🎯 Research Motivation & Problem Statement

### Motivation
Indonesia represents one of the largest, most active social media user bases in the world, with over 100 million active Instagram accounts. Rapid shifts in digital culture, local colloquialisms (*bahasa gaul*), and algorithmic recommendation engines make understanding content resonance both an academic imperative and an economic necessity for Indonesian digital researchers.

### Research Problem
Most social media analytics systems function as black boxes or rely on superficial vanity metrics. There is a lack of reproducible, explainable platforms tailored to Indonesian linguistic nuances that can bridge textual sentiment with granular feature attributions and rigorous forecasting toward the 2027 horizon.

### Research Questions (RQs)
* **RQ1 (Content Factors):** *Faktor apa yang berkaitan dengan munculnya konten dengan potensi viral di Instagram Indonesia?*
* **RQ2 (Temporal Transitions):** *Bagaimana topic, sentiment, emotion, dan engagement berubah dari waktu ke waktu?*
* **RQ3 (IndoBERT Extractor):** *Bagaimana IndoBERT dapat digunakan sebagai contextual neural feature extractor?*
* **RQ4 (Tree Ensembles):** *Bagaimana XGBoost dan LightGBM dapat digunakan untuk mempelajari pola viralitas dan persepsi pengguna?*
* **RQ5 (SHAP Explainability):** *Bagaimana SHAP menjelaskan kontribusi feature terhadap model prediksi secara global dan lokal?*
* **RQ6 (2027 Forecasting):** *Bagaimana trend momentum dapat digunakan sebagai sinyal penelitian forecasting menuju 2027?*

---

## 📊 Dataset & Ground Truth Audit

The current foundation of the platform is grounded in real-world audited data:

| Metric | Ground Truth Value | Verification Status |
|---|---|---|
| **Source File** | `data/Review Instagram.csv` | Verified |
| **Row Count** | 1,000 records | Verified |
| **Source Schema** | `UserName`, `Review Text`, `Rating` | Verified |
| **Missing Values** | 0 nulls detected | Verified |
| **Duplicate Text Rows** | 0 duplicates | Verified |
| **Unique Authors** | 992 users | Verified |
| **Class Distribution** | Rating 1: 481, Rating 2: 156, Rating 3: 134, Rating 4: 82, Rating 5: 147 | Verified |

### Data Limitation Notice
1. **Modality:** The initial dataset captures Indonesian consumer app reviews and feedback rather than public post captions.
2. **Missing Engagement Telemetry:** Post-level interaction figures (`likes`, `comments`, `shares`, `saves`, `impressions`, `views`) are absent. Consequently, the native Viral Score is marked as **`PARTIAL`**.
3. **Temporal Dimension:** Continuous post creation timestamps are absent. Time-series temporal analysis is marked as **`PARTIAL`** / **`MISSING`**, and simulated dates are strictly prohibited.

---

## 🛠️ End-to-End Pipeline Architecture

```
Instagram Data (Review Instagram.csv)
       │
       ▼
01 Data Cleaning (src/01_cleaning.py)
       │
       ▼
Master Clean Dataset (output/clean_dataset.csv)
       │
       ├────────────────────────┐
       ▼                        ▼
02 Viral Score Engine      03 IndoBERT Interface
   [Status: PARTIAL]          [Status: MISSING]
       │                        │
       └───────────┬────────────┘
                   ▼
04 Feature Engineering (src/04_feature_engineering.py)
       │
       ▼
05 Temporal / Stratified Split (src/05_temporal_split.py)
       │
       ▼
06 ML Benchmark & Training (src/06_train_models.py)
       │  (Logistic Regression, Random Forest, XGBoost, LightGBM)
       ▼
07 Performance Evaluation (src/07_evaluate.py)
       │
       ├────────────────────────┐
       ▼                        ▼
08 Trend Momentum          09 2027 Forecasting
   [Status: PARTIAL]          [Status: PARTIAL]
       │                        │
       └───────────┬────────────┘
                   ▼
10 SHAP Explainability (src/10_explainability.py)
       │  (TreeExplainer over 5,130 features)
       ▼
Interactive Research Dashboard (dashboard/app.py)
```

---

## 🔬 Core Components & Implementation

### 1. Data Cleaning (`src/01_cleaning.py`)
Normalizes text, strips extraneous URLs and noise while preserving social cues (hashtags, mentions, emojis). Standardizes schema and outputs `output/ig_01_cleaned.csv` and `output/ig_01_audit.json`.

### 2. Viral Score Engine (`src/02_viral_score.py`)
Establishes the formal mathematical formulation for Instagram Virality Potential:
$$\text{Viral Score} = w_1 \left(\frac{\text{Likes}}{\text{Reach}}\right) + 2.5\,w_2 \left(\frac{\text{Shares}}{\text{Reach}}\right) + 2.0\,w_3 \left(\frac{\text{Saves}}{\text{Reach}}\right) + 1.5\,w_4 \left(\frac{\text{Comments}}{\text{Reach}}\right) + w_5\,e^{-\lambda \Delta t}$$
Flags status as **`PARTIAL`** due to data gaps and supplies the structural Content Virality Propensity Proxy (CVPP).

### 3. IndoBERT Neural Interface (`src/03_indobert.py`)
Provides the interface for `indobenchmark/indobert-base-p1`. Confirms model weight presence in `models/indobert/`. Because offline weights are not yet placed, status is transparently reported as **`MISSING`** without triggering automated heavy downloads.

### 4. Feature Engineering (`src/04_feature_engineering.py`)
Extracts syntactic indicators, character lengths, punctuation frequencies, uppercase ratios, token diversity, and Indonesian sentiment lexicon scores alongside TF-IDF n-grams (1, 2).

### 5. Temporal Split (`src/05_temporal_split.py`)
Audits dataset for date/time columns. In their absence, reports **`MISSING`**, rejects synthetic timestamp generation, and provides a stratified fallback split (80:20) for reproducible benchmark testing.

### 6. Model Training & Benchmark (`src/06_train_models.py`)
Audits and interfaces with verified model artifacts:
* `best_model.joblib`
* `logistic_regression.joblib`
* `random_forest.joblib`
* `xgboost_model.joblib`
* `lightgbm_model.joblib`
* `tfidf_logistic_regression.joblib`

### 7. Performance Evaluation (`src/07_evaluate.py`)
Consolidates multiclass metrics across models:
* **Logistic Regression:** Accuracy 50.5%, Weighted F1 48.3%
* **Random Forest:** Accuracy 50.0%, Weighted F1 43.1%
* **XGBoost:** Accuracy 50.5%, Weighted F1 41.5%
* **LightGBM:** Accuracy 49.5%, Weighted F1 41.5%

### 8. Trend Momentum (`src/08_trend_momentum.py`)
Examines semantic topic distribution (Topic 0: 54.9%, Topic 1: 45.1%) and specifies the Trend Momentum differential equation:
$$\mathcal{M}(\text{Topic}_i, t) = \left( \frac{\partial \text{Volume}_i}{\partial t} \right) \times \text{PolarityResonance}_i(t) \times \left[ 1 + \alpha \frac{\partial^2 \text{Engagement}_i}{\partial t^2} \right]$$

### 9. 2027 Research Forecasting (`src/09_forecast_2027.py`)
Maintains **`FORECAST STATUS: PARTIAL`**. Outlines econometric SARIMAX with Indonesian cultural calendars (Ramadan, Harbolnas), Prophet with algorithmic changepoints, and Temporal Fusion Transformers (TFT).

### 10. SHAP Explainability Engine (`src/10_explainability.py`)
Interrogates genuine SHAP TreeExplainer attributions across 5,130 features. Top influential tokens include:
1. `kenapa` (0.103794)
2. `yang` (0.086908)
3. `bisa` (0.085416)
4. `bagus` (0.078869)
5. `untuk` (0.077572)

---

## 🎨 Interactive Research Dashboard (`dashboard/app.py`)

A comprehensive Streamlit research suite styled with **Material 3 × Research Lab × AI Analytics**:
* **13 Sections:** Overview, Dataset Audit, NLP / IndoBERT, Topic Intelligence, Viral Intelligence, Trend & Momentum, ML Benchmark, SHAP Explainability, Network Analysis, 2027 Forecasting, Research Pipeline, 10 Research Directions, Documentation.
* **Interactive Visualizations:** Plotly charts, expandable research cards, real-time sample SHAP inspector, and status badges.

To run:
```bash
streamlit run dashboard/app.py
```

---

## 🚀 10 Strategic Research Directions

1. **Viral Score Validation:** Ingest post-level interaction telemetry (likes, shares, saves, views) to empirically tune weight vectors.
2. **IndoBERT Emotion Analysis:** Fine-tune on Indonesian multi-label emotion corpora (anger, fear, joy, sadness, surprise).
3. **Sentiment & Viral Propagation:** Model propagation velocity differences between polar negative outrage vs positive brand resonance.
4. **Dynamic Topic Modeling (BERTopic):** Implement continuous dynamic topic modeling with c-TF-IDF over longitudinal time slices.
5. **Temporal Viral Dynamics:** Measure the half-life decay function of Reels vs Carousels in urban vs rural Indonesian settings.
6. **Hashtag Co-occurrence Network Analysis:** Build bipartite user-hashtag graph topologies to discover community hubs and viral bridges.
7. **Multimodal Instagram Research:** Merge CLIP visual embeddings of video keyframes with textual representations.
8. **Explainable Viral Prediction:** Surface actionable SHAP guidance for content creators and academic observers.
9. **Early Trend Detection:** Design online changepoint algorithms to detect viral themes prior to algorithmic saturation.
10. **Instagram Indonesia 2027 Forecasting:** Forecast Indonesian social commerce, AI-generated caption prevalence, and creator dynamics toward 2027.

---

## 💻 Installation & Setup

### Prerequisites
* Python 3.10+
* Virtual environment (recommended)

### Installation
```bash
# Clone the repository
git clone <YOUR_REPOSITORY_URL>
cd instagramindonesia

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Reproducing the Pipeline
Execute each stage independently or sequentially:
```bash
python3 src/01_cleaning.py
python3 src/02_viral_score.py
python3 src/03_indobert.py
python3 src/04_feature_engineering.py
python3 src/05_temporal_split.py
python3 src/06_train_models.py
python3 src/07_evaluate.py
python3 src/08_trend_momentum.py
python3 src/09_forecast_2027.py
python3 src/10_explainability.py
```

---

## 📁 Repository Structure

```
├── dashboard/
│   └── app.py                      # Interactive Streamlit Research Suite
├── data/
│   ├── Review Instagram.csv        # Ground truth raw dataset (1,000 rows)
│   └── crawl_log.txt               # Ingestion audit log
├── models/
│   ├── best_model.joblib           # Trained best pipeline artifact
│   ├── logistic_regression.joblib  # Trained Logistic Regression pipeline
│   ├── random_forest.joblib        # Trained Random Forest pipeline
│   ├── xgboost_model.joblib        # Trained XGBoost model dictionary
│   ├── lightgbm_model.joblib       # Trained LightGBM model dictionary
│   ├── tfidf_logistic_regression.joblib # TF-IDF baseline artifact
│   ├── metrics.json                # Verified evaluation metrics
│   ├── model_comparison.csv        # Linear benchmark table
│   └── tree_model_comparison.csv   # Tree ensemble benchmark table
├── network/
│   └── metrics.json                # Relational network topology audit
├── output/
│   ├── clean_dataset.csv           # Cleaned dataset (1,000 rows)
│   ├── topics_dataset.csv          # Dataset with assigned topic clusters
│   ├── topics.csv                  # Discovered topic cluster summaries
│   └── *.json                      # Stage audit reports
├── shap/
│   ├── global_importance.csv       # SHAP global feature importances (5,130 features)
│   ├── local_explanations.csv      # Sample-level SHAP attributions
│   ├── report.json                 # SHAP TreeExplainer verification report
│   ├── shap_bar.png                # Global importance bar chart
│   └── shap_summary.png            # Summary beeswarm distribution plot
├── src/
│   ├── 01_cleaning.py              # Step 1: Cleaning & Schema Audit
│   ├── 02_viral_score.py           # Step 2: Viral Score Engine
│   ├── 03_indobert.py              # Step 3: IndoBERT Interface
│   ├── 04_feature_engineering.py   # Step 4: Linguistic & Lexicon Features
│   ├── 05_temporal_split.py        # Step 5: Temporal Validation & Split
│   ├── 06_train_models.py          # Step 6: ML Model Benchmark & Training
│   ├── 07_evaluate.py              # Step 7: Model Evaluation & Error Analysis
│   ├── 08_trend_momentum.py        # Step 8: Trend Momentum Analytics
│   ├── 09_forecast_2027.py         # Step 9: 2027 Forecasting Specification
│   └── 10_explainability.py        # Step 10: SHAP Attribution Suite
├── requirements.txt                # Python package dependencies
└── README.md                       # Comprehensive Platform Documentation
```

---

## 📜 License & Citation

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

When utilizing this platform or its methodologies in academic research, please cite:
```bibtex
@software{instagram_indonesia_2027,
  author = {Research Team},
  title = {Instagram Indonesia 2027: Viral Intelligence & Research Platform},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/indri007/instagram-indonesia-2027}}
}
```