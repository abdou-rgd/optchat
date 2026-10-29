# OptChat: bench history

Every measurement of OptChat, benches v1 to v9, with the setup, the tables, the conclusions and the dated decisions; `README.md` holds no figure and points here.

## The recall benchmark

Recall benchmark (plants 8 facts, 32 turns of filler, 8 questions; uses `data_bench/`, never `data/`): `python bench.py 2 16`. The upstream server (`start_servers_upstream.sh`, on `http://127.0.0.1:18435`) takes about 15 s to start.

## Prototype and results (working notes, 7–8 October 2026)

Prototype of the OptChat idea (VictorTaelin's gist: an endless chat whose history is its memory, compressed into a binary tree of summaries) running locally on:

- **Model**: Ternary Bonsai 2 27B (PrismML, base Qwen3.8 27B), file `Ternary-Bonsai-2-27B-PTQ1_0.gguf` already present in the Hermes models folder.
- **Server**: the PrismML fork of llama.cpp (`~/mitsuba/llama/llama-server.exe`, prism build b10743, CUDA 13.3). The standard llama.cpp shipped with Hermes refuses this format (ggml type 143). Hermes had never managed to run Bonsai for that reason.
- **GPU**: RTX 3060 12 GB. Server with 2 slots of 12k tokens, q8 KV cache: 7.3 GB of VRAM (measured on the server alone).

All the work was done on the evening of 7 October 2026. Detailed notes are in `notes/` (Pi Durable, dsh, spikes) and the bench results in `bench_results_v*.md`.

## How it works

- `log.jsonl`: every message (user, assistant, tool calls, results) in clear, append-only, fsync. Nothing is ever lost.
- `tree.jsonl`: summary nodes, immutable. L0 = one message → one line (≤ 512 bytes). L(k+1) = merge of two adjacent L(k) lines.
- `view.json`: the view, an ordered list covering the whole chat. The coarsest nodes are on the left, the raw messages on the right. The levels decrease from left to right.
- Each turn = a fresh model call: `[system]` + `[digest <memory> as a user turn]` + recent raw messages + new message.
- Tools: `zoom(id)` opens a node onto its two children (or onto the original message for an L0); `read_message(n)` reads a full message.
- Compaction after each turn, in a background thread (hidden behind the user's thinking time), on **slot 1** of the server so that the chat's KV cache is never evicted.

### Choices forced by running locally, and what we learned

1. **Lazy, batched compaction** (hysteresis: raw zone 12 → 4 messages, summary zones 12 → 8). Each change to the view invalidates the KV cache from that point on; doing it in batches divides the frequency.
2. **The static prefix stays cached**: the digest is a separate user turn, not part of the system prompt. System + tool definitions (654 tokens) are never recomputed.
3. **Constraint of the hybrid model** (checked on a fresh server in three configurations: base flags, without `--cache-reuse`, with close checkpoints `--ctx-checkpoints 64 --checkpoint-min-step 256`; identical results, see `run/flag_experiment.log`): Qwen3.8 has recurrent layers (SSM). When a prompt diverges *inside* the cached sequence, the server goes back well before the point of divergence: 512 tokens back if the divergence is at the end of the prompt, up to the system prefix if it is in the middle. A simple append at the end of the prompt costs ~40 tokens; a change to the digest costs 1,500 to 2,500 tokens of recomputation (4 to 5 s). Hence the hysteresis. The tests with f16 KV and `-ub 128` made earlier in the evening are not valid (the old server had kept the port, see lesson 10) and were not redone.
4. **Short messages kept verbatim** (≤ 160 characters): exact L0 line without a model call. On bench v4, 88 L0 lines out of 90 cost nothing.
5. **Compactor output constrained by a JSON schema** (llama.cpp grammar): the grammar fixes the exact number of lines, so no more fragile parsing.
6. **Bonsai 8B as a compactor is a failure** (bench v3: recall 2/8). It copies instead of summarising and loses whole facts at each merge. The 27B remains necessary for compaction. The 8B file stays in `models/` (PQ2_0 variant; the repository's Q2_0 variant does not load on this build).
7. **The cost of compaction is generation**: ~5,000 tokens of summaries per 48 turns at 24 tok/s ≈ 190 s of GPU. Batching the calls changes nothing. Leads: shorter lines, or a small non-ternary *instruct* model (Qwen3-4B Q4) to test.
8. **A 27B zooms little**: when the summaries keep the exact values, it answers without zooming (7 times out of 8). When they are bad (v3), it reads the messages one by one and exhausts the tool turns. Hence the rule: the last allowed tool turn is made without tools, and the model must answer.
9. **Robustness** (code review by a subagent, 15 findings fixed): repair at startup (truncated line, messages not covered by the view), lock with dead-PID detection, `os.replace` with retry under Windows, cutting the raw zone at a user-turn boundary, handling of the compactor's HTTP errors, character budget per batch.
10. **Windows / Git Bash trap**: `taskkill /IM llama-server.exe` does nothing under Git Bash (the `/IM` is converted into a path). For a good part of the evening, each "restart" of the server added one (nine processes found at the end), and the old one kept the port. The VRAM measurements taken between 22:30 and 23:30 are therefore inflated, and the bench v4 times are noisy. Use `Stop-Process -Name llama-server -Force` in PowerShell.

## Bench results (Bonsai 2 27B, RTX 3060)

| bench | compactor | recall | cached turn | turn with promotion | remarks |
|---|---|---|---|---|---|
| v1 | 27B slot 1 | 8/8 | ~1.0 s | ~4.5 s | summaries in English, roles mixed up |
| v2 | 27B slot 1, fixed prompt | 8/8 | ~1.1 s | ~4.9 s | French summaries, correct attribution |
| v3 | Bonsai 8B (2nd server) | **2/8** | ~1 s | — | merges that lose facts, tool loops |
| v4 | 27B slot 1 + verbatim + fixes | 8/8 | ~1.5 s* | ~8 s* | 88/90 L0 lines free; *GPU shared with the Pi Durable spike during the bench |

One run per bench only (v1 to v4).

View at ~80 messages: 4 to 10 raw messages + ~28 summary lines ≈ 5.5 KB ≈ 1.5k tokens; total prompt ≈ 2.9k tokens.

## Integration into a harness

See `notes/pi-durable.md` and `notes/pi-durable-spike.md` (Pi Durable, Earendil), `notes/dsh-integration.md` and `notes/dsh-spike.md` (DeepSeek Harness), and the report `rapport.html` for the comparison and the recommendation.

## Bench v5: Underdog-Saluki-27B (8 October 2026)

Same Qwen3.8-27B base as Bonsai 2, 7.9 GB IQ2-mix compression readable by the standard llama.cpp. Result (`bench_results_v5_saluki.md`): recall 8/8 (one run), 48 turns in 3.9 min, cached turn ~1.2 s, turn with promotion ~5 s, generation ~21 tok/s (Bonsai: ~24), 10.0 GB of VRAM used (Bonsai: 7.3). Verdict: a valid replacement, especially if one wants to do without the PrismML fork; Bonsai remains the default for the VRAM margin. File: `models/Underdog-Saluki-27B-1.0-IQ2-mix.gguf`.

## Bench v6: Bonsai 2 9B and 4B (Q2_0) on upstream llama.cpp b11700 (17 October 2026)

Same recall bench, three runs per model, upstream server (`llama-server` build 11700, CUDA 12.4, no fork), `-c 24576 -np 2 -ngl 99 --jinja -fa on -ctk q8_0 -ctv q8_0`. Files `bench_results_v6_*.md`.

| model | file | server VRAM | generation | recall (3 runs) | duration of a run | 27B (v4, fork) |
|---|---|---|---|---|---|---|
| 9B | `Ternary-Bonsai-2-9B-Q2_0.gguf` (2.56 GB) | ≈ 2.95 GB | 77–80 tok/s | 7/8, 7/8, 8/8 | ≈ 1 min | 8/8, ≈ 4–5 min, 7.3 GB |
| 4B | `Ternary-Bonsai-2-4B-Q2_0.gguf` (1.21 GB) | ≈ 1.9 GB | 104–108 tok/s | 8/8, 5/8, 7/8 | < 1 min | |

The failures are "I cannot find it" answers on planted facts (name + date, SSH port), so they are losses at compaction, as with the old 8B but much less frequent. The 27B remains the reference for memory; the 9B is a plausible compromise, the 4B a candidate compactor to test alone on slot 1.

## Bench v7: Bonsai 2 27B (Q2_0) on upstream llama.cpp b11700 (17 October 2026)

Same bench, same upstream server as v6, file `Ternary-Bonsai-2-27B-Q2_0-prism-fork-required.gguf` (7.63 GB; despite its name and the README of the HF repository, it runs on the standard llama.cpp since b11555). Files `bench_results_v7_*.md`.

| model | server VRAM | generation | recall (3 runs) | 27B PTQ1_0 (v4, fork) |
|---|---|---|---|---|
| 27B Q2_0, upstream | ≈ 8.4 GB | ≈ 31 tok/s | 8/8, 7/8, 8/8 | 8/8, ≈ 24 tok/s, 7.3 GB |

The 7/8 of run 2 is a loop of tool calls on one question, not a loss at compaction. Conclusion: the PrismML fork is no longer needed for the 27B; it keeps a 1 GB lead in VRAM (7.3 against ≈ 8.4 GB), but the choice is made at bench v8 below: standard llama.cpp.

## Bench v8: 27B Q2_0 upstream, Apothicaire's full bench (17 October 2026)

Apothicaire's bench of 25 exercises (gate v1; 25 exercises × 8 turns = 200 turns) on the upstream server b11700: 193/200 correct turns, 0/897 numbers not found in a tool result or a user message (numbers checked by the gate, drafts as well as shown answers), 141/141 valid tool calls, 8.0 s per turn on average (PTQ1_0 fork, run of 2026-10-09b: 195/200, 0/926, 160/160, 10.4 s). One run each, one sampling; development figures, in-sample (exercises, wordings and scoring rules written at the same time as the gate they measure): counts, not rates with an interval. Decision: the 17 November demo runs on the standard llama.cpp (upstream b11700, Q2_0), script `start_servers_upstream.sh`; Apothicaire's frozen set is planned on that same server (`bench/FROZEN_SET.md` of the Apothicaire repository). The fork (`start_servers.sh`, `PTQ1_0` file) is only used to reproduce the old measurements (benches v1 to v4 and Apothicaire runs on the fork, from 8 to 18 October).

## Bench v9: 27B Q2_0 upstream, byte guard, model-free joins, clean cuts (21 October 2026)

The three memory fixes of 20 October (cards T-094 to T-096, PR #1 merged on 21 October): a byte guard on the digest and the raw zone with forced level merges (`view_max_bytes` 18,000, `digest_max_bytes` 12,000); a model-free merge of two short lines, messages kept verbatim up to 512 bytes (instead of 160 characters); cutting of summary lines at a word boundary, never inside a UTF-8 character, and head + tail of long messages for the compactor. Same recall bench, same upstream b11700 server and same Q2_0 file as v7, three runs (`bench_results_v9_27b_fixes_run1..3.md`, commit `6776a61`).

| | recall (3 runs) | duration of a run | compactor calls | model-free joins | merges forced by the guard |
|---|---|---|---|---|---|
| v9, with the fixes | 7/8, 8/8, 8/8 | 1.9 / 1.4 / 2.4 min | 5 / 3 / 9 | 56 / 54 / 72 | 0 / 0 / 0 |
| v7, before | 8/8, 7/8, 8/8 | 5.3 / 4.5 / 2.9 min | 30 / 27 / 17 | | |

The 7/8 of run 1 is a loss: on the SSH port question, after a zoom, the model answers that it does not have the information (the 7/8 of v7 is a loop of tool calls). 23 correct answers out of 24 on both sides (three runs of 8 questions, a single set of runs per version): no measured regression, no improvement in recall; the cost of compaction (compactor calls, run duration) goes down. The byte guard did not trigger in these 48-turn runs (0 forced merges): it is tested without a model (`tests/test_memory.py`), not by this bench.
