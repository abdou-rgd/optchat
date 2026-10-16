# Pi Durable spike: OptChat memory view on local llama.cpp (2026-10-07, 23:00-23:27)

## Verdict
1. **Works: yes, on this machine and this llama.cpp fork.** The tested parts were: Pi Durable 1.0.4, a `beforeRequest` hook that rebuilds the view, a `zoom` tool with `replay:"safe"`, JSONL storage, and Bonsai 27B via `createProvider` + `openAICompletionsApi`. Every turn of the final runs answered correctly ("2222", "PostgreSQL"), with no harness errors. The one bad answer, a truncated turn 2 in the first run, was caused by slot preemption on the shared server (gotcha a), not by Pi.
2. **Verified by RUNNING:**
   - npm install on Windows.
   - The exact request body sent: system prompt + tool schemas kept, `<memory>` digest + "Compris." + raw tail, plus `max_tokens`, `cache_prompt` and `chat_template_kwargs`.
   - Streamed `tool_calls` from build b10743: 7/7 zoom calls parsed, 0 malformed.
   - Kill during streaming: resumed by **re-sending** the identical request, completed, no duplicate user entry.
   - Kill inside `zoom`: the tool was **re-executed** and the run completed.
   - A second resume does nothing.
   - A background `defineTask` compactor calling Bonsai 8B, with its lines read by the hook.
3. **NOT run (only read or not attempted):**
   - Long conversations near the 12k context.
   - The real tree/hysteresis compactor and a crash during compaction.
   - `read_message` (registered, never called by the model).
   - SQLite storage, multi-process use, a bench at OptChat scale.
4. **Effort:**
   - This spike: about 25 min of coding with the research note in hand. The script is 338 lines, about 200 of them product code.
   - Full port, my estimate: **2-3 days**. That covers the tree/hysteresis `Compactor` (~160 Python lines) as a phased durable task, tree/view state in `defineDoc`s, the `#n`→entry index for `read_message`, the CLI/REPL, and bench parity.
   - The memory algorithm gains nothing. What you buy is durable runs and resume.
5. **Main gotchas:**
   - (a) On the shared llama.cpp server, a request pinned with `id_slot` took over my in-flight unpinned request's slot. My answer was cut after 12 tokens and reported as a normal `finish_reason:"stop"`, which Pi stores as a completed answer.
   - (b) The tail cut must be anchored per run, or every tool round rewrites the prefix and loses the KV cache.
   - (c) Each digest change re-prefills everything after the system prompt (2.7k tokens ≈ 5 s), the same as optchat.py.
   - (d) Crash recovery regenerates from scratch, not a continuation. The partial is kept as an `aborted` entry.
   - (e) A dummy apiKey and compat flags are mandatory. The API is "Experimental", so versions are pinned to exactly 1.0.4.
6. **Recommendation:** feasible and low-risk technically. Port only if you want durable/resumable runs or multi-client hosting. Keep `log.jsonl`/`tree.jsonl` semantics as the source of truth during the transition.

**Shared-GPU caveat:** `run/gpu_free` appeared at 23:02:05, but a benchmark (`data_bench`, `run/bench4.log`) started at 23:02:06 and ran until 23:07:35. 16 of my requests (23:05-23:06: 1 probe, 4 from `run1`, 11 replays) overlapped it. My requests were unpinned, so they should not truncate its answers, but its timings and cache hits in that window may be degraded. After 23:07:44 (`run/gpu_free_dsh`) another unpinned client shared the server. The final runs below show about 25 tok/s generation, consistent with no contention.

## Setup (ran)
- Node v22.23.2, npm 10.9.8, Windows 11, Git Bash.
- Folder: `C:\Users\abdou\apothicaire\optchat\pi-spike`.
- `npm init -y`, then `npm install @earendil-works/pi-durable @earendil-works/pi-ai @earendil-works/chord`:
  - 26.9 s, 90 packages, `node_modules` 106 MB, 0 vulnerabilities.
  - One warning: `npm warn deprecated node-domexception@1.0.0`.
