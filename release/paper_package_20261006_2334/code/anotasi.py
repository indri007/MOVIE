#!/usr/bin/env python3
"""
anotasi.py — Anotasi sentimen di terminal, satu komentar per layar   (pakai: ./bit anotasi 1 | 2)

  ./bit anotasi 1          anotator pertama mengisi kolom annotator_1
  ./bit anotasi 2          anotator kedua mengisi kolom annotator_2 (buta: label anotator 1 tidak ditampilkan)
  ./bit anotasi status     progres kedua anotator

Tombol:  1 = positif · 2 = netral · 3 = negatif · c = catatan · b = kembali · s = lewati · q = simpan & keluar
Setiap jawaban langsung disimpan, jadi aman ditutup kapan saja dan dilanjutkan nanti.
Panduan label: annotation/PANDUAN_ANOTASI.md ("serem banget" pada film horor = positif bila nadanya kagum).
"""
import csv, os, shutil, sys, tempfile, textwrap

BASE = os.path.dirname(os.path.realpath(__file__))
SHEET = os.path.join(BASE, "annotation", "annotation_sample.csv")
KEYS = {"1": "positif", "2": "netral", "3": "negatif"}
TARGET = 100


def load():
    if not os.path.exists(SHEET):
        sys.exit("⛔ Lembar anotasi belum ada. Buat dulu: ./bit sentiment sample --n 300")
    with open(SHEET, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def save(fields, rows):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(SHEET), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, SHEET)  # tulis atomik: file tidak pernah setengah jadi


def status(rows):
    a1 = sum(1 for r in rows if (r.get("annotator_1") or "").strip())
    a2 = sum(1 for r in rows if (r.get("annotator_2") or "").strip())
    both = sum(1 for r in rows if (r.get("annotator_1") or "").strip() and (r.get("annotator_2") or "").strip())
    bar = lambda n: "█" * int(20 * min(n, TARGET) / TARGET) + "░" * (20 - int(20 * min(n, TARGET) / TARGET))
    print(f"\nAnotator 1 : {bar(a1)} {a1}/{len(rows)}")
    print(f"Anotator 2 : {bar(a2)} {a2}/{len(rows)}")
    print(f"Lengkap 2x : {bar(both)} {both} (target ≥ {TARGET} untuk gerbang v1.0)")
    if both >= 30:
        print("→ Sudah bisa dihitung: ./bit sentiment validate")
    print()


def run(who):
    col = f"annotator_{who}"
    fields, rows = load()
    if "catatan" not in fields:
        fields.append("catatan")
    todo = [i for i, r in enumerate(rows) if not (r.get(col) or "").strip()]
    if not todo:
        print(f"✅ Semua {len(rows)} baris {col} sudah terisi."); status(rows); return
    print(f"\nAnotasi sebagai ANOTATOR {who} · {len(todo)} baris tersisa · panduan: annotation/PANDUAN_ANOTASI.md")
    print("1 positif · 2 netral · 3 negatif · c catatan · b kembali · s lewati · q keluar\n")
    history, k = [], 0
    while k < len(todo):
        i = todo[k]
        r = rows[i]
        done = len(rows) - sum(1 for x in rows if not (x.get(col) or "").strip())
        print("─" * 72)
        print(f"[{done + 1}/{len(rows)}]  video {r.get('video_id', '')}")
        print(textwrap.fill((r.get("text") or "").strip(), 70, initial_indent="  ", subsequent_indent="  "))
        ans = input("label > ").strip().lower()
        if ans == "q":
            break
        if ans == "s":
            k += 1; continue
        if ans == "b" and history:
            j = history.pop()
            rows[j][col] = ""
            save(fields, rows)
            k = todo.index(j); continue
        if ans == "c":
            r["catatan"] = input("catatan > ").strip()
            ans = input("label > ").strip().lower()
        if ans in KEYS or ans in KEYS.values():
            r[col] = KEYS.get(ans, ans)
            save(fields, rows)
            history.append(i)
            k += 1
        else:
            print("  ketik 1, 2, 3, c, b, s, atau q")
    status(rows)


def main(a):
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__); return
    if a[0] == "status":
        status(load()[1]); return
    if a[0] not in ("1", "2"):
        sys.exit("Pakai: ./bit anotasi 1  atau  ./bit anotasi 2")
    try:
        run(a[0])
    except (KeyboardInterrupt, EOFError):
        print("\n💾 Tersimpan. Lanjutkan kapan saja dengan perintah yang sama.")


if __name__ == "__main__":
    main(sys.argv[1:])
