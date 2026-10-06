#!/usr/bin/env python3
"""
prd_santet.py — PRD SANTET dalam bentuk Python yang bisa dijalankan   (pakai: ./bit prd)

PRD bukan lagi dokumen statis: setiap kebutuhan punya fungsi pengecek yang membaca repo,
sehingga kolom "Status" dan "Baseline hari ini" selalu dihitung ulang dari data, bukan diketik.

  ./bit prd                 ringkasan status di terminal (kebutuhan, metrik, gerbang rilis)
  ./bit prd --md            tulis juga docs/PRD_SANTET.md (versi dokumen, angka terbaru)
  ./bit prd --json          cetak JSON (untuk dashboard / CI)
  ./bit prd --gate          kode keluar 0 bila gerbang fase aktif lolos, 1 bila belum (untuk CI)
  ./bit prd putuskan        jawab 6 keputusan terbuka lewat tanya-jawab; disimpan di docs/keputusan_prd.json

Hanya pustaka standar Python.
"""
from __future__ import annotations

import csv, datetime as dt, glob, json, os, re, subprocess, sys
from dataclasses import dataclass, field, asdict
from typing import Callable, Optional

BASE = os.path.dirname(os.path.realpath(__file__))


# ================================================================== util baca repo
def p(*a):
    return os.path.join(BASE, *a)


def latest(pattern: str) -> Optional[str]:
    c = sorted(glob.glob(p(pattern)))
    return c[-1] if c else None


def read_csv(path: Optional[str]) -> list[dict]:
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f))


def read_json(path: Optional[str]) -> dict:
    if not path or not os.path.exists(path):
        return {}
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return {}


def num(x, default=None):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return default


def human_labels() -> int:
    rows = read_csv(p("annotation", "annotation_sample.csv"))
    return sum(1 for r in rows if (r.get("annotator_1") or "").strip() and (r.get("annotator_2") or "").strip())


def human_kappa() -> Optional[float]:
    v = read_json(p("annotation", "validation_result.json"))
    for k, val in v.items():
        if "manusia" in k.lower() or "human" in k.lower():
            if isinstance(val, dict) and "kappa" in val:
                return num(val["kappa"])
    return None


def llm_kappa() -> Optional[float]:
    v = read_json(p("annotation", "validation_result.json"))
    for k, val in v.items():
        if k.startswith("kappa_llm") and isinstance(val, dict):
            return num(val.get("kappa"))
    return None


def model_info() -> dict:
    return read_json(latest("results/model_*/model.json"))


def bh_passes() -> tuple[int, int]:
    rows = [r for r in read_csv(latest("results/robust_*/robustness.csv")) if num(r.get("q_BH")) is not None]
    return sum(1 for r in rows if num(r["q_BH"]) < 0.05), len(rows)


def audit_result() -> tuple[Optional[str], int]:
    d = read_json(latest("results/audit_*/audit.json"))
    if not d:
        return None, -1
    crit = sum(1 for i in d.get("items", []) if i.get("level") == "KRITIS")
    return d.get("hasil"), crit


def films_n() -> int:
    return len(read_csv(p("data", "films_clean.csv")))


def secret_present(name: str) -> bool:
    try:
        sys.path.insert(0, BASE)
        import secrets_tool  # type: ignore
        return bool(secrets_tool.resolve(name)[0])
    except Exception:
        return bool(os.environ.get(name))


def hook_installed() -> bool:
    r = subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=BASE, capture_output=True, text=True,
                       env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
    hp = os.path.join(BASE, r.stdout.strip() or ".git/hooks", "pre-commit")
    return os.path.exists(hp) and "bit secret hook" in open(hp, errors="ignore").read()


def salt_in_code() -> bool:
    try:
        return "kalimat-rahasia-yang-sama-terus" in open(p("bit"), encoding="utf-8").read()
    except Exception:
        return False


# ================================================================== model PRD
DONE, PARTIAL, TODO, BLOCKED, DEFERRED = "✅ Ada", "🟡 Sebagian", "⬜ Belum", "⏳ Menunggu", "➖ Ditunda"


@dataclass
class Requirement:
    id: str
    text: str
    priority: str          # Must / Should / Could / Won't
    acceptance: str
    check: Callable[[], tuple[str, str]] = field(repr=False)   # -> (status, bukti)
    status: str = ""
    evidence: str = ""

    def run(self):
        try:
            self.status, self.evidence = self.check()
        except Exception as e:  # satu pengecek gagal tidak menghentikan PRD
            self.status, self.evidence = "❓ Tidak bisa dicek", f"{type(e).__name__}: {e}"
        return self


