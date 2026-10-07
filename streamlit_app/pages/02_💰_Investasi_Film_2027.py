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

# Produser Kredibel
producer_idx = 0
if "Manoj Punjabi" in options["producers"]:
    producer_idx = options["producers"].index("Manoj Punjabi")
producer = st.sidebar.selectbox("Produser Film", options["producers"], index=producer_idx)

# Sutradara
director_idx = 0
if "Kimo Stamboel" in options["directors"]:
    director_idx = options["directors"].index("Kimo Stamboel")
director = st.sidebar.selectbox("Sutradara", options["directors"], index=director_idx)

# Pemeran Utama (Lead Cast)
lead_cast_idx = 0
if "Indra Jegel" in options["actors"]:
    lead_cast_idx = options["actors"].index("Indra Jegel")
lead_cast = st.sidebar.selectbox("Pemeran Utama (Lead Cast)", options["actors"], index=lead_cast_idx)

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
    director=director,
    producer=producer,
    lead_cast=lead_cast
)

waterfall_bear = engine.simulate_financial_waterfall(budget_idr, scenarios["bear_admissions"], atp_idr, pa_ratio)
waterfall_base = engine.simulate_financial_waterfall(budget_idr, scenarios["base_admissions"], atp_idr, pa_ratio)
waterfall_bull = engine.simulate_financial_waterfall(budget_idr, scenarios["bull_admissions"], atp_idr, pa_ratio)

risk_eval = engine.assess_project_risk(
    bep_admissions=waterfall_base["bep_admissions"],
    scenarios=scenarios,
    ph=ph,
    director=director,
    producer=producer,
    lead_cast=lead_cast
)

# --- PANDUAN PENGGUNAAN & TUTORIAL (EXPANDER) ---
with st.expander("📘 Panduan & Tutorial Penggunaan Simulator (Klik untuk Buka/Tutup)", expanded=False):
    st.markdown("""
    ### 🎯 Cara Menggunakan Simulator Investasi Film 2027
    
    Simulator ini membantu produser, komite investasi, dan investor perorangan/institusi mengevaluasi kelayakan finansial proyek film Indonesia secara empiris sebelum menyalurkan modal.
    
    #### 🧭 5 Langkah Praktis Penggunaan:
    1. **Atur Parameter Proyek di Sidebar (Sebelah Kiri):**
       - **Genre & Studio:** Pilih genre utama (*Horor*, *Komedi*, *Drama*, dll.) dan studio rumah produksi.
       - **Kombinasi Tim Kreatif:** Pilih **Produser Film** (dari Top 50 Produser Kredibel), **Sutradara** (dari Top 50 Sutradara Terbaik), dan **Pemeran Utama** (dari Top 50 Artis Box Office).
       - **Momen Rilis & IP:** Pilih jendela tayang (Lebaran, Libur Akhir Tahun, Libur Sekolah, Reguler) dan tipe intellectual property (Thread Viral, Adaptasi Novel, Remake, Orisinal).
    2. **Tentukan Parameter Finansial:**
       - Geser **Anggaran Produksi** (Bujet riil produksi, rata-rata Rp 5 Miliar – Rp 15 Miliar).
       - Tentukan **Rasio Biaya Promosi (P&A)** (Standar industri 25% – 35% dari biaya produksi).
       - Masukkan estimasi **Pre-Sale Hak Streaming/OTT** (Netflix/Prime/Vidio) jika sudah ada komitmen kontrak lisensi.
       - Tentukan **Benchmark ATP** (Rata-rata harga tiket bioskop nasional, default: Rp 50.000).
    3. **Evaluasi 4 Kartu Metrik Utama di Dashboard:**
       - **🎯 BEP Penonton:** Target minimal tiket bioskop yang harus terjual agar seluruh biaya produksi + P&A impas.
       - **📊 Proyeksi Penonton (Base Case):** Estimasi penonton realistis berbasis performa film-film dengan DNA setara.
       - **💰 Estimasi Net ROI Produser:** Persentase laba bersih bagian produser terhadap total biaya proyek.
       - **🛡️ Investment Risk Grade:** Peringkat keamanan modal (`AAA` = Sangat Aman s/d `C` = Berisiko Tinggi).
    4. **Jelajahi 6 Tab Analisis Mendalam:**
       - **💵 Skenario Air Terjun Finansial:** Rincian pembagian hasil tiket (Gross $\to$ Pajak Pemda 10% $\to$ Exhibitor 50% $\to$ Net Produser 42,5%) pada skenario Bear, Base, dan Bull.
       - **🧬 DNA Film Pembanding:** 5 film historis (2020–2026) dengan DNA genre, tim, atau skala bujet paling relevan.
       - **⚠️ Profil Risiko & Mitigasi:** Analisis sensitivitas BEP terhadap penurunan jumlah penonton.
       - **📑 Checklist Kontrak & Term Sheet:** Klausul pengaman modal bagi investor (Pre-sale OTT, Joint Escrow, Overrun Cap 10%, Blueprint Kampanye TikTok H-30).
       - **🏆 Database Box Office:** Data lengkap Top 50 Film Terlaris, Top 50 Sutradara, Top 50 Produser, Top 50 Artis, dan 10 Besar Genre beserta tombol unduh CSV.
       - **🕸️ Graf 6 Faktor Profit (NodeXL):** Visualisasi graf jaringan keterhubungan 6 pilar keuntungan tinggi bioskop.
    5. **Unduh Data untuk Pitch Deck:**
       - Setiap tabel pada tab Database Box Office dan Graf NodeXL dilengkapi tombol unduh CSV dan file GraphML untuk kebutuhan presentasi ke investor.
    """)

