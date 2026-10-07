"""
streamlit_app/pages/03_🌐_Benchmark_Global_TMDB.py
=================================================
Aplikasi Benchmark Global & NLP Recommendation Engine.
Mengaplikasikan dataset global film (TMDB 5000, MovieLens, Netflix, IMDb)
dan analisis sentimen teks untuk komparasi dengan perfilman Indonesia 2020–2027.
UI/UX: Google Material Design 3 — Light Theme
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np

# Pastikan root direktori ada di sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.global_movie_benchmark_engine import GlobalMovieBenchmarkEngine

st.set_page_config(
    page_title="Benchmark Global & NLP Recommender",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLING MATERIAL DESIGN 3 LIGHT THEME ───────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    color: #0F172A;
  }
  .stApp {
    background-color: #F8FAFC;
  }
  .hero-banner {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #075985 100%);
    border-radius: 16px;
    padding: 28px 36px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px -2px rgba(2, 132, 199, 0.25);
  }
  .hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0;
    color: #FFFFFF;
    letter-spacing: -0.02em;
  }
  .hero-subtitle {
    font-size: 0.95rem;
    color: #E0F2FE;
    margin-top: 8px;
    line-height: 1.5;
  }
  .kpi-card {
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 12px;
  }
  .kpi-val {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0284C7;
  }
  .kpi-lbl {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .rec-card {
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .rec-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A;
  }
  .rec-meta {
    font-size: 0.82rem;
    color: #64748B;
    margin-top: 4px;
  }
  .badge-sim {
    background: #E0F2FE;
    color: #0369A1;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
  }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_engine():
    return GlobalMovieBenchmarkEngine()

engine = get_engine()
stats = engine.get_summary_stats()

# ── HERO BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">🌐 Benchmark Global & NLP Movie Recommendation</div>
  <div class="hero-subtitle">
    Mengaplikasikan kecerdasan data global (TMDB 5000, MovieLens, Netflix, IMDb) 
    dan algoritma Cosine Similarity NLP untuk memvalidasi formula proyek film bioskop 2027.
  </div>
</div>
""", unsafe_allow_html=True)

