# OptChat local

An endless chat whose history is its memory. Every message is kept on disk, and the model sees a view in which recent messages are verbatim and older ones are progressively merged into summary lines arranged as a binary tree, with a `zoom` tool to open any node. Nothing is ever deleted, the view always covers the whole conversation, and the prompt cost stays bounded.

This is an independent implementation of the idea for a local `llama.cpp` model on one consumer GPU, written in October 2026 as the memory of [Apothicaire](https://github.com/abdou-rgd/apothicaire), the local DMPK assistant of the Officina project (an open, deterministic and verified pharmacokinetic engine, [Caladrius](https://github.com/abdou-rgd/caladrius), with a local assistant that never computes a number itself).

**Attribution.** The design follows the OptChat idea published by Victor Taelin as a gist (an infinite chat compressed into a binary tree of summary lines with zoom). The code here is a new implementation, adapted to `llama.cpp` (KV-cache-aware lazy compaction, a second server slot for the compactor, grammar-constrained summaries); it shares no code with the gist.

**Status.** A prototype with measurements. One file, `optchat.py`, plus `httpx`. The recall benchmark, its results and the decisions taken from them are in [`BENCH.md`](BENCH.md); this README states no figure.

**License.** MIT OR Apache-2.0, at your option (`LICENSE-MIT`, `LICENSE-APACHE`). Model weights are not included and carry their own licences.

## How it works

The state lives in `data/`. `log.jsonl` keeps every message in clear, append-only. `tree.jsonl` keeps immutable summary nodes: one line per message, then each node merges adjacent nodes of the level below. `view.json` is the ordered list the model sees: the coarsest summary nodes on the left, the raw recent messages on the right.

Each turn is one fresh model call: the system prompt, the digest of the summary lines as a separate user turn (so the static prefix stays in the KV cache), the recent raw messages, and the new message. The model has the tools `zoom(id)`, which opens a node onto its children (or onto the original message), and `read_message(n)`, which reads a full message. After each turn a background thread compacts the view, lazily and in batches, on its own server slot so that the chat's KV cache is never evicted.

## Run

OptChat needs Python 3.12 with `httpx`, and a `llama-server` from upstream [llama.cpp](https://github.com/ggml-org/llama.cpp) (build b11700, no fork) serving Ternary Bonsai 2 27B in the Q2_0 packing. The file is `Ternary-Bonsai-2-27B-Q2_0-prism-fork-required.gguf`: despite its name, upstream llama.cpp has read it since b11555.

```bash
pip install httpx
bash start_servers_upstream.sh   # llama-server on http://127.0.0.1:18435 (wait until /health answers)
curl http://127.0.0.1:18435/health
python optchat.py chat           # interactive chat, memory in data/
```

The two paths at the top of `start_servers_upstream.sh` (`LLAMA`, `M27`) point to the author's machine: edit them first. Other commands: `say "message"` (one turn), `view` (digest and raw messages of the view), `stats`, `reset` (erases `data/`, refuses while a chat is running). Environment: `OPTCHAT_URL`, `OPTCHAT_DATA`, `OPTCHAT_COMPACT_URL` (a second server for compaction). On Windows, stop the server with `Stop-Process -Name llama-server -Force` in PowerShell (`taskkill /IM` does nothing under Git Bash).

The current runtime is upstream llama.cpp. `start_servers.sh` starts the earlier PrismML fork of llama.cpp with the `PTQ1_0` file; it is kept only to reproduce the measurements made on the fork (benches v1 to v4, and the fork runs of the Apothicaire benchmark). Do not use it for new work.

Recall benchmark (it uses `data_bench/`, never `data/`; its description and results are in [`BENCH.md`](BENCH.md)):

```bash
python bench.py 2 16
```

Tests need no model server (a fake model stands in for `llama-server`) and run in CI on every pull request:

```bash
python -m unittest discover -s tests
```

## Apothicaire

Apothicaire imports `optchat.py` unchanged (`Agent`, `LLM`, `LLMError`, `CFG`, `SYSTEM_PROMPT`, `TOOLS`) as the conversation memory of its assistant. A change to these names breaks the Apothicaire repository, so run its tests too (see `CLAUDE.md`).

## Read more

- [`BENCH.md`](BENCH.md): the bench history (v1 to v9), the setup, the lessons learned and the dated decisions, with every figure. The raw results are the `bench_results*.md` files, which are measurements and are never edited by hand.
- `notes/`: working notes on hosting the memory in agent harnesses (Pi Durable and the DeepSeek Harness, dsh) and on the first prototype evening (some of them in French).
- `rapport.html`: the report of the first prototype evening, with the comparison of the harnesses and the recommendation (in French).