- Installed **pi-durable 1.0.4, pi-ai 1.0.4, chord 1.0.4**. `package.json` was afterwards edited to the exact `1.0.4` (no caret).
- Server: llama.cpp `build_info b10743-adfffbe41`, 2 slots × 12288 ctx, Jinja template with tool calls (from `/props`).
- 8B server: 1 slot × 8192 ctx.
- Startup:
  - `import` of pi-durable + pi-ai takes 0.37 s, RSS 69 MB.
  - Whole script start to first log line is about 0.5 s warm (2.0 s cold).
  - `Harness.open` on the JSONL store takes 0.01-0.03 s.

## Script: `C:\Users\abdou\apothicaire\optchat\pi-spike\optchat-pi.mjs` (338 lines, 21.3 KB, plain ESM, no build step)

| Section | Lines | What |
|---|---|---|
| read-only memory | 39-73 | Reads `run/data_v2/{tree.jsonl,log.jsonl,view.json}`. The digest uses the 30 `node` items of `view.json`, about 6.2 KB, same line format as `render_digest` (`[id Lk #first-#last MM-DD HH:MM] text`). `zoom(id)` returns the 2 child lines, or the original `log.jsonl` message for a node with `msg`. The `raw` items of `view.json` (msgs 90-101) are NOT used: the raw tail is Pi's own transcript. The system prompt is copied from `optchat.py`. |
| providers | 74-114 | `createProvider` + `openAICompletionsApi()` for 27B and 8B, dummy key `"local"`, compat `{supportsDeveloperRole:false, supportsReasoningEffort:false, supportsStore:false, maxTokensField:"max_tokens"}`, `samplingParams {temperature:0.3, cache_prompt:true, chat_template_kwargs:{enable_thinking:false}}`, `maxTokens 700`. A thin `streamSimple` wrapper with `onPayload` logs/dumps each request body (`last-payload.json`). No `id_slot` (see gotcha a). |
| background compactor | 115-153 | `defineDoc` `app.optchat-digest` (lines `{first,last,text}`). `defineTask` `optchat.compact` with one phase: `runtime.context()` → new messages → `runtime.models.completeSimple(bonsai8b, …)` → one commit that appends the line AND makes the task terminal. |
| extension | 154-214 | `zoom` and `read_message` via `defineTool({replay:"safe"})`, `section("preamble", SYSTEM_PROMPT)`, `tasks:[Compact]`, `hook(GenerationTask, {beforeRequest})`. The hook returns `[all system msgs] + user(<memory>…</memory> [+ compactor lines for msgs that left the tail]) + assistant("Compris.") + tail`. The tail is the last 6 chat msgs counted from the current run's user msg, snapped back to a user msg. It drops `aborted`/`error` assistant msgs. |
| plumbing | 215-256 | `openNodeJsonlStorage("./data", ctx, {fsync:true})`, `Harness.open(…, {settings:{compaction:{enabled:false}, retry:{maxRetries:1}}, onReport})`, `harness.root(ctx, {agent:{model:{provider:"llamacpp", modelId:"bonsai"}}})`. Turn = `root.submit({type:"input", content, requestId})` then `.wait()`. Answer and tool calls are read back with `root.entries({minEntryId})`. |
| modes (test harness) | 257-338 | `run [--fresh] [--compact]`, `turn4\|turn5`, `resume [turn5]`, `crashtest [tool]`, `digest`. |

The synthetic "Compris." message must be a full `AssistantMessage` (`api/provider/model/usage/stopReason:"stop"`, same provider/model) so pi-ai treats it as the model's own turn.

## Commands run and results (all against http://127.0.0.1:18435/v1 unless noted)

