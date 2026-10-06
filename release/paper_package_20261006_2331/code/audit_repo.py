#!/usr/bin/env python3
"""
audit_repo.py — Audit integritas GitHub + Streamlit untuk proyek SANTET   (pakai: ./bit audit)

Memeriksa, tanpa mengubah apa pun:
  G  Git      : remote, posisi lokal vs GitHub (ahead/behind), file penting yang belum di-commit/push
  S  Streamlit: file mana yang dijalankan Streamlit Cloud dari GitHub, proyek apa yang tampil, status URL
  C  Klaim    : DOI/Scopus ID/badge/angka yang tidak didukung data, link file:///, klaim berlebihan
  D  Data     : angka di README & halaman docs cocok dengan data/films_clean.csv dan results/ terbaru
  K  Keamanan : token/API key di file & riwayat git, token di ~/.zsh_history, teks komentar mentah ter-commit

Opsi:
  --no-fetch        jangan `git fetch` (pakai info origin terakhir yang tersimpan)
  --url URL         URL aplikasi Streamlit yang dicek (default: URL SANTET)
  --bin             tulis juga laporan dalam biner 8-bit (UTF-8, bisa dibalik)

Keluaran: results/audit_<waktu>/audit.md (+ audit.json, audit.bin.txt)
Kode keluar: 0 = aman, 1 = ada PERINGATAN, 2 = ada KRITIS
Hanya pustaka standar Python (tanpa pandas), agar bisa jalan di mana saja.
"""
import argparse, csv, datetime as dt, glob, json, os, re, subprocess, sys, urllib.request

BASE = os.path.dirname(os.path.realpath(__file__))
DEFAULT_URL = "https://santet-soraya-film-explorer-vw6emk9y9yavz2cxuaghkj.streamlit.app/"
SCAN_EXT = (".md", ".py", ".html", ".svg", ".txt", ".toml", ".json", ".js")
SKIP_DIRS = ("_backup", ".venv", ".git", "node_modules", "release", "__pycache__", "_to_delete", "downloads", "output", "results")

CLAIMS = [  # (level, pola, penjelasan)
    ("KRITIS", r"10\.1016/j\.ipm\.2026\.\d+", "DOI Elsevier untuk naskah yang belum terbit"),
    ("KRITIS", r"Scopus ID:?\s*\d{6,}", "Scopus ID yang tidak terverifikasi"),
    ("KRITIS", r"Scopus Q1 (Ready|Journal:\s*AVAILABLE)|SCOPUS Q1 ELSEVIER", "status 'Scopus Q1' padahal belum terbit"),
    ("KRITIS", r"100%\s*KPI", "klaim '100% KPI matched'"),
    ("PERINGATAN", r"badge/Spearman[^)]*-success", "badge hijau signifikansi (tidak lolos koreksi BH)"),
    ("PERINGATAN", r"MAPE\s*1[.,]55", "MAPE 1,55% tidak cocok dengan hasil model repo"),
    ("PERINGATAN", r"[Kk]appa\s*[κ=:]?\s*0[.,]83", "Cohen's kappa 0,83 tidak cocok dengan validation_result.json"),
    ("PERINGATAN", r"file:///", "link ke file di laptop (rusak di GitHub/Streamlit)"),
    ("PERINGATAN", r"estimasi akurat|sangat akurat|highly accurate", "klaim akurasi tanpa dasar"),
    ("PERINGATAN", r"(sistem|studi|riset|model)[^.\n]{0,40}\bpertama\b", "klaim 'pertama' belum diverifikasi SLR"),
]
SECRETS = [
    (r"ghp_[A-Za-z0-9]{30,}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{40,}", "GitHub fine-grained token"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key (YouTube Data API)"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI-style API key"),
    (r"apify_api_[A-Za-z0-9]{20,}", "Apify token"),
]


def sh(cmd, timeout=60):
    try:
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", LC_ALL="C.UTF-8")
        r = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True, timeout=timeout, env=env)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


