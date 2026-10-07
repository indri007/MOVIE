"""
streamlit_app/pages/02_💰_Investasi_Film_2027.py
================================================
Simulator & Intelijen Investasi Film Indonesia 2027
UI/UX: Google Material Design 3 — Light Theme (Warna Cerah Modern)
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

from src.investment_engine_2027 import FilmInvestmentEngine

st.set_page_config(
    page_title="Film Investment Intelligence 2027",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── MATERIAL DESIGN 3 LIGHT THEME (WARNA CERAH) ─────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

  :root {
    --m3-primary: #C2410C;
    --m3-on-primary: #FFFFFF;
    --m3-primary-container: #FFDBCF;
    --m3-surface: #FFFFFF;
    --m3-surface-container: #F8FAFC;
    --m3-on-surface: #0F172A;
    --m3-on-surface-var: #475569;
    --m3-outline: #E2E8F0;
  }

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    color: #0F172A;
  }

  .stApp {
    background-color: #F8FAFC;
    color: #0F172A;
  }

  section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.02);
  }

  h1 {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin-bottom: 0.25rem;
  }

  h2, h3, h4 {
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.02em;
  }

  /* M3 Card Container */
  .m3-hero {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF7ED 50%, #F0FDFA 100%);
    border: 1px solid #FED7AA;
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px -2px rgba(194, 65, 12, 0.06);
  }

  .m3-hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #9A3412;
    margin: 0;
    letter-spacing: -0.02em;
  }

  .m3-hero-sub {
    font-size: 1.02rem;
    color: #475569;
    margin-top: 0.5rem;
    line-height: 1.6;
  }

  /* Metric Card Styling */
  div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 1.1rem 1.35rem !important;
    box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.08) !important;
  }

  div[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    color: #64748B !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  div[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
  }

  /* Material Tabs */
  button[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: #64748B !important;
    padding: 0.75rem 1.25rem !important;
    border-radius: 10px 10px 0 0 !important;
  }
  button[data-baseweb="tab"][aria-selected="true"] {
    color: #C2410C !important;
    border-bottom-color: #C2410C !important;
    font-weight: 700 !important;
  }

  /* Tables & Dataframes */
  div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    overflow: hidden;
  }

  .m3-alert {
    background: #FFFFFF;
    border-left: 4px solid #C2410C;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    margin: 1rem 0;
  }
</style>
""", unsafe_allow_html=True)

# Inisialisasi engine
@st.cache_resource
def get_engine():
    return FilmInvestmentEngine()

try:
    engine = get_engine()
    options = engine.get_filter_options()
except Exception as e:
    st.error(f"Gagal memuat dataset film master: {e}")
    st.stop()

