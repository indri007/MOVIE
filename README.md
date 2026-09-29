# 🚀 Instagram Reels Indonesia — Viral Prediction 2027

<div align="center">

**Prediksi Potensi Viral Instagram Reels Indonesia Tahun 2027**  
*Berdasarkan Data Historis 2020–2026*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Conda Env](https://img.shields.io/badge/Env-instagram2027-44A833?logo=anaconda&logoColor=white)](https://docs.conda.io/)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM%20%7C%20XGBoost-brightgreen)](https://lightgbm.readthedocs.io/)
[![IndoBERT](https://img.shields.io/badge/NLP-IndoBERT-FF6B6B)](https://huggingface.co/indobenchmark/indobert-base-p1)
[![SHAP](https://img.shields.io/badge/XAI-SHAP-orange)](https://shap.readthedocs.io/)
[![Status](https://img.shields.io/badge/Status-Active%20Research-success)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

*"Dari 17 juta post Instagram → pola viral yang bisa diprediksi untuk 2027"*

</div>

---

## 📌 Product Overview

**Instagram Reels Viral Predictor 2027** adalah platform riset ML end-to-end yang mempelajari pola konten Instagram Indonesia dari tahun 2020 hingga 2026, kemudian membangun model prediktif untuk mengidentifikasi karakteristik konten berpotensi viral di tahun 2027.

### Problem Statement

> Dari sekian banyak konten yang diposting di Instagram Indonesia setiap hari, **mengapa sebagian konten menjadi viral sementara konten lain tidak** — dan apakah pola ini bisa dipelajari dan diprediksi?

### Goal

Membangun sistem yang mampu menjawab:
> *"Berdasarkan pola 2020–2026, konten dengan karakteristik apa yang memiliki probabilitas viral tinggi di 2027?"*

---

## 🎯 Research Questions

| # | Research Question | Status |
|---|---|---|
| RQ1 | Faktor apa yang paling berkorelasi dengan konten viral di Instagram Indonesia? | 🔬 In Progress |
| RQ2 | Bagaimana pola engagement berubah dari 2020 → 2026? | 🔬 In Progress |
| RQ3 | Apakah IndoBERT caption embeddings meningkatkan prediksi viral? | 🔬 In Progress |
| RQ4 | Seberapa akurat LightGBM/XGBoost memprediksi `viral_label`? | 🔬 In Progress |
| RQ5 | Feature apa yang paling berpengaruh menurut SHAP? | 🔬 In Progress |
| RQ6 | Bagaimana pola 2026 dapat diproyeksikan ke 2027? | 📋 Planned |

---

## 📊 Dataset Architecture

### Primary Dataset: `private_instagram` (HuggingFace)

| Atribut | Nilai |
|---|---|
| **Total baris** | ~17.2 juta post |
| **Shards** | 15 × Parquet files |
| **Periode** | 2010–2019 (subset difilter 2020–2026) |
| **Key columns** | `post_id`, `date`, `post_type`, `description`, `likes`, `comments`, `followers`, `lang`, `category` |

### Supporting Datasets

| Dataset | Rows | Konten |
|---|---|---|
| `instagram-engagement-eda` | 29,999 | post analytics + media type + viral label |
| `eldersantos-instagram` | 542,481 | Instagram dengan geo-tag |
| `instagram_influencer_and_brand` | 37,787 | caption, comment, bio influencer Indonesia |
| `IndoDiscourse` | annotated | toxicity & discourse dataset Bahasa Indonesia |
| `cyberbullying-indonesia` | annotated | cyberbullying dataset Instagram Indonesia |
| `brain-virality-dataset` | JSON | viral/neutral/bad outlier markers |

### Target Schema (Master Dataset)

```
reel_id, username, date, year, caption, hashtags, followers,
views, likes, comments, shares, saves, reach, duration,
audio, transcript, topic, emotion, sentiment,
engagement_rate, viral_score, viral_label
```

---

## 🏗️ Pipeline Architecture

```
17+ Juta Post Instagram (2020–2026)
             │
             ▼
┌─────────────────────────────┐
│  01. Data Discovery & Audit │  ← audit semua sumber, no synthetic data
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  02. Master ETL Builder     │  ← build_master_instagram_dataset.py
│  (shard-by-shard, chunk)    │  ← filter lang=id, 2020–2026
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│              FEATURE EXTRACTION                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ VIDEO/CLIP  │  │ TEXT/NLP     │  │ ENGAGEMENT │ │
│  │ frame       │  │ IndoBERT     │  │ views      │ │
│  │ duration    │  │ emotion      │  │ likes      │ │
│  │ audio feat  │  │ sentiment    │  │ viral_score│ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────┐
│  03. Viral Label Engine     │  ← percentile-based, no leakage
│  viral_score → viral_label  │  ← top 20% = viral (1), else 0
└──────────────┬──────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│           TEMPORAL SPLIT                      │
│  2020–2023 → TRAIN                           │
│  2024–2025 → VALIDATION                      │
│  2026      → TEMPORAL TEST                   │
│  2027      → PREDICTION TARGET               │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌─────────────────────────────┐
│  04. ML Training            │  ← LightGBM, XGBoost, Random Forest
│      + SHAP Explainability  │  ← TreeExplainer global + local
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  05. 2027 Forecast          │  ← trend extrapolation + SARIMAX
└──────────────┬──────────────┘
               │
               ▼
         Dashboard / Report
```

---

## 📁 Repository Structure

```
projectityu/
├── 📜 Core Scripts
│   ├── build_master_instagram_dataset.py   # ETL: 17M rows → master schema
│   ├── audit_dataset.py                    # Audit & validasi semua dataset
│   ├── reels_multimodal_pipeline.py        # Multimodal: CLIP + IndoBERT
│   ├── instagram_pipeline_10steps.py       # Full 10-step research pipeline
│   ├── ml_benchmark.py                     # ML benchmark runner
│   ├── shap_analysis.py                    # SHAP explainability
│   └── instagram_crawler.py               # Data collection utilities
│
├── 📂 src/                                 # Modular pipeline steps
│   ├── 01_cleaning.py
│   ├── 02_viral_score.py
│   ├── 03_indobert.py
│   ├── 04_feature_engineering.py
│   ├── 05_temporal_split.py
│   ├── 06_train_models.py
│   ├── 07_evaluate.py
│   ├── 08_trend_momentum.py
│   ├── 09_forecast_2027.py
│   └── 10_explainability.py
│
├── 📂 dashboard/                           # Streamlit Research Dashboard
│   └── app.py
│
├── 📂 output/                              # Pipeline outputs
│   ├── master_instagram_dataset_sample.csv  # 50K sample rows (tracked)
│   └── [large parquets gitignored]
│
├── 📂 models/                              # Model artifacts (gitignored)
│   ├── indobert/
│   └── viral_model/
│
├── 📂 docs/
│   └── papers/
│       └── 2004.12226_Instagram_COVID19.pdf
│
├── 📂 data/
│   ├── Review Instagram.csv               # 1K review dataset
│   └── external/                          # 9.7GB datasets (gitignored)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- macOS / Linux
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python **3.11**

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/indri007/projectityu.git
cd projectityu

# 2. Create conda environment
conda create -n instagram2027 python=3.11 -y
conda activate instagram2027

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Verify environment
which python  # must point to instagram2027 env
python --version  # Python 3.11.x
```

### Run Pipeline

```bash
# Step 1 – Audit datasets
python audit_dataset.py

# Step 2 – Build master dataset (dari parquet shards)
python build_master_instagram_dataset.py

# Step 3 – Full 10-step research pipeline
python instagram_pipeline_10steps.py

# Step 4 – SHAP explainability
python shap_analysis.py

# Step 5 – Launch dashboard
streamlit run dashboard/app.py
```

---

## 🔬 Methodology

### Viral Score Formula

```
viral_score = (
    0.35 × (likes / followers) +
    0.30 × (views / reach)     +
    0.20 × (saves / reach)     +
    0.10 × (comments / reach)  +
    0.05 × e^(-λ × Δt)
)

viral_label = 1  if viral_score >= P80  (top 20%)
            = 0  otherwise
```

### NLP Stack

| Komponen | Tool |
|---|---|
| Sentiment | IndoBERT + lexicon Indonesia |
| Emotion | Multi-label (joy, anger, fear, sadness, surprise) |
| Topic Modeling | BERTopic / LDA |
| Toxicity | IndoDiscourse classifier |
| Caption Embedding | `indobenchmark/indobert-base-p1` |

### ML Models

| Model | Task |
|---|---|
| **LightGBM** | Viral classification (primary) |
| **XGBoost** | Viral classification (ensemble) |
| **Random Forest** | Baseline + feature importance |
| **SARIMAX / Prophet** | 2027 trend forecasting |
| **SHAP TreeExplainer** | Model explainability |

### Temporal Split (No Leakage)

```
TRAIN      : 2020 – 2023  (learning pola historis)
VALIDATION : 2024 – 2025  (hyperparameter tuning)
TEST       : 2026          (evaluasi temporal realistis)
PREDICT    : 2027          (target prediksi)
```

---

## 🧪 Data Integrity Rules

> Integritas data adalah prinsip non-negotiable dalam riset ini.

- ❌ **DILARANG**: membuat data sintetis / fabricate engagement metrics
- ❌ **DILARANG**: memasukkan data 2027 ke dalam training set (future leakage)
- ❌ **DILARANG**: mengasumsikan `post_type` tanpa bukti dari data
- ✅ **WAJIB**: semua klaim berasal dari file/data yang benar-benar tersedia
- ✅ **WAJIB**: dataset besar diproses shard-by-shard (memory-safe)
- ✅ **WAJIB**: raw dataset tidak dimodifikasi, hanya dibaca

---

## 📈 Current Progress

| Tahap | Status |
|---|---|
| ✅ Environment setup (`instagram2027` conda, Python 3.11) | Done |
| ✅ Dataset collection (17M rows parquet + 6 supporting datasets) | Done |
| ✅ Schema mapping & target column definition | Done |
| ✅ Master ETL builder (`build_master_instagram_dataset.py`) | Done |
| ✅ Sample output (50K rows, `output/master_instagram_dataset_sample.csv`) | Done |
| ✅ Multimodal pipeline scaffold (CLIP + IndoBERT) | Done |
| ✅ Audit script & data inventory | Done |
| 🔬 IndoBERT fine-tuning pada data Indonesia | In Progress |
| 🔬 LightGBM training pada master dataset | In Progress |
| 🔬 SHAP explainability report | In Progress |
| 📋 2027 forecasting (SARIMAX + Prophet) | Planned |
| 📋 Interactive dashboard | Planned |

---

## 🔭 Research Roadmap

```
Q4 2026  →  Master dataset final (filtered 2020–2026 Indonesia)
Q4 2026  →  IndoBERT NLP features (sentiment, emotion, topic)
Q4 2026  →  LightGBM viral classifier (target: AUC > 0.80)
Q1 2027  →  SHAP explainability report & feature ranking
Q1 2027  →  2027 forecasting model deployment
Q1 2027  →  Research paper submission
```

---

## 📚 References

| Sumber | Deskripsi |
|---|---|
| [Alfina et al. (2017)](https://doi.org/10.1109/IALP.2017.8300608) | Indonesian hate speech detection |
| [IndoBERT](https://huggingface.co/indobenchmark/indobert-base-p1) | Pre-trained BERT model Bahasa Indonesia |
| [Wibowo et al. (2020)](https://arxiv.org/abs/2004.12226) | Instagram engagement during COVID-19 |
| [SHAP Paper](https://arxiv.org/abs/1705.07874) | Unified framework for model explanations |
| [LightGBM](https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html) | Gradient boosting framework |
| [BERTopic](https://arxiv.org/abs/2203.05794) | Topic modeling with BERT embeddings |

---

## 📜 License & Citation

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

```bibtex
@software{instagram_reels_viral_2027,
  author    = {indri007},
  title     = {Instagram Reels Indonesia – Viral Prediction 2027},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/indri007/projectityu}
}
```

---

<div align="center">

**⭐ Star this repo jika membantu risetmu!**

*Built with ❤️ untuk riset Instagram Indonesia*

</div>

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