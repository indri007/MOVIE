# Audit SANTET · GitHub + Streamlit

_06-10-2026 23:06 WIB · hasil: **❌ ADA MASALAH KRITIS**_

| Kode | Level | Pemeriksaan | Keterangan |
|---|---|---|---|
| G1 | INFO | Remote GitHub | movie-prediksi → https://github.com/indri007/prediksi-movie-2027.git |
| G2 | OK | git fetch | berhasil |
| G3 | PERINGATAN | Lokal vs GitHub | lokal lebih maju 1 commit, tertinggal 0 commit |
| G4 | OK | Perubahan belum di-commit | 0 file diubah, 0 file/folder baru |
| G5 | PERINGATAN | File penting belum ada di GitHub | 7 item hanya ada di laptop |
| S1 | INFO | Entrypoint Streamlit di GitHub | kemungkinan dijalankan: streamlit_app.py |
| S2 | KRITIS | Entrypoint memanggil file yang tidak ada di GitHub | streamlit_app.py → streamlit_app/app.py belum di-push |
| S3 | KRITIS | Proyek yang tampil di Streamlit | ? — bukan SANTET; push streamlit_app.py + streamlit_app/ atau ubah Main file path |
| S4 | OK | Tidak ada klaim bermasalah di streamlit_app.py |  |
| S5 | INFO | URL Streamlit tidak bisa dicek otomatis | URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issue · buka manual: https://santet-soraya-film-explorer-vw6emk9y9yavz2cxuaghkj.streamlit.app/ |
| C2 | PERINGATAN | Klaim bermasalah di folder kerja (peringatan) | 14 baris di 5 file |
| D1 | OK | Angka di landing page vs data | Suzzanna 2018=3.346.216; Racun Sangga 2024=525.034; rho likes=0,571; % negatif model=51,2; % negatif leksikon=10,0 |
| K1 | KRITIS | Token / API key di repo | 1 temuan (nilai tidak ditampilkan) |
| K2 | OK | Token GitHub di ~/.zsh_history | bersih |
| K3 | OK | Teks komentar mentah di GitHub (UU PDP) | tidak ada |

## Bukti

**G3 · Lokal vs GitHub**
- `lokal  : 2d92ba7 SANTET: pipeline bit (sna, audit, intro), Streamlit app, halaman 3D docs, perbaikan klaim (working paper)`
- `GitHub : 330368e docs(readme): add data pipeline transparency section detailing volumes, cleaning counts, training partitions, and IndoBERT fine-tuning`
- `GitHub tidak memuat commit terbaru lokal → Streamlit & Pages menjalankan versi lama`

**G5 · File penting belum ada di GitHub**
- `streamlit_app`
- `docs/santet`
- `docs/santet-3d`
- `docs/assets`
- `sna_youtube.py`
- `intro_draft.py`
- `audit_repo.py`

**S1 · Entrypoint Streamlit di GitHub**
- `tersedia di GitHub: streamlit_app.py, dashboard/app.py`
- `Cek di Streamlit Cloud → Manage app → Settings → 'Main file path' harus sama`

**C2 · Klaim bermasalah di folder kerja (peringatan)**
- `align_elsevier_kpi_formulas_bit.py:54: cohens_kappa = 0.8342 — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `align_elsevier_kpi_formulas_bit.py:67: "elsevier_benchmark": "< 10.0% (Highly Accurate, Lewis 1982)", — klaim akurasi tanpa dasar`
- `align_elsevier_kpi_formulas_bit.py:206: "- MAPE: 1.55% (Lewis 1982 Benchmark: < 10% = Highly Accurate) [EXCEEDED]", — klaim akurasi tanpa dasar`
- `build_scopus_q1_journal.py:40: Our methodological framework was rigorously benchmarked against Elsevier Scopus Q1 standar — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `build_scopus_q1_journal.py:124: | **Forecasting Accuracy** | KPI-FC-01 | MAPE | $\\frac{{100\\%}}{{n}} \\sum \\|\\frac{{y_ — klaim akurasi tanpa dasar`
- `build_scopus_q1_journal.py:150: Inter-coder agreement verified using Cohen's Kappa reached $\\kappa = 0.8342$, confirming  — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `build_scopus_q1_journal.py:393: "Specifically, our work contributes: (1) An empirical formulation and simplex normalizatio — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `build_scopus_q1_journal.py:435: Paragraph("&lt; 10.0% (Lewis 1982 Highly Accurate)", table_cell), — klaim akurasi tanpa dasar`
- `build_scopus_q1_journal.py:632: "Specifically, our work contributes: (1) An empirical formulation and simplex normalizatio — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `build_scopus_q1_journal.py:723: f"4. Affective Cohen's Kappa = 0.8342, ANOVA F = 69.74 (p < 0.0001), eta^2 = 0.1043\n" — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `build_repo_story_bit.py:77: - Inter-Annotator Agreement (Cohen's Kappa): kappa = 0.8342 (Landis & Koch "Almost Perfect — Cohen's kappa 0,83 tidak cocok dengan validation_result.json`
- `docs/DESIGN.md:137: - [ ] Semua link di README tidak mengarah ke `file:///` atau path lokal — link ke file di laptop (rusak di GitHub/Streamlit)`

**K1 · Token / API key di repo**
- `riwayat git 2d92ba7 SANTET: pipeline bit (sna, audit, intro), Streamlit app, halaman 3D docs, perbaikan klaim (working paper)`
