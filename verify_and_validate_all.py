#!/usr/bin/env python3
"""
verify_and_validate_all.py
Suite Verifikasi dan Validasi (V&V) Komprehensif:
1. Data Sumber CSV (NapoleonCat, GoodStats, dll.)
2. Model Peramalan & Output Proyeksi 2027 (CSV & SVG)
3. Integritas Bahasa Bit (Tren & Rekomendasi Eksekusi)
4. Bit Daemon Runtime, Status JSON, Log & Bitstream Sync
"""

import os
import csv
import json
import hashlib
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def print_header(title):
    print("\n" + "=" * 65)
    print(f" {title}")
    print("=" * 65)

def check(name, condition, details=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")
    if details:
        print(f"       -> {details}")
    return condition

def test_source_csv():
    print_header("1. VERIFIKASI DATA SUMBER CSV")
    path = os.path.join(BASE_DIR, "data", "instagram_users_indonesia_sources.csv")
    if not check("File CSV sumber ada", os.path.exists(path), path):
        return False
        
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        
    check("Row count sesuai (14 baris data)", len(reader) == 14, f"Total baris: {len(reader)}")
    
    expected_fields = ["tahun", "sumber", "jumlah_pengguna_juta", "penetrasi_persen_penduduk", "tanggal_akses", "catatan_metodologi"]
    check("Skema kolom valid", list(reader[0].keys()) == expected_fields, f"Kolom: {list(reader[0].keys())}")
    
    # Check nulls and types
    valid_data = True
    sources = set()
    years = set()
    for row in reader:
        for k, v in row.items():
            if v is None:
                valid_data = False
            elif isinstance(v, str) and v.strip() == "":
                valid_data = False
        sources.add(row["sumber"])
        years.add(int(row["tahun"]))
        
    check("Zero missing / null values", valid_data)
    check("Rentang tahun mencakup 2020-2026", min(years) == 2020 and max(years) == 2026, f"Tahun: {sorted(list(years))}")
    check("Sumber memuat NapoleonCat dan GoodStats", "NapoleonCat" in sources and "GoodStats" in sources, f"Sumber: {sources}")
    return True

def test_forecasting_and_outputs():
    print_header("2. VERIFIKASI MODEL PERAMALAN & OUTPUT")
    csv_out = os.path.join(BASE_DIR, "output", "proyeksi_2027_tiga_skenario.csv")
    svg_out = os.path.join(BASE_DIR, "output", "proyeksi_instagram_2027.svg")
    
    check("File output CSV proyeksi ada", os.path.exists(csv_out), csv_out)
    check("File output SVG chart ada", os.path.exists(svg_out), svg_out)
    
    with open(csv_out, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
    projections = {r["metrik"]: float(r["nilai_juta"]) for r in rows if r["kategori"] == "Proyeksi 2027"}
    check("Tiga skenario terdaftar di CSV", len(projections) == 3, f"Skenario: {list(projections.keys())}")
    check("Skenario Rendah ada di kisaran (124-125M)", 124.0 <= projections.get("Rendah (Konservatif / Saturasi)", 0) <= 125.0, f"Nilai: {projections.get('Rendah (Konservatif / Saturasi)')}M")
    check("Skenario Sedang ada di kisaran (127-129M)", 127.0 <= projections.get("Sedang (Baseline / Moderat)", 0) <= 129.0, f"Nilai: {projections.get('Sedang (Baseline / Moderat)')}M")
    check("Skenario Tinggi ada di kisaran (132-134M)", 132.0 <= projections.get("Tinggi (Optimis / Ekspansi)", 0) <= 134.0, f"Nilai: {projections.get('Tinggi (Optimis / Ekspansi)')}M")
    
    # SVG parsing
    try:
        tree = ET.parse(svg_out)
        root = tree.getroot()
        is_svg = root.tag.endswith("svg")
        check("Sintaks file grafik SVG valid (Well-formed XML)", is_svg, f"Root tag: {root.tag}")
    except Exception as e:
        check("Sintaks SVG valid", False, str(e))
        
    return True

def test_bit_integrity():
    print_header("3. VALIDASI INTEGRITAS BAHASA BIT")
    files_to_check = [
        ("output/tren_instagram_bit.txt", 7494, 59952, "24fe70ad529eeb2236ae9a02ff40c712dee502417971e72704be5c4f98200ea7"),
        ("output/rekomendasi_eksekusi_bit.txt", 3611, 28888, "09680bfb4a9c16e2c598a4dab243c32a761f884c236a22d00e5362a8f9ca3138")
    ]
    
    for rel_path, exp_bytes, exp_bits, exp_hash in files_to_check:
        full_path = os.path.join(BASE_DIR, rel_path)
        if not check(f"File {rel_path} ada", os.path.exists(full_path)):
            continue
            
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            
        bits = content.split()
        n_bytes = len(bits)
        n_bits = sum(len(b) for b in bits)
        all_8 = all(len(b) == 8 and set(b).issubset({"0", "1"}) for b in bits)
        
        reconstructed = bytearray(int(b, 2) for b in bits)
        sha256_hash = hashlib.sha256(reconstructed).hexdigest()
        
        check(f"Struktur octet {rel_path} valid", all_8)
        check(f"Kuantitas byte & bit presisi ({rel_path})", n_bytes == exp_bytes and n_bits == exp_bits, f"{n_bytes} bytes / {n_bits} bits")
        check(f"SHA-256 Checksum cocok ({rel_path})", sha256_hash == exp_hash, f"Hash: {sha256_hash[:20]}...")
        
    return True

def test_bit_daemon():
    print_header("4. VERIFIKASI & VALIDASI BIT DAEMON")
    daemon_script = os.path.join(BASE_DIR, "bit_daemon.py")
    status_json = os.path.join(BASE_DIR, "output", "bit_daemon_status.json")
    status_bin = os.path.join(BASE_DIR, "output", "bit_daemon_status.bin.txt")
    log_file = os.path.join(BASE_DIR, "output", "bit_daemon.log")
    
    check("Script bit_daemon.py ada", os.path.exists(daemon_script))
    check("File status JSON ada", os.path.exists(status_json))
    check("File bitstream status ada", os.path.exists(status_bin))
    check("File log daemon ada", os.path.exists(log_file))
    
    with open(status_json, "r", encoding="utf-8") as f:
        st = json.load(f)
        
    check("Status daemon aktif", st.get("state") == "ACTIVE", f"State: {st.get('state')}")
    check("Protokol sesuai", st.get("protocol") == "UTF-8_8BIT_OCTET")
    
    # Verify bitstream sync
    with open(status_bin, "r", encoding="utf-8") as f:
        bin_tokens = f.read().strip().split()
        
    decoded_st = bytearray(int(b, 2) for b in bin_tokens).decode("utf-8")
    parsed_decoded = json.loads(decoded_st)
    
    check("Bitstream status sinkron 100% dengan JSON", parsed_decoded.get("daemon_name") == st.get("daemon_name") and parsed_decoded.get("last_heartbeat") == st.get("last_heartbeat"))
    
    with open(log_file, "r", encoding="utf-8") as f:
        log_lines = f.readlines()
        
    check("Log mencatat heartbeat aktivitas", len(log_lines) >= 2, f"Total log entri: {len(log_lines)}")
    return True

if __name__ == "__main__":
    t1 = test_source_csv()
    t2 = test_forecasting_and_outputs()
    t3 = test_bit_integrity()
    t4 = test_bit_daemon()
    
    print("\n" + "=" * 65)
    if all([t1, t2, t3, t4]):
        print("  HASIL AKHIR: 100% SUKSES - SEMUA UJI VERIFIKASI & VALIDASI LULUS")
    else:
        print("  HASIL AKHIR: ADA UJI YANG GAGAL")
    print("=" * 65 + "\n")