class Report:
    def __init__(self):
        self.items = []

    def add(self, kode, level, judul, detail="", bukti=None):
        self.items.append({"kode": kode, "level": level, "judul": judul, "detail": detail, "bukti": bukti or []})
        icon = {"KRITIS": "❌", "PERINGATAN": "⚠️ ", "OK": "✅", "INFO": "ℹ️ "}[level]
        print(f"{icon} [{kode}] {judul}" + (f" — {detail}" if detail else ""))
        for b in (bukti or [])[:5]:
            print(f"      · {b}")

    def worst(self):
        lv = {x["level"] for x in self.items}
        return 2 if "KRITIS" in lv else 1 if "PERINGATAN" in lv else 0


# ------------------------------------------------------------------ G: git
def audit_git(R, fetch):
    remote = sh(["git", "remote"])[1].split("\n")[0] or "origin"
    url = sh(["git", "remote", "get-url", remote])[1]
    R.add("G1", "INFO", "Remote GitHub", f"{remote} → {url or '(tidak ada)'}")
    if fetch:
        rc, _, err = sh(["git", "fetch", "--quiet", remote], timeout=90)
        R.add("G2", "OK" if rc == 0 else "PERINGATAN", "git fetch", "berhasil" if rc == 0 else f"gagal: {err[:120]} (hasil di bawah memakai info lama)")
    branch = sh(["git", "branch", "--show-current"])[1] or "main"
    up = f"{remote}/{branch}"
    rc, out, _ = sh(["git", "rev-list", "--left-right", "--count", f"HEAD...{up}"])
    if rc == 0 and out:
        ahead, behind = map(int, out.split())
        head = sh(["git", "log", "--oneline", "-1", "HEAD"])[1]
        rhead = sh(["git", "log", "--oneline", "-1", up])[1]
        lvl = "OK" if ahead == behind == 0 else "PERINGATAN"
        R.add("G3", lvl, "Lokal vs GitHub", f"lokal lebih maju {ahead} commit, tertinggal {behind} commit",
              [f"lokal  : {head}", f"GitHub : {rhead}"] +
              (["GitHub tidak memuat commit terbaru lokal → Streamlit & Pages menjalankan versi lama"] if ahead else []))
    else:
        R.add("G3", "PERINGATAN", "Lokal vs GitHub", f"tidak bisa membandingkan dengan {up}")
    st = sh(["git", "status", "--porcelain"])[1].splitlines()
    mod = [l for l in st if not l.startswith("??")]
    unt = [l[3:] for l in st if l.startswith("??")]
    R.add("G4", "PERINGATAN" if st else "OK", "Perubahan belum di-commit", f"{len(mod)} file diubah, {len(unt)} file/folder baru", (mod + ["?? " + u for u in unt])[:8])
    key = ["streamlit_app.py", "streamlit_app", "docs/santet", "docs/santet-3d", "docs/assets", "sna_youtube.py", "intro_draft.py", "audit_repo.py"]
    missing = [k for k in key if os.path.exists(os.path.join(BASE, k)) and sh(["git", "cat-file", "-e", f"{up}:{k}"])[0] != 0]
    R.add("G5", "PERINGATAN" if missing else "OK", "File penting belum ada di GitHub",
          f"{len(missing)} item hanya ada di laptop" if missing else "semua sudah ada di GitHub", missing)
    return up


