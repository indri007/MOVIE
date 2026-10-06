# SANTET Design System
*docs/DESIGN.md — berlaku untuk README.md, docs/, dashboard/, streamlit_app/*  
*Versi 1.0 · 06-10-2026 · Indri Anjar Kartika Sari*

---

## 1. Prinsip

| # | Prinsip | Implikasi langsung |
|:---:|---|---|
| 1 | **Jujur sebelum indah** | Angka tidak dibulatkan. Badge tidak mengklaim hal yang belum terbukti. |
| 2 | **Hierarki yang teraba** | Judul → masalah → status → tindakan. Pembaca tahu di mana mereka dalam 10 detik. |
| 3 | **Warna membawa makna** | Amber = perhatian/highlight. Teal = konfirmasi/data. Abu = latar. Merah = peringatan. Tidak dekoratif. |
| 4 | **Ilustratif diberi label** | Setiap visual yang bukan screenshot data nyata harus menyebut "ilustratif" di alt-text dan caption. |

---

## 2. Palet Warna (Material 3 · Seed: Amber Lilin)

```
Token                 Hex         Kegunaan
──────────────────────────────────────────────────────────────
--md-primary          #C2410C     Heading utama, CTA, aksen highlight
--md-on-primary       #FFFFFF     Teks di atas primary
--md-secondary        #0F766E     Data konfirmasi, badge "Final"
--md-on-secondary     #FFFFFF
--md-tertiary         #7C3AED     Aksen ketiga (komunitas, SNA label)
--md-error            #B91C1C     Peringatan, angka sementara
--md-surface          #12121e     Latar kartu / dashboard
--md-surface-variant  #1e1e2e     Latar panel sekunder
--md-outline          #2a2a3e     Border, divider
--md-on-surface       #E7E5E4     Teks utama di atas surface
--md-on-surface-var   #A8A29E     Teks sekunder / label kecil
--md-background       #0a0a14     Latar halaman
```

**Kontras aksesibilitas:**  
- Teks utama (#E7E5E4) di atas surface (#12121e): rasio ≥ 12:1 ✓  
- Primary (#C2410C) di atas putih: rasio 4,8:1 — hanya untuk heading besar (≥18pt) ✓  
- Jangan gunakan primary sebagai warna teks body di atas background gelap.

---

## 3. Tipografi

| Peran | Font | Ukuran | Berat |
|---|---|---|---|
| **Display / Judul halaman** | Inter | 28–32px | 700 |
| **Section heading** | Inter | 18–22px | 600 |
| **Sub-heading / label kartu** | Inter | 14–16px | 600 |
| **Body teks** | Inter | 14–15px | 400 |
| **Kode / CLI** | JetBrains Mono | 13px | 400 |
| **Caption / footnote** | Inter | 12px | 400, italic |

Import:  
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
```

---

## 4. Ikon & Badge

- **Set ikon:** Material Symbols Outlined (Google CDN). Ukuran 20–24px.
- **Badge status** (Shields.io):  
  - `✅ Final` → warna `#0F766E`  
  - `⚠️ Belum divalidasi` → warna `#B45309`  
  - `⏳ Menunggu` → warna `#1D4ED8`  
  - `❌ Gagal / tidak tersedia` → warna `#B91C1C`  
- Jangan gunakan badge "Scopus Q1 Ready", "Akurasi Tinggi", atau klaim serupa sebelum ada reviewers' acceptance.

---

## 5. Komponen Kartu

```css
.card {
  background: var(--md-surface);
  border: 1px solid var(--md-outline);
  border-radius: 12px;
  padding: 1.2rem 1.4rem;
}
.card-highlight { border-left: 3px solid var(--md-primary); }
.card-data      { border-left: 3px solid var(--md-secondary); }
.card-warning   { border-left: 3px solid var(--md-error); }
```

---

## 6. Tabel Data

- Header: `font-weight: 600`, background `--md-surface-variant`.
- Kolom angka: rata kanan, font monospace.
- Angka sementara: diberi catatan kaki `*` — jangan gunakan warna merah inline (bisa diinterpretasi sebagai "salah").
- Baris yang merupakan total/ringkasan: bold.

---

## 7. Konvensi Nama File (docs/ & assets/)

| Tipe file | Pola nama | Contoh |
|---|---|---|
| Hero SVG | `{proyek}_hero.svg` | `santet_hero.svg` |
| Preview GIF | `{proyek}_preview.gif` | `santet_preview.gif` |
| Halaman 3D | `docs/{fitur}/index.html` | `docs/santet/index.html` |
| Design system | `docs/DESIGN.md` | — |
| Aset tambahan | `docs/assets/{nama_deskriptif}.{ext}` | `docs/assets/flowchart_pipeline.svg` |

**Aturan:** Satu halaman 3D per fitur. Tidak ada `santet/` dan `santet-3d/` yang identik isi dan tujuannya. Jika keduanya dipertahankan, harus ada perbedaan konten yang eksplisit dan link yang jelas dari satu ke yang lain.

---

## 8. Alt Text & Aksesibilitas

- Setiap `<img>` dan `![...]` harus memiliki alt text deskriptif.
- Visual ilustratif: alt text **wajib** menyebut kata "ilustratif". Contoh:  
  `alt="Diagram alur pipeline SANTET — ilustratif; bukan output sistem aktual"`
- Grafik SNA: sebutkan apa yang ditampilkan dan dari data apa.  
  `alt="Graf Louvain 13 komunitas dari 7.337 komentar YouTube, 4 set trailer, Oktober 2026"`
- Warna tidak boleh menjadi satu-satunya pembeda informasi (sertakan juga label atau ikon).

---

## 9. Link & Referensi

- Semua link di README dan docs/ harus **relatif** atau ke `https://github.com/indri007/prediksi-movie-2027`.
- Jangan gunakan `file:///` atau path absolut lokal.
- Setiap kutipan angka box office harus dapat ditelusuri ke `data/box_office_sources.csv` atau `AUDIT_REPORT.md`.

---

## 10. Checklist Sebelum Publikasi (GitHub Pages)

- [ ] `docs/santet/index.html` terbuka di `https://indri007.github.io/prediksi-movie-2027/docs/santet/`
- [ ] `docs/assets/santet_hero.svg` termuat di README (bukan 404)
- [ ] Semua link di README tidak mengarah ke `file:///` atau path lokal
- [ ] Alt text terpasang di semua gambar
- [ ] Angka sementara diberi tanda `*` dan catatan kaki
- [ ] Tidak ada badge atau klaim validasi yang belum terbukti
- [ ] Tabel status riset mencerminkan `results/paper_status.md` terbaru
- [ ] Tampilan di layar 375px (mobile): heading tidak terpotong, tabel scrollable
- [ ] Streamlit app berjalan tanpa error dengan data dari `results/sna_*/` terbaru
- [ ] `AUDIT_REPORT.md` mencatat tanggal update terbaru

---

*Design system ini adalah dokumen hidup. Perbarui setiap kali ada perubahan palet, komponen baru, atau keputusan aksesibilitas baru.*