# ── METRIC CARDS ────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-lbl">Dataset TMDB Global</div>
      <div class="kpi-val">{stats['total_tmdb_movies']:,}</div>
      <small style="color:#0284C7;">Film Terverifikasi</small>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-lbl">Katalog Netflix</div>
      <div class="kpi-val">{stats['total_netflix_titles']:,}</div>
      <small style="color:#10B981;">Film & Serial TV</small>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-lbl">IMDb Top Rated</div>
      <div class="kpi-val">{stats['total_imdb_top1000']:,}</div>
      <small style="color:#F59E0B;">Karya Terbaik Dunia</small>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-lbl">Top ROI Genre</div>
      <div class="kpi-val">Horor</div>
      <small style="color:#EA580C;">Median ROI >280%</small>
    </div>
    """, unsafe_allow_html=True)

# ── TABS UTAMA ──────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Finansial & ROI per Genre",
    "🔍 2. Rekomendasi NLP (Cosine Similarity)",
    "🎭 3. Analisis Sentimen Ulasan",
    "📁 4. Katalog Dataset Eksternal"
])

# ── TAB 1: FINANSIAL & ROI GENRE ────────────────────────────────────────────
with tab1:
    st.markdown("### 📈 Distribusi Keuntungan Finansial per Genre (Global Benchmark)")
    st.caption("Dianalisis dari 4.803 film TMDB dengan parameter modal produksi vs pendapatan box office.")

    df_genre = engine.get_genre_roi_benchmarks()
    if not df_genre.empty:
        c_left, c_right = st.columns([3, 2])
        with c_left:
            st.markdown("##### 🏆 Median Return on Investment (ROI %) per Genre")
            chart_df = df_genre.set_index("primary_genre")["median_roi_pct"].head(10)
            st.bar_chart(chart_df, color="#0284C7")
        with c_right:
            st.markdown("##### 💡 Analisis Strategis untuk Film 2027")
            st.info("""
            * **Genre Horor Memimpin Rasio ROI**: Secara global maupun di Indonesia, horor memiliki rasio modal-berbanding-keuntungan tertinggi karena biaya produksi relatif efisien namun daya pikat bioskop sangat tinggi.
            * **Animasi & Petualangan**: Membutuhkan modal masif (>US$ 80 Juta) dengan potensi pendapatan masif, namun risiko finansial lebih rentan jika terjadi kegagalan pembukaan (*opening weekend*).
            * **Komedi**: Memiliki *profit rate* stabil (>55% balik modal lebih dari 2x lipat), sangat cocok sebagai fondasi portofolio investasi studio.
            """)

        st.markdown("##### 📋 Tabel Agregasi Metrik Finansial per Genre")
        st.dataframe(
            df_genre.rename(columns={
                "primary_genre": "Genre",
                "film_count": "Jumlah Film",
                "median_budget": "Median Modal ($)",
                "median_revenue": "Median Revenue ($)",
                "median_roi_pct": "Median ROI (%)",
                "avg_rating": "Rata-rata Rating",
                "profit_rate": "Tingkat Profitabel (%)"
            }),
            width="stretch"
        )

# ── TAB 2: NLP RECOMMENDER ──────────────────────────────────────────────────
with tab2:
    st.markdown("### 🔍 Mesin Rekomendasi Narasi Serupa (Content-Based NLP)")
    st.caption("Menghitung kedekatan formula cerita, genre, dan kata kunci plot menggunakan representasi TF-IDF & Cosine Similarity.")

    preset_movies = [
        "Pilih Contoh Ide atau Film...",
        "Horror exorcism haunted house evil entity spirits",
        "Comedy family drama funny friends laughing vacation",
        "Action crime thriller heist revenge gangster",
        "Romance drama love marriage tears emotional couple",
        "Inception",
        "The Conjuring",
        "The Avengers",
        "Pengabdi Setan (Horor Klasik Rumah Berhantu)",
        "Agak Laen (Komedi Pasar Malam & Rumah Hantu)"
    ]

    sel_preset = st.selectbox("🎯 Pilih Preset Formula Cerita atau Ketik Sendiri:", preset_movies)
    user_query = st.text_input("✍️ Masukkan Sinopsis / Ide Cerita Film Anda:", 
                               value="" if sel_preset == preset_movies[0] else sel_preset)

    if user_query.strip():
        recs = engine.recommend_similar_movies(user_query, top_n=5)
        if recs:
            st.markdown(f"#### 🎬 5 Film Global Paling Relevan dengan Narasi Ini:")
            for r in recs:
                st.markdown(f"""
                <div class="rec-card">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="rec-title">{r['title']} ({r['release_year']})</div>
                    <span class="badge-sim">Skor Kemiripan: {int(r['similarity_score'] * 100)}%</span>
                  </div>
                  <div class="rec-meta"><b>Genre:</b> {r['genres']} | <b>Rating:</b> ⭐ {r['vote_average']} / 10 | <b>Revenue:</b> ${r['revenue_usd']:,}</div>
                  <p style="margin-top:10px; font-size:0.9rem; color:#334155;">{r['overview']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Tidak ditemukan kemiripan yang cukup signifikan. Coba gunakan kata kunci bahasa Inggris atau sinopsis yang lebih mendalam.")

# ── TAB 3: SENTIMENT ANALYZER ───────────────────────────────────────────────
with tab3:
    st.markdown("### 🎭 Analisis Sentimen Ulasan & Respon Penonton")
    st.caption("Menguji polaritas sentimen ulasan warganet untuk mengukur ekspektasi dan kepuasan penonton.")

    contoh_ulasan = [
        "Ketik ulasan sendiri...",
        "Filmnya gila banget, plot twist di akhir benar-benar memukau dan bikin merinding!",
        "Akting para pemainnya sangat apik, komedinya pecah dan menghibur sekeluarga.",
        "Sangat mengecewakan, ceritanya membosankan, garing dan alurnya berantakan buang waktu.",
        "Biasa saja sih, sinematografinya bagus tapi naskahnya agak monoton dan klise."
    ]

    pilihan = st.selectbox("📝 Pilih Contoh Ulasan Warganet:", contoh_ulasan)
    input_text = st.text_area("Teks Ulasan Penonton:", 
                              value="" if pilihan == contoh_ulasan[0] else pilihan, 
                              height=100)

    if input_text.strip():
        res = engine.analyze_sentiment(input_text)
        s1, s2, s3 = st.columns(3)
        with s1:
            color = "#10B981" if "Positif" in res["sentiment"] else ("#EF4444" if "Negatif" in res["sentiment"] else "#64748B")
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {color};">
              <div class="kpi-lbl">Kategori Sentimen</div>
              <div class="kpi-val" style="color: {color};">{res['sentiment']}</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-lbl">Tingkat Keyakinan (Confidence)</div>
              <div class="kpi-val">{int(res['confidence'] * 100)}%</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-lbl">Skor Polaritas (-1.0 s/d +1.0)</div>
              <div class="kpi-val">{res['score']}</div>
            </div>
            """, unsafe_allow_html=True)

        if res["positive_keywords"]:
            st.success(f"🟢 **Kata Kunci Positif Terdeteksi:** {', '.join(res['positive_keywords'])}")
        if res["negative_keywords"]:
            st.error(f"🔴 **Kata Kunci Negatif Terdeteksi:** {', '.join(res['negative_keywords'])}")

# ── TAB 4: KATALOG DATASET ──────────────────────────────────────────────────
with tab4:
    st.markdown("### 📁 Repositori & Dataset Eksternal yang Terintegrasi di Repositori")
    st.caption("Seluruh 17 paket dataset dan modul riset tersimpan di direktori `data/external/`:")

    dataset_info = [
        {"Nama Dataset / Modul": "TMDB 5000 Movies & Credits", "Fokus": "Metadata Finansial & Cast/Crew", "Path": "data/external/tmdb-5000-movie-dataset", "Status": "Aktif & Terhubung"},
        {"Nama Dataset / Modul": "MovieLens Latest Small", "Fokus": "Rating & Collaborative Filtering", "Path": "data/external/movielens-latest-small", "Status": "Aktif & Terhubung"},
        {"Nama Dataset / Modul": "Netflix Movies and TV Shows", "Fokus": "Katalog Streaming Global", "Path": "data/external/netflix-movies-and-tv-shows", "Status": "Aktif & Terhubung"},
        {"Nama Dataset / Modul": "IMDb Top 1000 Movies", "Fokus": "Benchmark Kualitas Kritikus", "Path": "data/external/top-rated-movies-imdb", "Status": "Aktif & Terhubung"},
        {"Nama Dataset / Modul": "TMDB Box Office Prediction", "Fokus": "Machine Learning Regresi Pendapatan", "Path": "data/external/tmdb-box-office-prediction", "Status": "Tersimpan"},
        {"Nama Dataset / Modul": "RoBERTa Movie Sentiment Analyzer", "Fokus": "NLP Deep Learning Transformer", "Path": "data/external/RoBERTa-movie-sentiment-analyzer", "Status": "Tersimpan"},
        {"Nama Dataset / Modul": "CineMA (mathpluscode)", "Fokus": "Pemrosesan & Analisis Video Film", "Path": "data/external/CineMA", "Status": "Tersimpan"},
        {"Nama Dataset / Modul": "Movie Video Colorization (davidpengg)", "Fokus": "Restorasi Warna Video & Film", "Path": "data/external/Movie_Video_Colorization", "Status": "Tersimpan"},
        {"Nama Dataset / Modul": "MongoDB Movie Search (Vector Search)", "Fokus": "Semantic Search & Embeddings", "Path": "data/external/MongoDB-Movie-Search", "Status": "Tersimpan"},
        {"Nama Dataset / Modul": "Movie Recommender (Sanyam10101)", "Fokus": "Hugging Face Space Aplikasi Web", "Path": "data/external/movie_recomedar", "Status": "Tersimpan"}
    ]
    st.table(pd.DataFrame(dataset_info))
