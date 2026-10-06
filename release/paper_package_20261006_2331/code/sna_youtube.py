#!/usr/bin/env python3
"""
sna_youtube.py — 20 analisis jaringan ala NodeXL untuk komentar trailer YouTube (proyek SANTET)

Pakai lewat CLI:
  ./bit sna list                    daftar 20 perintah
  ./bit sna 7                       jalankan analisis nomor 7
  ./bit sna komunitas irisan        jalankan beberapa sekaligus (nomor atau nama)
  ./bit sna all                     jalankan semua 20
  opsi: --set soraya,md            batasi set data (default: semua yt_*/)
        --bin                      tambahkan ringkasan dalam bahasa biner 8-bit (UTF-8, bisa dibalik)

Input : yt_<set>/comments.csv, videos.csv, ids_<set>.txt, data/films_clean.csv (tanggal rilis, waralaba)
Output: results/sna_<waktu>/NN_<nama>.{csv,png,graphml} + ringkasan.md (+ ringkasan.bin.txt)

Catatan etika: akun sudah berupa pseudonim (user_<hash>) dari pipeline scrape. Script ini tidak pernah
menulis teks komentar utuh ke keluaran; yang ditulis hanya hitungan, kata, dan pseudonim.
"""
import argparse, collections, datetime as dt, glob, math, os, re, sys

import networkx as nx
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.realpath(__file__))
SEED = 42

# ------------------------------------------------------------------ leksikon (eksploratif, belum tervalidasi)
FEAR = ["serem", "seram", "merinding", "ngeri", "takut", "horor", "horror", "jumpscare", "mencekam", "creepy", "bulu kuduk"]
INTENT = ["gas nonton", "wajib nonton", "harus nonton", "mau nonton", "pengen nonton", "pingin nonton", "auto nonton",
          "nonton di bioskop", "ke bioskop", "beli tiket", "tiket", "otw", "ditunggu", "gak sabar", "ga sabar",
          "nggak sabar", "tayang kapan", "kapan tayang", "first day", "hari pertama", "🎟", "🍿"]
STOP = set("""yang dan di ke dari ini itu ada aja aku gue gua gw lo lu kamu kau dia mereka kita kami jadi juga udah sudah
belum bisa akan atau tapi karena kalo kalau sama dengan buat untuk utk pada dalam nya nih sih deh dong kok kan lah ya yg
ga gak nggak enggak tidak bukan banget bgt apa siapa kenapa gimana mana kapan saja lagi masih tuh pun para
the a an of to is and in it you i this that for on so be are was my me not with just like""".split())
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")
WORD_RE = re.compile(r"[a-zA-Z\u00C0-\u024F]{3,}")
HASHTAG_RE = re.compile(r"#\w+")

COMMANDS = [
    # nomor, nama, judul, kelompok
    (1, "peta", "Peta jaringan keseluruhan (komentator–film + balasan)", "Gambar graf"),
    (2, "grup-kotak", "Group-in-a-Box: tiap komunitas dalam kotak sendiri", "Gambar graf"),
    (3, "per-film", "Graf balasan per film (small multiples)", "Gambar graf"),
    (4, "warna-niat", "Graf berwarna kategori komentar (takut / niat menonton / lain)", "Gambar graf"),
    (5, "film-film", "Proyeksi film–film: tebal garis = komentator bersama", "Gambar graf"),
    (6, "densitas", "Densitas & komponen terhubung per film", "Hubungan"),
    (7, "komunitas", "Komunitas Louvain + modularitas Q", "Hubungan"),
    (8, "irisan", "Irisan penonton antar-film (Jaccard)", "Hubungan"),
    (9, "jembatan", "Akun jembatan antar-komunitas", "Hubungan"),
    (10, "rantai-balasan", "Ukuran thread & persentase komentar yang dibalas", "Hubungan"),
    (11, "resiprositas", "Resiprositas balasan (saling membalas)", "Hubungan"),
    (12, "aktor-aktif", "Aktor paling aktif (out-degree)", "Aktor"),
    (13, "aktor-direspons", "Aktor paling banyak dibalas (in-degree)", "Aktor"),
    (14, "perantara", "Aktor perantara (betweenness)", "Aktor"),
    (15, "aktor-inti", "Aktor inti (PageRank)", "Aktor"),
    (16, "superfans", "Superfans: akun yang berkomentar di ≥3 film", "Aktor"),
    (17, "kata-teratas", "Kata teratas per film & per komunitas", "Isi komentar"),
    (18, "pasangan-kata", "Pasangan kata (bigram) teratas", "Isi komentar"),
    (19, "emoji-tagar", "Emoji & tagar teratas", "Isi komentar"),
    (20, "waktu", "Jaringan per jendela waktu (H-14, H-7, H-1, pasca-rilis)", "Waktu"),
]
BY_NAME = {c[1]: c for c in COMMANDS}
BY_NUM = {c[0]: c for c in COMMANDS}