| Command (in `pi-spike/`) | Log | Result |
|---|---|---|
| raw `curl` streamed tool-call probe | (terminal) | `delta.tool_calls` OpenAI-style: id+name in the 1st chunk, arguments split into 8 fragments (`{`,`"id":"`,`n`,`1`,`3`,`1`,`"`,`}`), `finish_reason:"tool_calls"`, usage chunk with `choices:[]`. The `model` field is the full .gguf path, which pi-ai stores as `responseModel` (cosmetic). |
| `node optchat-pi.mjs run --fresh` (1st version) | `run1.log` | t1 OK 8.7 s; **t2 answer truncated** "Le port SSH du serveur de prod d'Atlas est" (12 tokens, `stop`); t3 zoom(n132) → PostgreSQL. Cause in gotcha (a). |
| 11 manual `curl` replays of the t2 request (9 streamed, 2 not) | `t2-*.json` | Never truncated: 8× "…est 2222.", 2× zoom(n131), 1× read_message(1). Sampling varies at T=0.3. |
| `run --fresh` (1st version, after the bench stopped) | `run2.log` | 5.6 s / 1.2 s / 2.9 s (t3 zoom n132); all correct. |
| `crashtest` (1st version) | `crash1.log` | Same outcome as the final run below. Resume took 18.8 s because the other client shared the GPU (7.1 tok/s). |
| `OPTCHAT_PI_DATA=./data-compact run --fresh --compact` (1st cut logic) | `run-compact.log` | Works. Revealed gotcha (b): t3's 2nd request re-prefilled 2666 tokens. |
| **`run --fresh`** (final) | `final-run.log` | See table below. |
| **`crashtest`** (final) | `final-crash.log` | Durability A, plus C (`resume` again → `final-resume2.log`). |
| **`OPTCHAT_PI_DATA=./data-compact run --fresh --compact`** (final) | `final-compact.log` | Background compactor, see below. |
| **`crashtest tool`** (final) | `final-crash-tool.log` | Durability B. |

### Per-turn results, final script
Wall time is measured from `submit` to `wait()` returning, in-process. Token counts are from llama.cpp usage: new prompt / cached prompt / output.

| Run | Turn | Wall | Zoom | Tokens (per request) | Answer |
|---|---|---|---|---|---|
| final-run | 1 heure | 5.3 s | no | 2094/652/24 | "Je n'ai pas accès à l'heure actuelle…" |
| final-run | 2 port SSH | 1.2 s | no (2222 is verbatim in digest lines n131/n142) | 43/2769/18 | "…est 2222." |
| final-run | 3 base | 1.1 s | no (verbatim in n132) | 26/2829/17 | "PostgreSQL … à cause des transactions." |
| final-compact | 1 | 5.2 s | no | 2094/652/24 | same |
| final-compact | 2 | 3.0 s | **zoom(n131)** | 43/2769/28 + 231/2839/18 | "…est **2222**." |
| final-compact | 3 | 3.1 s | **zoom(n132)** | 26/3087/28 + 181/3140/23 | "…**PostgreSQL**…" |
| final-compact | 4 recap | 9.9 s | no | 2725/652/128 (digest changed → re-prefill) | 6-sentence recap, facts correct |
| final-crash | 4 resumed | 4.8 s (resume process) | no | 4/2910/117 | recap, facts correct |
| final-crash-tool | 5 resumed | 2.0 s (resume process) | zoom(n131) re-executed | 2368/652/28 (child), 231/3047/24 (resume) | "…10.0.3.47." |

Zoom happened in 7 of 20 scripted turns across all logs: run1 t3, run2 t3, run-compact t2+t3, final-compact t2+t3, final-crash-tool t5. Three of the 20 turns said "sans appeler d'outil" and one explicitly asked for zoom. The zoom was always on the right node (n131/n132), and every streamed tool call parsed. Bonsai answers directly when the value is already verbatim in the digest, which matches the system prompt.

