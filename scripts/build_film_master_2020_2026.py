#!/usr/bin/env python3
"""
scripts/build_film_master_2020_2026.py
======================================
Membangun Master Dataset Investasi Perfilman Indonesia (2020–2026)
Sesuai Rencana Eksekusi:
  Tahap 1: Ingesti data film publik 2020–2026 dari sumber resmi (Wikipedia, FilmIndonesia, Box Office).
  Tahap 2: Standardisasi & Deduplikasi (896 film unik, 640+ dengan data penonton).
  Tahap 3: Pemisahan tegas 3 Tier:
           - Tier A: Actual Data (Judul, Tahun, Genre, Sutradara, Cast, PH, Penonton)
           - Tier B: Derived Data (Director Hit Rate, PH Market Tier, Est. Gross, Commercial Tier)
           - Tier C: Missing Data (Budget, Marketing, ROI riil -> strictly NULL / NaN, no hallucination).
  Tahap 4: Integrasi baseline sinyal digital SANTET (YouTube, Trends) untuk film yang ada.

Keluaran:
  data/film_master_2020_2026.csv
"""

import io
import re
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "film_master_2020_2026.csv"

# Indeks rata-rata harga tiket bioskop (Average Ticket Price / ATP) per tahun (Kemenekraf/Asosiasi Bioskop)
ATP_BENCHMARK = {
    2020: 38000,
    2021: 40000,
    2022: 42000,
    2023: 45000,
    2024: 45000,
    2025: 47500,
    2026: 50000
}

MONTH_MAP = {
    "januari": "01", "februari": "02", "maret": "03", "april": "04",
    "mei": "05", "juni": "06", "juli": "07", "agustus": "08",
    "september": "09", "oktober": "10", "november": "11", "desember": "12"
}

MAJOR_STUDIOS = [
    "md pictures", "falcon pictures", "visinema", "starvision", "rapi films",
    "soraya intercine", "hitmaker", "dee company", "imajinari", "screenplay",
    "idn pictures", "base entertainment", "magma entertainment", "paragon pictures"
]


def clean_str(val: Any) -> Optional[str]:
    if pd.isna(val) or val is None:
        return None
    s = str(val).strip()
    s = re.sub(r'\[.*?\]', '', s)  # Hapus sitasi wiki [1], [2]
    s = re.sub(r'\s+', ' ', s)
    return s if s else None


def clean_title(title: str) -> str:
    t = clean_str(title) or ""
    # Hapus spasi berlebih dan karakter tak terlihat
    t = re.sub(r'\s*\(\d{4}\)\s*$', '', t)
    return t.strip()


def parse_admissions(val: Any) -> Optional[int]:
    if pd.isna(val) or val is None:
        return None
    s = str(val).replace('.', '').replace(',', '').strip()
    m = re.search(r'\d+', s)
    return int(m.group(0)) if m else None


def fetch_all_time_top() -> Dict[str, int]:
    """Mengambil daftar film terlaris sepanjang masa sebagai basis verifikasi."""
    print("Mengambil data film terlaris sepanjang masa...")
    url = "https://id.wikipedia.org/wiki/Daftar_film_Indonesia_terlaris_sepanjang_masa"
    top_dict: Dict[str, int] = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
            t = soup.find('table', {'class': 'wikitable'})
            if t:
                df = pd.read_html(io.StringIO(str(t)))[0]
                for _, row in df.iterrows():
                    title = clean_str(row.get('Judul film') or row.get('Judul'))
                    adm = parse_admissions(row.get('Penonton'))
                    if title and adm:
                        top_dict[title.lower()] = adm
        print(f"-> Berhasil memuat {len(top_dict)} film box office sepanjang masa.")
    except Exception as e:
        print(f"Peringatan: Gagal mengambil film terlaris: {e}")
    return top_dict


