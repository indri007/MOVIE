"""
streamlit_app.py — Root entrypoint untuk Streamlit Community Cloud.

Repo: indri007/prediksi-movie-2027
Proyek: SANTET — Sentiment Analysis for Nusantara Theatrical Expectation Tracking

Streamlit Cloud membaca file ini (nama wajib streamlit_app.py atau app.py di root).
App utama ada di streamlit_app/app.py (SNA dashboard) dengan halaman tambahan
di streamlit_app/pages/.

Cara deploy di Streamlit Cloud:
  Main file path: streamlit_app.py
  (biarkan field ini default, tidak perlu diubah)
"""
import os
import sys
from pathlib import Path

# Pastikan ROOT dan streamlit_app/ masuk ke path
ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "streamlit_app"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(APP_DIR))
os.chdir(ROOT)

# Jalankan app utama SANTET SNA Dashboard
import runpy
runpy.run_path(str(APP_DIR / "app.py"), run_name="__main__")