# ------------------------------------------------------------------ S: streamlit
def audit_streamlit(R, up, url):
    cands = ["streamlit_app.py", "app.py", "streamlit_app/app.py", "dashboard/app.py"]
    on_remote = [c for c in cands if sh(["git", "cat-file", "-e", f"{up}:{c}"])[0] == 0]
    entry = on_remote[0] if on_remote else None
    R.add("S1", "INFO" if entry else "KRITIS", "Entrypoint Streamlit di GitHub",
          f"kemungkinan dijalankan: {entry}" if entry else "tidak ada file app di GitHub",
          [f"tersedia di GitHub: {', '.join(on_remote) or '-'}",
           "Cek di Streamlit Cloud → Manage app → Settings → 'Main file path' harus sama"])
    if entry:
        src = sh(["git", "show", f"{up}:{entry}"])[1]
        if "runpy" in src and "streamlit_app/app.py" not in on_remote:
            R.add("S2", "KRITIS", "Entrypoint memanggil file yang tidak ada di GitHub", f"{entry} → streamlit_app/app.py belum di-push")
        proj = "SANTET" if re.search(r"SANTET|Soraya|horor", src, re.I) else "Instagram" if re.search(r"Instagram", src, re.I) else "?"
        if proj != "SANTET" and "runpy" in src:
            inner = sh(["git", "show", f"{up}:streamlit_app/app.py"])[1]
            proj = "SANTET" if re.search(r"SANTET|Soraya", inner) else proj
        R.add("S3", "OK" if proj == "SANTET" else "KRITIS", "Proyek yang tampil di Streamlit",
              f"{proj}" + ("" if proj == "SANTET" else " — bukan SANTET; push streamlit_app.py + streamlit_app/ atau ubah Main file path"))
        hits = scan_text(src, entry)
        for lvl in ("KRITIS", "PERINGATAN"):
            h = [x for x in hits if x[0] == lvl]
            if h:
                R.add("S4", lvl, f"Klaim bermasalah di app yang LIVE ({entry})", f"{len(h)} temuan", [f"{b} — {why}" for _, b, why in h])
        if not hits:
            R.add("S4", "OK", f"Tidak ada klaim bermasalah di {entry}")
    try:
        req = urllib.request.Request(url.rstrip("/") + "/_stcore/health", headers={"User-Agent": "santet-audit"})
        with urllib.request.urlopen(req, timeout=20) as r:
            R.add("S5", "OK", "URL Streamlit merespons", f"HTTP {r.status} · {url}")
    except Exception as e:
        R.add("S5", "INFO", "URL Streamlit tidak bisa dicek otomatis", f"{type(e).__name__}: {str(e)[:100]} · buka manual: {url}")


# ------------------------------------------------------------------ C: klaim
def scan_text(text, name):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"tidak mengklaim|jangan (menulis|memakai|gunakan)|tidak mengarah|di script proyek Instagram\?|do not claim|not claim|tidak boleh", line, re.I):
            continue  # kalimat yang justru melarang klaim tsb
        for lvl, pat, why in CLAIMS:
            if re.search(pat, line, re.I):
                out.append((lvl, f"{name}:{i}: {line.strip()[:90]}", why))
    return out


def files_to_scan():
    for root, dirs, files in os.walk(BASE):
        rel = os.path.relpath(root, BASE)
        if any(rel == d or rel.startswith(d + os.sep) for d in SKIP_DIRS):
            dirs[:] = []
            continue
        for f in files:
            if f.endswith(SCAN_EXT) and f not in ("audit_repo.py", "secrets_tool.py"):
                yield os.path.join(root, f)


def audit_claims(R):
    hits = []
    for p in files_to_scan():
        try:
            txt = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if len(txt) > 3_000_000:
            continue
        hits += scan_text(txt, os.path.relpath(p, BASE))
    for lvl in ("KRITIS", "PERINGATAN"):
        h = [x for x in hits if x[0] == lvl]
        files = sorted({b.split(":")[0] for _, b, _ in h})
        if h:
            R.add("C1" if lvl == "KRITIS" else "C2", lvl, f"Klaim bermasalah di folder kerja ({lvl.lower()})",
                  f"{len(h)} baris di {len(files)} file", [f"{b} — {why}" for _, b, why in h][:12])
    if not hits:
        R.add("C1", "OK", "Tidak ada klaim bermasalah di folder kerja")


# ------------------------------------------------------------------ D: data
def latest(pat):
    c = sorted(glob.glob(os.path.join(BASE, pat)))
    return c[-1] if c else None


def fmt_id(n):
    return f"{int(n):,}".replace(",", ".")


