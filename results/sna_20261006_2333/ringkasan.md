# SANTET · Analisis Jaringan Komentar YouTube

_06-10-2026 23:34 · 9,712 komentar · 7,391 akun (pseudonim) · 18 film · set: hitmaker, ivanna, md, soraya_

## 01. Peta jaringan keseluruhan (komentator–film + balasan)

Simpul: 7,409 · sisi: 9,858. Gambar `01_peta.png` (dibatasi komentator dengan derajat tertinggi agar terbaca); graf penuh `01_peta.graphml` bisa dibuka di NodeXL/Gephi.

## 02. Group-in-a-Box: tiap komunitas dalam kotak sendiri

`02_grup-kotak.png` menampilkan 9 komunitas terbesar (maks. 400 simpul per kotak).

## 03. Graf balasan per film (small multiples)

`03_per-film.png` · angka di `03_per-film.csv`.

| film                                             |   simpul_balasan |   sisi_balasan |
|:-------------------------------------------------|-----------------:|---------------:|
| Suzzanna: Malam Jumat Kliwon (2023)              |              309 |            288 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        |              272 |            255 |
| Indigo: What Do You See? (2023)                  |              135 |            120 |
| Jurnal Risa by Risa Saraswati (2024)             |              179 |            163 |
| The Doll 3 (2022)                                |              165 |            129 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)       |              136 |            107 |
| Official Trailer IVANNA (2022) - MD Pictures     |               88 |             95 |
| Badarawuhi di Desa Penari (2024)                 |               86 |             69 |
| Suzzanna: Bernapas dalam Kubur (2018)            |              105 |             72 |
| Ipar Adalah Maut (2024)                          |               82 |             94 |
| Santet Segoro Pitu (2024)                        |              120 |             98 |
| Ivanna (2022)                                    |               53 |             50 |
| Danur: The Last Chapter (2026)                   |               98 |             94 |
| Perewangan (2024)                                |              122 |            101 |
| Catatan Harian Menantu Sinting (2024)            |               71 |             49 |
| Racun Sangga: Santet Pemisah Rumah Tangga (2024) |               75 |             61 |
| Mata Batin (2017)                                |               49 |             35 |
| Siccin 8                                         |                9 |              5 |

## 04. Graf berwarna kategori komentar (takut / niat menonton / lain)

`04_warna-niat.png` · `04_warna-niat.csv`. Kategori dari kata kunci, bukan model — perlu validasi label manusia.

| kategori        |   persen_komentar |
|:----------------|------------------:|
| lain            |              80.6 |
| takut (pujian?) |              11.9 |
| niat menonton   |               7.5 |

## 05. Proyeksi film–film: tebal garis = komentator bersama

`05_film-film.png` · `05_film-film.csv`

| film_a                                       | film_b                                     |   komentator_bersama |
|:---------------------------------------------|:-------------------------------------------|---------------------:|
| Suzzanna: Malam Jumat Kliwon (2023)          | Suzzanna: Santet Dosa di Atas Dosa (2026)  |                   50 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)   | Suzzanna: Santet Dosa di Atas Dosa (2026)  |                   41 |
| Danur: The Last Chapter (2026)               | Suzzanna: Santet Dosa di Atas Dosa (2026)  |                   34 |
| Indigo: What Do You See? (2023)              | Suzzanna: Malam Jumat Kliwon (2023)        |                   30 |
| Danur: The Last Chapter (2026)               | Janur Ireng: Sewu Dino Prequel (2025/2026) |                   26 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)   | Suzzanna: Malam Jumat Kliwon (2023)        |                   25 |
| Jurnal Risa by Risa Saraswati (2024)         | Suzzanna: Malam Jumat Kliwon (2023)        |                   18 |
| Suzzanna: Bernapas dalam Kubur (2018)        | Suzzanna: Malam Jumat Kliwon (2023)        |                   18 |
| Official Trailer IVANNA (2022) - MD Pictures | Suzzanna: Malam Jumat Kliwon (2023)        |                   17 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)   | Jurnal Risa by Risa Saraswati (2024)       |                   15 |

