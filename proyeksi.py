#!/usr/bin/env python3
"""
proyeksi.py
Model Peramalan Tren Pengguna Instagram Indonesia (2020-2026) dan Proyeksi 2027
Tiga Skenario: Rendah (Konservatif), Sedang (Baseline), Tinggi (Optimis)
"""

import csv
import os
import math
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_SOURCE = os.path.join(BASE_DIR, "data", "instagram_users_indonesia_sources.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "proyeksi_2027_tiga_skenario.csv")
OUTPUT_SVG = os.path.join(OUTPUT_DIR, "proyeksi_instagram_2027.svg")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data(filepath):
    records = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "tahun": int(row["tahun"]),
                "sumber": row["sumber"],
                "jumlah_pengguna_juta": float(row["jumlah_pengguna_juta"]),
                "penetrasi_persen": float(row["penetrasi_persen_penduduk"]),
                "tanggal_akses": row["tanggal_akses"],
                "catatan": row["catatan_metodologi"]
            })
    return records

def compute_yearly_averages(records):
    grouped = defaultdict(list)
    for r in records:
        grouped[r["tahun"]].append(r["jumlah_pengguna_juta"])
    
    averages = {}
    for tahun in sorted(grouped.keys()):
        vals = grouped[tahun]
        avg = sum(vals) / len(vals)
        averages[tahun] = {
            "avg": round(avg, 2),
            "count": len(vals),
            "values": vals,
            "min": min(vals),
            "max": max(vals)
        }
    return averages

def linear_regression(x_vals, y_vals):
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    denominator = sum((x - mean_x) ** 2 for x in x_vals)
    
    slope = numerator / denominator if denominator != 0 else 0
    intercept = mean_y - slope * mean_x
    return slope, intercept

def backtest_model(averages):
    # Train on 2020-2025, test on 2026
    train_years = [y for y in averages.keys() if y <= 2025]
    test_year = 2026
    
    x_train = [y - 2020 for y in train_years]
    y_train = [averages[y]["avg"] for y in train_years]
    
    slope, intercept = linear_regression(x_train, y_train)
    
    pred_2026 = intercept + slope * (test_year - 2020)
    actual_2026 = averages[test_year]["avg"]
    
    abs_error = abs(pred_2026 - actual_2026)
    percentage_error = (abs_error / actual_2026) * 100
    
    return {
        "slope": slope,
        "intercept": intercept,
        "predicted_2026": round(pred_2026, 2),
        "actual_2026": round(actual_2026, 2),
        "abs_error": round(abs_error, 2),
        "mape": round(percentage_error, 2)
    }

def project_2027_scenarios(averages):
    val_2026 = averages[2026]["avg"]
    
    # Skenario 1: Rendah (Konservatif / Efek Saturasi)
    # Pertumbuhan melambat menjadi +3.0% (mengingat penetrasi sudah mencapai ~42-43% populasi)
    scen_rendah = round(val_2026 * 1.030, 2)
    
    # Skenario 2: Sedang (Baseline Tren / Pertumbuhan Moderat)
    # Pertumbuhan moderat +6.0% melanjutkan momentum rebound 2025-2026
    scen_sedang = round(val_2026 * 1.060, 2)
    
    # Skenario 3: Tinggi (Optimis / Ekspansi Reels & Social Commerce)
    # Pertumbuhan ekspansif +10.0% didorong adopsi luar Jawa & usia muda
    scen_tinggi = round(val_2026 * 1.100, 2)
    
    scenarios = {
        "Rendah (Konservatif / Saturasi)": {
            "proyeksi_2027": scen_rendah,
            "pertumbuhan_vs_2026": round(((scen_rendah - val_2026) / val_2026) * 100, 2),
            "estimasi_penetrasi": "±42.5% - 43.5%",
            "asumsi_kunci": "Saturasi pengguna aktif tercapai, pembersihan akun pasif oleh Meta, adopsi melambat ke +3.0%"
        },
        "Sedang (Baseline / Moderat)": {
            "proyeksi_2027": scen_sedang,
            "pertumbuhan_vs_2026": round(((scen_sedang - val_2026) / val_2026) * 100, 2),
            "estimasi_penetrasi": "±44.5% - 45.5%",
            "asumsi_kunci": "Tren pemulihan pasca-2024 berlanjut stabil dengan laju pertumbuhan wajar (+6.0%)"
        },
        "Tinggi (Optimis / Ekspansi)": {
            "proyeksi_2027": scen_tinggi,
            "pertumbuhan_vs_2026": round(((scen_tinggi - val_2026) / val_2026) * 100, 2),
            "estimasi_penetrasi": "±46.5% - 47.5%",
            "asumsi_kunci": "Akselerasi adopsi Reels, penetrasi agresif luar pulau Jawa, dan belanja iklan digital (+10.0%)"
        }
    }
    return scenarios