def audit_data(R):
    fc = os.path.join(BASE, "data", "films_clean.csv")
    if not os.path.exists(fc):
        R.add("D1", "PERINGATAN", "data/films_clean.csv tidak ada", "jalankan ./bit rebuild-master"); return
    rows = {r["film_id"]: r for r in csv.DictReader(open(fc, encoding="utf-8"))}
    expect = {}
    if "suzzanna-2018" in rows:
        expect["Suzzanna 2018"] = fmt_id(float(rows["suzzanna-2018"]["penonton"]))
    if "racun-sangga-2024" in rows:
        expect["Racun Sangga 2024"] = fmt_id(float(rows["racun-sangga-2024"]["penonton"]))
    rob = latest("results/robust_*/robustness.csv")
    q = None
    if rob:
        for r in csv.DictReader(open(rob, encoding="utf-8")):
            if r["metrik"] == "likes_total":
                expect["rho likes"] = f"{float(r['rho']):.3f}".replace(".", ",")
                q = float(r["q_BH"])
    sdir = latest("results/sentiment_*")
    if sdir and os.path.exists(os.path.join(sdir, "crosstab_lexicon_vs_indobert.csv")):
        ct = {r["sent_lexicon"]: r for r in csv.DictReader(open(os.path.join(sdir, "crosstab_lexicon_vs_indobert.csv"), encoding="utf-8"))}
        a = ct["All"]
        expect["% negatif model"] = f"{100*float(a['negatif'])/float(a['All']):.1f}".replace(".", ",")
        expect["% negatif leksikon"] = f"{100*float(ct['negatif']['All'])/float(a['All']):.1f}".replace(".", ",")
    targets = ["README.md", "docs/santet/index.html", "docs/santet-3d/index.html", "docs/assets/santet_hero.svg", "docs/papers/introduction_draft.md"]
    bukti, bad = [], 0
    for t in targets:
        p = os.path.join(BASE, t)
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8", errors="ignore").read()
        txt_n = txt.replace("3,346,216", "3.346.216").replace("525,034", "525.034").replace("51.2%", "51,2%").replace("10.0%", "10,0%").replace("0.571", "0,571")
        for k, v in expect.items():
            ok = v in txt_n
            if not ok and k in ("Suzzanna 2018", "Racun Sangga 2024", "% negatif model", "% negatif leksikon"):
                # hanya laporkan bila file memang membahas angka itu tapi dengan nilai lain
                if (k.startswith("Suzzanna") and "Bernapas" in txt) or (k.startswith("Racun") and "Racun Sangga" in txt) or (k.startswith("%") and re.search(r"\d+[.,]\d\s*%\s*negatif", txt_n)):
                    bad += 1; bukti.append(f"{t}: tidak memuat {k} = {v}")
        if "Racun Sangga" in txt and "525" in txt and not re.search(r"sementara|provisional|\*", txt):
            bad += 1; bukti.append(f"{t}: angka Racun Sangga tanpa tanda 'sementara'")
        if q is not None and q >= 0.05 and re.search(r"signifikan", txt, re.I) and not re.search(r"tidak lolos|q\s*=\s*0[.,]2", txt):
            bukti.append(f"{t}: menyebut 'signifikan' tanpa menyebut koreksi BH (q = {q:.2f})")
    R.add("D1", "PERINGATAN" if bad else "OK", "Angka di landing page vs data",
          "; ".join(f"{k}={v}" for k, v in expect.items()), bukti)