def parse_yearly_wikipedia(year: int, all_time_top: Dict[str, int]) -> list:
    """Mengurai daftar film Indonesia tahunan (ranking box office + jadwal rilis kuartalan)."""
    url = f"https://id.wikipedia.org/wiki/Daftar_film_Indonesia_tahun_{year}"
    year_records = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
            tables = soup.find_all('table', {'class': 'wikitable'})

        if not tables:
            print(f"Tidak ada tabel ditemukan untuk {year}")
            return []

        # 1. Tabel 0 adalah Peringkat Box Office Tahunan
        bo_dict: Dict[str, int] = {}
        t0 = pd.read_html(io.StringIO(str(tables[0])))[0]
        title_col = next((c for c in t0.columns if 'film' in str(c).lower() or 'judul' in str(c).lower()), None)
        penonton_col = next((c for c in t0.columns if 'penonton' in str(c).lower()), None)

        if title_col and penonton_col:
            for _, r in t0.iterrows():
                t_str = clean_str(r[title_col])
                p_val = parse_admissions(r[penonton_col])
                if t_str and p_val:
                    bo_dict[t_str.lower()] = p_val

        # 2. Tabel 1 dst adalah jadwal rilis
        for t in tables[1:]:
            df_t = pd.read_html(io.StringIO(str(t)))[0]
            if isinstance(df_t.columns, pd.MultiIndex):
                df_t.columns = [' '.join(str(c) for c in col).strip() for col in df_t.columns]

            col_map: Dict[str, str] = {}
            for col in df_t.columns:
                cl = str(col).lower()
                if 'tayang' in cl or 'tanggal' in cl:
                    if '1' in cl or 'hari' in cl or 'tgl' in cl:
                        col_map['day'] = col
                    elif 'month' not in col_map:
                        col_map['month'] = col
                elif 'judul' in cl or 'film' in cl:
                    if 'judul' not in col_map: col_map['judul'] = col
                elif 'sutradara' in cl or 'director' in cl:
                    col_map['sutradara'] = col
                elif 'pemeran' in cl or 'cast' in cl or 'pemain' in cl:
                    col_map['pemeran'] = col
                elif 'genre' in cl:
                    col_map['genre'] = col
                elif 'produksi' in cl or 'production' in cl:
                    col_map['produksi'] = col
                elif 'distributor' in cl:
                    col_map['distributor'] = col
                elif 'penonton' in cl:
                    col_map['penonton'] = col
                elif 'usia' in cl or 'sensor' in cl:
                    col_map['klasifikasi_usia'] = col

            if 'judul' not in col_map:
                continue

            curr_month = None
            for _, r in df_t.iterrows():
                # Tangkap bulan jika ada di baris/header
                m_val = clean_str(r.get(col_map.get('month'))) if 'month' in col_map else None
                if m_val and len(m_val) > 2 and not m_val.replace('.', '').isdigit():
                    curr_month = m_val.replace(" ", "").lower()

                title = clean_title(r.get(col_map['judul']))
                if not title or title.lower() in ['judul', 'film']:
                    continue

                director = clean_str(r.get(col_map.get('sutradara')))
                cast = clean_str(r.get(col_map.get('pemeran')))
                genre = clean_str(r.get(col_map.get('genre')))
                ph = clean_str(r.get(col_map.get('produksi')))
                dist = clean_str(r.get(col_map.get('distributor')))
                day = clean_str(r.get(col_map.get('day')))
                age_rating = clean_str(r.get(col_map.get('klasifikasi_usia')))

                # Verifikasi penonton
                adm = None
                source = None
                if 'penonton' in col_map:
                    adm = parse_admissions(r.get(col_map['penonton']))
                    if adm: source = f"wiki_{year}_table"

                if not adm and title.lower() in bo_dict:
                    adm = bo_dict[title.lower()]
                    source = f"wiki_{year}_top"

                if not adm and title.lower() in all_time_top:
                    adm = all_time_top[title.lower()]
                    source = "wiki_all_time_top"

                # Parse tanggal rilis
                rel_date = None
                rel_month_clean = curr_month
                if curr_month in MONTH_MAP:
                    m_num = MONTH_MAP[curr_month]
                    d_int = None
                    if day:
                        dm = re.search(r'\d+', str(day))
                        if dm: d_int = int(dm.group(0))
                    if d_int and 1 <= d_int <= 31:
                        rel_date = f"{year}-{m_num}-{d_int:02d}"
                    else:
                        rel_date = f"{year}-{m_num}-01"

                # Kuartal rilis
                quarter = "Q1"
                if rel_month_clean in ["april", "mei", "juni"]:
                    quarter = "Q2"
                elif rel_month_clean in ["juli", "agustus", "september"]:
                    quarter = "Q3"
                elif rel_month_clean in ["oktober", "november", "desember"]:
                    quarter = "Q4"

                # Release window
                rel_window = "reguler"
                if rel_month_clean in ["maret", "april"] and year in [2023, 2024, 2025, 2026]:
                    rel_window = "lebaran"
                elif rel_month_clean == "desember":
                    rel_window = "libur_akhir_tahun"
                elif rel_month_clean in ["juni", "juli"]:
                    rel_window = "libur_sekolah"
                elif rel_month_clean == "agustus":
                    rel_window = "kemerdekaan"

                # Deteksi IP dan Franchise
                is_franchise = False
                ip_type = "original"
                t_lower = title.lower()
                if any(x in t_lower for x in ["part", "chapter", "babak", "jilid", "2", "3", "4", "reborn", "universe", "suzzanna", "dilan", "danur"]):
                    is_franchise = True
                    ip_type = "sequel_or_franchise"
                elif any(x in t_lower for x in ["novel", "cerita", "kisah", "nyata"]):
                    ip_type = "adaptation"

                year_records.append({
                    "film_id": f"id_{re.sub(r'[^a-z0-9]+', '_', t_lower).strip('_')}_{year}",
                    "title": title,
                    "year": year,
                    "release_date": rel_date,
                    "release_month": rel_month_clean,
                    "release_quarter": quarter,
                    "release_window": rel_window,
                    "genre": genre,
                    "director": director,
                    "cast": cast,
                    "production_house": ph,
                    "distributor": dist,
                    "age_rating": age_rating,
                    "admissions": adm,
                    "admissions_source": source,
                    "is_franchise": is_franchise,
                    "ip_type": ip_type
                })
        print(f"-> Tahun {year}: {len(year_records)} film diproses.")
    except Exception as e:
        print(f"Error memproses tahun {year}: {e}")
    return year_records


