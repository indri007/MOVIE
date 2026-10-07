"""
src/investment_engine_2027.py
=============================
Mesin Analitik & Simulasi Investasi Film Indonesia 2027
Komponen Inti:
  1. Comparable Film Matcher (Pencari DNA Film Historis 2020–2026 Paling Mirip)
  2. Multi-Scenario Audience Forecaster (Skenario Bear, Base, Bull)
  3. Financial Waterfall & BEP Calculator (Sensitivitas Biaya vs Return Investor)
  4. Investment Risk Rating (AAA, AA, A, B, C) & SHAP Driver Attribution
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "film_master_2020_2026.csv"
PRODUCERS_FILE = REPO_ROOT / "data" / "top_50_producers_indonesia_2020_2026.csv"
ACTORS_FILE = REPO_ROOT / "data" / "top_50_actors_indonesia_2020_2026.csv"
REVENUE_FILMS_FILE = REPO_ROOT / "data" / "top_50_highest_revenue_films_2020_2026.csv"
DIRECTORS_FILE = REPO_ROOT / "data" / "top_50_directors_indonesia_2020_2026.csv"
GENRES_FIT_FILE = REPO_ROOT / "data" / "top_10_genres_market_fit.csv"
NODEXL_DIR = REPO_ROOT / "results" / "nodexl_profit_engine"

MAJOR_STUDIOS = [
    "md pictures", "falcon pictures", "visinema", "starvision", "rapi films",
    "soraya intercine", "hitmaker", "dee company", "imajinari", "screenplay",
    "idn pictures", "base entertainment", "magma entertainment", "paragon pictures"
]


class FilmInvestmentEngine:
    """Mesin Analisis dan Prediksi Kelayakan Investasi Proyek Film Indonesia 2027."""

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or DATA_FILE
        self.df = self._load_data()
        self.valid_df = self.df[self.df["admissions"].notna()].copy()
        self.df_producers = pd.read_csv(PRODUCERS_FILE) if PRODUCERS_FILE.exists() else pd.DataFrame()
        self.df_actors = pd.read_csv(ACTORS_FILE) if ACTORS_FILE.exists() else pd.DataFrame()
        self.df_revenue_films = pd.read_csv(REVENUE_FILMS_FILE) if REVENUE_FILMS_FILE.exists() else pd.DataFrame()
        self.df_directors = pd.read_csv(DIRECTORS_FILE) if DIRECTORS_FILE.exists() else pd.DataFrame()
        self.df_genres_fit = pd.read_csv(GENRES_FIT_FILE) if GENRES_FIT_FILE.exists() else pd.DataFrame()

    def _load_data(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset tidak ditemukan: {self.data_path}")
        df = pd.read_csv(self.data_path)

        def normalize_genre(g):
            if pd.isna(g): return "Drama"
            g_str = str(g).split(",")[0].strip()
            if "horor" in g_str.lower(): return "Horor"
            if "komedi" in g_str.lower(): return "Komedi"
            if "drama" in g_str.lower(): return "Drama"
            if "aksi" in g_str.lower() or "action" in g_str.lower(): return "Aksi"
            if "romantis" in g_str.lower() or "roman" in g_str.lower(): return "Romansa"
            if "animasi" in g_str.lower(): return "Animasi"
            return "Drama"

        df["genre_clean"] = df["genre"].apply(normalize_genre)
        return df

    def get_filter_options(self) -> Dict[str, List[str]]:
        """Mengambil daftar opsi parameter untuk antarmuka simulator."""
        genres = sorted(self.df["genre_clean"].dropna().unique().tolist())
        ph_list = [
            "MD Pictures", "Falcon Pictures", "Visinema Studios", "Imajinari",
            "Starvision Plus", "Rapi Films", "Soraya Intercine Films", "Hitmaker Studios",
            "Dee Company", "IDN Pictures", "Screenplay Films", "Rumah Produksi Lainnya / Indie"
        ]
        windows = ["Lebaran", "Libur_akhir_tahun", "Libur_sekolah", "Kemerdekaan", "Reguler"]
        ip_types = ["Original", "Adaptation (Novel/Wattpad/X)", "Sequel Or Franchise"]

        # Ambil daftar 50 sutradara terbaik
        if not self.df_directors.empty:
            directors = ["Sutradara Baru / Debut"] + self.df_directors["director_name"].tolist()
        else:
            dir_counts = self.valid_df["director"].value_counts()
            directors = ["Sutradara Baru / Debut"] + sorted(dir_counts[dir_counts >= 2].index.tolist())

        producers = ["Produser Baru / Independen"]
        if not self.df_producers.empty:
            producers += self.df_producers["producer_name"].tolist()

        actors = ["Artis Pendatang Baru"]
        if not self.df_actors.empty:
            actors += self.df_actors["actor_name"].tolist()

        return {
            "genres": genres,
            "production_houses": ph_list,
            "release_windows": windows,
            "ip_types": ip_types,
            "directors": directors,
            "producers": producers,
            "actors": actors
        }

    def find_comparables(
        self,
        genre: str,
        ph: str,
        release_window: str,
        ip_type: str,
        director: str = "Sutradara Baru / Debut",
        producer: str = "Produser Baru / Independen",
        lead_cast: str = "Artis Pendatang Baru",
        top_k: int = 5
    ) -> pd.DataFrame:
        """Mencari film pembanding 2020–2026 dengan kecocokan DNA proyek paling tinggi."""
        df_comp = self.valid_df.copy()

        ph_is_major = any(m in ph.lower() for m in MAJOR_STUDIOS) if ph else False
        clean_ip = "adaptation" if "adapt" in ip_type.lower() else ("sequel_or_franchise" if "sequel" in ip_type.lower() or "franchise" in ip_type.lower() else "original")

        def calc_similarity(row):
            score = 0.0
            # 1. Kecocokan Genre (Bobot: 25%)
            if str(row["genre_clean"]).lower() == genre.lower():
                score += 25.0

            # 2. Kecocokan Studio Tier (Bobot: 20%)
            row_ph = str(row["ph_tier"]).lower()
            if ph_is_major and row_ph == "major_studio":
                score += 20.0
            elif not ph_is_major and row_ph != "major_studio":
                score += 20.0

            # 3. Kecocokan Release Window (Bobot: 15%)
            if str(row["release_window"]).lower() == release_window.lower():
                score += 15.0

            # 4. Kecocokan Tipe IP (Bobot: 15%)
            if str(row["ip_type"]).lower() == clean_ip:
                score += 15.0

            # 5. Kecocokan Sutradara (Bobot: 10%)
            if director != "Sutradara Baru / Debut" and str(row["director"]).lower() == director.lower():
                score += 10.0

            # 6. Kecocokan Pemeran Utama (Bobot: 10%)
            if lead_cast != "Artis Pendatang Baru" and lead_cast.lower() in str(row["cast"]).lower():
                score += 10.0

            # 7. Kecocokan Produser / PH Portfolio (Bobot: 5%)
            if producer != "Produser Baru / Independen" and not self.df_producers.empty:
                p_match = self.df_producers[self.df_producers["producer_name"].str.lower() == producer.lower()]
                if not p_match.empty:
                    p_ph = str(p_match.iloc[0]["primary_production_house"]).lower()
                    if p_ph in str(row["production_house"]).lower():
                        score += 5.0

            return score

        df_comp["similarity_score"] = df_comp.apply(calc_similarity, axis=1)
        top_matches = df_comp.sort_values(by=["similarity_score", "admissions"], ascending=[False, False]).head(top_k)

        cols_return = [
            "title", "year", "genre_clean", "director", "production_house",
            "release_window", "ip_type", "admissions", "est_gross_box_office_idr", "similarity_score"
        ]
        return top_matches[cols_return].reset_index(drop=True)

    def predict_audience_scenarios(
        self,
        genre: str,
        ph: str,
        release_window: str,
        ip_type: str,
        director: str = "Sutradara Baru / Debut",
        producer: str = "Produser Baru / Independen",
        lead_cast: str = "Artis Pendatang Baru"
    ) -> Dict[str, Any]:
        """Menghitung skenario penonton (Bear, Base, Bull) berbasis distribusi komparatif empiris."""
        comparables = self.find_comparables(genre, ph, release_window, ip_type, director, producer, lead_cast, top_k=20)
        admissions_sample = comparables["admissions"].dropna().values

        # Jika sampel terlalu sedikit, fallback ke subset genre + studio tier
        if len(admissions_sample) < 5:
            ph_is_major = any(m in ph.lower() for m in MAJOR_STUDIOS) if ph else False
            target_tier = "major_studio" if ph_is_major else "mid_or_indie"
            fallback_subset = self.valid_df[
                (self.valid_df["genre_clean"].str.lower() == genre.lower()) &
                (self.valid_df["ph_tier"] == target_tier)
            ]
            admissions_sample = fallback_subset["admissions"].dropna().values

        if len(admissions_sample) == 0:
            admissions_sample = self.valid_df["admissions"].dropna().values

        # Skenario distribusi
        p25 = float(np.percentile(admissions_sample, 25))
        p50 = float(np.percentile(admissions_sample, 50))
        p75 = float(np.percentile(admissions_sample, 75))
        p90 = float(np.percentile(admissions_sample, 90))

        # Pengali Sutradara
        dir_mult = 1.0
        if director != "Sutradara Baru / Debut":
            d_rows = self.valid_df[self.valid_df["director"].str.lower() == director.lower()]
            if len(d_rows) >= 2:
                d_avg = d_rows["admissions"].mean()
                ind_avg = self.valid_df["admissions"].mean()
                dir_mult = np.clip(d_avg / ind_avg, 0.8, 1.4)

        # Pengali Produser
        prod_mult = 1.0
        if producer != "Produser Baru / Independen" and not self.df_producers.empty:
            p_match = self.df_producers[self.df_producers["producer_name"].str.lower() == producer.lower()]
            if not p_match.empty:
                tier = p_match.iloc[0]["credibility_tier"]
                if tier == "AAA": prod_mult = 1.15
                elif tier == "AA": prod_mult = 1.08
                elif tier == "A": prod_mult = 1.03

        # Pengali Pemeran Utama
        cast_mult = 1.0
        if lead_cast != "Artis Pendatang Baru" and not self.df_actors.empty:
            c_match = self.df_actors[self.df_actors["actor_name"].str.lower() == lead_cast.lower()]
            if not c_match.empty:
                tier = c_match.iloc[0]["credibility_tier"]
                if tier == "AAA": cast_mult = 1.15
                elif tier == "AA": cast_mult = 1.08
                elif tier == "A": cast_mult = 1.03

        total_multiplier = np.clip(dir_mult * prod_mult * cast_mult, 0.75, 1.85)

        bear_case = int(round(p25 * total_multiplier))
        base_case = int(round(p50 * total_multiplier))
        bull_case = int(round(p75 * total_multiplier))
        stretch_case = int(round(p90 * total_multiplier))

        return {
            "bear_admissions": max(15000, bear_case),
            "base_admissions": max(50000, base_case),
            "bull_admissions": max(150000, bull_case),
            "stretch_admissions": max(300000, stretch_case),
            "sample_size": len(admissions_sample),
            "driver_multiplier": round(total_multiplier, 2),
            "dir_multiplier": round(dir_mult, 2),
            "prod_multiplier": round(prod_mult, 2),
            "cast_multiplier": round(cast_mult, 2)
        }

    def simulate_financial_waterfall(
        self,
        production_budget_idr: float,
        admissions: int,
        atp_idr: float = 50000.0,
        pa_ratio: float = 0.35,
        investor_share_pct: float = 80.0
    ) -> Dict[str, Any]:
        """
        Kalkulasi model air terjun (waterfall) finansial bioskop Indonesia:
          - Gross Box Office = Admissions * ATP
          - Pajak Hiburan Pemda = 10%
          - Net Box Office (DPO) = 90% Gross
          - Bioskop Split (Exhibitor Share) = 50% DPO
          - Net Producer Ticket Share ~ 42.5% Gross
          - Total Biaya Proyek = Production Budget + P&A (Marketing)
          - BEP Admissions = Total Biaya / (ATP * 0.425)
          - Net Producer Profit = Net Producer Share - Total Biaya
        """
        gross_box_office = admissions * atp_idr
        producer_net_ticket = gross_box_office * 0.425

        marketing_budget = production_budget_idr * pa_ratio
        total_project_cost = production_budget_idr + marketing_budget

        net_profit_loss = producer_net_ticket - total_project_cost
        roi_pct = (net_profit_loss / total_project_cost) * 100.0

        bep_admissions = int(round(total_project_cost / (atp_idr * 0.425)))
        bep_margin_admissions = admissions - bep_admissions

        investor_payout = 0.0
        if net_profit_loss > 0:
            investor_payout = total_project_cost * (investor_share_pct / 100.0) + (net_profit_loss * (investor_share_pct / 100.0))
        else:
            recov = max(0.0, producer_net_ticket * (investor_share_pct / 100.0))
            investor_payout = recov

        return {
            "admissions": admissions,
            "gross_box_office_idr": gross_box_office,
            "producer_net_ticket_idr": producer_net_ticket,
            "production_budget_idr": production_budget_idr,
            "marketing_budget_idr": marketing_budget,
            "total_project_cost_idr": total_project_cost,
            "bep_admissions": bep_admissions,
            "bep_margin_admissions": bep_margin_admissions,
            "net_profit_loss_idr": net_profit_loss,
            "roi_pct": round(roi_pct, 1),
            "investor_payout_idr": investor_payout
        }

    def assess_project_risk(
        self,
        bep_admissions: int,
        scenarios: Dict[str, Any],
        ph: str,
        director: str,
        producer: str = "Produser Baru / Independen",
        lead_cast: str = "Artis Pendatang Baru"
    ) -> Dict[str, Any]:
        """Memberikan Rating Kelayakan Investasi (AAA, AA, A, B, C) & Mitigasi Risiko."""
        base_adm = scenarios["base_admissions"]
        bear_adm = scenarios["bear_admissions"]

        # Hitung rasio kecukupan BEP terhadap Base Case
        bep_coverage = base_adm / max(1, bep_admissions)

        if bep_coverage >= 2.0 and bear_adm >= bep_admissions * 0.8:
            rating = "AAA"
            verdict = "Sangat Layak Investasi (Prime Investment Grade)"
            risk_desc = "Probabilitas impas sangat tinggi bahkan dalam skenario konservatif."
        elif bep_coverage >= 1.3:
            rating = "AA"
            verdict = "Layak Investasi (High Yield Potential)"
            risk_desc = "Skenario realistis melampaui BEP dengan potensi margin laba yang sehat."
        elif bep_coverage >= 0.95:
            rating = "A"
            verdict = "Moderat (Breakeven Risk Bound)"
            risk_desc = "Skenario realistis berada di sekitar titik impas. Memerlukan kontrol anggaran ketat."
        elif bep_coverage >= 0.6:
            rating = "B"
            verdict = "Spekulatif Terukur (High Risk)"
            risk_desc = "Skenario dasar belum menutup BEP bioskop. Membutuhkan pre-sale OTT untuk mitigasi."
        else:
            rating = "C"
            verdict = "Spekulatif Tinggi (Capital Loss Risk)"
            risk_desc = "Biaya produksi terlalu tinggi dibanding daya serap pasar kategori ini."

        # Identifikasi Driver Utama
        drivers = []
        if any(m in ph.lower() for m in MAJOR_STUDIOS):
            drivers.append("Dukungan jaringan distribusi Major Studio (Layar Hari-1 terjamin).")
        if director != "Sutradara Baru / Debut":
            drivers.append(f"Rekam jejak sutradara ({director}) memiliki basis penonton terbukti.")

        if producer != "Produser Baru / Independen" and not self.df_producers.empty:
            p_match = self.df_producers[self.df_producers["producer_name"].str.lower() == producer.lower()]
            if not p_match.empty:
                p_row = p_match.iloc[0]
                drivers.append(f"Produser kredibel: {producer} ({p_row['credibility_tier']}, est. {p_row['total_admissions_estimate_2020_2026']/1e6:.1f}M penonton, hit: {p_row['top_blockbuster']}).")

        if lead_cast != "Artis Pendatang Baru" and not self.df_actors.empty:
            c_match = self.df_actors[self.df_actors["actor_name"].str.lower() == lead_cast.lower()]
            if not c_match.empty:
                c_row = c_match.iloc[0]
                drivers.append(f"Pemeran utama berdaya tarik tinggi: {lead_cast} ({c_row['credibility_tier']}, est. {c_row['total_admissions_2020_2026']/1e6:.1f}M penonton, hit: {c_row['biggest_hit']}).")

        if scenarios.get("driver_multiplier", 1.0) > 1.1:
            drivers.append("Genre, momen rilis, dan kombinasi talenta memiliki daya ungkit komersial tinggi.")

        mitigations = [
            "Kunci minimum 25-30% biaya produksi melalui pre-sale hak lisensi OTT (Netflix/Prime/Vidio).",
            "Buat klausul completion bond dengan rumah produksi untuk mencegah pembengkakan bujet di atas 10%.",
            "Terapkan strategi promosi digital terfokus TikTok & trailer YouTube H-30 untuk memicu viralitas organik."
        ]

        return {
            "rating": rating,
            "verdict": verdict,
            "bep_coverage_ratio": round(bep_coverage, 2),
            "risk_description": risk_desc,
            "positive_drivers": drivers,
            "recommended_mitigations": mitigations
        }