# ------------------------------------------------------------------ K: keamanan
def audit_security(R, up):
    found, cur = [], ""
    for p in files_to_scan():
        try:
            txt = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for pat, what in SECRETS:
            if re.search(pat, txt):
                found.append(f"{os.path.relpath(p, BASE)}: {what}")
    rc, out, _ = sh(["git", "log", "--all", "-p", "-G", "ghp_[A-Za-z0-9]{30}|github_pat_[A-Za-z0-9_]{40}|AIza[0-9A-Za-z_-]{35}",
                     "--format=%h %s", "--", ".", ":(exclude)audit_repo.py", ":(exclude)secrets_tool.py"], timeout=120)
    hist = []
    for l in out.splitlines():
        if re.match(r"^[0-9a-f]{7,} ", l):
            cur = l
        elif l.startswith("+") and any(re.search(p, l) for p, _ in SECRETS) and cur not in hist:
            hist.append(cur)
    found += [f"riwayat git {h}" for h in hist[:5]]
    R.add("K1", "KRITIS" if found else "OK", "Token / API key di repo", f"{len(found)} temuan (nilai tidak ditampilkan)" if found else "tidak ditemukan", found)
    hp = os.path.expanduser("~/.zsh_history")
    if os.path.exists(hp):
        try:
            n = sum(1 for _ in re.finditer(rb"ghp_[A-Za-z0-9]{20,}|github_pat_", open(hp, "rb").read()))
            R.add("K2", "KRITIS" if n else "OK", "Token GitHub di ~/.zsh_history",
                  f"{n} kemunculan — hapus: LC_ALL=C sed -i '' '/ghp_/d' ~/.zsh_history, lalu REVOKE di GitHub" if n else "bersih")
        except Exception as e:
            R.add("K2", "INFO", "~/.zsh_history tidak bisa dibaca", str(e)[:80])
    tracked = sh(["git", "ls-tree", "-r", "--name-only", up])[1].splitlines()
    raw = [t for t in tracked if re.search(r"(^|/)yt_[^/]+/comments\.csv$|comments_sentiment\.csv$", t)]
    R.add("K3", "PERINGATAN" if raw else "OK", "Teks komentar mentah di GitHub (UU PDP)",
          f"{len(raw)} file berisi teks komentar publik ter-commit — pertimbangkan .gitignore & paket tanpa teks" if raw else "tidak ada", raw)


# ------------------------------------------------------------------ main
def to_binary(text):
    return " ".join(f"{b:08b}" for b in text.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--bin", action="store_true")
    a = ap.parse_args()
    if sh(["git", "rev-parse", "--is-inside-work-tree"])[0] != 0:
        sys.exit("Folder ini bukan repo git.")
    print("\n🕯️  SANTET · audit GitHub + Streamlit\n")
    R = Report()
    print("— G · Git"); up = audit_git(R, not a.no_fetch)
    print("\n— S · Streamlit"); audit_streamlit(R, up, a.url)
    print("\n— C · Klaim"); audit_claims(R)
    print("\n— D · Data"); audit_data(R)
    print("\n— K · Keamanan"); audit_security(R, up)
    w = R.worst()
    verdict = ["✅ AMAN", "⚠️  ADA PERINGATAN", "❌ ADA MASALAH KRITIS"][w]
    print(f"\nHasil: {verdict}")
    out = os.path.join(BASE, "results", f"audit_{dt.datetime.now():%Y%m%d_%H%M}")
    os.makedirs(out, exist_ok=True)
    md = [f"# Audit SANTET · GitHub + Streamlit\n\n_{dt.datetime.now():%d-%m-%Y %H:%M} WIB · hasil: **{verdict}**_\n",
          "| Kode | Level | Pemeriksaan | Keterangan |", "|---|---|---|---|"]
    for i in R.items:
        md.append(f"| {i['kode']} | {i['level']} | {i['judul']} | {i['detail'].replace('|', '/')} |")
    md.append("\n## Bukti\n")
    for i in R.items:
        if i["bukti"]:
            md.append(f"**{i['kode']} · {i['judul']}**\n" + "\n".join(f"- `{b}`" for b in i["bukti"]) + "\n")
    text = "\n".join(md)
    open(os.path.join(out, "audit.md"), "w", encoding="utf-8").write(text)
    json.dump({"hasil": verdict, "items": R.items}, open(os.path.join(out, "audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"📄 {os.path.relpath(out, BASE)}/audit.md")
    if a.bin:
        p = os.path.join(out, "audit.bin.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write("# SANTET · audit dalam biner 8-bit (UTF-8). Baris ke-3 dst. = isi.\n#\n" + to_binary(text))
        back = bytes(int(b, 2) for b in open(p, encoding="utf-8").read().split("\n", 2)[2].split()).decode("utf-8")
        assert back == text
        print(f"🔢 {os.path.relpath(p, BASE)} (terverifikasi lossless)")
    sys.exit(w)


if __name__ == "__main__":
    main()
