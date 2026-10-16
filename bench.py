#!/usr/bin/env python
"""
Recall benchmark for the OptChat prototype. Uses its own data folder (data_bench/), never the chat's.

Phase 1: a scripted conversation in French. Facts are planted early, filler turns push them
         down into the summary tree (L0 -> L1 -> L2 ...).
Phase 2: recall questions. We check whether the expected value is in the answer and whether
         the agent zoomed to find it.
Every turn records: wall time (whole turn, incl. waiting for the previous compaction), prompt
tokens, uncached (re-prefilled) tokens summed over rounds, zooms. Rows are written as they come
to data_bench/bench_rows.jsonl; the report goes to bench_results.md.
usage: python bench.py [n_filler_between] [n_tail_filler]
"""
import sys, time, json, os, re
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
import optchat
optchat.CFG["data_dir"] = os.path.join(ROOT, "data_bench")

FACTS = [  # (statement planted by the user, recall question, regex that the answer must match)
    ("Pour info, mon chat s'appelle Pixel et il a 4 ans.", "Comment s'appelle mon chat ?", r"\bpixel\b"),
    ("Le serveur de prod du projet Atlas est 10.0.3.47, et on y accède en SSH sur le port 2222.", "Quel est le port SSH du serveur de prod d'Atlas ?", r"\b2222\b"),
    ("J'ai finalement choisi PostgreSQL pour Atlas, pas MongoDB, à cause des transactions.", "Quelle base de données ai-je choisie pour Atlas, et pourquoi ?", r"postgre"),
    ("Note que ma collègue Inès Marchetti reprend le module de facturation à partir du 15 novembre.", "Qui reprend le module de facturation, et quand ?", r"marchetti.*15|15.*marchetti"),
    ("Le token de build s'appelle ATLAS_BUILD_KEY et il est dans le fichier .env.ci, pas dans .env.", "Dans quel fichier se trouve ATLAS_BUILD_KEY ?", r"\.env\.ci"),
    ("Mon budget max pour le nouveau GPU est de 650 euros.", "Quel est mon budget max pour le GPU ?", r"(?<!\d)650(?!\d)"),
    ("Le rendez-vous chez le dentiste est le jeudi 23 octobre à 9h15.", "À quelle heure est mon rendez-vous chez le dentiste ?", r"(?<!\d)0?9\s*[h:]\s*15(?!\d)"),
    ("Pour le bot Discord, le préfixe de commande est !ax et la couleur d'embed est #3FA7D6.", "Quelle est la couleur d'embed du bot Discord ?", r"3fa7d6"),
]

FILLER = [
    "Explique en une phrase ce qu'est un arbre binaire.", "Donne-moi un synonyme de 'rapide'.",
    "Combien font 17 fois 23 ? Réponds juste le nombre.", "Cite une capitale européenne au hasard, un mot.",
    "En une phrase : différence entre TCP et UDP ?", "Quel est le pluriel de 'cheval' ?",
    "Propose un nom de variable pour un compteur de tentatives.", "En une phrase, c'est quoi un cache KV ?",
    "Donne un exemple de palindrome.", "Un conseil court pour bien dormir ?", "Traduis 'bonne chance' en anglais.",
    "C'est quoi le complément à deux, en une phrase ?", "Donne-moi une couleur froide, un mot.",
    "En une phrase, pourquoi utiliser git ?", "Quelle est la racine carrée de 144 ?", "Cite un langage fonctionnel.",
    "Une phrase sur le théorème de Pythagore.", "Donne un prénom commençant par T.",
    "En une phrase, c'est quoi une regex ?", "Un fruit qui commence par M ?",
    "Explique en trois phrases comment fonctionne un cache LRU.", "Décris en trois phrases ce qu'est une transaction ACID.",
]

def main(n_filler_between=2, n_tail_filler=14):
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
    optchat.cmd_reset(None)
    ag = optchat.Agent()
    rows_path = os.path.join(optchat.CFG["data_dir"], "bench_rows.jsonl")
    open(rows_path, "w").close()
    rows = []
    def do(q, tag, **extra):
        ans, s = ag.turn(q, verbose=False)
        s = dict(s, tag=tag, q=q, ans=ans, **extra)
        if "expect" in extra:
            s["ok"] = re.search(extra["expect"], ans.lower().replace(" ", " ").replace(" ", " ")) is not None
        rows.append(s)
        with open(rows_path, "a", encoding="utf-8") as f: f.write(json.dumps(s, ensure_ascii=False) + "\n")
        print(f"[{tag}] {s['wall_s']:>6}s prompt={s['prompt_tokens']} uncached={s['uncached_tokens']} zooms={s['zooms']} | {q[:50]} -> {ans[:90]!r}")
        if ag.compactor.last_error: print(f"   compaction error: {ag.compactor.last_error}"); ag.compactor.last_error = None
        return ans
    t0 = time.time(); hits = 0
    try:
        fi = 0
        for stmt, _, _ in FACTS:                       # phase 1: plant facts, with filler between
            do(stmt, "fact")
            for _ in range(n_filler_between):
                do(FILLER[fi % len(FILLER)], "filler"); fi += 1
        for _ in range(n_tail_filler):                  # push everything deeper
            do(FILLER[fi % len(FILLER)], "filler"); fi += 1
        ag.wait_bg()
        print("\n--- tree state before recall:"); optchat.cmd_stats(None)
        for _, q, pat in FACTS:                         # phase 2: recall
            do(q, "recall", expect=pat); hits += rows[-1]["ok"]
    finally:
        total = time.time() - t0
        ag.close()
    rec = [r for r in rows if r["tag"] == "recall"]
    lines = [f"# OptChat local bench ({os.environ.get('OPTCHAT_MODEL_LABEL', 'model not labelled')}, RTX 3060 12GB)", "",
             f"Turns: {len(rows)}  |  total wall: {total/60:.1f} min  |  compactor: {optchat.CFG['compact_url'] or 'same server, slot 1'}  |  compaction stats: {ag.compactor.stats}", "",
             f"## Recall: {hits}/{len(rec)}", "", "| question | expected | ok | zooms | rounds | s | answer |", "|---|---|---|---|---|---|---|"]
    for r in rec:
        lines.append(f"| {r['q']} | `{r['expect']}` | {'OK' if r.get('ok') else 'MISS'} | {r['zooms']} | {r['rounds']} | {r['wall_s']} | {r['ans'][:120].replace('|','/').replace(chr(10),' ')} |")
    head = len(lines)
    lines += ["", "## Per-turn cost", "", "| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |", "|---|---|---|---|---|---|---|---|"]
    for k, r in enumerate(rows):
        lines.append(f"| {k} | {r['tag']} | {r['wall_s']} | {r['compact_wait_s']} | {r['prompt_tokens']} | {r['uncached_tokens']} | {r['cached_tokens']} | {r['zooms']} |")
    with open(os.path.join(ROOT, "bench_results.md"), "w", encoding="utf-8") as f: f.write("\n".join(lines))
    print("\n".join(lines[:head]))

if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:3]]
    main(*a)