st.markdown("<br/>", unsafe_allow_html=True)

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
tab_waterfall, tab_comps, tab_risk, tab_checklist, tab_intelligence, tab_nodexl = st.tabs([
    "💵 Skenario Air Terjun Finansial",
    "🧬 DNA Film Pembanding (2020–2026)",
    "⚠️ Profil Risiko & Mitigasi",
    "📑 Checklist Kontrak & Term Sheet",
    "🏆 Database Box Office (50 Film, 50 Sutradara, 50 Artis)",
    "🕸️ Graf 6 Faktor Profit (NodeXL)"
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
    st.markdown("Algoritma mencocokkan kemiripan genre, rekam jejak studio, momen rilis kalender, tipe IP, produser, dan pemeran utama:")

    comps_df = engine.find_comparables(
        genre=genre,
        ph=ph,
        release_window=release_window,
        ip_type=ip_type,
        director=director,
        producer=producer,
        lead_cast=lead_cast,
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

# --- TAB 4: CHECKLIST KONTRAK & TERM SHEET INVESTOR ---
with tab_checklist:
    st.subheader("📑 Checklist Proteksi Modal & Term Sheet Investor Film 2027")
    st.markdown("""
    Gunakan instrumen ini sebagai panduan negosiasi formal antara **Investor / Executive Producer** dan **Production House (PH)** untuk memastikan modal terproteksi sebelum syuting dimulai.
    """)

    # Hitung dampak finansial mitigasi
    ott_min_idr = budget_miliar * 0.25
    ott_max_idr = budget_miliar * 0.30
    contingency_idr = budget_miliar * 0.10
    total_capital_idr = total_cost_miliar * 1e9
    producer_share_per_ticket = atp_idr * 0.425
    adjusted_bep_ott = max(0, int((total_capital_idr - (ott_min_idr * 1e9)) / producer_share_per_ticket))
    bep_reduction = waterfall_base['bep_admissions'] - adjusted_bep_ott

    st.markdown(f"""
    <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-left:4px solid #16A34A; border-radius:12px; padding:1.1rem 1.4rem; margin-bottom:1.5rem;">
      <h4 style="color:#166534; margin:0 0 0.5rem 0;">💡 Dampak Finansial Proteksi Modal</h4>
      <p style="color:#15803D; margin:0; font-size:0.95rem; line-height:1.6;">
        Dengan mengunci <b>Pre-Sale OTT (25%) sebesar Rp {ott_min_idr:.2f} Miliar</b> di muka, target BEP tiket bioskop Anda berkurang sebesar <b>{bep_reduction:,} tiket</b> (dari <b>{waterfall_base['bep_admissions']:,}</b> menjadi hanya <b>{adjusted_bep_ott:,} tiket</b>). Hal ini memangkas risiko penurunan modal (<i>downside risk</i>) secara drastis!
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_chk1, col_chk2 = st.columns(2)

    with col_chk1:
        st.markdown("#### 1. 🛡️ Proteksi Hak Lisensi OTT (Pre-Buy)")
        st.checkbox(
            f"Pre-Sale OTT Minimum Guarantee (MG) Rp {ott_min_idr:.2f} – {ott_max_idr:.2f} Miliar (25–30% bujet) terkunci sebelum produksi",
            value=True,
            key="chk_ott_mg"
        )
        st.checkbox(
            "Termin pembayaran bertahap OTT: 20% Sign, 30% Wrap syuting, 50% Master delivery",
            value=True,
            key="chk_ott_tranche"
        )
        st.checkbox(
            "Klausul Theatrical Holdback: Jendela eksklusif bioskop 45–60 hari sebelum tayang streaming",
            value=True,
            key="chk_ott_holdback"
        )

        st.markdown("#### 2. 🏛️ Tata Kelola Rekening & Overrun Bond")
        st.checkbox(
            "Rekening Bersama (Joint Escrow Account) dengan otorisasi ganda (Kuasa Investor + Produser)",
            value=True,
            key="chk_escrow"
        )
        st.checkbox(
            f"Batas kontinjensi darurat maksimal 10% (Rp {contingency_idr:.2f} Miliar)",
            value=True,
            key="chk_contingency"
        )
        st.checkbox(
            "Klausul 100% Tanggung Jawab PH atas pembengkakan biaya di atas 10% (tanpa dilusi ekuitas investor)",
            value=True,
            key="chk_overrun_liability"
        )
        st.checkbox(
            "Hak Intervensi Investor (Step-In Rights) jika jadwal syuting terlambat >3 hari",
            value=True,
            key="chk_stepin"
        )

    with col_chk2:
        st.markdown("#### 3. 📣 Mesin Pemasaran Organik H-30")
        st.checkbox(
            "Peluncuran Trailer Resmi YouTube H-30 dengan pemantauan sentimen warganet (SANTET engine)",
            value=True,
            key="chk_trailer_h30"
        )
        st.checkbox(
            "Ekstraksi 15 detik audio soundtrack/skor untuk template sound viral TikTok & Reels",
            value=True,
            key="chk_sound_tiktok"
        )
        st.checkbox(
            "Kemitraan 10–20 mikro-kreator niche TikTok untuk UGC reaksi/POV di H-21 s/d H-14",
            value=True,
            key="chk_ugc_tiktok"
        )
        st.checkbox(
            "Advance Ticket Sales (ATS) di M-Tix/CGV/Cinepolis H-7 dengan gimmick tiket khusus",
            value=True,
            key="chk_ats_presale"
        )
        st.checkbox(
            "Amplifikasi status bioskop 'SOLD OUT' di hari pertama rilis untuk menciptakan efek FOMO",
            value=True,
            key="chk_soldout_fomo"
        )

        st.markdown("#### 4. ⚖️ Kepatuhan Legal & Audit")
        st.checkbox(
            "Verifikasi Hak Cipta Naskah (Chain of Title) bersih tanpa sengketa",
            value=True,
            key="chk_chain_title"
        )
        st.checkbox(
            "Letter of Intent (LoI) / Kontrak Eksklusif terikat untuk Sutradara & Cast Utama",
            value=True,
            key="chk_loi_cast"
        )
        st.checkbox(
            "Audit Laporan Keuangan Produksi oleh Kantor Akuntan Publik (KAP) independen sebelum pencairan sisa fee",
            value=True,
            key="chk_audit_kap"
        )

    st.markdown("---")
    st.subheader("📥 Ekspor Draf Term Sheet & Nota Kesepakatan (MoA)")
    st.markdown("Unduh ringkasan kesepakatan investasi berbasis klausul mitigasi di atas:")

    # Buat Dokumen Term Sheet Markdown
    term_sheet_content = f"""# TERM SHEET & REKOMENDASI PERLINDUNGAN INVESTASI FILM
## Proyek: {film_title} (Rilis 2027)

---

### I. PROFIL PROYEK FILM
- **Judul Proyek**: {film_title}
- **Genre Utama**: {genre}
- **Rumah Produksi (PH)**: {ph}
- **Produser**: {producer}
- **Sutradara**: {director}
- **Pemeran Utama (Lead Cast)**: {lead_cast}
- **Jendela Rilis**: {release_window}
- **Karakter IP / Sumber Cerita**: {ip_type}
- **Investment Risk Grade**: {risk_eval['rating']} ({risk_eval['verdict']})

---

### II. STRUKTUR PERMODALAN & PARAMETER KEUANGAN
- **Bujet Produksi Fisik**: Rp {budget_miliar:,.2f} Miliar
- **Bujet Promosi & Distribusi (P&A)**: Rp {pa_miliar:,.2f} Miliar
- **Total Investasi Proyek**: Rp {total_cost_miliar:,.2f} Miliar
- **Asumsi Harga Tiket Rata-rata (ATP)**: Rp {atp_idr:,.0f}
- **Bagi Hasil Bersih Produser/Investor Bioskop**: 42.5% dari Gross Box Office

---

### III. TARGET KELAYAKAN BIOSKOP & SKENARIO PENONTON
- **BEP Tiket Standar (Tanpa Pre-Sale)**: {waterfall_base['bep_admissions']:,} penonton (Gross Box Office: Rp {waterfall_base['bep_gross_box_office_idr']:,.0f})
- **BEP Tiket Terproteksi (Dengan Pre-Sale OTT 25%)**: {adjusted_bep_ott:,} penonton (Penghematan: {bep_reduction:,} tiket)
- **Proyeksi Skenario Penonton**:
  * Bear Case (P25) : {waterfall_bear['admissions']:,} penonton | ROI: {waterfall_bear['roi_pct']:+.1f}%
  * Base Case (P50) : {waterfall_base['admissions']:,} penonton | ROI: {waterfall_base['roi_pct']:+.1f}%
  * Bull Case (P75) : {waterfall_bull['admissions']:,} penonton | ROI: {waterfall_bull['roi_pct']:+.1f}%

---

### IV. KLAUSUL PERLINDUNGAN MODAL INVESTOR (DOWNSIDE MITIGATION)

#### 1. Pre-Sale Hak Lisensi OTT (Streaming Pre-Buy)
- **Target Minimum Guarantee (MG)**: Rp {ott_min_idr:.2f} – {ott_max_idr:.2f} Miliar (25% – 30% biaya produksi).
- **Termin Pembayaran**:
  * 20% saat penandatanganan perjanjian & bukti keterikatan cast utama.
  * 30% saat penyelesaian syuting (wrap principal photography).
  * 50% saat penyerahan master film setelah jendela bioskop berakhir.
- **Theatrical Holdback**: Eksklusivitas bioskop selama 45–60 hari kalender sebelum penayangan SVOD.

#### 2. Tata Kelola Rekening Bersama & Batas Overrun (Completion Bond Equivalent)
- **Rekening Bersama (Joint Escrow)**: Rekening bank khusus proyek yang memerlukan tanda tangan ganda (Kuasa Investor + Produser Pelaksana).
- **Pencairan Bertahap**: Pra-produksi (30%), Produksi (40%), Pasca-produksi (20%), LSF & Delivery (10%).
- **Cadangan Kontinjensi**: Dibatasi maksimal 10% (Rp {contingency_idr:.2f} Miliar).
- **Tanggung Jawab Pembengkakan (Overrun Liability)**: Setiap biaya melebihi kontinjensi 10% menjadi tanggung jawab penuh Production House tanpa mengurangi kepemilikan/porsi bagi hasil investor.
- **Hak Intervensi (Step-In Rights)**: Investor berhak menunjuk Line Producer independen atau membekukan pencairan jika jadwal syuting terlambat lebih dari 3 hari kerja tanpa justifikasi sah.

#### 3. Cetak Biru Pemasaran Digital Organik H-30
- **H-30**: Peluncuran trailer resmi YouTube ber-hooking kuat; pemotongan 15 detik audio soundtrack untuk audio template resmi TikTok/Reels.
- **H-21 s/d H-14**: Kampanye User-Generated Content (UGC) melibatkan 10–20 mikro-kreator TikTok bertema premis film; pemantauan sentimen respons penonton melalui sistem analitik SANTET.
- **H-7**: Pembukaan Advance Ticket Sales (ATS) di jaringan bioskop (XXI M-Tix, CGV, Cinepolis) dengan merchandise/tiket koleksi khusus.
- **Hari-H s/d H+3**: Amplifikasi status bioskop "SOLD OUT" di media sosial guna memicu efek psikologis FOMO (Fear of Missing Out).

#### 4. Kepatuhan & Audit
- Verifikasi keabsahan rantai hak cipta naskah (*Chain of Title*).
- Keterikatan hukum sutradara ({director}) dan aktor utama ({lead_cast}).
- Audit pengeluaran produksi oleh Kantor Akuntan Publik (KAP) independen sebelum pelunasan fee produser.

---
*Dihasilkan secara otomatis oleh Platform Indonesian Film Investment Intelligence 2027*
*Tanggal Dokumen: {pd.Timestamp.now().strftime('%d %B %Y')}*
"""

    slug_title = "".join(c if c.isalnum() else "_" for c in film_title.lower())[:30]
    st.download_button(
        label="📄 Unduh Draf Term Sheet & MoA Proteksi Modal (.md)",
        data=term_sheet_content,
        file_name=f"term_sheet_investasi_{slug_title}_2027.md",
        mime="text/markdown",
        help="Klik untuk mengunduh dokumen term sheet lengkap berbasis parameter simulasi saat ini."
    )

# --- TAB 5: DATABASE BOX OFFICE (50 FILM, 50 SUTRADARA, 50 PRODUSER, 50 ARTIS) ---
with tab_intelligence:
    st.subheader("🏆 Direktori Intelijen Box Office & Investor Indonesia (2020–2026)")
    st.markdown("""
    Eksplorasi basis data komersial resmi perfilman Indonesia 2020–2026: **Top 50 Film Berpenjualan Tertinggi**, **Top 50 Sutradara Berprestasi**, **Top 50 Produser Kredibel**, **Top 50 Artis Box Office**, **Peta Market Fit Genre**, dan **100 Investor Film Indonesia Beserta Tesis Investasinya**.
    """)

    sub_films, sub_directors, sub_producers, sub_actors, sub_genres, sub_investors = st.tabs([
        "🎬 Top 50 Film Terlaris (Revenue)",
        "🎥 Top 50 Sutradara Terbaik",
        "💼 Top 50 Produser Kredibel",
        "🎭 Top 50 Artis Box Office",
        "📊 10 Besar Market Fit Genre",
        "💰 100 Investor Film & Tesis ROI"
    ])

    # 1. TOP 50 REVENUE FILMS
    with sub_films:
        st.markdown("### 🎬 50 Film Indonesia Pencetak Revenue & Penonton Tertinggi (2020–2026)")
        st.markdown("Diurutkan berdasarkan total penjualan tiket bioskop (*admissions*) dan estimasi *Gross Box Office*:")

        search_f = st.text_input("🔍 Cari Judul Film / Studio / Sutradara:", "", key="search_film_box")
        df_f_show = engine.df_revenue_films.copy()
        if search_f:
            df_f_show = df_f_show[
                df_f_show["title"].str.contains(search_f, case=False, na=False) |
                df_f_show["production_house"].str.contains(search_f, case=False, na=False) |
                df_f_show["director"].str.contains(search_f, case=False, na=False)
            ]

        df_f_disp = df_f_show.copy()
        df_f_disp["Penonton"] = df_f_disp["admissions"].apply(lambda x: f"{int(x):,}")
        df_f_disp["Gross Box Office"] = df_f_disp["est_gross_box_office_idr"].apply(lambda x: f"Rp {x:,.0f}")
        df_f_disp["Net Produser (42.5%)"] = df_f_disp["est_producer_net_ticket_idr"].apply(lambda x: f"Rp {x:,.0f}")
        df_f_disp = df_f_disp.rename(columns={
            "rank": "Rank", "title": "Judul Film", "year": "Tahun", "genre": "Genre",
            "director": "Sutradara", "production_house": "Rumah Produksi", "release_window": "Jendela Rilis"
        })

        st.dataframe(
            df_f_disp[["Rank", "Judul Film", "Tahun", "Genre", "Sutradara", "Rumah Produksi", "Jendela Rilis", "Penonton", "Gross Box Office", "Net Produser (42.5%)"]],
            use_container_width=True
        )

        csv_f = engine.df_revenue_films.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Unduh Top 50 Film CSV", csv_f, "top_50_highest_revenue_films_2020_2026.csv", "text/csv", key="dl_f_csv")

    # 2. TOP 50 DIRECTORS
    with sub_directors:
        st.markdown("### 🎥 50 Sutradara Terbaik Film Indonesia (2020–2026) & Prestasinya")
        st.markdown("Diurutkan berdasarkan rekam jejak jumlah penonton bioskop kumulatif dan pencapaian penghargaan perfilman:")

        search_d = st.text_input("🔍 Cari Sutradara:", "", key="search_dir_box")
        df_d_show = engine.df_directors.copy()
        if search_d:
            df_d_show = df_d_show[df_d_show["director_name"].str.contains(search_d, case=False, na=False)]

        df_d_disp = df_d_show.copy()
        df_d_disp["Total Penonton"] = df_d_disp["total_admissions_2020_2026"].apply(lambda x: f"{int(x):,}")
        df_d_disp["Rata-rata/Film"] = df_d_disp["avg_admissions"].apply(lambda x: f"{int(x):,}")
        df_d_disp = df_d_disp.rename(columns={
            "rank": "Rank", "director_name": "Nama Sutradara", "credibility_tier": "Tier",
            "film_count": "Jumlah Film", "top_blockbuster": "Film Terlaris", "prestasi_dan_penghargaan": "Prestasi & Rekor Box Office"
        })

        st.dataframe(
            df_d_disp[["Rank", "Nama Sutradara", "Tier", "Total Penonton", "Jumlah Film", "Rata-rata/Film", "Film Terlaris", "Prestasi & Rekor Box Office"]],
            use_container_width=True
        )

        csv_d = engine.df_directors.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Unduh Top 50 Sutradara CSV", csv_d, "top_50_directors_indonesia_2020_2026.csv", "text/csv", key="dl_d_csv")

    # 3. TOP 50 PRODUCERS
    with sub_producers:
        st.markdown("### 💼 50 Produser Film Indonesia Paling Kredibel (2020–2026)")
        st.markdown("Diurutkan berdasarkan estimasi penonton bioskop kumulatif film yang diproduseri:")

        prod_search = st.text_input("🔍 Cari Produser / PH:", "", key="search_prod_box")
        df_p_show = engine.df_producers.copy()
        if prod_search:
            df_p_show = df_p_show[
                df_p_show["producer_name"].str.contains(prod_search, case=False, na=False) |
                df_p_show["primary_production_house"].str.contains(prod_search, case=False, na=False)
            ]

        df_p_disp = df_p_show.copy()
        df_p_disp["Estimasi Penonton Kumulatif"] = df_p_disp["total_admissions_estimate_2020_2026"].apply(lambda x: f"{x:,.0f}")
        df_p_disp = df_p_disp.rename(columns={
            "rank": "Rank", "producer_name": "Nama Produser", "primary_production_house": "Studio / PH Utama",
            "top_blockbuster": "Film Terlaris", "film_count": "Jumlah Film", "credibility_tier": "Tier",
            "primary_genre": "Spesialisasi Genre", "notable_portfolio": "Portofolio Utama"
        })

        st.dataframe(
            df_p_disp[["Rank", "Nama Produser", "Studio / PH Utama", "Tier", "Estimasi Penonton Kumulatif", "Film Terlaris", "Jumlah Film", "Spesialisasi Genre", "Portofolio Utama"]],
            use_container_width=True
        )

        csv_p = engine.df_producers.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Unduh Top 50 Produser CSV", csv_p, "top_50_producers_indonesia_2020_2026.csv", "text/csv", key="dl_p_csv")

    # 4. TOP 50 ACTORS
    with sub_actors:
        st.markdown("### 🎭 50 Artis Indonesia Pencetak Penonton Tertinggi (2020–2026)")
        st.markdown("Diurutkan berdasarkan total penonton bioskop kumulatif dari film yang dibintangi:")

        actor_search = st.text_input("🔍 Cari Artis / Genre:", "", key="search_act_box")
        df_a_show = engine.df_actors.copy()
        if actor_search:
            df_a_show = df_a_show[
                df_a_show["actor_name"].str.contains(actor_search, case=False, na=False) |
                df_a_show["primary_genre"].str.contains(actor_search, case=False, na=False)
            ]

        df_a_disp = df_a_show.copy()
        df_a_disp["Total Penonton Kumulatif"] = df_a_disp["total_admissions_2020_2026"].apply(lambda x: f"{x:,.0f}")
        df_a_disp["Rata-rata per Film"] = df_a_disp["avg_admissions"].apply(lambda x: f"{x:,.0f}")
        df_a_disp = df_a_disp.rename(columns={
            "rank": "Rank", "actor_name": "Nama Artis", "gender": "Kategori", "film_count": "Jumlah Film",
            "credibility_tier": "Tier", "biggest_hit": "Film Terlaris", "primary_genre": "Genre Utama", "notable_films": "Film Terkenal"
        })

        st.dataframe(
            df_a_disp[["Rank", "Nama Artis", "Kategori", "Tier", "Total Penonton Kumulatif", "Rata-rata per Film", "Film Terlaris", "Jumlah Film", "Genre Utama", "Film Terkenal"]],
            use_container_width=True
        )

        csv_a = engine.df_actors.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Unduh Top 50 Artis CSV", csv_a, "top_50_actors_indonesia_2020_2026.csv", "text/csv", key="dl_a_csv")

    # 5. TOP 10 GENRES MARKET FIT
    with sub_genres:
        st.markdown("### 📊 10 Besar Genre dan Market Fit Komersial di Indonesia (2020–2026)")
        st.markdown("Pangsa pasar penonton bioskop dan profil risiko komersial berdasarkan 896 film terdata:")

        df_g_disp = engine.df_genres_fit.copy()
        df_g_disp["Pangsa Pasar"] = df_g_disp["market_share_pct"].apply(lambda x: f"{x:.1f}%")
        df_g_disp["Total Penonton (2020-2026)"] = df_g_disp["total_admissions_2020_2026"].apply(lambda x: f"{int(x):,}")
        df_g_disp = df_g_disp.rename(columns={
            "rank": "Rank", "genre": "Genre", "total_films_2020_2026": "Jumlah Judul",
            "market_fit_score": "Skor Market Fit", "risk_profile": "Profil Risiko",
            "target_audience": "Segmen Target Penonton", "commercial_dna": "Karakter DNA Komersial"
        })

        st.dataframe(
            df_g_disp[["Rank", "Genre", "Pangsa Pasar", "Skor Market Fit", "Total Penonton (2020-2026)", "Jumlah Judul", "Profil Risiko", "Segmen Target Penonton", "Karakter DNA Komersial"]],
            use_container_width=True
        )

    # 6. TOP 100 FILM INVESTORS & THESES
    with sub_investors:
        st.markdown("### 💰 100 Investor Film Indonesia & Alasan Tesis Investasinya")
        st.markdown("""
        Direktori lengkap 100 entitas investor perfilman di Indonesia (Studio Konglomerasi, Platform OTT SVOD, Venture Capital & Private Equity, FinTech Equity Crowdfunding, Brand FMCG/Perbankan, Celebrity Angels, Hibah Pemerintah/BUMN, dan Co-Producer Asing) beserta motif pengembalian investasinya:
        """)

        inv_search = st.text_input("🔍 Cari Investor / Tipe / Tesis Investasi:", "", key="search_inv_box")
        df_inv_show = engine.df_investors.copy()
        if inv_search:
            df_inv_show = df_inv_show[
                df_inv_show["investor_name"].str.contains(inv_search, case=False, na=False) |
                df_inv_show["investor_type"].str.contains(inv_search, case=False, na=False) |
                df_inv_show["investment_thesis"].str.contains(inv_search, case=False, na=False)
            ]

        df_inv_disp = df_inv_show.copy().rename(columns={
            "id": "No", "investor_name": "Nama Investor / Institusi", "investor_type": "Tipe Investor",
            "key_portfolio_films": "Portofolio / Film Terkait", "typical_ticket_size": "Rentang Alokasi Dana (Ticket Size)",
            "investment_thesis": "Tesis Investasi & Alasan Menaruh Modal"
        })

        st.dataframe(
            df_inv_disp[["No", "Nama Investor / Institusi", "Tipe Investor", "Rentang Alokasi Dana (Ticket Size)", "Portofolio / Film Terkait", "Tesis Investasi & Alasan Menaruh Modal"]],
            use_container_width=True
        )

        csv_inv = engine.df_investors.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Unduh 100 Investor Film Indonesia CSV", csv_inv, "top_100_film_investors_indonesia.csv", "text/csv", key="dl_inv_csv")

# --- TAB 6: GRAF 6 FAKTOR PROFIT (NODEXL ARCHITECTURE) ---
with tab_nodexl:
    st.subheader("🕸️ Arsitektur Graf: 6 Faktor Penentu Keuntungan Film Tertinggi (NodeXL Model)")
    st.markdown("""
    Model jaringan interkoneksi sistemik yang menghubungkan **6 Faktor Kunci Penentu Laba Bersih** menuju **Return on Investment (ROI) Maksimal**.
    Didesain sesuai format topologi **NodeXL Pro Network Analysis** (*Vertices, Directed Weighted Edges, Centrality Levers*).
    """)

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 2px 10px rgba(15,23,42,0.04);">
      <h4 style="color:#C2410C; margin-top:0;">🌐 6 Pilar Penentu Keuntungan Film Indonesia:</h4>
      <ol style="color:#334155; line-height:1.8; margin-bottom:0; font-size:0.95rem;">
        <li><b>Genre & Market Fit Kuat:</b> Memilih genre dengan basis massa likuid (Horor 51.9% atau Komedi 7.2%).</li>
        <li><b>Cost Control & BEP Efisien:</b> Batasi bujet fisik (< Rp 10M) agar tiket impas tercapai sebelum 300.000 penonton.</li>
        <li><b>Strategi Distribusi & Timing:</b> Rebut momentum hari libur (Lebaran multiplier 2.1x) dan slot layar bioskop utama.</li>
        <li><b>Hook (IP & Artis Jangkar):</b> Amankan penonton Opening Weekend (D1-D4) lewat IP viral (Thread X / Novel) dan Top 50 Artis.</li>
        <li><b>Kualitas Cerita & Word-of-Mouth:</b> Memicu mantra organik warganet & FYP TikTok agar film bertahan (long-tail legs) >30 hari.</li>
        <li><b>Diversifikasi Revenue Streams:</b> Kunci Pre-Sale OTT (25-30% MG), sponsor brand placement, dan lisensi TV internasional.</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)

    c_g1, c_g2 = st.columns([3, 2])

    with c_g1:
        st.markdown("#### 🗺️ Peta Relasi Jaringan Antar-Faktor (Directed Graph Topology)")
        st.markdown("""
```
               [F4: Hook IP & Artis] ────(9.5)────┐
                         │ (7.5)                   │
                         ▼                         ▼
  [F1: Genre Fit] ──(8.0)──► [L1: Opening Week] ──────(8.5)──────┐
                         ▲                         ▲             │
                         │ (9.0)                   │             │
  [F3: Timing Lebaran] ──┴────(8.5)──► [L4: Kuota Layar]         ▼
                                                   │      [L6: Net Produser (42.5%)]
  [F5: Cerita & WoM] ───────(10.0)──► [L2: Long-Tail Legs] ──────(9.5)──▲    │ (10.0)
                         │ (8.5)                                        │    ▼
                         ▼                                              ├──► [🎯 ROI & Laba Maksimal]
  [F6: Diversifikasi] ──(9.5)──► [L5: Pre-Sale OTT]                     │    ▲
                         │ (9.0)                   │                    │    │ (10.0)
                         ▼                         ▼                    │    │
  [F2: Cost Control] ──────────(10.0)─────────► [L3: BEP Rendah] ───────┴────┘
```
        """)

    with c_g2:
        st.markdown("#### 📥 Unduh Paket Data NodeXL Pro")
        st.markdown("Paket berkas jaringan ini siap diimpor ke **NodeXL Pro**, **Gephi**, atau **Cytoscape**:")

        # Baca file nodexl
        nodexl_path = REPO_ROOT / "results" / "nodexl_profit_engine"
        v_file = nodexl_path / "vertices.csv"
        e_file = nodexl_path / "edges.csv"
        g_file = nodexl_path / "profit_factors_network.graphml"

        if v_file.exists():
            with open(v_file, "rb") as f:
                st.download_button("⬇️ Unduh vertices.csv (Simpul)", f.read(), "nodexl_profit_vertices.csv", "text/csv", key="dl_nx_v")
        if e_file.exists():
            with open(e_file, "rb") as f:
                st.download_button("⬇️ Unduh edges.csv (Sisi Relasi & Bobot)", f.read(), "nodexl_profit_edges.csv", "text/csv", key="dl_nx_e")
        if g_file.exists():
            with open(g_file, "rb") as f:
                st.download_button("⬇️ Unduh profit_factors_network.graphml", f.read(), "profit_factors_network.graphml", "application/xml", key="dl_nx_g")

    st.markdown("---")
    st.markdown("#### 📊 Tabel Matriks Relasi Sisi & Mekanisme Pengaruh (NodeXL Edges Table)")
    if e_file.exists():
        df_edges = pd.read_csv(e_file)
        st.dataframe(df_edges[["Vertex 1", "Vertex 2", "Relationship", "Weight", "Mechanism"]], use_container_width=True)


