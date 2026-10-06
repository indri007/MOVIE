# PRD SANTET

_06-10-2026 23:32 WIB · Indri Anjar Kartika Sari · dibuat otomatis oleh `./bit prd` — status & baseline dihitung dari repo_

**SANTET — Sentiment Analysis for Nusantara Theatrical Expectation Tracking** — Membaca 'mantra' warganet sebelum film tayang · Fear is demand

## Ringkasan eksekutif

SANTET (Sentiment Analysis for Nusantara Theatrical Expectation Tracking) adalah perangkat riset terbuka yang membaca sinyal digital pra-rilis film horor Indonesia untuk memperkirakan minat menonton.

Setiap film lahir dari kerja bertahun-tahun, tetapi nasibnya baru diketahui setelah layar menyala. Padahal penonton sudah memberi tanda jauh sebelumnya: di kolom komentar trailer, mereka menulis "serem banget" dan "gas nonton". SANTET hadir agar suara itu terdengar tepat waktu, saat keputusan masih bisa diubah.

> Riset akademik independen; tidak berafiliasi dengan Soraya Intercine Films, Hitmaker Studios, atau MD Pictures.

**Fase aktif:** v1.0 · Riset jujur

## Kebutuhan fungsional

| ID | Kebutuhan | Prioritas | Kriteria terima | Status | Bukti |
|---|---|---|---|---|---|
| F-01 | ./bit scrape/convert: metadata & komentar trailer, akun dipseudonimkan | Must | Tidak ada nama akun asli; salt sama = ID sama | ✅ Ada | 4 set, akun terpseudonim |
| F-02 | ./bit precise: komentar via YouTube Data API dengan tanggal tepat | Must | Timestamp asli; jendela H-14/H-7/H-1 terisi | ⏳ Menunggu | API key belum ada: ./bit secret set YT_API_KEY · 6 folder kosong (run gagal) |
| F-03 | ./bit sentiment validate: κ & F1 terhadap label manusia | Must | ≥ 100 baris dua anotator; laporan κ dan F1 | ⏳ Menunggu | 0 baris berlabel dua anotator (target ≥ 100) |
| F-04 | Watch Intent Index per komentar | Must | Tervalidasi label manusia, κ ≥ 0,80 | ⬜ Belum | hanya kategori kata kunci (sna 04_warna-niat), belum tervalidasi |
| F-05 | ./bit correlate/robust: Spearman eksak, bootstrap, Bonferroni, BH, parsial | Must | Semua uji dilaporkan, termasuk yang tidak signifikan | ✅ Ada | results/robust_20261006_1252/robustness.csv · lolos BH 0/10 |
| F-06 | ./bit model: LOOCV vs baseline naif dengan CI MAPE | Must | Laporan menyatakan model menang/kalah | 🟡 Sebagian | MAPE model 85.8% vs baseline 70.3% · belum mengalahkan baseline |
| F-07 | ./bit sna: 20 analisis jaringan + ekspor NodeXL | Should | edges/vertices terbuka di NodeXL Pro | ✅ Ada | results/sna_20261006_2331/nodexl/edges.csv |
| F-08 | ./bit package: paket rilis tanpa teks + MANIFEST SHA-256 | Must | Checksum cocok; tanpa kolom teks | ✅ Ada | release/paper_package_20261006_2331/MANIFEST.sha256 |
| F-09 | ./bit audit: git, Streamlit, klaim, angka, rahasia | Must | 0 kritis sebelum setiap rilis | ✅ Ada | audit terakhir: ⚠️  ADA PERINGATAN (0 kritis) |
| F-10 | ./bit secret: Keychain + blokir commit berisi token | Must | scan bersih; hook aktif | ✅ Ada | pre-commit hook aktif |
| F-11 | Dashboard Streamlit SANTET membaca results/ terbaru | Should | Angka dashboard = results/ | 🟡 Sebagian | streamlit_app/app.py ada · cek tampilan live & Reboot app |
| F-12 | ./bit intro: draf Introduction dengan angka otomatis | Could | Angka ikut berubah saat pipeline diulang | ✅ Ada | diperbarui 06-10-2026 23:31 |
| F-13 | Kalkulator prediksi untuk produser | Won't (v1.0) | Setelah model mengalahkan baseline | ➖ Ditunda | dibuka hanya setelah gerbang v2.0 lolos |

## Metrik keberhasilan

| Metrik | Hari ini | Target v1.0 | Target v2.0 |
|---|---|---|---|
| Film dengan penonton bersumber | 15 | 15 | ≥ 40 |
| Label manusia (dua anotator) | 0 baris | ≥ 100, κ ≥ 0,80 | ≥ 300 |
| κ antar-anotator LLM (pembanding) | 0.536 | dilaporkan | - |
| Uji korelasi lolos BH (q < 0,05) | 0 dari 10 | dilaporkan | ≥ 1 sinyal pra-rilis |
| MAPE model vs baseline | 85.8% vs 70.3% | dilaporkan | model < baseline, CI terpisah |
| Pengambilan API presisi | 0 run | semua set | semua set |
| Hasil ./bit audit | ⚠️  ADA PERINGATAN (0 kritis) | 0 kritis | 0 kritis, 0 peringatan |

## Gerbang rilis

**v1.0 · Riset jujur** — 100 label manusia, 2 anotator · Salt baru, results/ diulang · Paper explanatory dikirim
- [x] ./bit audit: 0 kritis
- [ ] ≥ 100 label manusia
- [ ] κ antar-anotator manusia ≥ 0,80
- [x] Salt default tidak lagi tertulis di kode

**v1.1 · Data presisi** — Komentar via YouTube API · Jendela H-14 / H-7 / H-1 · Watch Intent Index tervalidasi
- [ ] Data YouTube API presisi tersedia
- [ ] Watch Intent Index tervalidasi (F-04)

**v2.0 · Prediktif** — Ekspansi ke 40+ film · Model dibanding baseline · Kalkulator untuk produser
- [ ] ≥ 40 film bersumber
- [ ] MAPE model < baseline
- [ ] CI MAPE model dan baseline tidak tumpang tindih

## Keputusan

- [ ] Setuju v1.0 diposisikan sebagai riset explanatory (n = 15) dan klaim prediktif ditunda ke v2.0?
- [x] Ganti salt pseudonim kapan? (semua ID berubah, results/ dibuat ulang) → **Sekarang, sebelum rilis dataset** (2026-10-06 23:27)
- [ ] Siapa anotator kedua dan kapan 100 baris label selesai?
- [x] Repo GitHub untuk SANTET? → **Tetap prediksi-movie-2027** (2026-10-06 23:27)
- [x] Jurnal target pertama? → **Jalur data (mis. Telematics and Informatics)** (2026-10-06 23:27)
- [x] Angka κ 0,8342 dan MAPE 1,55% di script proyek Instagram? → **Ada sumber hitungannya (simpan & tautkan)** (2026-10-06 23:27)