## 06. Densitas & komponen terhubung per film

`06_densitas.csv`. Densitas pada graf balasan per film.

| film                                             |   komentator |   sisi_balasan |   densitas |   komponen |   komponen_terbesar_% |   terisolasi_% |
|:-------------------------------------------------|-------------:|---------------:|-----------:|-----------:|----------------------:|---------------:|
| Suzzanna: Malam Jumat Kliwon (2023)              |         1421 |            288 |   0.000285 |       1160 |                  13.3 |           78.3 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        |          985 |            255 |   0.000526 |        750 |                  19.6 |           72.4 |
| Jurnal Risa by Risa Saraswati (2024)             |          650 |            163 |   0.000773 |        496 |                  15.7 |           72.5 |
| Indigo: What Do You See? (2023)                  |          616 |            120 |   0.000634 |        503 |                  10.2 |           78.1 |
| The Doll 3 (2022)                                |          535 |            129 |   0.000903 |        414 |                   6.2 |           69.2 |
| Official Trailer IVANNA (2022) - MD Pictures     |          468 |             95 |   0.000869 |        382 |                  17.9 |           81.2 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)       |          442 |            107 |   0.001098 |        336 |                   5.2 |           69.2 |
| Suzzanna: Bernapas dalam Kubur (2018)            |          438 |             72 |   0.000752 |        367 |                   2.7 |           76   |
| Badarawuhi di Desa Penari (2024)                 |          415 |             69 |   0.000803 |        348 |                   5.8 |           79.3 |
| Santet Segoro Pitu (2024)                        |          369 |             98 |   0.001443 |        275 |                  13.6 |           67.5 |
| Ipar Adalah Maut (2024)                          |          353 |             94 |   0.001513 |        274 |                  22.1 |           76.8 |
| Ivanna (2022)                                    |          281 |             50 |   0.001271 |        234 |                  13.2 |           81.1 |
| Danur: The Last Chapter (2026)                   |          251 |             94 |   0.002996 |        164 |                  27.5 |           61   |
| Perewangan (2024)                                |          246 |            101 |   0.003352 |        147 |                  13   |           50.4 |
| Catatan Harian Menantu Sinting (2024)            |          234 |             49 |   0.001797 |        187 |                   4.7 |           69.7 |
| Racun Sangga: Santet Pemisah Rumah Tangga (2024) |          168 |             61 |   0.004348 |        107 |                  22   |           55.4 |
| Mata Batin (2017)                                |           83 |             35 |   0.010285 |         48 |                  18.1 |           41   |
| Siccin 8                                         |           21 |              5 |   0.02381  |         16 |                  14.3 |           57.1 |

## 07. Komunitas Louvain + modularitas Q

Louvain (seed 42) → 18 komunitas, modularitas **Q = 0.835** (struktur komunitas kuat). `07_komunitas.csv`

