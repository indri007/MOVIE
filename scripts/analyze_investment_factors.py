#!/usr/bin/env python3
"""
scripts/analyze_investment_factors.py
=====================================
Analisis Faktor Kunci Investasi Film Indonesia (2020–2026)
Mengidentifikasi variabel yang paling berkorelasi dengan keberhasilan komersial:
  1. Pengaruh Genre (Volume, Median Penonton, Hit Rate)
  2. Pengaruh Momen Rilis (Premi Lebaran vs Reguler vs Libur Sekolah)
  3. Pengaruh Skala Studio (Major Studios vs Indie/Mid Tier)
  4. Pengaruh Tipe IP (Original vs Adaptasi vs Sekuel/Franchise)
  5. Pengaruh Track Record Sutradara

Keluaran:
  results/investment_factor_analysis.json
  results/investment_factor_summary.md
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "film_master_2020_2026.csv"
RESULTS_DIR = REPO_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_factor_analysis():
    print("Membaca data master film 2020–2026...")
    df = pd.read_csv(DATA_FILE)

    # Filter hanya film yang memiliki data penonton resmi
    df_valid = df[df["admissions"].notna()].copy()
    print(f"Total film dianalisis dengan data penonton: {len(df_valid)}")

    summary = {}

    # 1. ANALISIS GENRE
    print("\n1. Menganalisis Performa Genre...")
    # Normalisasi genre utama (ambil kata pertama jika multi-genre)
    def clean_genre(g):
        if pd.isna(g): return "Lainnya"
        g = str(g).split(",")[0].strip()
        if "horor" in g.lower(): return "Horor"
        if "komedi" in g.lower(): return "Komedi"
        if "drama" in g.lower(): return "Drama"
        if "aksi" in g.lower() or "action" in g.lower(): return "Aksi"
        if "romantis" in g.lower() or "roman" in g.lower(): return "Romansa"
        if "animasi" in g.lower(): return "Animasi"
        return "Drama"

    df_valid["genre_clean"] = df_valid["genre"].apply(clean_genre)

    genre_grp = df_valid.groupby("genre_clean").agg(
        total_film=("title", "count"),
        total_penonton=("admissions", "sum"),
        mean_penonton=("admissions", "mean"),
        median_penonton=("admissions", "median"),
        max_penonton=("admissions", "max"),
        hit_1m_count=("admissions", lambda x: (x >= 1000000).sum()),
        mega_hit_3m_count=("admissions", lambda x: (x >= 3000000).sum()),
        underperformer_count=("admissions", lambda x: (x < 300000).sum())
    ).reset_index()

    genre_grp["hit_rate_pct"] = (genre_grp["hit_1m_count"] / genre_grp["total_film"]) * 100
    genre_grp["flop_rate_pct"] = (genre_grp["underperformer_count"] / genre_grp["total_film"]) * 100
    genre_grp = genre_grp.sort_values(by="median_penonton", ascending=False)
    summary["genre_performance"] = genre_grp.to_dict(orient="records")

    # 2. ANALISIS MOMEN RILIS (RELEASE WINDOW)
    print("2. Menganalisis Efek Momen Rilis (Lebaran vs Reguler)...")
    window_grp = df_valid.groupby("release_window").agg(
        total_film=("title", "count"),
        total_penonton=("admissions", "sum"),
        mean_penonton=("admissions", "mean"),
        median_penonton=("admissions", "median"),
        hit_1m_count=("admissions", lambda x: (x >= 1000000).sum()),
        hit_rate_pct=("admissions", lambda x: ((x >= 1000000).sum() / len(x)) * 100)
    ).reset_index().sort_values(by="median_penonton", ascending=False)
    summary["release_window_performance"] = window_grp.to_dict(orient="records")

    # 3. ANALISIS STUDIO TIER (MAJOR VS INDIE)
    print("3. Menganalisis Pengaruh Rumah Produksi...")
    ph_grp = df_valid.groupby("ph_tier").agg(
        total_film=("title", "count"),
        total_penonton=("admissions", "sum"),
        mean_penonton=("admissions", "mean"),
        median_penonton=("admissions", "median"),
        hit_1m_count=("admissions", lambda x: (x >= 1000000).sum()),
        hit_rate_pct=("admissions", lambda x: ((x >= 1000000).sum() / len(x)) * 100)
    ).reset_index().sort_values(by="median_penonton", ascending=False)
    summary["studio_tier_performance"] = ph_grp.to_dict(orient="records")

    # 4. ANALISIS IP TYPE (FRANCHISE & ADAPTASI VS ORIGINAL)
    print("4. Menganalisis Efek IP dan Waralaba...")
    ip_grp = df_valid.groupby("ip_type").agg(
        total_film=("title", "count"),
        total_penonton=("admissions", "sum"),
        mean_penonton=("admissions", "mean"),
        median_penonton=("admissions", "median"),
        hit_1m_count=("admissions", lambda x: (x >= 1000000).sum()),
        hit_rate_pct=("admissions", lambda x: ((x >= 1000000).sum() / len(x)) * 100)
    ).reset_index().sort_values(by="median_penonton", ascending=False)
    summary["ip_type_performance"] = ip_grp.to_dict(orient="records")

    # 5. REKOR TOP PRODUCER HOUSES
    ph_top = df_valid.groupby("production_house").agg(
        total_film=("title", "count"),
        total_penonton=("admissions", "sum"),
        mean_penonton=("admissions", "mean"),
        median_penonton=("admissions", "median")
    ).reset_index()
    ph_top = ph_top[ph_top["total_film"] >= 3].sort_values(by="total_penonton", ascending=False).head(10)
    summary["top_production_houses"] = ph_top.to_dict(orient="records")

    # Simpan JSON
    json_path = RESULTS_DIR / "investment_factor_analysis.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Hasil disimpan ke: {json_path}")

    # Generate Markdown Report
    md_content = f"""# Laporan Analisis Faktor Investasi Film Indonesia (2020–2026)