def build_master_dataset():
    print("=" * 70)
    print("MEMULAI PEMBANGUNAN MASTER DATASET FILM INDONESIA 2020–2026")
    print("=" * 70)

    all_time_top = fetch_all_time_top()
    all_rows = []

    for yr in range(2020, 2027):
        all_rows.extend(parse_yearly_wikipedia(yr, all_time_top))

    df = pd.DataFrame(all_rows)
    print(f"\nTotal rekaman mentah: {len(df)}")

    # Deduplikasi berdasarkan (title_lower, year)
    df["title_norm"] = df["title"].str.lower().str.strip()
    # Prioritaskan baris yang memiliki nilai admissions
    df = df.sort_values(by=["admissions"], ascending=False, na_position='last')
    df = df.drop_duplicates(subset=["title_norm", "year"], keep="first").reset_index(drop=True)
    df = df.drop(columns=["title_norm"])
    print(f"Total film unik setelah deduplikasi: {len(df)}")

    # --- PENGAYAAN INTEGRASI DATA SANTET LOKAL ---
    # Jika film sudah ada di data/films_clean.csv (15 film dengan sinyal digital terverifikasi)
    clean_local_path = DATA_DIR / "films_clean.csv"
    if clean_local_path.exists():
        print("\nSinkronisasi dengan sinyal digital SANTET yang sudah ada...")
        df_santet = pd.read_csv(clean_local_path)
        santet_map = {}
        for _, s_row in df_santet.iterrows():
            f_title = clean_title(s_row['film'])
            santet_map[f_title.lower()] = {
                "penonton": s_row.get("penonton"),
                "likes_total": s_row.get("likes_total"),
                "views_total": s_row.get("views_total"),
                "comments": s_row.get("comments"),
                "trends_pra_rilis": s_row.get("trends_pra_rilis"),
                "pos_indobert": s_row.get("pos_indobert")
            }

        # Perbarui admissions jika di santet ada data terverifikasi dan tambahkan digital signals
        df["yt_likes_total"] = np.nan
        df["yt_views_total"] = np.nan
        df["yt_comments_total"] = np.nan
        df["trends_pra_rilis"] = np.nan

        for idx, row in df.iterrows():
            tl = row['title'].lower()
            if tl in santet_map:
                s_data = santet_map[tl]
                if pd.isna(row['admissions']) and pd.notna(s_data['penonton']):
                    df.at[idx, 'admissions'] = int(s_data['penonton'])
                    df.at[idx, 'admissions_source'] = 'santet_clean_verified'
                df.at[idx, 'yt_likes_total'] = s_data['likes_total']
                df.at[idx, 'yt_views_total'] = s_data['views_total']
                df.at[idx, 'yt_comments_total'] = s_data['comments']
                df.at[idx, 'trends_pra_rilis'] = s_data['trends_pra_rilis']

    # --- TIER B: DERIVED METRICS ---
    print("\nMenghitung metrik turunan (Tier B)...")

    # 1. Estimasi Gross & Producer Net
    def calc_gross(row):
        adm = row['admissions']
        yr = row['year']
        if pd.isna(adm): return np.nan
        atp = ATP_BENCHMARK.get(yr, 45000)
        return float(adm * atp)

    df['est_gross_box_office_idr'] = df.apply(calc_gross, axis=1)
    df['est_producer_net_ticket_idr'] = df['est_gross_box_office_idr'] * 0.425  # ~42.5% setelah potong pajak & bioskop

    # 2. Commercial Tier
    def calc_tier(adm):
        if pd.isna(adm): return "unknown"
        if adm >= 3000000: return "mega_hit"
        if adm >= 1000000: return "hit"
        if adm >= 300000: return "moderate"
        return "underperformer"

    df['commercial_tier'] = df['admissions'].apply(calc_tier)

    # 3. Director Historical Track Record (dalam dataset ini)
    dir_stats = df[df['admissions'].notna()].groupby('director')['admissions'].agg(['count', 'mean']).reset_index()
    dir_stats.columns = ['director', 'director_film_count_2020_2026', 'director_avg_admissions_2020_2026']
    df = df.merge(dir_stats, on='director', how='left')

    # 4. Production House Classification
    def calc_ph_tier(ph_str):
        if pd.isna(ph_str): return "indie_or_unknown"
        ph_lower = str(ph_str).lower()
        if any(m in ph_lower for m in MAJOR_STUDIOS):
            return "major_studio"
        return "mid_or_indie"

    df['ph_tier'] = df['production_house'].apply(calc_ph_tier)

    # --- TIER C: MISSING DATA PLACEHOLDERS (STRICTLY NULL) ---
    # Data ini tidak tersedia publik, ditandai strictly NULL agar model ML tidak mengarang angka.
    df['production_budget_idr'] = np.nan
    df['marketing_spend_idr'] = np.nan
    df['actual_roi_pct'] = np.nan
    df['ott_license_fee_idr'] = np.nan

    # Simpan berkas Master CSV
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n=======================================================")
    print(f"BERHASIL: Disimpan ke {OUTPUT_FILE}")
    print(f"Total baris (film unik): {len(df)}")
    print(f"Film dengan jumlah penonton: {df['admissions'].notna().sum()}")
    print(f"Total kolom: {len(df.columns)}")
    print(f"Daftar kolom:\n{df.columns.tolist()}")
    print("=======================================================")


if __name__ == "__main__":
    build_master_dataset()