|   grup |   akun | film_dalam_grup                |
|-------:|-------:|:-------------------------------|
|      1 |   1309 | Suzzanna: Malam Jumat Kliwon   |
|      2 |    850 | Suzzanna: Santet Dosa di Atas… |
|      3 |    604 | Jurnal Risa by Risa Saraswati  |
|      4 |    571 | Indigo: What Do You See?       |
|      5 |    517 | The Doll 3                     |
|      6 |    430 | Official Trailer IVANNA (2022… |
|      7 |    412 | Suzzanna: Bernapas dalam Kubur |
|      8 |    399 | Badarawuhi di Desa Penari      |
|      9 |    383 | Janur Ireng: Sewu Dino Preque… |
|     10 |    356 | Santet Segoro Pitu             |
|     11 |    338 | Ipar Adalah Maut               |
|     12 |    279 | Ivanna                         |
|     13 |    233 | Danur: The Last Chapter        |
|     14 |    227 | Perewangan                     |
|     15 |    221 | Catatan Harian Menantu Sinting |

## 08. Irisan penonton antar-film (Jaccard)

426 dari 7,391 akun (5.8%) berkomentar di ≥2 film. `08_irisan.png` · `08_irisan.csv`

## 09. Akun jembatan antar-komunitas

Betweenness aproksimasi (k=400 sampel) pada graf komentator–film. `09_jembatan.csv`

| akun              |   betweenness |   komunitas_tersambung | film                                                                                                                                                                             |
|:------------------|--------------:|-----------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user_420746dfe39f |       0.03994 |                     10 | Catatan Harian Mena…; Danur: The Last Cha…; Indigo: What Do You…; Janur Ireng: Sewu D…; Jurnal Risa by Risa…; Mata Batin; Racun Sangga: Sante…; Suzzanna: Santet Do…; The Doll 3 |
| user_8dfbe436bafd |       0.02975 |                      7 | Badarawuhi di Desa …; Indigo: What Do You…; Mata Batin; Official Trailer IV…; Perewangan; Suzzanna: Bernapas …; The Doll 3                                                       |
| user_ed49989a3225 |       0.02559 |                      8 | Badarawuhi di Desa …; Danur: The Last Cha…; Jurnal Risa by Risa…; Official Trailer IV…; Suzzanna: Malam Jum…; Suzzanna: Santet Do…                                               |
| user_bc1cd6f06fbc |       0.01873 |                      5 | Badarawuhi di Desa …; Catatan Harian Mena…; Indigo: What Do You…; Jurnal Risa by Risa…; Suzzanna: Malam Jum…                                                                     |
| user_e83f0d434910 |       0.01851 |                      5 | Ipar Adalah Maut; Official Trailer IV…; Suzzanna: Malam Jum…; Suzzanna: Santet Do…; The Doll 3                                                                                   |
| user_4b992b83d60d |       0.01706 |                      5 | Badarawuhi di Desa …; Indigo: What Do You…; Jurnal Risa by Risa…; Racun Sangga: Sante…; Suzzanna: Malam Jum…                                                                     |
| user_6138efaa569c |       0.01627 |                      6 | Janur Ireng: Sewu D…; Official Trailer IV…; Racun Sangga: Sante…; Suzzanna: Malam Jum…; The Doll 3                                                                               |
| user_0b3d09c62210 |       0.01483 |                      7 | Danur: The Last Cha…; Ipar Adalah Maut; Janur Ireng: Sewu D…; Perewangan; Suzzanna: Malam Jum…; Suzzanna: Santet Do…                                                             |
| user_ad1d60dd0fe9 |       0.01475 |                      5 | Catatan Harian Mena…; Indigo: What Do You…; Suzzanna: Malam Jum…; Suzzanna: Santet Do…; The Doll 3                                                                               |
| user_fa7f96025493 |       0.0144  |                      5 | Indigo: What Do You…; Ivanna; Suzzanna: Bernapas …; Suzzanna: Malam Jum…; The Doll 3                                                                                             |

## 10. Ukuran thread & persentase komentar yang dibalas

YouTube hanya punya satu tingkat balasan, jadi 'rantai' diukur sebagai ukuran thread. `10_rantai-balasan.csv`

| film                                             |   komentar_induk |   dibalas_pct |   rata_balasan |   thread_terpanjang |
|:-------------------------------------------------|-----------------:|--------------:|---------------:|--------------------:|
| Mata Batin (2017)                                |               57 |          35.1 |           0.58 |                   7 |
| Siccin 8                                         |               16 |          25   |           0.31 |                   2 |
| Danur: The Last Chapter (2026)                   |              222 |          20.7 |           0.33 |                   5 |
| Perewangan (2024)                                |              185 |          20.5 |           0.48 |                  18 |
| Racun Sangga: Santet Pemisah Rumah Tangga (2024) |              130 |          20   |           0.46 |                  15 |
| The Doll 3 (2022)                                |              497 |          14.9 |           0.25 |                   6 |
| Suzzanna: Bernapas dalam Kubur (2018)            |              409 |          14.9 |           0.18 |                   4 |
| Catatan Harian Menantu Sinting (2024)            |              203 |          13.8 |           0.21 |                   8 |
| Santet Segoro Pitu (2024)                        |              312 |          13.8 |           0.26 |                   8 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)       |              404 |          13.6 |           0.21 |                  10 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        |              917 |          13.1 |           0.24 |                  18 |
| Jurnal Risa by Risa Saraswati (2024)             |              597 |          12.9 |           0.23 |                   9 |
| Indigo: What Do You See? (2023)                  |              638 |          12.1 |           0.19 |                   9 |
| Ivanna (2022)                                    |              272 |          10.7 |           0.17 |                   5 |
| Badarawuhi di Desa Penari (2024)                 |              400 |          10.5 |           0.16 |                   4 |
| Ipar Adalah Maut (2024)                          |              326 |          10.4 |           0.28 |                  11 |
| Suzzanna: Malam Jumat Kliwon (2023)              |             1376 |           8.2 |           0.17 |                  28 |
| Official Trailer IVANNA (2022) - MD Pictures     |              400 |           2   |           0.2  |                  52 |

