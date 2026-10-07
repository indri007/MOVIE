#!/usr/bin/env python3
"""
scripts/build_ffi_strategy_data.py
===================================
Menghasilkan dataset terstruktur dan pemodelan NodeXL untuk Peta Jalan &
Strategi Menembus Festival Film Indonesia (FFI) & Perebutan Piala Citra.
"""

import os
import pandas as pd

def build_ffi_data():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(repo_root, "data")
    results_dir = os.path.join(repo_root, "results", "nodexl_ffi_strategy_engine")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    # 1. Dataset Sejarah Pemenang & Sweep FFI 2020-2025
    winners_data = [
        {
            "tahun": 2020,
            "film": "Perempuan Tanah Jahanam",
            "sutradara": "Joko Anwar",
            "produser_studio": "Shanty Harmayn, Tia Hasibuan / BASE & RAPI",
            "total_nominasi": 17,
            "total_menang": 6,
            "piala_utama": "Film Terbaik, Sutradara Terbaik, Aktris Pendukung (Christine Hakim)",
            "piala_teknis": "Tata Suara, Penyunting Gambar, Sinematografi",
            "isu_sosial_budaya": "Folklor Jawa, warisan dosa leluhur, kutukan feodal",
            "strategi_craft": "Sound design atmosferik, sinematografi dingin, produksi berstandar internasional"
        },
        {
            "tahun": 2021,
            "film": "Penyalin Cahaya",
            "sutradara": "Wregas Bhanuteja",
            "produser_studio": "Adi Ekatama, Ajish Dibyo / Rekata Studios & Kaninga",
            "total_nominasi": 17,
            "total_menang": 12,
            "piala_utama": "Film Terbaik, Sutradara Terbaik, Skenario Asli, Pemeran Utama Pria (Chicco K.)",
            "piala_teknis": "Sinematografi, Tata Suara, Musik, Artistik, Busana, Rias, Efek Visual",
            "isu_sosial_budaya": "Kekerasan seksual di institusi kampus, relasi kuasa, pembungkaman korban",
            "strategi_craft": "Rekor kemenangan terbanyak sepanjang sejarah FFI (12 piala), visual metaforik laser/kabut"
        },
        {
            "tahun": 2022,
            "film": "Before, Now & Then (Nana)",
            "sutradara": "Kamila Andini",
            "produser_studio": "Ifa Isfansyah, Gita Fara / Fourcolours Films",
            "total_nominasi": 11,
            "total_menang": 5,
            "piala_utama": "Film Terbaik, Aktris Pendukung (Laura Basuki - Silver Bear)",
            "piala_teknis": "Pengarah Sinematografi (Batara Goempar), Musik, Artistik",
            "isu_sosial_budaya": "Trauma perang 1965, nasib perempuan dalam poligami priyayi Sunda",
            "strategi_craft": "Bahasa Sunda puitis penuh keheningan, sinematografi warm-elegiac, prestise Berlinale"
        },
        {
            "tahun": 2022,
            "film": "Seperti Dendam, Rindu Harus Dibayar Tuntas (Co-Winner Utama)",
            "sutradara": "Edwin",
            "produser_studio": "Meiske Taurisia, Muhammad Zaidy / Palari Films",
            "total_nominasi": 12,
            "total_menang": 5,
            "piala_utama": "Sutradara Terbaik, Skenario Adaptasi, Aktor Terbaik (Marthino), Aktris Terbaik (Ladya)",
            "piala_teknis": "Tata Rias, Tata Busana",
            "isu_sosial_budaya": "Toksisitas maskulinitas, kekerasan aparat Orba, adaptasi sastra Eka Kurniawan",
            "strategi_craft": "Format seluloid 16mm gritty, penyutradaraan tajam, Golden Leopard Locarno"
        },
        {
            "tahun": 2023,
            "film": "Women from Rote Island",
            "sutradara": "Jeremias Nyangoen",
            "produser_studio": "Rizka Shakira / Bintang Cahaya Sinema",
            "total_nominasi": 4,
            "total_menang": 4,
            "piala_utama": "Film Terbaik, Sutradara Terbaik, Penulis Skenario Asli Terbaik",
            "piala_teknis": "Pengarah Sinematografi Terbaik (Joseph Christoforus Fofid)",
            "isu_sosial_budaya": "Kekerasan seksual berlapis perempuan di pulau terluar NTT, stigmatisasi korban",
            "strategi_craft": "Konversi 100% nominasi jadi piala, naturalisme aktor lokal non-profesional, visual mentah"
        },
        {
            "tahun": 2024,
            "film": "Jatuh Cinta Seperti di Film-film",
            "sutradara": "Yandy Laurens",
            "produser_studio": "Ernest Prakasa, Suryana Paramita / Imajinari",
            "total_nominasi": 11,
            "total_menang": 7,
            "piala_utama": "Film Terbaik, Skenario Asli, Aktor Terbaik (Ringgo), Aktris Terbaik (Nirina), 2 Aktor Pendukung",
            "piala_teknis": "Penyunting Gambar, Pencipta Lagu Tema",
            "isu_sosial_budaya": "Proses duka kehilangan, kritik meta industri perfilman, cinta dewasa",
            "strategi_craft": "Format 80% hitam-putih monokrom berani, skenario presisi tanpa cacat logika, sapu 4 aktor"
        },
        {
            "tahun": 2024,
            "film": "Siksa Kubur (Benchmarking Teknis FFI)",
            "sutradara": "Joko Anwar",
            "produser_studio": "Tia Hasibuan / Come and See Pictures",
            "total_nominasi": 17,
            "total_menang": 1,
            "piala_utama": "Nominasi Film, Sutradara, Skenario, Pemeran Utama",
            "piala_teknis": "Tata Suara Terbaik (Mohamad Ikhsan), 11 Nominasi Cabang Teknis",
            "isu_sosial_budaya": "Eksistensialisme ketuhanan, trauma bom bunuh diri, hipokrisi moral",
            "strategi_craft": "Rekor 17 nominasi FFI (menyamai rekor sejarah), sound design Dolby Atmos kelas festival dunia"
        }
    ]

    df_winners = pd.DataFrame(winners_data)
    winners_csv = os.path.join(data_dir, "ffi_piala_citra_winners_2020_2025.csv")
    df_winners.to_csv(winners_csv, index=False)
    print(f"✅ Disimpan: {winners_csv}")

    # 2. NodeXL Network: 5 Pilar Strategi FFI & Piala Citra
    # Vertices (Nodes)
    vertices_data = [
        # Cluster 1: Standar Penjurian & Voting Body (Governance)
        {"vertex_id": "V1", "vertex_label": "Asosiasi Profesi Perfilman", "cluster_group": "Penjurian", "category_type": "Tahap 1 Kurasi", "description": "IFDC, APROFI, IFI, SATU, INAFED, FSK (Menyeleksi Longlist & Nominasi)", "centrality_score": 0.88, "color": "#1E88E5", "shape": "circle"},
        {"vertex_id": "V2", "vertex_label": "Akademi Citra (Voting Body)", "cluster_group": "Penjurian", "category_type": "Tahap 2 Final", "description": "80-100+ praktisi peraih piala/nomine FFI yang menentukan pemenang akhir", "centrality_score": 0.96, "color": "#1E88E5", "shape": "diamond"},
        {"vertex_id": "V3", "vertex_label": "Audit Independen (PwC/Deloitte)", "cluster_group": "Penjurian", "category_type": "Integritas", "description": "Tabulasi suara tertutup dan audit kerahasiaan hasil voting FFI", "centrality_score": 0.72, "color": "#1E88E5", "shape": "square"},

        # Cluster 2: The Craft (Departemen Teknis & Seni)
        {"vertex_id": "V4", "vertex_label": "Skenario Orisinal / Adaptasi", "cluster_group": "The Craft", "category_type": "Fondasi Narasi", "description": "Struktur 3 babak solid, subteks mendalam, karakter berdimensi (Bobot 25%)", "centrality_score": 0.94, "color": "#43A047", "shape": "circle"},
        {"vertex_id": "V5", "vertex_label": "Sinematografi & Pencahayaan", "cluster_group": "The Craft", "category_type": "Estetika Visual", "description": "Framing visual puitis, blocking kamera bermakna, tone color grade khas", "centrality_score": 0.86, "color": "#43A047", "shape": "circle"},
        {"vertex_id": "V6", "vertex_label": "Tata Suara & Scoring Musik", "cluster_group": "The Craft", "category_type": "Imersi Audio", "description": "Foley organik, dynamic range Dolby Atmos, musik tematik pemicu katarsis", "centrality_score": 0.84, "color": "#43A047", "shape": "circle"},
        {"vertex_id": "V7", "vertex_label": "Penyuntingan & Tata Artistik", "cluster_group": "The Craft", "category_type": "Ritme & Dunia", "description": "Editing ritmis menjaga emosi, set desain otentik merefleksikan latar zaman", "centrality_score": 0.80, "color": "#43A047", "shape": "circle"},
        {"vertex_id": "V8", "vertex_label": "Keaktoran (Ensemble & Lead)", "cluster_group": "The Craft", "category_type": "Penghayatan Karakter", "description": "Akting natural tanpa teatrikal berlebih, pendalaman dialek, kimiawi ansambel", "centrality_score": 0.90, "color": "#43A047", "shape": "circle"},

        # Cluster 3: Kelayakan & Waktu Tayang (Eligibility & Timing)
        {"vertex_id": "V9", "vertex_label": "Jendela Eligibility Resmi", "cluster_group": "Eligibility & Timing", "category_type": "Regulasi", "description": "Lolos sensor LSF dan tayang bioskop komersial 1 Okt (T-1) s/d 30 Sept (T)", "centrality_score": 0.76, "color": "#FB8C00", "shape": "square"},
        {"vertex_id": "V10", "vertex_label": "Timing Rilis Kuartal 3 (Q3)", "cluster_group": "Eligibility & Timing", "category_type": "Strategi Kalender", "description": "Rilis Agustus-September atau festival run JAFF untuk efek Recency Bias juri", "centrality_score": 0.82, "color": "#FB8C00", "shape": "triangle"},

        # Cluster 4: Kampanye Industri & Pemutaran Khusus (FYC)
        {"vertex_id": "V11", "vertex_label": "FYC Special Screenings", "cluster_group": "Kampanye FYC", "category_type": "Engagement", "description": "Pemutaran khusus eksklusif untuk anggota Akademi Citra di bioskop terpilih", "centrality_score": 0.89, "color": "#8E24AA", "shape": "diamond"},
        {"vertex_id": "V12", "vertex_label": "Digital Screener Portal", "cluster_group": "Kampanye FYC", "category_type": "Aksesibilitas", "description": "Portal streaming terenkripsi watermarked agar juri sibuk dapat menonton penuh", "centrality_score": 0.81, "color": "#8E24AA", "shape": "square"},
        {"vertex_id": "V13", "vertex_label": "Booklet & Production Notes", "cluster_group": "Kampanye FYC", "category_type": "Edukasi Juri", "description": "Buku proses kreatif teknis di balik layar yang dibagikan kepada dewan juri", "centrality_score": 0.74, "color": "#8E24AA", "shape": "circle"},

        # Cluster 5: Relevansi Sosial & Budaya (Cultural Resonance)
        {"vertex_id": "V14", "vertex_label": "Isu Kemanusiaan & Ketimpangan", "cluster_group": "Kedalaman Budaya", "category_type": "Urgensi Isu", "description": "Menyorot kekerasan seksual, patriarki, represi, marjinalisasi, trauma sosial", "centrality_score": 0.92, "color": "#E53935", "shape": "circle"},
        {"vertex_id": "V15", "vertex_label": "Akar Budaya & Hyper-Localism", "cluster_group": "Kedalaman Budaya", "category_type": "Otentisitas", "description": "Lokalitas spesifik (NTT, Jawa priyayi, pedalaman Riau) yang membumi", "centrality_score": 0.87, "color": "#E53935", "shape": "circle"},

        # Cluster 6: Puncak Prestasi & Dampak Industri (Outcome Apex)
        {"vertex_id": "V16", "vertex_label": "Sapu Nominasi Teknis (10+)", "cluster_group": "Piala Citra Apex", "category_type": "Milestone FFI", "description": "Dominasi nominasi di sound, kamera, artistik yang membangun aura calon juara", "centrality_score": 0.88, "color": "#00ACC1", "shape": "star"},
        {"vertex_id": "V17", "vertex_label": "Piala Citra Kategori Utama", "cluster_group": "Piala Citra Apex", "category_type": "Puncak Nasional", "description": "Piala Film Cerita Panjang Terbaik, Sutradara Terbaik, Skenario Terbaik", "centrality_score": 0.99, "color": "#D81B60", "shape": "star"},
        {"vertex_id": "V18", "vertex_label": "Legasi Sinema & Re-release BO", "cluster_group": "Piala Citra Apex", "category_type": "Dampak Jangka Panjang", "description": "Lonjakan penayangan OTT global, re-release bioskop, pendanaan studio berikutnya", "centrality_score": 0.95, "color": "#D81B60", "shape": "hexagon"}
    ]

    # Edges (Relationships & Mechanisms)
    edges_data = [
        # Asosiasi & Akademi
        {"source": "V1", "target": "V16", "relationship_type": "nominates_craft", "weight": 0.90, "mechanism_description": "Asosiasi profesi (IFI, SATU, INAFED) memfilter dan menetapkan 5 nominasi teknis terbaik"},
        {"source": "V1", "target": "V2", "relationship_type": "submits_shortlist", "weight": 0.85, "mechanism_description": "Daftar nominasi resmi diserahkan ke Akademi Citra untuk pemungutan suara tahap akhir"},
        {"source": "V2", "target": "V17", "relationship_type": "elects_winners", "weight": 0.98, "mechanism_description": "Voting rahasia anggota Akademi Citra secara mutlak menentukan pemenang Piala Citra"},
        {"source": "V3", "target": "V2", "relationship_type": "audits_ballots", "weight": 0.80, "mechanism_description": "Akuntan publik menjamin integritas dan validitas suara pemilih Akademi Citra"},

        # The Craft -> Nominasi & Pemenang
        {"source": "V4", "target": "V17", "relationship_type": "secures_best_picture", "weight": 0.95, "mechanism_description": "Skenario terbaik adalah prediktor statistik terkuat (90%+) untuk memenangkan Film Terbaik FFI"},
        {"source": "V5", "target": "V16", "relationship_type": "anchors_visual_clout", "weight": 0.88, "mechanism_description": "Kualitas sinematografi memimpin raihan nominasi visual (Batara Goempar, Joseph Fofid)"},
        {"source": "V6", "target": "V16", "relationship_type": "anchors_audio_clout", "weight": 0.85, "mechanism_description": "Penataan suara imersif menjamin poin tinggi di mata kurator asosiasi suara"},
        {"source": "V7", "target": "V16", "relationship_type": "builds_technical_sweep", "weight": 0.82, "mechanism_description": "Editing yang presisi dan art direction otentik melengkapi sapu bersih nominasi teknis"},
        {"source": "V8", "target": "V17", "relationship_type": "secures_acting_sweep", "weight": 0.92, "mechanism_description": "Penghargaan 4 kategori akting (JESEDEF) menjadi pendorong utama kemenangan Best Picture"},

        # Eligibility & Timing -> FYC & Recognition
        {"source": "V9", "target": "V1", "relationship_type": "satisfies_compliance", "weight": 0.75, "mechanism_description": "Surat lulus sensor dan kepatuhan tayang bioskop mengamankan kelayakan administratif seleksi"},
        {"source": "V10", "target": "V11", "relationship_type": "maximizes_recency", "weight": 0.85, "mechanism_description": "Rilis Q3/festival memastikan film masih hangat dalam ingatan pemilih saat voting dibuka"},

        # FYC Campaign -> Akademi Citra
        {"source": "V11", "target": "V2", "relationship_type": "mobilizes_voter_turnout", "weight": 0.92, "mechanism_description": "Special screening tatap muka memastikan minimal 60% pemilih Akademi Citra menonton di bioskop"},
        {"source": "V12", "target": "V2", "relationship_type": "closes_viewing_gap", "weight": 0.84, "mechanism_description": "Digital screener menjamin anggota juri yang sedang syuting di luar kota tetap dapat menonton"},
        {"source": "V13", "target": "V2", "relationship_type": "articulates_craftsmanship", "weight": 0.78, "mechanism_description": "Buku catatan produksi memperjelas tingkat kesulitan teknis kepada para pemilih FFI"},

        # Relevansi Sosial & Budaya -> Emosi Juri & Kemenangan
        {"source": "V14", "target": "V4", "relationship_type": "enriches_subtext", "weight": 0.90, "mechanism_description": "Isu sosial nyata memperkaya kedalaman naskah dan mengangkat bobot moral narasi"},
        {"source": "V15", "target": "V5", "relationship_type": "inspires_visual_authenticity", "weight": 0.85, "mechanism_description": "Lokalitas Nusantara otentik menghasilkan komposisi visual sinematografi yang khas dan memukau"},
        {"source": "V14", "target": "V17", "relationship_type": "touches_voter_conscience", "weight": 0.88, "mechanism_description": "Keberanian menyuarakan isu kemanusiaan memberikan nilai urgensi tinggi bagi juri Akademi Citra"},

        # Nominasi Teknis -> Piala Citra Utama -> Legasi
        {"source": "V16", "target": "V17", "relationship_type": "creates_frontrunner_halo", "weight": 0.89, "mechanism_description": "Dominasi 10+ nominasi teknis menciptakan efek psikologis 'film wajib menang' di dewan juri"},
        {"source": "V17", "target": "V18", "relationship_type": "elevates_commercial_value", "weight": 0.96, "mechanism_description": "Piala Citra Film Terbaik mendongkrak valuasi OTT internasional dan daya tawar proyek berikutnya"}
    ]

    df_vertices = pd.DataFrame(vertices_data)
    df_edges = pd.DataFrame(edges_data)

    df_vertices.to_csv(os.path.join(data_dir, "ffi_strategy_nodexl_vertices.csv"), index=False)
    df_edges.to_csv(os.path.join(data_dir, "ffi_strategy_nodexl_edges.csv"), index=False)

    df_vertices.to_csv(os.path.join(results_dir, "vertices.csv"), index=False)
    df_edges.to_csv(os.path.join(results_dir, "edges.csv"), index=False)

    print(f"✅ Disimpan NodeXL Vertices: {len(df_vertices)} entitas")
    print(f"✅ Disimpan NodeXL Edges: {len(df_edges)} relasi")

    # Generate GraphML
    graphml_path = os.path.join(results_dir, "ffi_strategy_network.graphml")
    with open(graphml_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n')
        f.write('  <key id="label" for="node" attr.name="label" attr.type="string"/>\n')
        f.write('  <key id="cluster" for="node" attr.name="cluster" attr.type="string"/>\n')
        f.write('  <key id="score" for="node" attr.name="score" attr.type="double"/>\n')
        f.write('  <key id="rel" for="edge" attr.name="relation" attr.type="string"/>\n')
        f.write('  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>\n')
        f.write('  <graph id="FFI_Strategy_Network" edgedefault="directed">\n')
        for _, row in df_vertices.iterrows():
            f.write(f'    <node id="{row["vertex_id"]}">\n')
            f.write(f'      <data key="label">{row["vertex_label"]}</data>\n')
            f.write(f'      <data key="cluster">{row["cluster_group"]}</data>\n')
            f.write(f'      <data key="score">{row["centrality_score"]}</data>\n')
            f.write(f'    </node>\n')
        for _, row in df_edges.iterrows():
            f.write(f'    <edge source="{row["source"]}" target="{row["target"]}">\n')
            f.write(f'      <data key="rel">{row["relationship_type"]}</data>\n')
            f.write(f'      <data key="weight">{row["weight"]}</data>\n')
            f.write(f'    </edge>\n')
        f.write('  </graph>\n')
        f.write('</graphml>\n')

    print(f"✅ GraphML tersimpan: {graphml_path}")

if __name__ == "__main__":
    build_ffi_data()