### Durability A: kill while the answer streams (`final-crash.log`; same in `crash1.log`)
1. The child submits turn 4 (`requestId:"turn-4"`). The parent kills it (`child.kill("SIGKILL")` = TerminateProcess) 2 s after the first committed partial (3.4 s after start).
2. Storage after the kill: `main.jsonl`, `task-22.jsonl` (generation checkpoint), `doc-2.jsonl` (live partial, 4 KB).
3. llama.cpp logged `stop: cancel task` for the dropped connection and released the slot, so generation did not keep running.
4. `resume` in a new process:
   - Reopen took 0.03 s.
   - `harness.inspect()`: `task 22 pi.generation pending phase=request -> ready`, `submission 21 requestId=turn-4 status=placed`, committed partial present.
   - Re-submitting with the same `requestId` returned **the same submission 21**.
   - The harness converted the partial into an `aborted` assistant entry, re-ran `beforeRequest` and **re-sent a byte-identical request** (same 10 msgs, 9035 B).
   - Server log: the killed request was cancelled (`stop: cancel task, id_task = 26933`). The re-sent task 26996 matched the slot cache (`f_sim_best = 1.000`), prefilled 4 tokens, and generated 117 tokens at 26.6 tok/s. Status `done`.
   - Transcript: 4 user entries (no duplicate); kinds end `…,user,assistant(aborted),assistant`.
5. Verdict: **resumed by retry/re-send; not duplicated; not failed.** The partial is not continued: its tokens are regenerated.

### Durability B: kill inside the `zoom` tool (`final-crash-tool.log`)
1. Turn 5 asks for zoom first. `ZOOM_DELAY_MS=5000` keeps the call open, and the kill lands 1 s into it.
2. After reopen: `task 29 pi.tool pending phase=execute -> ready`, `task 27 pi.generation waiting phase=tools`, submission 26 `placed`.
3. On `resume`, **`zoom(n131)` executed again** (`replay:"safe"`), then the next generation request carried the tool result and the answer was "10.0.3.47".
4. 5 user entries, one tool call, one tool result: no duplicate model call for the tool round.

### Durability C: resume again on finished storage (`final-resume2.log`)
No pending tasks. Submitting `turn-4` again returned the same submission 21, already `done`. No HTTP request, transcript unchanged. The process ran in 0.5 s.

### Background compactor (`final-compact.log`)
- After each turn the host commits `tx.createTask(Compact, {upTo}, {ownership:{kind:"conversation"}, background:true})`.
- The conversation is immediately idle, so the next input could start.
- Before the next turn the host joins with `harness.waitForTask(id)` (the optchat.py `thread.join` equivalent). Joins waited 0.4-0.5 s.
- 4 tasks completed. The 8B took 0.4-0.8 s per line (3.5 s on the first cold call in `run-compact.log`).
- Lines are good French one-liners, e.g. "L'utilisateur demande le port SSH du serveur de prod d'Atlas et l'assistant confirme que c'est **2222**." The 8B copies markdown from the answer, so the prompt needs a "sans markdown" fix.
- `beforeRequest` reads the doc with `hookApi.snapshot(DigestDoc, conversationId, ctx)`. It injected the turn-1 line at turn 4, once turn 1 left the tail.
- The doc is stored in `data-compact/doc-13.jsonl` (1.5 KB).
- Not tested: a crash inside the compactor. The atomic "line + terminal" commit makes a rerun idempotent, but that is by design, not run.

### Storage (`data/`, after 5 turns and 2 crashes)
- `main.jsonl`: 114 commit lines, 24 KB, each `{"format":1,"type":"commit","seq":…,"writes":[…]}`.
- Writes: 5 `pi.user`, 7 `pi.assistant` (1 aborted, 1 tool call), 1 `pi.tool-result`, 1 `pi.system`, 101 document changes (mostly the 100 ms live-partial throttle), 27 task sidecars.
- `task-*.jsonl` files exist only while a task is live and are reclaimed afterwards.
- `doc-*.jsonl` are small rewritten documents.
- No torn line after two hard kills with `fsync:true`.
- No locking: a second process on `./data` would not be stopped.