## 11. Resiprositas balasan (saling membalas)

Proporsi sisi balasan yang dibalas balik. `11_resiprositas.csv`

| film                                             |   pasangan |   resiprositas |
|:-------------------------------------------------|-----------:|---------------:|
| SEMUA                                            |       2101 |         0.2075 |
| Badarawuhi di Desa Penari (2024)                 |         77 |         0.2078 |
| Catatan Harian Menantu Sinting (2024)            |         52 |         0.1154 |
| Danur: The Last Chapter (2026)                   |        107 |         0.243  |
| Indigo: What Do You See? (2023)                  |        136 |         0.2353 |
| Ipar Adalah Maut (2024)                          |         98 |         0.0816 |
| Ivanna (2022)                                    |         65 |         0.4615 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)       |        128 |         0.3281 |
| Jurnal Risa by Risa Saraswati (2024)             |        185 |         0.2378 |
| Mata Batin (2017)                                |         40 |         0.25   |
| Official Trailer IVANNA (2022) - MD Pictures     |         98 |         0.0612 |
| Perewangan (2024)                                |        110 |         0.1636 |
| Racun Sangga: Santet Pemisah Rumah Tangga (2024) |         65 |         0.1231 |
| Santet Segoro Pitu (2024)                        |        109 |         0.2018 |
| Siccin 8                                         |          5 |         0      |
| Suzzanna: Bernapas dalam Kubur (2018)            |         79 |         0.1772 |
| Suzzanna: Malam Jumat Kliwon (2023)              |        321 |         0.2056 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        |        280 |         0.1786 |
| The Doll 3 (2022)                                |        147 |         0.2449 |

## 12. Aktor paling aktif (out-degree)

`12_aktor-aktif.csv`

| akun              |   komentar+balasan_dibuat | film                                                                                                                   |
|:------------------|--------------------------:|:-----------------------------------------------------------------------------------------------------------------------|
| user_5f75706e0cdf |                        38 | Indigo: What Do Y…                                                                                                     |
| user_dd616835d271 |                        36 | Danur: The Last C…; Janur Ireng: Sewu…; Racun Sangga: San…; Siccin 8; Suzzanna: Santet …                               |
| user_ed49989a3225 |                        30 | Badarawuhi di Des…; Danur: The Last C…; Jurnal Risa by Ri…; Official Trailer …; Suzzanna: Malam J…; Suzzanna: Santet … |
| user_06fdbbd67398 |                        29 | Janur Ireng: Sewu…; Suzzanna: Malam J…; Suzzanna: Santet …                                                             |
| user_f7eb7d098ca9 |                        28 | Jurnal Risa by Ri…                                                                                                     |
| user_52c7cf99cad3 |                        26 | Ivanna                                                                                                                 |
| user_65c4e0cf747d |                        26 | Ipar Adalah Maut                                                                                                       |
| user_ef42b4c3bad7 |                        20 | Indigo: What Do Y…; Suzzanna: Malam J…                                                                                 |
| user_2ddcd5ac3326 |                        18 | Mata Batin; The Doll 3                                                                                                 |
| user_ad1d60dd0fe9 |                        17 | Catatan Harian Me…; Indigo: What Do Y…; Suzzanna: Malam J…; Suzzanna: Santet …; The Doll 3                             |