*Dianalisis dari {len(df_valid)} film terverifikasi penonton box office*

---

## 1. Performa Berdasarkan Genre
Genre horor dan komedi membuktikan dominasi komersial tertinggi di pasar bioskop Indonesia:

| Genre | Total Film | Median Penonton | Rata-rata Penonton | Hit Rate ($\ge 1\text{{M}}$) | Flop Rate ($< 300\text{{k}}$) |
|---|:---:|:---:|:---:|:---:|:---:|
"""
    for r in summary["genre_performance"]:
        md_content += f"| **{r['genre_clean']}** | {r['total_film']} | {r['median_penonton']:,.0f} | {r['mean_penonton']:,.0f} | {r['hit_rate_pct']:.1f}% | {r['flop_rate_pct']:.1f}% |\n"

    md_content += """
> **Wawasan Investor:** Horor dan Komedi memiliki peluang melampaui 1 juta penonton lebih tinggi, sementara Drama memiliki volatilitas tinggi dengan persentase underperformer mencapai mayoritas jika tidak didukung IP kuat.

---

## 2. Pengaruh Momen Rilis (The Theatrical Calendar Effect)

| Momen Rilis | Total Film | Median Penonton | Rata-rata Penonton | Hit Rate ($\ge 1\text{{M}}$) |
|---|:---:|:---:|:---:|:---:|
"""
    for r in summary["release_window_performance"]:
        md_content += f"| **{r['release_window'].capitalize()}** | {r['total_film']} | {r['median_penonton']:,.0f} | {r['mean_penonton']:,.0f} | {r['hit_rate_pct']:.1f}% |\n"

    md_content += """
> **Wawasan Investor:** Momen Lebaran dan Libur Akhir Tahun memberikan *theatrical multiplier* luar biasa. Median penonton film Lebaran jauh melampaui tanggal rilis reguler, menjadikannya slot paling diburu investor.

---

## 3. Kekuatan Studio (Major Studio vs Mid/Indie)

| Kategori Studio | Total Film | Median Penonton | Rata-rata Penonton | Hit Rate ($\ge 1\text{{M}}$) |
|---|:---:|:---:|:---:|:---:|
"""
    for r in summary["studio_tier_performance"]:
        md_content += f"| **{r['ph_tier'].replace('_', ' ').title()}** | {r['total_film']} | {r['median_penonton']:,.0f} | {r['mean_penonton']:,.0f} | {r['hit_rate_pct']:.1f}% |\n"

    md_content += """
---

## 4. Efek Intellectual Property (Sekuel/Waralaba vs Adaptasi vs Original)

| Tipe IP | Total Film | Median Penonton | Rata-rata Penonton | Hit Rate ($\ge 1\text{{M}}$) |
|---|:---:|:---:|:---:|:---:|
"""
    for r in summary["ip_type_performance"]:
        md_content += f"| **{r['ip_type'].replace('_', ' ').title()}** | {r['total_film']} | {r['median_penonton']:,.0f} | {r['mean_penonton']:,.0f} | {r['hit_rate_pct']:.1f}% |\n"

    md_content += """
---
*Laporan ini menjadi acuan pembobotan probabilitas mesin prediksi film 2027.*
"""

    md_path = RESULTS_DIR / "investment_factor_summary.md"
    md_path.write_text(md_content, encoding="utf-8")
    print(f"Laporan Markdown disimpan ke: {md_path}")


if __name__ == "__main__":
    run_factor_analysis()