def c_f01():
    files = glob.glob(p("yt_*", "comments.csv"))
    if not files:
        return TODO, "belum ada yt_*/comments.csv"
    users = [r.get("user", "") for r in read_csv(files[0])[:200]]
    ok = users and all(re.fullmatch(r"user_[0-9a-f]{8,}", u or "") for u in users)
    salt = " · ⚠️ salt default masih tertulis di kode" if salt_in_code() else ""
    return (DONE if ok else PARTIAL), f"{len(files)} set, akun {'terpseudonim' if ok else 'BELUM terpseudonim'}{salt}"


def api_runs():
    """Folder data/youtube_api/<set>_<waktu>/ yang benar-benar berisi komentar (folder kosong = run gagal)."""
    out = []
    for d in glob.glob(p("data", "youtube_api", "*")):
        files = glob.glob(os.path.join(d, "*comment*.csv"))
        if any(sum(1 for _ in open(f, encoding="utf-8", errors="ignore")) > 1 for f in files):
            out.append(d)
    return out


def c_f02():
    runs = api_runs()
    empty = len([d for d in glob.glob(p("data", "youtube_api", "*")) if os.path.isdir(d)]) - len(runs)
    note = f" · {empty} folder kosong (run gagal)" if empty else ""
    if runs:
        return DONE, f"{len(runs)} pengambilan API berisi komentar{note}"
    return BLOCKED, "API key " + ("tersimpan, jalankan ./bit precise all" if secret_present("YT_API_KEY") else "belum ada: ./bit secret set YT_API_KEY") + note


def c_f03():
    n, k = human_labels(), human_kappa()
    if n >= 100 and k is not None:
        return DONE, f"{n} baris, κ manusia = {k:.2f}"
    return (PARTIAL if n else BLOCKED), f"{n} baris berlabel dua anotator (target ≥ 100)"


def c_f04():
    hits = glob.glob(p("results", "*intent*")) + glob.glob(p("results", "*", "*intent*"))
    k = human_kappa()
    if hits and k is not None and k >= 0.8:
        return DONE, f"tervalidasi, κ = {k:.2f}"
    return (PARTIAL if hits else TODO), "hanya kategori kata kunci (sna 04_warna-niat), belum tervalidasi" if not hits else f"{len(hits)} berkas intent, belum tervalidasi"


def c_f05():
    r = latest("results/robust_*/robustness.csv")
    if not r:
        return TODO, "belum ada results/robust_*"
    ok, tot = bh_passes()
    return DONE, f"{os.path.relpath(r, BASE)} · lolos BH {ok}/{tot}"


def c_f06():
    m = model_info()
    if not m:
        return TODO, "belum ada results/model_*"
    mm, mb = num(m.get("MAPE_model_%")), num(m.get("MAPE_baseline_%"))
    win = mm is not None and mb is not None and mm < mb
    return (DONE if win else PARTIAL), f"MAPE model {mm}% vs baseline {mb}% · {'model menang' if win else 'belum mengalahkan baseline'}"


def c_f07():
    e = latest("results/sna_*/nodexl/edges.csv")
    return (DONE if e and os.path.exists(p("sna_youtube.py")) else TODO), (os.path.relpath(e, BASE) if e else "jalankan ./bit sna all")


def c_f08():
    m = latest("release/paper_package_*/MANIFEST.sha256")
    return (DONE if m else TODO), (os.path.relpath(m, BASE) if m else "jalankan ./bit package")


def c_f09():
    hasil, crit = audit_result()
    if hasil is None:
        return TODO, "jalankan ./bit audit"
    return (DONE if crit == 0 else PARTIAL), f"audit terakhir: {hasil.strip()} ({crit} kritis)"


def c_f10():
    hook = hook_installed()
    return (DONE if hook else PARTIAL), "pre-commit hook " + ("aktif" if hook else "belum dipasang: ./bit secret hook")


def c_f11():
    return (PARTIAL if os.path.exists(p("streamlit_app", "app.py")) else TODO), "streamlit_app/app.py ada · cek tampilan live & Reboot app"


def c_f12():
    d = p("docs", "papers", "introduction_draft.md")
    return (DONE if os.path.exists(d) else TODO), (f"diperbarui {dt.datetime.fromtimestamp(os.path.getmtime(d)):%d-%m-%Y %H:%M}" if os.path.exists(d) else "jalankan ./bit intro")


def c_f13():
    return DEFERRED, "dibuka hanya setelah gerbang v2.0 lolos"