# --- HERO BANNER (MATERIAL 3 LIGHT) ---
st.markdown("""
<div class="m3-hero">
  <div class="m3-hero-title">🎬 Indonesian Film Investment Intelligence 2027</div>
  <div class="m3-hero-sub">
    <b>Simulator Bisnis & Sensitivitas ROI Proyek Film Indonesia</b> — Didukung basis data historis <b>896 film Indonesia (2020–2026)</b> dengan total <b>328,2 Juta penonton bioskop</b> dan metodologi <i>comparable DNA matching</i>.
  </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.markdown("### 📋 Parameter Proyek Film 2027")

film_title = st.sidebar.text_input("Judul Rencana Proyek", value="Proyek Film Horor Nusantara 2027")
genre = st.sidebar.selectbox("Genre Utama", options["genres"], index=options["genres"].index("Horor") if "Horor" in options["genres"] else 0)
ph = st.sidebar.selectbox("Rumah Produksi (Studio)", options["production_houses"], index=0)

director_idx = 0
if "Kimo Stamboel" in options["directors"]:
    director_idx = options["directors"].index("Kimo Stamboel")
director = st.sidebar.selectbox("Sutradara", options["directors"], index=director_idx)

release_window = st.sidebar.selectbox("Momen Rilis Bioskop 2027", options["release_windows"], index=0)
ip_type = st.sidebar.selectbox("Tipe Cerita / Intellectual Property (IP)", options["ip_types"], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Parameter Keuangan")

budget_miliar = st.sidebar.slider(
    "Anggaran Produksi (Miliar IDR)",
    min_value=2.0,
    max_value=35.0,
    value=8.0,
    step=0.5,
    help="Biaya langsung praproduksi, produksi fisik, dan pascaproduksi."
)
budget_idr = budget_miliar * 1_000_000_000

pa_pct = st.sidebar.slider(
    "Alokasi P&A / Promosi (% dari Budget)",
    min_value=15,
    max_value=60,
    value=35,
    step=5,
    help="Biaya promosi, media placement, trailer campaign, dan premiere."
)
pa_ratio = pa_pct / 100.0

atp_idr = st.sidebar.selectbox(
    "Benchmark Harga Tiket / ATP (IDR)",
    [45000, 50000, 55000],
    index=1,
    help="Rata-rata harga tiket bioskop nasional (gabungan XXI, CGV, Cinepolis)."
)

# --- KALKULASI MODEL ---
scenarios = engine.predict_audience_scenarios(
    genre=genre,
    ph=ph,
    release_window=release_window,
    ip_type=ip_type,
    director=director
)

waterfall_bear = engine.simulate_financial_waterfall(budget_idr, scenarios["bear_admissions"], atp_idr, pa_ratio)
waterfall_base = engine.simulate_financial_waterfall(budget_idr, scenarios["base_admissions"], atp_idr, pa_ratio)
waterfall_bull = engine.simulate_financial_waterfall(budget_idr, scenarios["bull_admissions"], atp_idr, pa_ratio)

risk_eval = engine.assess_project_risk(
    bep_admissions=waterfall_base["bep_admissions"],
    scenarios=scenarios,
    ph=ph,
    director=director
)

# --- RINGKASAN METRIK UTAMA (M3 LIGHT METRIC CARDS) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 BEP Penonton (Tiket Impas)",
        value=f"{waterfall_base['bep_admissions']:,}",
        help="Target tiket minimal bioskop agar biaya produksi + P&A tertutup penuh."
    )

with col2:
    base_adm = scenarios["base_admissions"]
    diff_bep = base_adm - waterfall_base['bep_admissions']
    st.metric(
        label="📊 Proyeksi Penonton (Base Case)",
        value=f"{base_adm:,}",
        delta=f"{diff_bep:+,} tiket vs BEP",
        delta_color="normal" if diff_bep >= 0 else "inverse"
    )

with col3:
    base_roi = waterfall_base["roi_pct"]
    st.metric(
        label="📈 Estimasi ROI Produser",
        value=f"{base_roi:+.1f}%",
        delta=f"Rp {waterfall_base['net_profit_loss_idr']:+,.0f}",
        delta_color="normal" if base_roi >= 0 else "inverse"
    )

with col4:
    badge_symbol = {
        "AAA": "🟢", "AA": "🔵", "A": "🟡", "B": "🟠", "C": "🔴"
    }.get(risk_eval["rating"], "⚪")
    st.metric(
        label="🛡️ Investment Risk Grade",
        value=f"{badge_symbol} {risk_eval['rating']}",
        delta=f"BEP Coverage {risk_eval['bep_coverage_ratio']}x"
    )

st.markdown(f"""
<div class="m3-alert">
  <b>Keputusan Kelayakan Proyek:</b> <span style="color:#C2410C; font-weight:700;">{risk_eval['verdict']}</span> — <i>{risk_eval['risk_description']}</i>
</div>
""", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# --- TABS ANALISIS MENDALAM ---
tab_waterfall, tab_comps, tab_risk = st.tabs([
    "💵 Skenario Air Terjun Finansial",
    "🧬 DNA Film Pembanding (2020–2026)",
    "⚠️ Profil Risiko & Rekomendasi Mitigasi"
])

# --- TAB 1: WATERFALL & ROI ---
with tab_waterfall:
    st.subheader("Model Air Terjun Pendapatan Tiket Bioskop (Theatrical Waterfall)")

    summary_df = pd.DataFrame([
        {
            "Skenario": "🐻 Bear Case (Konservatif)",
            "Penonton (Tiket)": f"{waterfall_bear['admissions']:,}",
            "Gross Box Office": f"Rp {waterfall_bear['gross_box_office_idr']:,.0f}",
            "Bagian Bersih Produser (42.5%)": f"Rp {waterfall_bear['producer_net_ticket_idr']:,.0f}",
            "Total Biaya (Produksi + P&A)": f"Rp {waterfall_bear['total_project_cost_idr']:,.0f}",
            "Net Profit / Loss": f"Rp {waterfall_bear['net_profit_loss_idr']:+,.0f}",
            "Estimasi ROI": f"{waterfall_bear['roi_pct']:+.1f}%"
        },
        {
            "Skenario": "⚖️ Base Case (Paling Realistis)",
            "Penonton (Tiket)": f"{waterfall_base['admissions']:,}",
            "Gross Box Office": f"Rp {waterfall_base['gross_box_office_idr']:,.0f}",
            "Bagian Bersih Produser (42.5%)": f"Rp {waterfall_base['producer_net_ticket_idr']:,.0f}",
            "Total Biaya (Produksi + P&A)": f"Rp {waterfall_base['total_project_cost_idr']:,.0f}",
            "Net Profit / Loss": f"Rp {waterfall_base['net_profit_loss_idr']:+,.0f}",
            "Estimasi ROI": f"{waterfall_base['roi_pct']:+.1f}%"
        },
        {
            "Skenario": "🐂 Bull Case (Optimis / Tren Kuat)",
            "Penonton (Tiket)": f"{waterfall_bull['admissions']:,}",
            "Gross Box Office": f"Rp {waterfall_bull['gross_box_office_idr']:,.0f}",
            "Bagian Bersih Produser (42.5%)": f"Rp {waterfall_bull['producer_net_ticket_idr']:,.0f}",
            "Total Biaya (Produksi + P&A)": f"Rp {waterfall_bull['total_project_cost_idr']:,.0f}",
            "Net Profit / Loss": f"Rp {waterfall_bull['net_profit_loss_idr']:+,.0f}",
            "Estimasi ROI": f"{waterfall_bull['roi_pct']:+.1f}%"
        }
    ])
    st.table(summary_df)

    st.info("""
    **Struktur Bagi Hasil Finansial Industri Bioskop Indonesia:**
    - **Gross Box Office** dihitung dari $\\text{Admissions} \\times \\text{ATP}$.
    - **Pajak Hiburan Pemda** dipotong $\\approx 10\\%$ di hulu.
    - **Bagi Hasil Bioskop (Exhibitor Split)** mengambil $50\\%$ dari Net Box Office.
    - Produser & Investor menerima rata-rata **$42.5\\%$** dari total omzet kotor tiket bioskop.
    """)

# --- TAB 2: COMPARABLES DNA ---
with tab_comps:
    st.subheader("Top 5 Film Historis 2020–2026 Paling Mirip (Comparable Match)")
    st.markdown("Algoritma mencocokkan kemiripan genre, rekam jejak studio, momen rilis kalender, dan tipe IP:")

    comps_df = engine.find_comparables(
        genre=genre,
        ph=ph,
        release_window=release_window,
        ip_type=ip_type,
        director=director,
        top_k=5
    )

    display_comps = comps_df.copy()
    display_comps["Penonton"] = display_comps["admissions"].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "-")
    display_comps["Est. Gross Box Office"] = display_comps["est_gross_box_office_idr"].apply(lambda x: f"Rp {x:,.0f}" if pd.notna(x) else "-")
    display_comps["Skor Kecocokan DNA"] = display_comps["similarity_score"].apply(lambda x: f"{x:.0f}%")

    st.dataframe(
        display_comps[[
            "title", "year", "genre_clean", "director", "production_house",
            "release_window", "Penonton", "Est. Gross Box Office", "Skor Kecocokan DNA"
        ]],
        use_container_width=True
    )

# --- TAB 3: RISK & MITIGATIONS ---
with tab_risk:
    st.subheader("Audit Profil Risiko & Rekomendasi Investor")

    c_r1, c_r2 = st.columns(2)

    with c_r1:
        st.markdown("### 🟢 Faktor Pendorong Keberhasilan (Drivers)")
        for d in risk_eval["positive_drivers"]:
            st.markdown(f"- ✅ **{d}**")

    with c_r2:
        st.markdown("### 🛡️ Rekomendasi Perlindungan Modal Investor")
        for m in risk_eval["recommended_mitigations"]:
            st.markdown(f"- 📌 **{m}**")

    st.divider()
    st.markdown("""
    > **Catatan Tata Kelola Riset & Etika Investasi:**  
    > Model ini mematuhi standar objektivitas data tanpa fabrikasi variabel biaya tertutup. Angka-angka finansial disajikan dalam bentuk kalkulasi air terjun standar industri bioskop Indonesia, memberikan proyeksi berbasis skenario yang dapat dipertanggungjawabkan di hadapan komite investasi.
    """)