def export_results_csv(averages, scenarios, filepath):
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["kategori", "tahun", "metrik", "nilai_juta", "pertumbuhan_persen", "keterangan"])
        
        # Historical averages
        prev_val = None
        for yr, data in averages.items():
            val = data["avg"]
            growth = round(((val - prev_val) / prev_val) * 100, 2) if prev_val else 0.0
            writer.writerow(["Historis", yr, "Rata-rata Konsensus", val, growth, f"Berdasarkan {data['count']} sumber"])
            prev_val = val
            
        # 2027 Scenarios
        for skenario, info in scenarios.items():
            writer.writerow(["Proyeksi 2027", 2027, skenario, info["proyeksi_2027"], info["pertumbuhan_vs_2026"], info["asumsi_kunci"]])

def generate_svg_chart(averages, scenarios, filepath):
    w, h = 820, 480
    margin_l, margin_r, margin_t, margin_b = 85, 80, 70, 70
    plot_w = w - margin_l - margin_r
    plot_h = h - margin_t - margin_b
    
    years = list(sorted(averages.keys())) + [2027]
    min_year, max_year = min(years), max(years)
    
    min_val = 70.0
    max_val = 145.0
    
    def x_pos(year):
        return margin_l + (year - min_year) / (max_year - min_year) * plot_w
    
    def y_pos(val):
        return margin_t + plot_h - (val - min_val) / (max_val - min_val) * plot_h
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" style="background:#090d16; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">')
    
    # Title & Subtitle
    svg.append(f'<text x="{w/2}" y="32" text-anchor="middle" fill="#f8fafc" font-size="18" font-weight="bold">Proyeksi Pengguna Instagram di Indonesia (2020–2027)</text>')
    svg.append(f'<text x="{w/2}" y="52" text-anchor="middle" fill="#94a3b8" font-size="12">Kompilasi Sumber (NapoleonCat, GoodStats) &amp; Tiga Skenario Pertumbuhan</text>')
    
    # Grid lines & Y-axis labels
    for y_val in range(70, 150, 10):
        yp = y_pos(y_val)
        svg.append(f'<line x1="{margin_l}" y1="{yp}" x2="{w - margin_r}" y2="{yp}" stroke="#1e293b" stroke-dasharray="4,4" />')
        svg.append(f'<text x="{margin_l - 12}" y="{yp + 4}" text-anchor="end" fill="#64748b" font-size="11">{y_val} Jt</text>')
        
    # X-axis labels
    for yr in years:
        xp = x_pos(yr)
        svg.append(f'<line x1="{xp}" y1="{margin_t}" x2="{xp}" y2="{h - margin_b}" stroke="#1e293b" />')
        is_proj = (yr == 2027)
        color = "#38bdf8" if is_proj else "#cbd5e1"
        svg.append(f'<text x="{xp}" y="{h - margin_b + 24}" text-anchor="middle" fill="{color}" font-size="12" font-weight="{"bold" if is_proj else "normal"}">{yr}</text>')

    # Historical line
    pts = []
    for yr in sorted(averages.keys()):
        pts.append(f"{x_pos(yr)},{y_pos(averages[yr]['avg'])}")
    poly_pts = " ".join(pts)
    svg.append(f'<polyline fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" points="{poly_pts}" />')
    
    # Historical points
    for yr in sorted(averages.keys()):
        xp = x_pos(yr)
        yp = y_pos(averages[yr]["avg"])
        svg.append(f'<circle cx="{xp}" cy="{yp}" r="5" fill="#38bdf8" stroke="#090d16" stroke-width="2.5" />')
        svg.append(f'<text x="{xp}" y="{yp - 12}" text-anchor="middle" fill="#e2e8f0" font-size="11" font-weight="600">{averages[yr]["avg"]:.1f}M</text>')

    # 2027 Projections
    p2026_x = x_pos(2026)
    p2026_y = y_pos(averages[2026]["avg"])
    p2027_x = x_pos(2027)
    
    scen_meta = [
        ("Rendah (Konservatif / Saturasi)", "#f59e0b", "124.4 Jt"),
        ("Sedang (Baseline / Moderat)", "#10b981", "128.0 Jt"),
        ("Tinggi (Optimis / Ekspansi)", "#a855f7", "132.8 Jt")
    ]
    
    for skenario, c, short_lbl in scen_meta:
        info = scenarios[skenario]
        val = info["proyeksi_2027"]
        yp = y_pos(val)
        svg.append(f'<line x1="{p2026_x}" y1="{p2026_y}" x2="{p2027_x}" y2="{yp}" stroke="{c}" stroke-width="2.5" stroke-dasharray="6,4" />')
        svg.append(f'<circle cx="{p2027_x}" cy="{yp}" r="6.5" fill="{c}" stroke="#090d16" stroke-width="2.5" />')
        svg.append(f'<text x="{p2027_x + 12}" y="{yp + 4}" text-anchor="start" fill="{c}" font-size="11" font-weight="bold">{info["proyeksi_2027"]}M</text>')

    # Legend
    legend_y = h - 20
    svg.append(f'<circle cx="120" cy="{legend_y}" r="4" fill="#0284c7" />')
    svg.append(f'<text x="130" y="{legend_y + 4}" fill="#cbd5e1" font-size="11">Historis Konsensus</text>')
    svg.append(f'<circle cx="310" cy="{legend_y}" r="4" fill="#f59e0b" />')
    svg.append(f'<text x="320" y="{legend_y + 4}" fill="#f59e0b" font-size="11">Rendah: 124.4M</text>')
    svg.append(f'<circle cx="470" cy="{legend_y}" r="4" fill="#10b981" />')
    svg.append(f'<text x="480" y="{legend_y + 4}" fill="#10b981" font-size="11">Sedang: 128.0M</text>')
    svg.append(f'<circle cx="630" cy="{legend_y}" r="4" fill="#a855f7" />')
    svg.append(f'<text x="640" y="{legend_y + 4}" fill="#a855f7" font-size="11">Tinggi: 132.8M</text>')
    
    svg.append('</svg>')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