REQUIREMENTS = [
    Requirement("F-01", "./bit scrape/convert: metadata & komentar trailer, akun dipseudonimkan", "Must", "Tidak ada nama akun asli; salt sama = ID sama", c_f01),
    Requirement("F-02", "./bit precise: komentar via YouTube Data API dengan tanggal tepat", "Must", "Timestamp asli; jendela H-14/H-7/H-1 terisi", c_f02),
    Requirement("F-03", "./bit sentiment validate: κ & F1 terhadap label manusia", "Must", "≥ 100 baris dua anotator; laporan κ dan F1", c_f03),
    Requirement("F-04", "Watch Intent Index per komentar", "Must", "Tervalidasi label manusia, κ ≥ 0,80", c_f04),
    Requirement("F-05", "./bit correlate/robust: Spearman eksak, bootstrap, Bonferroni, BH, parsial", "Must", "Semua uji dilaporkan, termasuk yang tidak signifikan", c_f05),
    Requirement("F-06", "./bit model: LOOCV vs baseline naif dengan CI MAPE", "Must", "Laporan menyatakan model menang/kalah", c_f06),
    Requirement("F-07", "./bit sna: 20 analisis jaringan + ekspor NodeXL", "Should", "edges/vertices terbuka di NodeXL Pro", c_f07),
    Requirement("F-08", "./bit package: paket rilis tanpa teks + MANIFEST SHA-256", "Must", "Checksum cocok; tanpa kolom teks", c_f08),
    Requirement("F-09", "./bit audit: git, Streamlit, klaim, angka, rahasia", "Must", "0 kritis sebelum setiap rilis", c_f09),
    Requirement("F-10", "./bit secret: Keychain + blokir commit berisi token", "Must", "scan bersih; hook aktif", c_f10),
    Requirement("F-11", "Dashboard Streamlit SANTET membaca results/ terbaru", "Should", "Angka dashboard = results/", c_f11),
    Requirement("F-12", "./bit intro: draf Introduction dengan angka otomatis", "Could", "Angka ikut berubah saat pipeline diulang", c_f12),
    Requirement("F-13", "Kalkulator prediksi untuk produser", "Won't (v1.0)", "Setelah model mengalahkan baseline", c_f13),
]


@dataclass
class Metric:
    name: str
    now: str
    v10: str
    v20: str


def metrics() -> list[Metric]:
    m = model_info()
    ok, tot = bh_passes()
    hasil, crit = audit_result()
    kl = llm_kappa()
    api = len(api_runs())
    return [
        Metric("Film dengan penonton bersumber", str(films_n()), "15", "≥ 40"),
        Metric("Label manusia (dua anotator)", f"{human_labels()} baris", "≥ 100, κ ≥ 0,80", "≥ 300"),
        Metric("κ antar-anotator LLM (pembanding)", f"{kl:.3f}" if kl is not None else "-", "dilaporkan", "-"),
        Metric("Uji korelasi lolos BH (q < 0,05)", f"{ok} dari {tot}", "dilaporkan", "≥ 1 sinyal pra-rilis"),
        Metric("MAPE model vs baseline", f"{m.get('MAPE_model_%', '-')}% vs {m.get('MAPE_baseline_%', '-')}%", "dilaporkan", "model < baseline, CI terpisah"),
        Metric("Pengambilan API presisi", f"{api} run", "semua set", "semua set"),
        Metric("Hasil ./bit audit", f"{(hasil or 'belum dijalankan').strip()} ({max(crit, 0)} kritis)", "0 kritis", "0 kritis, 0 peringatan"),
    ]


@dataclass
class Gate:
    phase: str
    items: list[str]
    criteria: list[tuple[str, Callable[[], bool]]] = field(repr=False)

    def evaluate(self):
        return [(text, bool(fn())) for text, fn in self.criteria]


def _safe(fn):
    def w():
        try:
            return fn()
        except Exception:
            return False
    return w