## 13. Aktor paling banyak dibalas (in-degree)

`13_aktor-direspons.csv`

| akun              |   balasan_diterima | film                                                                                                                                                               |
|:------------------|-------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user_480f5add592c |                 52 | Official Trailer …                                                                                                                                                 |
| user_0b3d09c62210 |                 38 | Danur: The Last C…; Ipar Adalah Maut; Janur Ireng: Sewu…; Perewangan; Suzzanna: Malam J…; Suzzanna: Santet …                                                       |
| user_523c8c99297c |                 28 | Suzzanna: Malam J…                                                                                                                                                 |
| user_6f78a844ba5e |                 20 | Suzzanna: Santet …                                                                                                                                                 |
| user_a9e3afa36b48 |                 19 | Indigo: What Do Y…; Official Trailer …; Santet Segoro Pitu; Suzzanna: Malam J…                                                                                     |
| user_52c7cf99cad3 |                 19 | Ivanna                                                                                                                                                             |
| user_9dba45c81d5c |                 18 | Official Trailer …                                                                                                                                                 |
| user_7921142f4fb8 |                 18 | Perewangan                                                                                                                                                         |
| user_b766f1f64ed4 |                 17 | Suzzanna: Malam J…; Suzzanna: Santet …                                                                                                                             |
| user_420746dfe39f |                 17 | Catatan Harian Me…; Danur: The Last C…; Indigo: What Do Y…; Janur Ireng: Sewu…; Jurnal Risa by Ri…; Mata Batin; Racun Sangga: San…; Suzzanna: Santet …; The Doll 3 |

## 14. Aktor perantara (betweenness)

Pada graf balasan (aproksimasi k=500). `14_perantara.csv`

| akun              |   betweenness | film                                                                                                                                                               |
|:------------------|--------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user_ed49989a3225 |      0.122954 | Badarawuhi di Des…; Danur: The Last C…; Jurnal Risa by Ri…; Official Trailer …; Suzzanna: Malam J…; Suzzanna: Santet …                                             |
| user_dd616835d271 |      0.103575 | Danur: The Last C…; Janur Ireng: Sewu…; Racun Sangga: San…; Siccin 8; Suzzanna: Santet …                                                                           |
| user_0b3d09c62210 |      0.080903 | Danur: The Last C…; Ipar Adalah Maut; Janur Ireng: Sewu…; Perewangan; Suzzanna: Malam J…; Suzzanna: Santet …                                                       |
| user_72fcd77aa215 |      0.063199 | Suzzanna: Malam J…; Suzzanna: Santet …; The Doll 3                                                                                                                 |
| user_ef42b4c3bad7 |      0.048159 | Indigo: What Do Y…; Suzzanna: Malam J…                                                                                                                             |
| user_480f5add592c |      0.04742  | Official Trailer …                                                                                                                                                 |
| user_2578d624d4e9 |      0.046979 | Santet Segoro Pitu; Suzzanna: Malam J…; Suzzanna: Santet …                                                                                                         |
| user_f7eb7d098ca9 |      0.046851 | Jurnal Risa by Ri…                                                                                                                                                 |
| user_420746dfe39f |      0.04596  | Catatan Harian Me…; Danur: The Last C…; Indigo: What Do Y…; Janur Ireng: Sewu…; Jurnal Risa by Ri…; Mata Batin; Racun Sangga: San…; Suzzanna: Santet …; The Doll 3 |
| user_65c4e0cf747d |      0.040359 | Ipar Adalah Maut                                                                                                                                                   |

## 15. Aktor inti (PageRank)

PageRank pada graf balasan berarah. `15_aktor-inti.csv`