# ------------------------------------------------------------------ data
def film_map(path):
    m, cur = {}, None
    if not os.path.exists(path):
        return m
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            lab = s.lstrip("#").strip().lstrip("-").strip()
            if lab and not lab.lower().startswith(("trailer", "diverifikasi")) and not re.match(r"^[A-Za-z0-9_-]{11}\s", lab):
                cur = lab
            continue
        v = re.search(r"([A-Za-z0-9_-]{11})", s)
        if v:
            m[v.group(1)] = cur
    return m


def norm(t):
    return re.sub(r"[^a-z0-9]", "", str(t).lower().split("(")[0])


def load(sets):
    C = []
    for name in sets:
        d = os.path.join(BASE, f"yt_{name}")
        if not os.path.exists(os.path.join(d, "comments.csv")):
            print(f"[!] lewati {name}: yt_{name}/comments.csv tidak ada")
            continue
        fm = film_map(os.path.join(BASE, f"ids_{name}.txt"))
        v = pd.read_csv(os.path.join(d, "videos.csv"))
        v["film"] = v.video_id.map(fm).fillna(v.title)
        c = pd.read_csv(os.path.join(d, "comments.csv"))
        c = c.merge(v[["video_id", "film"]], on="video_id", how="left")
        c["set"] = name
        C.append(c)
    if not C:
        sys.exit("Tidak ada data komentar. Jalankan dulu: ./bit scrape all")
    c = pd.concat(C, ignore_index=True).drop_duplicates("comment_id")
    c["film"] = c.film.fillna("Tanpa label").str.strip()
    c["text"] = c.text.fillna("").astype(str)
    c["is_reply"] = c.is_reply.astype(str).str.lower().eq("true")
    # metadata film
    meta = {}
    fc = os.path.join(BASE, "data", "films_clean.csv")
    if os.path.exists(fc):
        for r in pd.read_csv(fc).to_dict("records"):
            meta[norm(r["film"])] = r
    def m(f, key):
        r = meta.get(norm(f))
        return r.get(key) if r else None
    films = sorted(c.film.unique())
    info = pd.DataFrame({"film": films})
    info["tanggal_rilis"] = [m(f, "tanggal_rilis") for f in films]
    info["is_franchise"] = [m(f, "is_franchise") for f in films]
    info["penonton"] = [m(f, "penonton") for f in films]
    return c, info


def category(text):
    t = text.lower()
    if any(w in t for w in INTENT):
        return "niat menonton"
    if any(w in t for w in FEAR):
        return "takut (pujian?)"
    return "lain"


# ------------------------------------------------------------------ graf
class Graphs:
    def __init__(self, c):
        self.c = c
        author = dict(zip(c.comment_id, c.user))
        r = c[c.is_reply & c.parent_id.notna()].copy()
        r["target"] = r.parent_id.map(author)
        r = r[r.target.notna() & (r.user != r.target)]
        self.replies = r
        # DiGraph balasan: pembalas -> penulis komentar induk
        R = nx.DiGraph()
        for (u, v), w in r.groupby(["user", "target"]).size().items():
            R.add_edge(u, v, weight=int(w))
        self.R = R
        # Bipartit komentator–film (+ balasan) untuk peta & komunitas
        A = nx.Graph()
        for (u, f), w in c.groupby(["user", "film"]).size().items():
            A.add_node(u, kind="user"); A.add_node("FILM::" + f, kind="film", label=f)
            A.add_edge(u, "FILM::" + f, weight=int(w), kind="komentar")
        for u, v, d in R.edges(data=True):
            if A.has_edge(u, v):
                A[u][v]["weight"] += d["weight"]
            else:
                A.add_edge(u, v, weight=d["weight"], kind="balasan")
        self.A = A
        self._comm = None

    def communities(self):
        if self._comm is None:
            comms = nx.community.louvain_communities(self.A, weight="weight", seed=SEED)
            comms = sorted(comms, key=len, reverse=True)
            self._comm = comms
            self.cmap = {n: i for i, cm in enumerate(comms) for n in cm}
        return self._comm