GATES = [
    Gate("v1.0 · Riset jujur", ["100 label manusia, 2 anotator", "Salt baru, results/ diulang", "Paper explanatory dikirim"], [
        ("./bit audit: 0 kritis", _safe(lambda: audit_result()[1] == 0)),
        ("≥ 100 label manusia", _safe(lambda: human_labels() >= 100)),
        ("κ antar-anotator manusia ≥ 0,80", _safe(lambda: (human_kappa() or 0) >= 0.80)),
        ("Salt default tidak lagi tertulis di kode", _safe(lambda: not salt_in_code())),
    ]),
    Gate("v1.1 · Data presisi", ["Komentar via YouTube API", "Jendela H-14 / H-7 / H-1", "Watch Intent Index tervalidasi"], [
        ("Data YouTube API presisi tersedia", _safe(lambda: bool(api_runs()))),
        ("Watch Intent Index tervalidasi (F-04)", _safe(lambda: c_f04()[0] == DONE)),
    ]),
    Gate("v2.0 · Prediktif", ["Ekspansi ke 40+ film", "Model dibanding baseline", "Kalkulator untuk produser"], [
        ("≥ 40 film bersumber", _safe(lambda: films_n() >= 40)),
        ("MAPE model < baseline", _safe(lambda: num(model_info().get("MAPE_model_%"), 999) < num(model_info().get("MAPE_baseline_%"), 0))),
        ("CI MAPE model dan baseline tidak tumpang tindih", _safe(lambda: model_info()["MAPE_model_CI95_%"][1] < model_info()["MAPE_baseline_CI95_%"][0])),
    ]),
]

DECISION_SPECS = [  # (kunci, pertanyaan, pilihan; [] = jawaban bebas)
    ("framing", "Setuju v1.0 diposisikan sebagai riset explanatory (n = 15) dan klaim prediktif ditunda ke v2.0?",
     ["Setuju", "Tidak, tetap prediktif di v1.0"]),
    ("salt", "Ganti salt pseudonim kapan? (semua ID berubah, results/ dibuat ulang)",
     ["Sekarang, sebelum rilis dataset", "Setelah ekspansi data v2.0"]),
    ("anotator", "Siapa anotator kedua dan kapan 100 baris label selesai?", []),
    ("repo", "Repo GitHub untuk SANTET?",
     ["Tetap prediksi-movie-2027", "Repo terpisah khusus SANTET"]),
    ("jurnal", "Jurnal target pertama?",
     ["Jalur komunikasi (mis. Asian Journal of Communication)", "Jalur data (mis. Telematics and Informatics)"]),
    ("kpi_instagram", "Angka κ 0,8342 dan MAPE 1,55% di script proyek Instagram?",
     ["Ada sumber hitungannya (simpan & tautkan)", "Hapus dari kode"]),
]
DECISIONS = [q for _, q, _ in DECISION_SPECS]
DECISIONS_FILE = os.path.join(BASE, "docs", "keputusan_prd.json")


def load_decisions() -> dict:
    return read_json(DECISIONS_FILE)