| akun              |   pagerank | film                                                                                                         |
|:------------------|-----------:|:-------------------------------------------------------------------------------------------------------------|
| user_0dba4d1e6b04 |   0.010924 | Perewangan; Racun Sangga: San…; Santet Segoro Pitu                                                           |
| user_480f5add592c |   0.009993 | Official Trailer …                                                                                           |
| user_b766f1f64ed4 |   0.009768 | Suzzanna: Malam J…; Suzzanna: Santet …                                                                       |
| user_c9a0d2374efa |   0.009751 | Danur: The Last C…; Perewangan; Racun Sangga: San…; Santet Segoro Pitu; Suzzanna: Santet …                   |
| user_0b3d09c62210 |   0.008634 | Danur: The Last C…; Ipar Adalah Maut; Janur Ireng: Sewu…; Perewangan; Suzzanna: Malam J…; Suzzanna: Santet … |
| user_835853c3c30d |   0.008429 | Suzzanna: Malam J…                                                                                           |
| user_84d508e05f82 |   0.008411 | Janur Ireng: Sewu…                                                                                           |
| user_89a12485e1ad |   0.007439 | Janur Ireng: Sewu…                                                                                           |
| user_6aac1d230982 |   0.006626 | Santet Segoro Pitu                                                                                           |
| user_a8cd225d7fb9 |   0.006489 | Racun Sangga: San…; Santet Segoro Pitu; Suzzanna: Santet …                                                   |

## 16. Superfans: akun yang berkomentar di ≥3 film

101 akun berkomentar di ≥3 film. Pengganti 'akun resmi', karena data tidak menandai akun kanal/pemeran. `16_superfans.csv`

Film yang paling banyak didatangi superfans:

| film                                         |   komentar_superfans |
|:---------------------------------------------|---------------------:|
| Suzzanna: Malam Jumat Kliwon (2023)          |                  122 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)    |                  118 |
| Janur Ireng: Sewu Dino Prequel (2025/2026)   |                   66 |
| Danur: The Last Chapter (2026)               |                   61 |
| Indigo: What Do You See? (2023)              |                   49 |
| Jurnal Risa by Risa Saraswati (2024)         |                   39 |
| Santet Segoro Pitu (2024)                    |                   26 |
| Suzzanna: Bernapas dalam Kubur (2018)        |                   25 |
| The Doll 3 (2022)                            |                   23 |
| Official Trailer IVANNA (2022) - MD Pictures |                   23 |

## 17. Kata teratas per film & per komunitas

`17_kata-teratas.csv`

