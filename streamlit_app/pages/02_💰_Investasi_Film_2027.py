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
tab_waterfall, tab_comps, tab_risk, tab_checklist = st.tabs([
    "💵 Skenario Air Terjun Finansial",
    "🧬 DNA Film Pembanding (2020–2026)",
    "⚠️ Profil Risiko & Mitigasi",
    "📑 Checklist Kontrak & Term Sheet"
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
- **Sutradara**: {director}
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

