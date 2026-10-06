# Audit SANTET · GitHub + Streamlit

_06-10-2026 16:01 WIB · hasil: **❌ ADA MASALAH KRITIS**_

| Kode | Level | Pemeriksaan | Keterangan |
|---|---|---|---|
| G1 | INFO | Remote GitHub | movie-prediksi → https://github.com/indri007/prediksi-movie-2027.git |
| G3 | OK | Lokal vs GitHub | lokal lebih maju 0 commit, tertinggal 0 commit |
| G4 | PERINGATAN | Perubahan belum di-commit | 8 file diubah, 23 file/folder baru |
| G5 | PERINGATAN | File penting belum ada di GitHub | 7 item hanya ada di laptop |
| S1 | INFO | Entrypoint Streamlit di GitHub | kemungkinan dijalankan: streamlit_app.py |
| S2 | KRITIS | Entrypoint memanggil file yang tidak ada di GitHub | streamlit_app.py → streamlit_app/app.py belum di-push |
| S3 | KRITIS | Proyek yang tampil di Streamlit | ? — bukan SANTET; push streamlit_app.py + streamlit_app/ atau ubah Main file path |
| S4 | OK | Tidak ada klaim bermasalah di streamlit_app.py |  |
| S5 | INFO | URL Streamlit tidak bisa dicek otomatis | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> · buka manual: https://santet-soraya-film-explorer-vw6emk9y9yavz2cxuaghkj.streamlit.app/ |
| C1 | KRITIS | Klaim bermasalah di folder kerja (kritis) | 19 baris di 6 file |
| C2 | PERINGATAN | Klaim bermasalah di folder kerja (peringatan) | 15 baris di 5 file |
| D1 | OK | Angka di landing page vs data | Suzzanna 2018=3.346.216; Racun Sangga 2024=525.034; rho likes=0,571; % negatif model=51,2; % negatif leksikon=10,0 |
| K1 | OK | Token / API key di repo | tidak ditemukan |
| K3 | OK | Teks komentar mentah di GitHub (UU PDP) | tidak ada |

## Bukti

**G3 · Lokal vs GitHub**
- `lokal  : dc610e8 chore(release): update final clean dataset and LOOCV model output`
- `GitHub : dc610e8 chore(release): update final clean dataset and LOOCV model output`

**G4 · Perubahan belum di-commit**
- `M AUDIT_REPORT.md`
- ` M README.md`
- ` M annotation/llm_labels_all.csv`
- ` M bit`
- ` M data/trends/trends_long.csv`
- ` M paper_tools.py`
- ` M results/paper_status.md`
- ` M streamlit_app.py`

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

**C1 · Klaim bermasalah di folder kerja (kritis)**
- `verify_and_validate_all.py:205: print_header("5. VALIDASI NASKAH JURNAL SCOPUS Q1 ELSEVIER & DOWNLOADS") — status 'Scopus Q1' padahal belum terbit`
- `align_elsevier_kpi_formulas_bit.py:179: "compliance_summary": "100% KPI MATCHED AND VERIFIED", — klaim '100% KPI matched'`
- `build_scopus_q1_journal.py:50: **Artifact Digital Identifier:** DOI: 10.1016/j.ipm.2026.103982 | Scopus ID: 8518920194 — DOI Elsevier untuk naskah yang belum terbit`
- `build_scopus_q1_journal.py:50: **Artifact Digital Identifier:** DOI: 10.1016/j.ipm.2026.103982 | Scopus ID: 8518920194 — Scopus ID yang tidak terverifikasi`
- `build_scopus_q1_journal.py:245: self.drawRightString(555, 810, "DOI: 10.1016/j.ipm.2026.103982") — DOI Elsevier untuk naskah yang belum terbit`
- `build_scopus_q1_journal.py:712: f"=== SCOPUS Q1 ELSEVIER ACADEMIC MANUSCRIPT & KPI AUDIT (BAHASA BIT) ===\n" — status 'Scopus Q1' padahal belum terbit`
- `build_scopus_q1_journal.py:716: f"DOI: 10.1016/j.ipm.2026.103982\n" — DOI Elsevier untuk naskah yang belum terbit`
- `build_scopus_q1_journal.py:775: "doi": "10.1016/j.ipm.2026.103982", — DOI Elsevier untuk naskah yang belum terbit`
- `build_scopus_q1_journal.py:776: "status": "100% KPI MATCHED AND VERIFIED", — klaim '100% KPI matched'`
- `docs/DESIGN.md:71: - Jangan gunakan badge "Scopus Q1 Ready", "Akurasi Tinggi", atau klaim serupa sebelum ada  — status 'Scopus Q1' padahal belum terbit`
- `dashboard/app.py:298: # FEATURED: Scopus Q1 Elsevier Academic Journal & Instant Download Hub — status 'Scopus Q1' padahal belum terbit`
- `dashboard/app.py:304: <span class="badge-available">SCOPUS Q1 ELSEVIER</span> — status 'Scopus Q1' padahal belum terbit`

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
- `docs/DESIGN.md:128: - Jangan gunakan `file:///` atau path absolut lokal. — link ke file di laptop (rusak di GitHub/Streamlit)`