## Errors and anomalies (first lines)
- No exceptions, no `onReport` calls, no `[report]` lines in any log.
- Truncation in `run1.log`, turn 2: `ANSWER: Le port SSH du serveur de prod d'Atlas est`, usage `43in/12out/2769cached`, `stopReason:"stop"`, `rawStopReason:"stop"`. Server log (`run/server.log`, read only):
  ```
  54.44.904 I slot get_availabl: id  1 | task -1 | selected slot by LCP similarity, f_sim_best = 0.985 ...   (my request -> slot 1)
  54.47.257 I slot get_availabl: id  1 | task 17468 | selected slot by id (1)                              (a pinned request arrives)
  54.47.257 W srv         alloc:  - making room for prompt cache entry, removing oldest entry (size = 816.070 MiB)
  54.47.705 I slot print_timing: id  1 | task 17468 |        eval time =    1468.50 ms /    12 tokens
  54.47.706 I slot      release: id  1 | task 17468 | stop processing: n_tokens = 730, truncated = 0         (730 = the other client's prompt)
  ```
  The bench pinned `id_slot:1`. My unpinned in-flight request on slot 1 ended after 12 tokens with a normal `stop`. Pi had no way to notice.
- My own tooling slip, which had no effect on files: one malformed heredoc command was stopped and redone with Edit.

## Gotchas for a full port
1. **Slot pinning:** optchat.py pins `id_slot` (chat/compactor). Never mix pinned and unpinned clients on one server, and give each process its own slots. With pi-ai, pin per `Model` via `samplingParams.id_slot`.
2. **Stable view per run:** compute the tail cut from the run's user message (done in the final script). Otherwise each tool round moves the cut, changes the prefix, and re-prefills about 2.7k tokens (`run-compact.log`).
3. **Digest changes cost a re-prefill** of everything after the system prompt. Batch compactor lines and add them at turn boundaries only, as optchat.py does.
4. **Recovery is re-generation,** not continuation. The partial stays in storage as `aborted`; pi-ai and the hook both drop it from the context.
5. **Output cap:** pi-ai sends `max_tokens = min(maxTokens, contextWindow - estimate - 4096)`, so the view must stay under about 7.5k tokens for a 700-token answer at 12k ctx (read, consistent with the run).
6. **Required boilerplate:**
   - Dummy `apiKey`; pi-ai otherwise throws "No API key for provider".
   - Compat flags.
   - `samplingParams` for the llama.cpp extras.
   - Full `AssistantMessage` fields on synthetic messages.
   - Keep all `system` messages, which carry the tool schemas.
7. **pi-ai always streams.** This fork's streamed `tool_calls` are fine. `content:null` on replayed tool-call messages was accepted.
8. **Experimental API:** pin exact versions (done). JSONL replays the whole store into memory at open (fine here: 0.03 s for 114 commits).

## Files
- `C:\Users\abdou\apothicaire\optchat\pi-spike\optchat-pi.mjs`: the script.
- `package.json` (exact 1.0.4 pins) and `package-lock.json`.
- Stores:
  - `data/`: final 3 turns + crash tests A/B/C.
  - `data-after-3turns/` and `data-after-4turns/`: snapshots.
  - `data-compact/`: compactor run.
- Logs:
  - `final-run.log`, `final-crash.log`, `final-resume2.log`, `final-crash-tool.log`, `final-compact.log`: final script.
  - `run1.log`, `run2.log`, `crash1.log`, `resume2.log`, `run-compact.log`: earlier versions. `resume2.log` shows a cosmetic "NEW" label bug, since fixed.
- `last-payload.json`: last request body. `t2-stream.json` / `t2-nostream.json`: turn-2 replay payloads.
- Nothing outside `pi-spike/` was modified except this note. `run/server.log`, `run/bench*.log` and `data_bench/` were only read, for diagnosis.