| kelompok                                               | kata_teratas                                                                                                                                       |
|:-------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| film: Badarawuhi di Desa Penari (2024)                 | film(173), nonton(99), badarawuhi(83), kkn(78), desa(66), penari(55), lebih(41), cerita(41), horor(36), bagus(28), saya(27), mau(25)               |
| film: Catatan Harian Menantu Sinting (2024)            | radit(98), bang(52), film(39), adegan(21), nonton(18), peran(12), ariel(12), main(11), tatum(11), mau(9), punya(9), papa(9)                        |
| film: Danur: The Last Chapter (2026)                   | danur(123), film(80), lebaran(28), last(24), chapter(23), ivanna(20), bagus(17), risa(17), sampah(16), semoga(13), nonton(13), tayang(13)          |
| film: Indigo: What Do You See? (2023)                  | film(238), nonton(122), indigo(114), mata(93), batin(87), keren(78), hitmaker(63), horor(61), filmnya(53), bagus(52), aliando(52), amanda(51)      |
| film: Ipar Adalah Maut (2024)                          | film(92), nonton(62), aris(59), ipar(58), rani(41), adalah(37), suami(28), adik(28), maut(28), rumah(28), bikin(27), selingkuh(26)                 |
| film: Ivanna (2022)                                    | film(106), ivanna(59), nonton(58), danur(35), bagus(34), horor(23), lebih(22), lagu(22), bikin(19), setan(17), saya(16), filmnya(16)               |
| film: Janur Ireng: Sewu Dino Prequel (2025/2026)       | film(93), sewu(67), dino(66), ireng(50), nonton(45), janur(43), bikin(37), kuncoro(34), jawa(29), tayang(29), kimo(29), bagus(26)                  |
| film: Jurnal Risa by Risa Saraswati (2024)             | film(129), nonton(127), risa(72), medium(50), keren(47), liat(36), jurnal(36), trailer(36), serem(34), teh(34), horor(31), bioskop(30)             |
| film: Mata Batin (2017)                                | inn(96), film(15), nonton(13), mata(11), batin(11), serem(8), kenapaa(6), filmnya(5), movie(4), kak(4), watch(4), what(4)                          |
| film: Official Trailer IVANNA (2022) - MD Pictures     | film(218), nonton(124), keren(88), ivanna(82), bagus(59), kimo(58), horor(51), danur(46), filmnya(45), indonesia(39), sabar(33), bioskop(30)       |
| film: Perewangan (2024)                                | film(109), nonton(44), indonesia(32), horror(23), cerita(21), bagus(20), horor(19), tempat(19), filmnya(18), nessie(18), perewangan(17), lahir(16) |
| film: Racun Sangga: Santet Pemisah Rumah Tangga (2024) | film(67), nonton(36), kalimantan(22), bagus(19), horor(16), soraya(16), keren(15), cerita(14), baru(13), tayang(12), racun(12), santet(11)         |
| film: Santet Segoro Pitu (2024)                        | film(101), nonton(60), keren(43), santet(39), bagus(29), sumala(22), horor(21), bioskop(21), hitmaker(18), trailer(17), emang(17), cerita(16)      |
| film: Siccin 8                                         | nonton(11), siccin(5), film(5), senayan(2), sabar(2), mau(2), udh(2), kaya(2), bang(2), tayang(2), hari(2), bioskop(2)                             |
| film: Suzzanna: Bernapas dalam Kubur (2018)            | film(144), luna(95), maya(70), nonton(59), mirip(49), suzzana(38), suzanna(37), bagus(34), suzzanna(31), filmnya(28), full(27), movie(22)          |
| film: Suzzanna: Malam Jumat Kliwon (2023)              | film(348), nonton(277), luna(187), keren(176), maya(114), suzanna(106), sabar(103), bagus(97), wajib(85), serem(85), horor(80), lebih(80)          |
| film: Suzzanna: Santet Dosa di Atas Dosa (2026)        | film(300), luna(154), nonton(116), maya(111), suzanna(108), mirip(94), keren(90), bagus(84), lebih(81), suzzana(81), reza(73), suzzanna(69)        |
| film: The Doll 3 (2022)                                | film(212), doll(107), chucky(102), boneka(69), nonton(49), indonesia(40), bikin(34), movie(31), bonekanya(30), mirip(28), beda(27), horror(27)     |
| komunitas 1                                            | film(346), nonton(256), luna(184), keren(162), maya(112), suzanna(102), sabar(99), bagus(86), wajib(80), lebih(77), horor(75), serem(75)           |
| komunitas 2                                            | film(275), luna(135), nonton(107), maya(96), suzanna(93), mirip(91), keren(80), lebih(75), bagus(75), suzzana(69), reza(65), suzzanna(53)          |
| komunitas 3                                            | film(127), nonton(127), risa(66), keren(48), medium(44), teh(35), horor(34), liat(33), jurnal(33), bioskop(30), serem(29), trailer(29)             |
| komunitas 4                                            | film(230), nonton(124), indigo(107), keren(85), mata(83), batin(77), horor(61), filmnya(54), semoga(54), bagus(52), aliando(51), hitmaker(49)      |
| komunitas 5                                            | film(218), chucky(99), doll(95), boneka(68), nonton(46), indonesia(38), bikin(32), movie(31), bonekanya(29), beda(28), horror(27), mirip(26)       |
| komunitas 6                                            | film(204), nonton(118), keren(86), ivanna(69), kimo(50), bagus(49), filmnya(45), horor(43), indonesia(36), sabar(35), danur(31), semoga(28)        |

## 18. Pasangan kata (bigram) teratas

`18_pasangan-kata.csv` · per film di `18_pasangan-kata-per-film.csv`. Bahan kandidat leksikon Watch Intent Index.