# ------------------------------------------------------------------ util keluaran
class Out:
    def __init__(self, d, bin_):
        self.d, self.bin, self.lines = d, bin_, []
        os.makedirs(d, exist_ok=True)

    def path(self, n, name, ext):
        return os.path.join(self.d, f"{n:02d}_{name}.{ext}")

    def csv(self, n, name, df):
        p = self.path(n, name, "csv"); df.to_csv(p, index=False); return os.path.basename(p)

    def png(self, n, name, fig):
        p = self.path(n, name, "png"); fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
        return os.path.basename(p)

    def note(self, n, title, text):
        self.lines.append(f"## {n:02d}. {title}\n\n{text}\n")
        print(f"[✓] {n:02d} {title}")


def short(f, k=26):
    f = re.sub(r"\s*\(\d{4}\)$", "", f)
    return f if len(f) <= k else f[: k - 1] + "…"


def tbl(df, k=10):
    try:
        return df.head(k).to_markdown(index=False)   # butuh paket 'tabulate'
    except ImportError:
        return "```\n" + df.head(k).to_string(index=False) + "\n```"


PALETTE = ["#C2410C", "#0F766E", "#7C3AED", "#B45309", "#1D4ED8", "#BE185D", "#15803D", "#4B5563", "#9333EA", "#0369A1"]


def draw(G, pos, ax, node_color, node_size, title, labels=None):
    ax.set_title(title, fontsize=11)
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.12, width=0.4, edge_color="#57534E")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_color, node_size=node_size, linewidths=0)
    if labels:
        nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7, font_weight="bold")
    ax.set_axis_off()


def sample_nodes(A, cap=2500):
    films = [n for n, d in A.nodes(data=True) if d.get("kind") == "film"]
    users = sorted((n for n, d in A.nodes(data=True) if d.get("kind") == "user"), key=lambda n: -A.degree(n))
    return films + users[:cap]


# ------------------------------------------------------------------ 20 analisis
def a1(g, o):
    H = g.A.subgraph(sample_nodes(g.A)).copy()
    films = [n for n, d in H.nodes(data=True) if d["kind"] == "film"]
    fixed = {f: (math.cos(2 * math.pi * i / len(films)) * 3, math.sin(2 * math.pi * i / len(films)) * 3) for i, f in enumerate(films)}
    pos = nx.spring_layout(H, pos=fixed, fixed=films, seed=SEED, iterations=40, k=0.08)
    col = ["#C2410C" if H.nodes[n]["kind"] == "film" else "#A8A29E" for n in H]
    size = [60 if H.nodes[n]["kind"] == "film" else 3 for n in H]
    fig, ax = plt.subplots(figsize=(12, 12))
    draw(H, pos, ax, col, size, f"Peta jaringan: {len(films)} film, {H.number_of_nodes()-len(films)} komentator teratas",
         {f: short(H.nodes[f]["label"], 18) for f in films})
    png = o.png(1, "peta", fig)
    gml = o.path(1, "peta", "graphml"); nx.write_graphml(g.A, gml)
    o.note(1, BY_NUM[1][2], f"Simpul: {g.A.number_of_nodes():,} · sisi: {g.A.number_of_edges():,}. Gambar `{png}` (dibatasi komentator dengan derajat tertinggi agar terbaca); graf penuh `{os.path.basename(gml)}` bisa dibuka di NodeXL/Gephi.")


def a2(g, o):
    comms = g.communities()[:9]
    n = len(comms); cols = 3; rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5))
    axes = axes.flatten() if n > 1 else [axes]
    for i, cm in enumerate(comms):
        sub = sorted(cm, key=lambda x: -g.A.degree(x))[:400]
        H = g.A.subgraph(sub)
        pos = nx.spring_layout(H, seed=SEED, iterations=30)
        films = [x for x in H if H.nodes[x]["kind"] == "film"]
        lab = {f: short(H.nodes[f]["label"], 16) for f in films}
        draw(H, pos, axes[i], [PALETTE[i % 10]] * H.number_of_nodes(),
             [50 if H.nodes[x]["kind"] == "film" else 4 for x in H], f"Grup {i+1} · {len(cm):,} simpul", lab)
    for j in range(n, len(axes)):
        axes[j].set_axis_off()
    o.note(2, BY_NUM[2][2], f"`{o.png(2, 'grup-kotak', fig)}` menampilkan {n} komunitas terbesar (maks. 400 simpul per kotak).")


