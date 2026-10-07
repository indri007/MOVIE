"""
streamlit_app.py — Entrypoint Streamlit Community Cloud untuk SANTET.

Repo   : indri007/prediksi-movie-2027
Proyek : SANTET — Sentiment Analysis for Nusantara Theatrical Expectation Tracking

Router multi-halaman (st.navigation). Halaman aslinya tetap di streamlit_app/,
jadi bisa juga dijalankan langsung secara lokal:  streamlit run streamlit_app/app.py

Streamlit Cloud → Main file path: streamlit_app.py (default, tidak perlu diubah)
Dependensi cloud ringan: requirements.txt di root (pipeline berat ada di requirements-pipeline.txt).
"""
from pathlib import Path
import os
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "streamlit_app"

nav = st.navigation([
    st.Page(PAGES / "pages" / "02_💰_Investasi_Film_2027.py", title="Simulator Investasi Film 2027", icon="🎬", default=True),
    st.Page(PAGES / "pages" / "03_🌐_Benchmark_Global_TMDB.py", title="Benchmark Global & NLP (TMDB)", icon="🌐"),
    st.Page(PAGES / "pages" / "01_📖_Cerita.py", title="Cerita Riset SANTET", icon="🕯️"),
    st.Page(PAGES / "app.py", title="Dashboard Jaringan (SNA)", icon="🕸️"),
])
nav.run()
