#!/usr/bin/env python3
"""
scripts/generate_all_sna_pngs.py
================================
Menghasilkan grafik visualisasi PNG lengkap dan berkualitas tinggi
untuk seluruh 20 langkah analisis SNA yang belum memiliki berkas PNG.

Membaca CSV dari seluruh folder results/sna_*/ dan menghasilkan:
  - 06_densitas.png
  - 07_komunitas.png
  - 09_jembatan.png
  - 10_rantai-balasan.png
  - 11_resiprositas.png
  - 12_aktor-aktif.png
  - 13_aktor-direspons.png
  - 14_perantara.png
  - 15_aktor-inti.png
  - 16_superfans.png
  - 17_kata-teratas.png
  - 18_pasangan-kata.png
  - 19_emoji-tagar.png
  - 20_waktu.png
"""

import os
import glob
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Styling Material 3 / Modern Clean
plt.rcParams['font.sans-serif'] = 'DejaVu Sans', 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['text.color'] = '#0F172A'
plt.rcParams['axes.labelcolor'] = '#0F172A'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

def shorten(text, max_len=25):
    text = str(text)
    return text[:max_len] + "..." if len(text) > max_len else text

def generate_pngs_for_folder(folder):
    print(f"\n[MEMPROSES] Folder: {folder}")

    # 06. Densitas & Komponen Terhubung
    csv_06 = os.path.join(folder, "06_densitas.csv")
    png_06 = os.path.join(folder, "06_densitas.png")
    if os.path.exists(csv_06) and not os.path.exists(png_06):
        try:
            df = pd.read_csv(csv_06).head(15)
            fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            ax1.barh(y_pos, df['komentator'], color='#EA580C', alpha=0.85, label='Komentator')
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels([shorten(x, 28) for x in df['film']], fontsize=9)
            ax1.invert_yaxis()
            ax1.set_xlabel('Jumlah Akun Komentator', color='#EA580C', fontweight='bold')
            ax1.set_title('06. Densitas Komentator & Sisi Balasan per Film', fontsize=12, fontweight='bold', pad=12)
            ax1.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_06, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 06_densitas.png")
        except Exception as e:
            print(f"  Err 06: {e}")

    # 07. Komunitas Louvain
    csv_07 = os.path.join(folder, "07_komunitas.csv")
    png_07 = os.path.join(folder, "07_komunitas.png")
    if os.path.exists(csv_07) and not os.path.exists(png_07):
        try:
            df = pd.read_csv(csv_07).head(12)
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            bars = ax.bar([f"Grup {g}" for g in df['grup']], df['akun'], color='#2563EB', alpha=0.85)
            ax.set_ylabel('Jumlah Akun Komentator', fontweight='bold')
            ax.set_title('07. Sebaran Anggota per Komunitas Louvain (Q Modularitas)', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:,}', xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
            plt.savefig(png_07, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 07_komunitas.png")
        except Exception as e:
            print(f"  Err 07: {e}")

    # 09. Akun Jembatan Antar-Komunitas (Betweenness)
    csv_09 = os.path.join(folder, "09_jembatan.csv")
    png_09 = os.path.join(folder, "09_jembatan.png")
    if os.path.exists(csv_09) and not os.path.exists(png_09):
        try:
            df = pd.read_csv(csv_09).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            bars = ax.barh(y_pos, df['betweenness'], color='#0D9488', alpha=0.85)
            ax.set_yticks(y_pos)
            labels = [f"{shorten(row['akun'], 14)} ({row['komunitas_tersambung']} grup)" for _, row in df.iterrows()]
            ax.set_yticklabels(labels, fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Skor Betweenness Centrality (Jembatan Informasi)', fontweight='bold')
            ax.set_title('09. Akun Jembatan Kunci Penghubung Antar-Komunitas Warganet', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_09, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 09_jembatan.png")
        except Exception as e:
            print(f"  Err 09: {e}")

    # 10. Rantai Balasan & Persentase Dibalas
    csv_10 = os.path.join(folder, "10_rantai-balasan.csv")
    png_10 = os.path.join(folder, "10_rantai-balasan.png")
    if os.path.exists(csv_10) and not os.path.exists(png_10):
        try:
            df = pd.read_csv(csv_10).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['dibalas_pct'], color='#7C3AED', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 28) for x in df['film']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Persentase Komentar Dibalas (%)', fontweight='bold')
            ax.set_title('10. Tingkat Interaktivitas: Persentase Komentar Induk yang Dibalas', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_10, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 10_rantai-balasan.png")
        except Exception as e:
            print(f"  Err 10: {e}")

    # 11. Resiprositas Balasan
    csv_11 = os.path.join(folder, "11_resiprositas.csv")
    png_11 = os.path.join(folder, "11_resiprositas.png")
    if os.path.exists(csv_11) and not os.path.exists(png_11):
        try:
            df = pd.read_csv(csv_11)
            df = df[df['film'] != 'SEMUA'].head(12)
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['resiprositas'] * 100, color='#DB2777', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 28) for x in df['film']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Rasio Saling Balas / Resiprositas (%)', fontweight='bold')
            ax.set_title('11. Resiprositas Percakapan Dua Arah per Film', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_11, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 11_resiprositas.png")
        except Exception as e:
            print(f"  Err 11: {e}")

    # 12. Aktor Paling Aktif (Out-degree)
    csv_12 = os.path.join(folder, "12_aktor-aktif.csv")
    png_12 = os.path.join(folder, "12_aktor-aktif.png")
    if os.path.exists(csv_12) and not os.path.exists(png_12):
        try:
            df = pd.read_csv(csv_12).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            val_col = 'komentar+balasan_dibuat' if 'komentar+balasan_dibuat' in df.columns else df.columns[1]
            ax.barh(y_pos, df[val_col], color='#059669', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 18) for x in df['akun']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Total Komentar & Balasan Dibuat', fontweight='bold')
            ax.set_title('12. Aktor Paling Aktif Berkomentar (Out-Degree Leader)', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_12, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 12_aktor-aktif.png")
        except Exception as e:
            print(f"  Err 12: {e}")

    # 13. Aktor Paling Banyak Dibalas (In-degree)
    csv_13 = os.path.join(folder, "13_aktor-direspons.csv")
    png_13 = os.path.join(folder, "13_aktor-direspons.png")
    if os.path.exists(csv_13) and not os.path.exists(png_13):
        try:
            df = pd.read_csv(csv_13).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            val_col = 'balasan_diterima' if 'balasan_diterima' in df.columns else df.columns[1]
            ax.barh(y_pos, df[val_col], color='#D97706', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 18) for x in df['akun']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Total Balasan yang Diterima', fontweight='bold')
            ax.set_title('13. Aktor Paling Banyak Memicu Respons Warganet (In-Degree Magnet)', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_13, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 13_aktor-direspons.png")
        except Exception as e:
            print(f"  Err 13: {e}")

    # 14. Aktor Perantara (Betweenness)
    csv_14 = os.path.join(folder, "14_perantara.csv")
    png_14 = os.path.join(folder, "14_perantara.png")
    if os.path.exists(csv_14) and not os.path.exists(png_14):
        try:
            df = pd.read_csv(csv_14).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['betweenness'], color='#4F46E5', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 18) for x in df['akun']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Betweenness Centrality', fontweight='bold')
            ax.set_title('14. Aktor Perantara Utama dalam Jaringan Balasan', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_14, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 14_perantara.png")
        except Exception as e:
            print(f"  Err 14: {e}")

    # 15. Aktor Inti (PageRank)
    csv_15 = os.path.join(folder, "15_aktor-inti.csv")
    png_15 = os.path.join(folder, "15_aktor-inti.png")
    if os.path.exists(csv_15) and not os.path.exists(png_15):
        try:
            df = pd.read_csv(csv_15).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['pagerank'], color='#0284C7', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 18) for x in df['akun']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Nilai PageRank', fontweight='bold')
            ax.set_title('15. Aktor Inti Jaringan Percakapan Komentar (PageRank Centrality)', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_15, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 15_aktor-inti.png")
        except Exception as e:
            print(f"  Err 15: {e}")

    # 16. Superfans (>=3 Film)
    csv_16 = os.path.join(folder, "16_superfans.csv")
    png_16 = os.path.join(folder, "16_superfans.png")
    if os.path.exists(csv_16) and not os.path.exists(png_16):
        try:
            df = pd.read_csv(csv_16).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['jumlah_film'], color='#DC2626', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([shorten(x, 18) for x in df['akun']], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Jumlah Film Unik yang Dikomentari', fontweight='bold')
            ax.set_title('16. Superfans: Akun Loyal yang Mengomentari Banyak Film Bioskop', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_16, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 16_superfans.png")
        except Exception as e:
            print(f"  Err 16: {e}")

    # 17. Kata Teratas
    csv_17 = os.path.join(folder, "17_kata-teratas.csv")
    png_17 = os.path.join(folder, "17_kata-teratas.png")
    if os.path.exists(csv_17) and not os.path.exists(png_17):
        try:
            df = pd.read_csv(csv_17)
            # Ekstrak frekuensi kata
            words = []
            freqs = []
            for _, row in df.head(8).iterrows():
                tokens = str(row['kata_teratas']).split(',')
                for tok in tokens[:3]:
                    m = re.search(r'([a-zA-Z]+)\s*\((\d+)\)', tok.strip())
                    if m:
                        words.append(m.group(1))
                        freqs.append(int(m.group(2)))
            if words:
                sub_df = pd.DataFrame({'kata': words, 'freq': freqs}).drop_duplicates('kata').sort_values('freq', ascending=False).head(15)
                fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
                y_pos = np.arange(len(sub_df))
                ax.barh(y_pos, sub_df['freq'], color='#CA8A04', alpha=0.85)
                ax.set_yticks(y_pos)
                ax.set_yticklabels(sub_df['kata'], fontsize=10)
                ax.invert_yaxis()
                ax.set_xlabel('Frekuensi Kemunculan Kata', fontweight='bold')
                ax.set_title('17. Kata Kunci Paling Sering Diperbincangkan Warganet', fontsize=12, fontweight='bold', pad=12)
                ax.grid(axis='x', linestyle='--', alpha=0.3)
                plt.savefig(png_17, bbox_inches='tight')
                plt.close()
                print("  -> Dibuat: 17_kata-teratas.png")
        except Exception as e:
            print(f"  Err 17: {e}")

    # 18. Pasangan Kata (Bigram)
    csv_18 = os.path.join(folder, "18_pasangan-kata.csv")
    png_18 = os.path.join(folder, "18_pasangan-kata.png")
    if os.path.exists(csv_18) and not os.path.exists(png_18):
        try:
            df = pd.read_csv(csv_18).head(15)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['frekuensi'], color='#9333EA', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(df['pasangan'], fontsize=10)
            ax.invert_yaxis()
            ax.set_xlabel('Frekuensi Kemunculan Pasangan Kata (Bigram)', fontweight='bold')
            ax.set_title('18. Pasangan Kata (Bigram) Terpopuler dalam Komentar YouTube', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_18, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 18_pasangan-kata.png")
        except Exception as e:
            print(f"  Err 18: {e}")

    # 19. Emoji & Tagar Teratas
    csv_19 = os.path.join(folder, "19_emoji-tagar.csv")
    png_19 = os.path.join(folder, "19_emoji-tagar.png")
    if os.path.exists(csv_19) and not os.path.exists(png_19):
        try:
            df = pd.read_csv(csv_19).head(15)
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['frekuensi'], color='#E11D48', alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([f"{row['jenis']}: {row['item']}" for _, row in df.iterrows()], fontsize=10)
            ax.invert_yaxis()
            ax.set_xlabel('Frekuensi Kemunculan', fontweight='bold')
            ax.set_title('19. Emoji & Tagar Paling Dominan dalam Respons Warganet', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_19, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 19_emoji-tagar.png")
        except Exception as e:
            print(f"  Err 19: {e}")

    # 20. Jaringan per Jendela Waktu
    csv_20 = os.path.join(folder, "20_waktu.csv")
    png_20 = os.path.join(folder, "20_waktu.png")
    if os.path.exists(csv_20) and not os.path.exists(png_20):
        try:
            df = pd.read_csv(csv_20).head(12)
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            y_pos = np.arange(len(df))
            ax.barh(y_pos, df['komentar'], color='#0891B2', alpha=0.85)
            ax.set_yticks(y_pos)
            labels = [f"{shorten(row['film'], 20)} ({row['jendela']})" for _, row in df.iterrows()]
            ax.set_yticklabels(labels, fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Jumlah Komentar per Jendela Rilis', fontweight='bold')
            ax.set_title('20. Distribusi Volume Percakapan Berdasarkan Jendela Waktu Penayangan', fontsize=12, fontweight='bold', pad=12)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            plt.savefig(png_20, bbox_inches='tight')
            plt.close()
            print("  -> Dibuat: 20_waktu.png")
        except Exception as e:
            print(f"  Err 20: {e}")

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(repo_root, "results")
    sna_folders = sorted(glob.glob(os.path.join(results_dir, "sna_*")))
    
    print(f"Ditemukan {len(sna_folders)} folder SNA di results/:")
    for f in sna_folders:
        generate_pngs_for_folder(f)

    print("\n✅ SELESAI: Seluruh grafik PNG yang sebelumnya absen kini telah terbuat secara otomatis!")

if __name__ == "__main__":
    main()
