# OptChat: notes for Claude Code

An endless chat whose history is its memory: `optchat.py` (one file, Python 3.12 + `httpx`), recall
benchmark `bench.py`, results in `bench_results*.md`.

- **Apothicaire imports `optchat.py` unchanged** (`Agent`, `LLM`, `LLMError`, `CFG`, `SYSTEM_PROMPT`,
  `TOOLS`, `_calls_of`, `_utf`). A change to these breaks the apothicaire repository: run its tests too.
- **Tests** need no model server (a fake model stands in), as CI runs them:
  `pip install httpx==0.28.1 && python -m unittest discover -s tests`, then `git diff --exit-code`.
- **Server.** `start_servers_upstream.sh` starts upstream llama.cpp b11700 with the 27B Q2_0 on port
  18435; its two paths point to the author's PC. `start_servers.sh` (PrismML fork) only reproduces old
  measurements. `bench.py` needs the server, so it runs on the PC only.
- `bench_results*.md` are measurements: never edit them by hand. `data/`, `data_bench/`, `run/` and
  model weights are git-ignored and stay local.
- **README.** It states no figure that a run can change (no count, ratio or percentage): the figures live
  in `BENCH.md` and `bench_results*.md`, and the README links to them (caladrius T-124).