def main():
    print("=" * 65)
    print("   MODEL PERAMALAN INSTAGRAM INDONESIA (2020-2027)")
    print("=" * 65)
    
    # 1. Load Data
    records = load_data(CSV_SOURCE)
    print(f"\n[1] Data Sumber Berhasil Dimuat: {len(records)} baris data dari CSV")
    print(f"    Lokasi CSV: {CSV_SOURCE}")
    
    # 2. Yearly Averages
    averages = compute_yearly_averages(records)
    print("\n[2] Rata-rata Konsensus Tahunan (2020-2026):")
    print("-" * 55)
    print(f"{'Tahun':<8} | {'Rata-rata (Juta)':<18} | {'Rentang Sumber':<15} | {'N Sumber':<8}")
    print("-" * 55)
    for yr, d in averages.items():
        min_max = f"{d['min']} - {d['max']}" if d['min'] != d['max'] else f"{d['min']}"
        print(f"{yr:<8} | {d['avg']:<18.2f} | {min_max:<15} | {d['count']:<8}")
    print("-" * 55)
    
    # 3. Backtesting on 2026
    backtest = backtest_model(averages)
    print("\n[3] Hasil Backtest Model Baseline (Train: 2020-2025 -> Test: 2026):")
    print("-" * 55)
    print(f"Persamaan Baseline (Regresi Linier) : Y = {backtest['intercept']:.2f} + {backtest['slope']:.2f} * t")
    print(f"Aktual Rata-rata 2026               : {backtest['actual_2026']:.2f} juta")
    print(f"Prediksi Baseline 2026              : {backtest['predicted_2026']:.2f} juta")
    print(f"Absolute Error                      : {backtest['abs_error']:.2f} juta")
    print(f"MAPE (Mean Absolute % Error)        : {backtest['mape']:.2f}%")
    if backtest['mape'] <= 10.0:
        print("Status Evaluasi Baseline            : SANGAT AKURAT (MAPE < 10%)")
    else:
        print("Status Evaluasi Baseline            : MODERAT")
    print("-" * 55)
    
    # 4. Scenario Projections for 2027
    scenarios = project_2027_scenarios(averages)
    print("\n[4] Proyeksi 2027: Tiga Skenario Pertumbuhan (Rentang 124–133 Juta):")
    print("=" * 65)
    for name, info in scenarios.items():
        print(f"• Skenario {name}:")
        print(f"  - Proyeksi Pengguna : {info['proyeksi_2027']} Juta")
        print(f"  - Pertumbuhan vs 2026: +{info['pertumbuhan_vs_2026']}%")
        print(f"  - Estimasi Penetrasi: {info['estimasi_penetrasi']}")
        print(f"  - Asumsi             : {info['asumsi_kunci']}")
        print()
    print("=" * 65)
    
    # 5. Export Output
    export_results_csv(averages, scenarios, OUTPUT_CSV)
    generate_svg_chart(averages, scenarios, OUTPUT_SVG)
    print(f"\n[5] Ekspor Berhasil:")
    print(f"    - File CSV Hasil: {OUTPUT_CSV}")
    print(f"    - Grafik SVG    : {OUTPUT_SVG}")

if __name__ == "__main__":
    main()