def a3(g, o):
    films = g.c.film.value_counts().index.tolist()
    cols = 4; rows = math.ceil(len(films) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    axes = axes.flatten()
    rows_out = []
    for i, f in enumerate(films):
        r = g.replies[g.replies.film == f]
        H = nx.Graph(); H.add_edges_from(zip(r.user, r.target))
        rows_out.append({"film": f, "simpul_balasan": H.number_of_nodes(), "sisi_balasan": H.number_of_edges()})
        if H.number_of_nodes():
            pos = nx.spring_layout(H, seed=SEED, iterations=40)
            draw(H, pos, axes[i], PALETTE[i % 10], 6, short(f, 30))
        else:
            axes[i].set_title(short(f, 30) + " (tanpa balasan)", fontsize=10); axes[i].set_axis_off()
    for j in range(len(films), len(axes)):
        axes[j].set_axis_off()
    df = pd.DataFrame(rows_out)
    o.note(3, BY_NUM[3][2], f"`{o.png(3, 'per-film', fig)}` · angka di `{o.csv(3, 'per-film', df)}`.\n\n{tbl(df, 20)}")


def a4(g, o):
    cat = g.c.groupby("user").text.apply(lambda s: collections.Counter(category(t) for t in s).most_common(1)[0][0])
    H = g.A.subgraph(sample_nodes(g.A, 2000))
    pos = nx.spring_layout(H, seed=SEED, iterations=40, k=0.08)
    cmap = {"niat menonton": "#0F766E", "takut (pujian?)": "#C2410C", "lain": "#D6D3D1"}
    col = ["#1C1917" if H.nodes[n]["kind"] == "film" else cmap[cat.get(n, "lain")] for n in H]
    size = [50 if H.nodes[n]["kind"] == "film" else 5 for n in H]
    fig, ax = plt.subplots(figsize=(12, 12))
    draw(H, pos, ax, col, size, "Kategori komentar dominan per akun (leksikon eksploratif)")
    for k, v in cmap.items():
        ax.scatter([], [], c=v, label=k, s=40)
    ax.legend(loc="lower left", frameon=False)
    share = g.c.text.map(category).value_counts(normalize=True).mul(100).round(1).rename_axis("kategori").reset_index(name="persen_komentar")
    o.note(4, BY_NUM[4][2], f"`{o.png(4, 'warna-niat', fig)}` · `{o.csv(4, 'warna-niat', share)}`. Kategori dari kata kunci, bukan model — perlu validasi label manusia.\n\n{tbl(share)}")


def bip(g):
    return {f: set(s) for f, s in g.c.groupby("film").user}


def a5(g, o):
    S = bip(g); films = list(S)
    P = nx.Graph()
    rows = []
    for i, a in enumerate(films):
        P.add_node(a)
        for b in films[i + 1:]:
            w = len(S[a] & S[b])
            if w:
                P.add_edge(a, b, weight=w); rows.append({"film_a": a, "film_b": b, "komentator_bersama": w})
    pos = nx.circular_layout(P)
    fig, ax = plt.subplots(figsize=(11, 11))
    ws = [P[u][v]["weight"] for u, v in P.edges()] or [1]
    mx = max(ws)
    nx.draw_networkx_edges(P, pos, ax=ax, width=[0.5 + 8 * w / mx for w in ws], edge_color="#C2410C", alpha=0.55)
    nx.draw_networkx_nodes(P, pos, ax=ax, node_size=[40 + 4 * len(S[f]) ** 0.75 for f in P], node_color="#0F766E")
    nx.draw_networkx_labels(P, pos, labels={f: short(f, 22) for f in P}, ax=ax, font_size=8)
    ax.set_title("Proyeksi film–film (tebal = komentator bersama)"); ax.set_axis_off()
    df = pd.DataFrame(rows).sort_values("komentator_bersama", ascending=False) if rows else pd.DataFrame(columns=["film_a", "film_b", "komentator_bersama"])
    o.note(5, BY_NUM[5][2], f"`{o.png(5, 'film-film', fig)}` · `{o.csv(5, 'film-film', df)}`\n\n{tbl(df)}")


def a6(g, o):
    rows = []
    for f, d in g.c.groupby("film"):
        r = g.replies[g.replies.film == f]
        H = nx.Graph(); H.add_nodes_from(d.user.unique()); H.add_edges_from(zip(r.user, r.target))
        comps = sorted((len(x) for x in nx.connected_components(H)), reverse=True)
        rows.append({"film": f, "komentator": H.number_of_nodes(), "sisi_balasan": H.number_of_edges(),
                     "densitas": round(nx.density(H), 6), "komponen": len(comps),
                     "komponen_terbesar_%": round(100 * comps[0] / max(1, H.number_of_nodes()), 1) if comps else 0,
                     "terisolasi_%": round(100 * sum(1 for x in comps if x == 1) / max(1, H.number_of_nodes()), 1)})
    df = pd.DataFrame(rows).sort_values("komentator", ascending=False)
    o.note(6, BY_NUM[6][2], f"`{o.csv(6, 'densitas', df)}`. Densitas pada graf balasan per film.\n\n{tbl(df, 20)}")


def a7(g, o):
    comms = g.communities()
    Q = nx.community.modularity(g.A, comms, weight="weight")
    rows = []
    for i, cm in enumerate(comms[:15]):
        films = [g.A.nodes[x]["label"] for x in cm if g.A.nodes[x]["kind"] == "film"]
        users = [x for x in cm if g.A.nodes[x]["kind"] == "user"]
        rows.append({"grup": i + 1, "akun": len(users), "film_dalam_grup": "; ".join(short(f, 30) for f in films) or "-"})
    df = pd.DataFrame(rows)
    o.note(7, BY_NUM[7][2], f"Louvain (seed {SEED}) → {len(comms)} komunitas, modularitas **Q = {Q:.3f}** "
           f"({'struktur komunitas kuat' if Q > 0.3 else 'struktur komunitas lemah'}). `{o.csv(7, 'komunitas', df)}`\n\n{tbl(df, 15)}")


def a8(g, o):
    S = bip(g); films = sorted(S, key=lambda f: -len(S[f]))
    M = pd.DataFrame(0.0, index=films, columns=films)
    for a in films:
        for b in films:
            u = len(S[a] | S[b]); M.loc[a, b] = round(len(S[a] & S[b]) / u, 4) if u else 0
    fig, ax = plt.subplots(figsize=(11, 9))
    im = ax.imshow(M.values, cmap="Oranges", vmin=0, vmax=max(0.05, M.values[~pd.DataFrame(M).eq(1).values].max() if len(films) > 1 else 1))
    ax.set_xticks(range(len(films))); ax.set_yticks(range(len(films)))
    ax.set_xticklabels([short(f, 18) for f in films], rotation=70, ha="right", fontsize=7)
    ax.set_yticklabels([short(f, 22) for f in films], fontsize=7)
    fig.colorbar(im, ax=ax, label="Jaccard"); ax.set_title("Irisan komentator antar-film (Jaccard)")
    multi = g.c.groupby("user").film.nunique()
    txt = f"{(multi >= 2).sum():,} dari {len(multi):,} akun ({100*(multi>=2).mean():.1f}%) berkomentar di ≥2 film."
    out = M.reset_index().rename(columns={"index": "film"})
    o.note(8, BY_NUM[8][2], f"{txt} `{o.png(8, 'irisan', fig)}` · `{o.csv(8, 'irisan', out)}`")


def a9(g, o):
    g.communities()
    U = g.A
    bc = nx.betweenness_centrality(U, k=min(400, U.number_of_nodes()), seed=SEED, weight=None)
    rows = []
    for n, b in sorted(bc.items(), key=lambda x: -x[1]):
        if U.nodes[n]["kind"] != "user":
            continue
        nb = {g.cmap[x] for x in U.neighbors(n)}
        if len(nb) >= 2:
            films = sorted({U.nodes[x]["label"] for x in U.neighbors(n) if U.nodes[x]["kind"] == "film"})
            rows.append({"akun": n, "betweenness": round(b, 5), "komunitas_tersambung": len(nb), "film": "; ".join(short(f, 20) for f in films)})
        if len(rows) >= 30:
            break
    df = pd.DataFrame(rows)
    o.note(9, BY_NUM[9][2], f"Betweenness aproksimasi (k=400 sampel) pada graf komentator–film. `{o.csv(9, 'jembatan', df)}`\n\n{tbl(df)}")


def a10(g, o):
    top = g.c[~g.c.is_reply]
    nrep = g.c[g.c.is_reply].groupby("parent_id").size()
    top = top.assign(balasan=top.comment_id.map(nrep).fillna(0).astype(int))
    df = top.groupby("film").agg(komentar_induk=("comment_id", "size"),
                                 dibalas_pct=("balasan", lambda s: round(100 * (s > 0).mean(), 1)),
                                 rata_balasan=("balasan", lambda s: round(s.mean(), 2)),
                                 thread_terpanjang=("balasan", "max")).reset_index().sort_values("dibalas_pct", ascending=False)
    o.note(10, BY_NUM[10][2], f"YouTube hanya punya satu tingkat balasan, jadi 'rantai' diukur sebagai ukuran thread. `{o.csv(10, 'rantai-balasan', df)}`\n\n{tbl(df, 20)}")


def a11(g, o):
    rows = [{"film": "SEMUA", "pasangan": g.R.number_of_edges(), "resiprositas": round(nx.reciprocity(g.R), 4) if g.R.number_of_edges() else 0}]
    for f, r in g.replies.groupby("film"):
        D = nx.DiGraph(); D.add_edges_from(zip(r.user, r.target))
        rows.append({"film": f, "pasangan": D.number_of_edges(), "resiprositas": round(nx.reciprocity(D), 4) if D.number_of_edges() else 0})
    df = pd.DataFrame(rows)
    o.note(11, BY_NUM[11][2], f"Proporsi sisi balasan yang dibalas balik. `{o.csv(11, 'resiprositas', df)}`\n\n{tbl(df, 20)}")


def rank(g, o, n, name, scores, label, extra=""):
    films = g.c.groupby("user").film.apply(lambda s: "; ".join(sorted({short(f, 18) for f in s})))
    df = pd.DataFrame([{"akun": k, label: round(v, 6) if isinstance(v, float) else v, "film": films.get(k, "")}
                       for k, v in sorted(scores.items(), key=lambda x: -x[1])[:30]])
    o.note(n, BY_NUM[n][2], f"{extra}`{o.csv(n, name, df)}`\n\n{tbl(df)}")


def a12(g, o):
    s = g.c.groupby("user").size().to_dict()
    rank(g, o, 12, "aktor-aktif", s, "komentar+balasan_dibuat")


def a13(g, o):
    rank(g, o, 13, "aktor-direspons", dict(g.R.in_degree(weight="weight")), "balasan_diterima")


def a14(g, o):
    U = g.R.to_undirected()
    bc = nx.betweenness_centrality(U, k=min(500, U.number_of_nodes()), seed=SEED) if U.number_of_nodes() else {}
    rank(g, o, 14, "perantara", bc, "betweenness", "Pada graf balasan (aproksimasi k=500). ")


def a15(g, o):
    pr = nx.pagerank(g.R, weight="weight") if g.R.number_of_nodes() else {}
    rank(g, o, 15, "aktor-inti", pr, "pagerank", "PageRank pada graf balasan berarah. ")


def a16(g, o):
    k = g.c.groupby("user").film.nunique()
    sup = k[k >= 3].sort_values(ascending=False)
    films = g.c[g.c.user.isin(sup.index)].groupby("user").film.apply(lambda s: "; ".join(sorted({short(f, 18) for f in s})))
    df = pd.DataFrame({"akun": sup.index, "jumlah_film": sup.values, "film": [films[u] for u in sup.index]})
    fr = g.c[g.c.user.isin(sup.index)].film.value_counts().rename_axis("film").reset_index(name="komentar_superfans")
    o.note(16, BY_NUM[16][2], f"{len(df):,} akun berkomentar di ≥3 film. Pengganti 'akun resmi', karena data tidak menandai akun kanal/pemeran. "
           f"`{o.csv(16, 'superfans', df)}`\n\nFilm yang paling banyak didatangi superfans:\n\n{tbl(fr)}")


def tokens(t):
    return [w for w in WORD_RE.findall(t.lower()) if w not in STOP]


def a17(g, o):
    rows = []
    for f, s in g.c.groupby("film").text:
        cnt = collections.Counter(w for t in s for w in tokens(t))
        rows.append({"kelompok": "film: " + f, "kata_teratas": ", ".join(f"{w}({n})" for w, n in cnt.most_common(12))})
    g.communities()
    users = g.c.user.map(g.cmap)
    for i in range(min(6, len(g._comm))):
        cnt = collections.Counter(w for t in g.c.text[users == i] for w in tokens(t))
        rows.append({"kelompok": f"komunitas {i+1}", "kata_teratas": ", ".join(f"{w}({n})" for w, n in cnt.most_common(12))})
    df = pd.DataFrame(rows)
    o.note(17, BY_NUM[17][2], f"`{o.csv(17, 'kata-teratas', df)}`\n\n{tbl(df, 30)}")


def a18(g, o):
    cnt, per = collections.Counter(), collections.defaultdict(collections.Counter)
    for f, t in zip(g.c.film, g.c.text):
        w = tokens(t)
        for a, b in zip(w, w[1:]):
            cnt[(a, b)] += 1; per[f][(a, b)] += 1
    df = pd.DataFrame([{"pasangan": f"{a} {b}", "frekuensi": n} for (a, b), n in cnt.most_common(40)])
    pf = pd.DataFrame([{"film": f, "pasangan_teratas": ", ".join(f"{a} {b}({n})" for (a, b), n in c.most_common(6))} for f, c in per.items()])
    o.csv(18, "pasangan-kata-per-film", pf)
    o.note(18, BY_NUM[18][2], f"`{o.csv(18, 'pasangan-kata', df)}` · per film di `18_pasangan-kata-per-film.csv`. Bahan kandidat leksikon Watch Intent Index.\n\n{tbl(df, 20)}")


def a19(g, o):
    em = collections.Counter(e for t in g.c.text for e in EMOJI_RE.findall(t))
    ht = collections.Counter(h.lower() for t in g.c.text for h in HASHTAG_RE.findall(t))
    df = pd.DataFrame([{"jenis": "emoji", "item": k, "frekuensi": v} for k, v in em.most_common(25)] +
                      [{"jenis": "tagar", "item": k, "frekuensi": v} for k, v in ht.most_common(25)])
    pct = 100 * g.c.text.map(lambda t: bool(EMOJI_RE.search(t))).mean()
    o.note(19, BY_NUM[19][2], f"{pct:.1f}% komentar memakai emoji. `{o.csv(19, 'emoji-tagar', df)}`\n\n{tbl(df, 20)}")


def a20(g, o, info):
    rel = {r.film: pd.to_datetime(r.tanggal_rilis, errors="coerce") for r in info.itertuples()}
    c = g.c.copy()
    c["t"] = pd.to_datetime(c.timestamp, unit="s", errors="coerce")
    c["rilis"] = c.film.map(rel)
    c = c[c.rilis.notna() & c.t.notna()]
    c["h"] = (c.t.dt.tz_localize(None) - c.rilis.dt.tz_localize(None)).dt.days
    bins = [(-10_000, -15, "< H-14"), (-14, -8, "H-14..H-8"), (-7, -2, "H-7..H-2"), (-1, -1, "H-1"), (0, 10_000, "pasca-rilis")]
    def win(h):
        for a, b, lab in bins:
            if a <= h <= b:
                return lab
    c["jendela"] = c.h.map(win)
    rows = []
    for (f, w), d in c.groupby(["film", "jendela"]):
        r = d[d.is_reply & d.parent_id.notna()]
        rows.append({"film": f, "jendela": w, "komentar": len(d), "akun": d.user.nunique(), "balasan": len(r),
                     "niat_menonton_%": round(100 * d.text.map(lambda t: category(t) == "niat menonton").mean(), 1)})
    df = pd.DataFrame(rows)
    order = {lab: i for i, (_, _, lab) in enumerate(bins)}
    if len(df):
        df = df.sort_values(["film", "jendela"], key=lambda s: s.map(order) if s.name == "jendela" else s)
    precise = bool(glob.glob(os.path.join(BASE, "data", "youtube_api", "*")))
    caveat = ("⚠️ Stempel waktu yt-dlp dibulatkan ('3 bulan lalu'), jadi jendela H-14/H-7/H-1 belum presisi. "
              "Untuk klaim prediktif, pakai data `./bit precise` (YouTube Data API)." if not precise else
              "Data YouTube API presisi tersedia di data/youtube_api/ — pertimbangkan memuatnya untuk analisis final.")
    o.note(20, BY_NUM[20][2], f"{caveat} Film tanpa tanggal rilis di films_clean.csv dilewati. `{o.csv(20, 'waktu', df)}`\n\n{tbl(df, 40)}")


FUNCS = {1: a1, 2: a2, 3: a3, 4: a4, 5: a5, 6: a6, 7: a7, 8: a8, 9: a9, 10: a10,
         11: a11, 12: a12, 13: a13, 14: a14, 15: a15, 16: a16, 17: a17, 18: a18, 19: a19}


# ------------------------------------------------------------------ ekspor NodeXL Pro
def export_nodexl(g, o):
    """Dua CSV yang bisa langsung diimpor NodeXL Pro (Import > From Open Workbook / tempel ke sheet Edges & Vertices)."""
    g.communities()
    cat = g.c.groupby("user").text.apply(lambda s: collections.Counter(category(t) for t in s).most_common(1)[0][0])
    E = [{"Vertex 1": u, "Vertex 2": (g.A.nodes[v].get("label", v) if g.A.nodes[v]["kind"] == "film" else v),
          "Edge Weight": d["weight"], "Relationship": d["kind"]} for u, v, d in g.A.edges(data=True)]
    # pastikan kolom Vertex 1 = akun, Vertex 2 = film/akun
    for e in E:
        if str(e["Vertex 1"]).startswith("FILM::"):
            e["Vertex 1"], e["Vertex 2"] = e["Vertex 2"], e["Vertex 1"]
    V = [{"Vertex": (d.get("label", n) if d["kind"] == "film" else n), "Jenis": d["kind"],
          "Komunitas": g.cmap.get(n, -1) + 1, "Kategori": "film" if d["kind"] == "film" else cat.get(n, "lain"),
          "Jumlah Film": (g.c[g.c.user == n].film.nunique() if False else None)} for n, d in g.A.nodes(data=True)]
    nf = g.c.groupby("user").film.nunique()
    for v in V:
        v["Jumlah Film"] = int(nf.get(v["Vertex"], 0)) if v["Jenis"] == "user" else None
    d = os.path.join(o.d, "nodexl")
    os.makedirs(d, exist_ok=True)
    pd.DataFrame(E).to_csv(os.path.join(d, "edges.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame(V).to_csv(os.path.join(d, "vertices.csv"), index=False, encoding="utf-8-sig")
    print(f"[✓] NodeXL : {os.path.relpath(d, BASE)}/edges.csv + vertices.csv ({len(E):,} sisi, {len(V):,} simpul)")


# ------------------------------------------------------------------ biner
def to_binary(text):
    return " ".join(f"{b:08b}" for b in text.encode("utf-8"))


def write_binary(path_md):
    txt = open(path_md, encoding="utf-8").read()
    out = path_md.replace(".md", ".bin.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# SANTET · ringkasan SNA dalam biner 8-bit (UTF-8). Balik dengan:\n")
        f.write("# python3 -c \"import sys;print(bytes(int(b,2) for b in open(sys.argv[1]).read().split('\\n',2)[2].split()).decode())\" <file>\n")
        f.write(to_binary(txt))
    # verifikasi lossless
    back = bytes(int(b, 2) for b in open(out, encoding="utf-8").read().split("\n", 2)[2].split()).decode("utf-8")
    assert back == txt, "konversi biner tidak lossless"
    return out


# ------------------------------------------------------------------ main
def print_list():
    print("\n20 perintah SNA (./bit sna <nomor|nama> ... | all | list)  [--set a,b] [--bin]\n")
    grp = None
    for n, name, title, kel in COMMANDS:
        if kel != grp:
            print(f"  — {kel}"); grp = kel
        print(f"  ./bit sna {n:<3} | ./bit sna {name:<16} {title}")
    print()


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--set", default="")
    ap.add_argument("--bin", action="store_true")
    a = ap.parse_args(argv)
    if not a.targets or a.targets[0] in ("list", "help", "-h", "--help"):
        print_list(); return
    if "all" in a.targets:
        todo = list(range(1, 21))
    else:
        todo = []
        for t in a.targets:
            c = BY_NUM.get(int(t)) if t.isdigit() else BY_NAME.get(t)
            if not c:
                sys.exit(f"Perintah tidak dikenal: {t}. Lihat: ./bit sna list")
            todo.append(c[0])
    sets = [s for s in a.set.split(",") if s] or sorted(os.path.basename(d)[3:] for d in glob.glob(os.path.join(BASE, "yt_*")) if os.path.isdir(d))
    c, info = load(sets)
    print(f"[i] {len(c):,} komentar · {c.user.nunique():,} akun · {c.film.nunique()} film · set: {', '.join(sets)}")
    g = Graphs(c)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M")
    o = Out(os.path.join(BASE, "results", f"sna_{stamp}"), a.bin)
    for n in todo:
        try:
            a20(g, o, info) if n == 20 else FUNCS[n](g, o)
        except Exception as e:  # satu analisis gagal tidak menghentikan yang lain
            o.note(n, BY_NUM[n][2], f"❌ gagal: {type(e).__name__}: {e}")
    md = os.path.join(o.d, "ringkasan.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(f"# SANTET · Analisis Jaringan Komentar YouTube\n\n_{dt.datetime.now():%d-%m-%Y %H:%M} · "
                f"{len(c):,} komentar · {c.user.nunique():,} akun (pseudonim) · {c.film.nunique()} film · set: {', '.join(sets)}_\n\n")
        f.write("\n".join(o.lines))
    export_nodexl(g, o)
    print(f"[✓] ringkasan: {os.path.relpath(md, BASE)}")
    if a.bin:
        print(f"[✓] biner   : {os.path.relpath(write_binary(md), BASE)} (terverifikasi lossless)")


if __name__ == "__main__":
    main()