def decide():
    """Tanya-jawab di terminal; jawaban disimpan ke docs/keputusan_prd.json (bisa diubah kapan saja)."""
    saved = load_decisions()
    print("Keputusan terbuka PRD SANTET · Enter = lewati / pertahankan jawaban lama\n")
    for i, (key, q, opts) in enumerate(DECISION_SPECS, 1):
        old = saved.get(key, {}).get("jawaban")
        print(f"{i}. {q}" + (f"\n   (sekarang: {old})" if old else ""))
        for j, o in enumerate(opts, 1):
            print(f"   [{j}] {o}")
        ans = input("   jawab" + (" nomor" if opts else "") + ": ").strip()
        if not ans:
            print()
            continue
        if opts and ans.isdigit() and 1 <= int(ans) <= len(opts):
            ans = opts[int(ans) - 1]
        saved[key] = {"pertanyaan": q, "jawaban": ans, "tanggal": f"{dt.datetime.now():%Y-%m-%d %H:%M}"}
        print(f"   ✅ {ans}\n")
    os.makedirs(os.path.dirname(DECISIONS_FILE), exist_ok=True)
    json.dump(saved, open(DECISIONS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"📄 {os.path.relpath(DECISIONS_FILE, BASE)} · {len(saved)}/{len(DECISION_SPECS)} keputusan terjawab")

META = {
    "produk": "SANTET — Sentiment Analysis for Nusantara Theatrical Expectation Tracking",
    "tagline": "Membaca 'mantra' warganet sebelum film tayang · Fear is demand",
    "pemilik": "Indri Anjar Kartika Sari",
    "ringkasan": ("SANTET (Sentiment Analysis for Nusantara Theatrical Expectation Tracking) adalah perangkat riset terbuka "
                  "yang membaca sinyal digital pra-rilis film horor Indonesia untuk memperkirakan minat menonton."),
    "cerita": ("Setiap film lahir dari kerja bertahun-tahun, tetapi nasibnya baru diketahui setelah layar menyala. "
               "Padahal penonton sudah memberi tanda jauh sebelumnya: di kolom komentar trailer, mereka menulis "
               "\"serem banget\" dan \"gas nonton\". SANTET hadir agar suara itu terdengar tepat waktu, "
               "saat keputusan masih bisa diubah."),
    "independensi": "Riset akademik independen; tidak berafiliasi dengan Soraya Intercine Films, Hitmaker Studios, atau MD Pictures.",
}


# ================================================================== keluaran
def build():
    reqs = [r.run() for r in REQUIREMENTS]
    gates = [(g, g.evaluate()) for g in GATES]
    active = next((g for g, res in gates if not all(ok for _, ok in res)), None)
    return reqs, metrics(), gates, active


def to_markdown(reqs, mets, gates, active) -> str:
    L = [f"# PRD {META['produk'].split(' —')[0]}", "",
         f"_{dt.datetime.now():%d-%m-%Y %H:%M} WIB · {META['pemilik']} · dibuat otomatis oleh `./bit prd` — status & baseline dihitung dari repo_", "",
         f"**{META['produk']}** — {META['tagline']}", "",
         "## Ringkasan eksekutif", "", META["ringkasan"], "", META["cerita"], "",
         f"> {META['independensi']}", "",
         f"**Fase aktif:** {active.phase if active else 'semua gerbang lolos'}", "",
         "## Kebutuhan fungsional", "", "| ID | Kebutuhan | Prioritas | Kriteria terima | Status | Bukti |", "|---|---|---|---|---|---|"]
    L += [f"| {r.id} | {r.text} | {r.priority} | {r.acceptance} | {r.status} | {r.evidence} |" for r in reqs]
    L += ["", "## Metrik keberhasilan", "", "| Metrik | Hari ini | Target v1.0 | Target v2.0 |", "|---|---|---|---|"]
    L += [f"| {m.name} | {m.now} | {m.v10} | {m.v20} |" for m in mets]
    L += ["", "## Gerbang rilis", ""]
    for g, res in gates:
        L.append(f"**{g.phase}** — " + " · ".join(g.items))
        L += [f"- [{'x' if ok else ' '}] {t}" for t, ok in res]
        L.append("")
    dec = load_decisions()
    L += ["## Keputusan", ""]
    for key, q, _ in DECISION_SPECS:
        a = dec.get(key, {})
        L.append(f"- [x] {q} → **{a['jawaban']}** ({a['tanggal']})" if a.get("jawaban") else f"- [ ] {q}")
    return "\n".join(L) + "\n"


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if argv[:1] == ["putuskan"]:
        decide()
        return 0
    reqs, mets, gates, active = build()
    if "--json" in argv:
        print(json.dumps({"meta": META, "requirements": [{k: v for k, v in asdict(r).items() if k != "check"} for r in reqs],
                          "metrics": [asdict(m) for m in mets],
                          "gates": [{"phase": g.phase, "items": g.items, "criteria": [{"text": t, "ok": ok} for t, ok in res]} for g, res in gates],
                          "active_phase": active.phase if active else None, "decisions": DECISIONS}, ensure_ascii=False, indent=2))
        return 0
    import textwrap
    print(f"\n🕯️  PRD {META['produk']}\n   {META['tagline']}\n")
    for para in (META["ringkasan"], META["cerita"]):
        print(textwrap.fill(para, 100, initial_indent="   ", subsequent_indent="   ") + "\n")
    print("— Kebutuhan fungsional")
    for r in reqs:
        print(f"  {r.status:<14} {r.id} [{r.priority}] {r.text}\n{'':17}↳ {r.evidence}")
    print("\n— Metrik (hari ini → target v1.0 → v2.0)")
    for m in mets:
        print(f"  • {m.name}: {m.now} → {m.v10} → {m.v20}")
    print("\n— Gerbang rilis")
    for g, res in gates:
        mark = "▶" if g is active else ("✓" if all(ok for _, ok in res) else " ")
        print(f"  {mark} {g.phase}")
        for t, ok in res:
            print(f"      [{'x' if ok else ' '}] {t}")
    print("\n— Keputusan")
    dec = load_decisions()
    for key, q, _ in DECISION_SPECS:
        a = dec.get(key, {}).get("jawaban")
        print(f"  [{'x' if a else ' '}] {q}" + (f" → {a}" if a else ""))
    if len(dec) < len(DECISION_SPECS):
        print("      jawab di terminal: ./bit prd putuskan")
    print(f"\nFase aktif: {active.phase if active else 'semua gerbang lolos'}")
    if "--md" in argv:
        out = p("docs", "PRD_SANTET.md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(to_markdown(reqs, mets, gates, active))
        print(f"📄 {os.path.relpath(out, BASE)}")
    if "--gate" in argv and active is not None:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