| pasangan         |   frekuensi |
|:-----------------|------------:|
| luna maya        |         296 |
| film horor       |         218 |
| nonton film      |         131 |
| wajib nonton     |         104 |
| mata batin       |         101 |
| film horror      |          94 |
| inn inn          |          94 |
| pengen nonton    |          82 |
| nonton bioskop   |          78 |
| mau nonton       |          75 |
| sewu dino        |          75 |
| desa penari      |          66 |
| film indonesia   |          61 |
| harus nonton     |          54 |
| bikin film       |          51 |
| kkn desa         |          50 |
| kisah nyata      |          49 |
| pengabdi setan   |          49 |
| janur ireng      |          48 |
| soraya intercine |          48 |

## 19. Emoji & tagar teratas

28.2% komentar memakai emoji. `19_emoji-tagar.csv`

| jenis   | item   |   frekuensi |
|:--------|:-------|------------:|
| emoji   | ♋     |        1378 |
| emoji   | 😂     |         840 |
| emoji   | ❤      |         756 |
| emoji   | 😭     |         452 |
| emoji   | 🤩     |         365 |
| emoji   | 👍     |         349 |
| emoji   | 😅     |         348 |
| emoji   | 🔥     |         308 |
| emoji   | 🎉     |         270 |
| emoji   | 😢     |         224 |
| emoji   | 😊     |         213 |
| emoji   | 🤣     |         200 |
| emoji   | 😮     |         180 |
| emoji   | 🦄     |         167 |
| emoji   | 😰     |         164 |
| emoji   | 😍     |         150 |
| emoji   | 😱     |         102 |
| emoji   | 🥐     |          93 |
| emoji   | 🙏     |          87 |
| emoji   | 🏻     |          80 |

## 20. Jaringan per jendela waktu (H-14, H-7, H-1, pasca-rilis)

Data YouTube API presisi tersedia di data/youtube_api/ — pertimbangkan memuatnya untuk analisis final. Film tanpa tanggal rilis di films_clean.csv dilewati. `20_waktu.csv`

| film                                             | jendela     |   komentar |   akun |   balasan |   niat_menonton_% |
|:-------------------------------------------------|:------------|-----------:|-------:|----------:|------------------:|
| Badarawuhi di Desa Penari (2024)                 | pasca-rilis |        500 |    415 |       100 |               6   |
| Catatan Harian Menantu Sinting (2024)            | pasca-rilis |        257 |    234 |        54 |               3.5 |
| Indigo: What Do You See? (2023)                  | H-14..H-8   |        446 |    327 |       108 |              13.7 |
| Indigo: What Do You See? (2023)                  | pasca-rilis |        347 |    298 |        47 |               6.1 |
| Ipar Adalah Maut (2024)                          | pasca-rilis |        426 |    353 |       100 |               4.5 |
| Ivanna (2022)                                    | pasca-rilis |        372 |    280 |       100 |               3.8 |
| Jurnal Risa by Risa Saraswati (2024)             | pasca-rilis |        792 |    650 |       195 |              10.4 |
| Perewangan (2024)                                | < H-14      |        103 |     89 |        37 |               4.9 |
| Perewangan (2024)                                | pasca-rilis |        196 |    164 |        77 |               2   |
| Racun Sangga: Santet Pemisah Rumah Tangga (2024) | pasca-rilis |        198 |    168 |        68 |               3   |
| Santet Segoro Pitu (2024)                        | pasca-rilis |        425 |    369 |       113 |               7.1 |
| Suzzanna: Bernapas dalam Kubur (2018)            | pasca-rilis |        500 |    438 |        91 |               2.6 |
| Suzzanna: Malam Jumat Kliwon (2023)              | pasca-rilis |       1728 |   1421 |       352 |              12.6 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        | < H-14      |        750 |    636 |       166 |               6.1 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        | H-14..H-8   |        105 |     97 |        21 |               2.9 |
| Suzzanna: Santet Dosa di Atas Dosa (2026)        | pasca-rilis |        360 |    277 |       111 |               5   |
| The Doll 3 (2022)                                | pasca-rilis |        680 |    535 |       183 |               3.1 |
