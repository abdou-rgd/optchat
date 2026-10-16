# DeepSeek Harness (dsh) + local Bonsai 27B - hands-on spike (2026-10-07, 23:02-23:25)

## Verdict
1. **Works with local Bonsai: YES (I ran it).** dsh 0.1.7-rc.2 headless drove Ternary Bonsai 2 27B on llama.cpp `http://127.0.0.1:18435/v1` through `@deepseek-ai/dsh-llm-pi-ai`, in an isolated `DSH_HOME` (the real `~/.dsh` was not touched). 13 real-model runs, all exit 0, none failed. Each prompt took 7-36 s, about 3.5 s of which is process boot and exit.
2. **Tool calls: OK.** Bonsai correctly called `glob`, `pwsh` (`Get-Date` inside the Windows ACL sandbox), `write`, `read` (4 parallel reads in one step) and the custom `zoom`. The request carried `chat_template_kwargs:{enable_thinking:false}`. The llama.cpp prompt cache was reused across processes (~5.9k cached tokens per follow-up).
3. **Session format:** one append-only JSONL file per session at `$DSH_HOME/sessions/--<cwd>--/session-<uuid>/session.v4.jsonl`. It is zstd-framed by default; `compression: none` gives plain lines. Events are `{type, seq, time, data, surfaceOp?}`. You continue a session with `--session-id`. `/compact` can't be reached headless, but automatic compaction ran. Once tuned for 12k it wrote a checkpoint.
4. **Plugin: YES, ran end to end.** A ~45-line ESM plugin that registers `zoom(id)` loaded two ways:
   - with `dsh plugin --profile <p> add <local path>` (pnpm `link:` + bundle patch, using the pnpm bundled with the Desktop app);
   - as a patch row whose `name` is a file path under `$DSH_HOME/profiles/`.
   A file path anywhere else fails with "failed to import", because `@deepseek-ai/dsh-tools` doesn't resolve from there.
5. **Effort to host an OptChat memory backend (my estimate):**
   - zoom/read_message tools: ~2 h (zoom is already done here).
   - The memory view: dsh has no per-request message hook like Pi's `beforeRequest`. It would have to be a custom compaction backend (documented base class) that writes durable surface-replacement events. Porting that is ~2-4 days, under framework constraints: one summary message per replaced span, the summary must be smaller than the span, and it runs inside the turn.
6. **Main gotchas:**
   - Stock headless sends 24 tools + a coding persona = 5.8k prompt tokens, 47% of the 12k window. A lean overlay brings it to 2.76k.
   - The default compaction headroom (65,536) silently disables auto-compaction at 12k. When it does run, the summary call blocks the turn 10-30 s, evicts part of the KV cache, and is rejected unless smaller than its span.
   - `enable_thinking` is only sent if the model is declared reasoning-capable with `thinkingFormat: chat-template`.
   - One process per prompt.
   - pnpm isn't installed on this machine.
   - dsh is a release candidate (0.1.7-rc.2).

Legend: **[R]** = I ran it and saw the result. **[D]** = I only read it in a package README or in the source.

---

## 0. What RAN vs what I only READ
- **RAN:**
  - `dsh --version`, `dsh --help`, `--dump-default-config`, `--dump-config`.
  - Profile setup in an isolated home.
  - 13 headless runs against Bonsai: the 3 required prompts, 2 zoom, 6 compaction-related, 1 lean.
  - 6 headless runs against a local mock OpenAI server (`tools/mock-openai.mjs`, 127.0.0.1:18499, no GPU). These checked the config, the request shape and plugin loading before I used the GPU.
  - `dsh plugin --profile zoomtest add <local path>`, using the Desktop app's bundled pnpm 11.7.0.
  - Creating a custom profile with `--from-default-profile headless`.
- **READ only:**
  - plugin-manager service, registries and version exemptions;
  - the compaction backend base-class API;
  - the SDK/ACP profiles;
  - `agent/request` waterfall semantics;
  - the approval fail-closed path;
  - Desktop app internals.
- **GPU:** `run\gpu_free_dsh` already existed (created 23:07) when I first checked at 23:10. My first request to the model server was at ~23:10:40 (`/v1/models`, `/props`, `/slots`). The real runs were 23:11-23:20.
- **Credentials and real home:** I never read `.credentials.yaml`. Nothing under `C:\Users\abdou\.dsh` was modified: `find ~/.dsh -newermt '2026-10-07 23:00'` returns nothing.

## 1. Isolation [R]
- `@deepseek-ai/dsh-home-paths` picks the home in this order: explicit path, then `$DSH_HOME`, then `~/.dsh` (a blank env value is ignored). Profiles, sessions, storages, logs, credentials and the home patch all live under it.
- I used `DSH_HOME=C:\Users\abdou\apothicaire\optchat\dsh-spike\home`. The shipped `headless` profile set itself up at `home\profiles\headless\`:
  - `package.json` with bundles `[@deepseek-ai/dsh-base, @deepseek-ai/dsh-headless]`;
  - an empty `cordis.patch.yml`;
  - `pnpm-workspace.yaml` (`nodeLinker: hoisted`, `autoInstallPeers: false`).
- I also exported `DSH_TELEMETRY_DISABLED=1`. Otherwise the base row `session-telemetry-otel` runs in FEEDBACK_ONLY mode towards `harness-telemetry.deepseeksvc.com`, and only exports after explicit user feedback [D].
- Layer order [D], each layer overriding the one before:
  1. bundle patches;
  2. the profile's `cordis.patch.yml`;
  3. `$DSH_HOME\cordis.patch.yml`;
  4. `--patch <file>` overlays (repeatable).
  A patch replaces a row's whole `config`, so you must restate every field you keep.
- I ran the cached launcher directly, with no npx and no network: `node C:\Users\abdou\AppData\Local\npm-cache\_npx\1e7f6d9597241db0\node_modules\@deepseek-ai\dsh\lib\bin.js`.

## 2. Provider route + default model [R]
The config is in `dsh-spike\home\profiles\headless\cordis.patch.yml` (the isolated profile), with a copy in `dsh-spike\patches\bonsai.yml`:
```yaml
- id: llm-pi-ai                       # row from dsh-base, mounted dormant with zero routes
  config:
    providers:
      bonsai-local:
        displayName: Bonsai 27B (llama.cpp local)
        apiKeyEnv: BONSAI_API_KEY       # credential reference; export BONSAI_API_KEY=dummy-local-key
        api: openai-completions
        baseURL: http://127.0.0.1:18435/v1
        compat:
          supportsStore: false
          supportsDeveloperRole: false
          supportsReasoningEffort: false
          supportsStrictMode: false
          maxTokensField: max_tokens
          thinkingFormat: chat-template
          chatTemplateKwargs:
            enable_thinking:
              $var: thinking.enabled    # -> false unless a reasoning effort is selected
        models:
          - id: bonsai
            name: Ternary Bonsai 2 27B
            contextWindow: 12288
            maxTokens: 2048
            input: [text]
            reasoningEfforts:           # declaring it reasoning is what makes pi-ai send chat_template_kwargs
              off:
              high: high
        retryPolicy:
          mode: normal
          maxRetries: 1

- id: agent-default-model             # makes it the default; base default is deepseek-official / deepseek-flash
  config:
    provider: bonsai-local
    model: bonsai

- id: session-persistence-jsonl       # plain-text logs instead of zstd frames
  config:
    root: !!js dshHomePath('sessions')
    compression: none

- id: compaction-basic                # see section 4; defaults do not work at 12k
  config:
    modelPolicies:
      - provider: bonsai-local
        model: bonsai
        headroomTokens: 1024
        maxTokens: 1024
        thresholdRatio: 0.75
        retainTokens: 2048

- id: session-title-llm               # skip one extra LLM call per new session (fallback title used)
  disabled: true
```
The mock captured this request [R]:
- Body: `{model:"bonsai", stream:true, stream_options:{include_usage:true}, max_tokens:2048, chat_template_kwargs:{enable_thinking:false}, messages:[system, user task, user runtime-context], tools:[24 functions]}`.
- Headers: `Authorization: Bearer dummy-local-key` and user agent `deepseek-harness/0.1.7-rc.2`.

Notes:
- **Thinking control:** pi-ai sends `chat_template_kwargs` only when `thinkingFormat: chat-template` is set and the model is reasoning-capable. With `reasoningEfforts: false`, nothing is sent (see `buildParams` in `@earendil-works/pi-ai/dist/api/openai-completions.js`) [D]. The mock capture confirms it [R].
- **`cache_prompt`:** it can't be set; the profile schema has no extra-body passthrough. llama.cpp's default (on) applied, and cache hits were observed [R].
- **Placeholder key:** a server without a key still needs one, either via `apiKeyEnv` or an `Authorization` entry in `headers` [D, README]. The env var is resolved on every request, so no secret goes in the YAML [R].
- **Model name:** llama.cpp ignores it. The log stores `responseModel` as the gguf path [R].

## 3. Headless runs [R]
Command (wrapped by `dsh-spike\tools\run.sh`), with cwd `C:\Users\abdou\apothicaire\optchat\dsh-spike\workspace` (sample files `README.md`, `recettes.csv`, `todo.txt`, `calc.py`):
```
DSH_HOME='C:\Users\abdou\apothicaire\optchat\dsh-spike\home' DSH_TELEMETRY_DISABLED=1 BONSAI_API_KEY=dummy-local-key \
  node <npx-cache>/node_modules/@deepseek-ai/dsh/lib/bin.js --profile headless [--patch X.yml] --json [--session-id <id>] "<prompt>"
```
Outputs per run:
- `dsh-spike\runs\<label>.jsonl`: the event stream (session, status, text, tool_call, tool_result, final);
- `.err`: empty for every real run;
- `.meta`: exit code and wall time.

| run | session/turn | prompt | wall | agent turn | tools called | first-step input tokens |
|---|---|---|---|---|---|---|
| a | S1/1 | Réponds en une phrase : que vois-tu dans ce dossier ? | 20.3 s | 16.7 s | glob `**/*` | 5835 (cold) |
| b | S1/2 | Crée un fichier notes.txt contenant la date du jour | 21.1 s | 17.4 s | pwsh `Get-Date`, then write | 25 + 5935 cached |
| c | S1/3 | Qu'as-tu écrit dans notes.txt ? | 10.2 s | 6.5 s | read | 24 + 6181 cached |
| e | S2/1 | zoom sur n148, quel prénom en T ? | 16.6 s | 13.3 s | zoom(n148) | 5972 (cold) |
| f | S2/2 | Fais zoom sur le nœud n999. | 7.0 s | 3.5 s | zoom(n999) -> "node not found" | 27 + 6234 cached |
| g | S3/1 | Lis les 4 fichiers et résume-les | 32.2 s | 28.7 s | read x4 in one step | 5844 (cold) |
| i | S3/3 | Lis calc.py, que s'affiche-t-il ? | 9.1 s | 5.6 s | read | 35 + 6685 cached |
| m | S4/1 | lean overlay + zoom n149, quel fruit ? | 12.7 s | 9.4 s | zoom(n149) | 2758 (cold) |

Runs d, h, j, k and l are the compaction runs, covered in section 4.

Answers:
- (a) "Le dossier contient 4 fichiers : README.md, recettes.csv, todo.txt et calc.py."
- (b) Wrote `workspace\notes.txt` = "7 octobre 2026" and replied "Le fichier notes.txt a été créé avec la date du jour : 7 octobre 2026."
- (c) Re-read the file, then "J'ai écrit la date du jour : « 7 octobre 2026 »."
- (e) "Théodore" (correct).
- (f) Said n999 does not exist (correct).
- (g) 4 one-line summaries.
- (i) "46.25" (correct).
- (m) "Melon" (correct).

Speed:
- Cold prefill: ~11.4-11.9 s to first token for ~5.9k tokens (~500 tok/s); 5.9 s for 2.76k tokens (lean).
- Decode: roughly 15-25 tok/s.
- Per-invocation overhead (wall time minus agent turn): 3.4-3.7 s.

Errors:
- None on the model path.
- The only failures were my own: a plugin path outside the profile (section 5) and a Windows path literal mangled by my shell (fixed).
- The date came from a real tool call; the stock system prompt contains no date.

## 4. Sessions and compaction [R]
**Where it lives:**
- Session S1 (the 3 required prompts): `home\sessions\--C-Users-abdou-optchat-dsh-spike-workspace--\session-01f1d0f7-2964-4fd7-affd-ba747eb4bb0a\session.v4.jsonl`. After those 3 short turns it had 57 lines (85 KB).
- Projection cache: `home\storages\session_projcache\sessions\<id>.json` (title, tokenUsage, contextPressure, todos, goal, plan, ...).

**Format:**
- Line 0 is a header: `{"type":"session","version":4,"id":..,"createdAt":ms,"cwd":..,"isSeeded":false,"delegationDepth":0}`.
- After that, one event per line: `{type, seq, time(ms), data, surfaceOp?, sourceEventSeqs?}`.

Event types seen:

| type | content |
|---|---|
| `permission/preset`, `sandbox/mode`, `approval/policy` | session settings |
| `agent/inbox/spliced` | queued input |
| `turn/start`, `turn/end`, `step/start`, `step/end` | turn and step boundaries |
| `system/message` | system prompt |
| `user/message` | the task, plus a separate runtime-context user message |
| `request/header` | `{config:{provider,model,maxTokens}, adapterDefaults, tools:[24 full schemas]}`, ~19.6 KB, written again by each new process |
| `request/context` | `{provider, model, contextWindow}` |
| `session/title` | session title |
| `assistant/message` | text/tool-call blocks, `usage`, pi-ai `replayState`, and the full token stream with per-chunk timings |
| `tool/call`, `tool/result` | tool calls; results carry `isError` and `meta` |
| `session/end-seed` | written when a new process adopts the session |
| `compaction/start`, `compaction/summary`, `compaction/end` | compaction |

**Continuing a session:**
- `--session-id <id>` adopts an existing log [R, same cwd].
- It is refused if the cwd or preset differs, or if the id is unknown [D].
- One task per process; there is no interactive follow-up.

**`/compact`:** it is a UI command, provided by the `dsh-commands` adapters in Web/TUI. Headless sends the task as a plain user message, so `/compact` can't be reached headless [D]. The SDK and ACP profiles don't expose it either [D].

**Automatic compaction (`compaction-basic`):**
- The trigger is `floor(min(W*thresholdRatio, W - maxTokens - headroomTokens))`. With the default headroom of 65,536, `W - O - B` is negative at 12k, so auto-compaction is skipped with a warning until you configure it [D].
- I forced it with a low threshold [R]:

| run | session | settings | result |
|---|---|---|---|
| d | S1 | ratio 0.49, retain 256 | `compaction/start`, a 29.6 s LLM call, then `compaction/end` with error "summary is not smaller than the shadowed content (388 estimated framed tokens >= 226)". The turn was then answered normally. |
| h | S3 | ratio 0.52 | rejected (426 >= 162) |
| j | S3 | ratio 0.52 | rejected (586 >= 581) |
| k | S3 | ratio 0.52, summary cap 200 | rejected: "summarization truncated at the token cap (incomplete checkpoint)" |
| l | S3 | ratio 0.52, retainTokens 64 | **success** (below) |

What run l wrote:
- **`compaction/summary`:** `{summary, rawOutput, shadowedRange:{start:8,end:61}, shadowedSeqs, shadowedTokenCount:986, provider, model, maxTokens:1024, usage:{in 732 + 6642 cached, out 588}}`, after a 25.7 s call.
- **Replacement message:** a `user/message` with `surfaceOp:{op:"replace",startSeq:8,endSeq:61}`. Its text is an English preamble ("This is an automatically generated checkpoint condensing an earlier span of the conversation..."), then `<compacted-summary>`, then the summary.
- **Template:** the summary follows a fixed, English, coding-oriented template: Primary Request and Intent / Key Technical Concepts / Files and Code / Errors and Fixes / Pending Jobs / Current Work / Next Step / Critical Context.
- **Accuracy:** it contained one factual error: it said the Pixel question was still unanswered.
- **Original events:** they stay in the log. The log is append-only; only the in-context view (the "surface") is replaced.

**Cost:**
- Each attempt is a synchronous LLM call inside the turn (10-30 s here).
- After one, the next chat request had only 5.3-5.9k cached tokens and recomputed 0.4-1.7k (the hybrid SSM cache rolls back).
- So compaction shares and disturbs the chat's KV cache. OptChat avoids this with its background compactor on slot 1.

## 5. Plugin [R]
**How a third-party plugin is added** [D]:
- The package declares `"dsh": {"bundle": {"patch": "./cordis.patch.yml"}}`, plus peerDependencies on the dsh packages it imports.
- `dsh plugin --profile <name> add <spec>` runs pnpm in the profile directory. The spec can be a registry name, git, a tarball, or an absolute local path. It then appends the package to `dsh.profile.bundles`.
- Peer ranges are checked against the exact runtime version. Exemptions go in the profile's `compatibility.json`.
- Alternatively, any patch layer can `insert` a row whose `name` is a package, an absolute path, a file URL or a patch-relative path.

**The plugin I wrote:** `dsh-spike\plugins\optchat-zoom\` (`index.mjs`, `package.json` named `@optchat/dsh-zoom` with peer `@deepseek-ai/dsh-tools: 0.1.7-rc.2`, and a bundle `cordis.patch.yml` that inserts row `optchat-zoom`). The core:
```js
import { readFile } from 'node:fs/promises';
import { defineTool } from '@deepseek-ai/dsh-tools';
export const name = 'optchat-zoom';
export const inject = ['tools'];          // named exports only, no default export
export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'zoom',
    description: 'OptChat long-term memory. Expand one node of the conversation summary tree ...',
    parameters: { id: { type: 'string', required: true, description: 'Tree node id, e.g. "n148".' } },
    output: { schema: { type: 'string' }, render: (_a, v) => [{ type: 'text', text: v }] },
    isConcurrencySafe: () => true,
    async execute(args, exec) {
      // read C:/Users/abdou/apothicaire/optchat/run/data_v2/tree.jsonl (override: OPTCHAT_TREE),
      // return the children's JSON lines, 'leaf node (no children): <line>' or 'node not found'
    },
  }));
}
```
**Results, by loading method:**
1. **`--patch patches\zoom.yml` with `name: ../plugins/optchat-zoom/index.mjs`** (outside the profile): it fails, but the run goes on without the tool. stderr:
   ```
   dsh: warning: 1 entry did not activate
   optchat-zoom (file:///C:/Users/abdou/apothicaire/optchat/dsh-spike/plugins/optchat-zoom/index.mjs): failed to import
   ```
   Cause: the bare import `@deepseek-ai/dsh-tools` only resolves for files under `$DSH_HOME\profiles\` or linked into a profile.
2. **A copy at `home\profiles\headless\plugins\optchat-zoom\index.mjs`**, loaded by the overlay `patches\zoom-inprofile.yml` (absolute path): it loads. Bonsai used it in runs e, f and m.
3. **The official route:** `PATH=<spike>\tools\bin:$PATH dsh plugin --profile zoomtest add C:/Users/abdou/apothicaire/optchat/dsh-spike/plugins/optchat-zoom`. It took 1.5 s and:
   - added `"@optchat/dsh-zoom": "link:C:/Users/abdou/apothicaire/optchat/dsh-spike/plugins/optchat-zoom"` to the profile's `package.json`;
   - appended it to `dsh.profile.bundles`.
   The bundle row then loaded and the tool executed. I checked this against the mock; it is the same code as in the real-model runs.

**pnpm:** it is not installed on this machine. `tools\bin\pnpm.cmd` calls the Desktop app's `resources\runtime\pnpm\bin\pnpm.cjs` (11.7.0). Since `autoInstallPeers: false`, nothing was downloaded, though pnpm did print an "update available" notice (it pinged the npm registry).

**Security:** plugins run in-process with full Node rights, outside the workspace sandbox [D].

## 6. Hosting an OptChat memory backend - what it would take [D, estimates are mine]
- **Tools:** easy, as this spike shows. `read_message(n)` is the same pattern over `log.jsonl`.
- **Memory view:**
  - dsh builds each request from the session surface: `header.config` + `deriveMessages()` + `header.tools`. From the agent-loop README, the `agent/request` waterfall adjusts route and effort, not messages.
  - To change what the model sees, you replace part of the surface durably. That is exactly what a compaction backend does: in `dsh-compaction` you extend the base class, implement the auto, on-demand and explicit-range operations, and emit the checkpoint marker.
  - So OptChat = a custom compaction backend that replaces the old span with one `<memory>` digest message, plus the zoom/read_message tools.
  - Unlike Pi's `beforeRequest`, every view change is logged and replayed.
- **Mismatches to design around:**
  - Compaction runs inside `agent/pre-step`, so it blocks the turn. Precompute after `turn/end` and apply cheaply at the next pre-step.
  - One replacement message per span.
  - The summary must be smaller than the span it replaces.
  - The shared LLM service has no llama.cpp `id_slot` control. To keep summaries on slot 1, call the server directly.
  - Trim the prompt: the lean overlay, plus a non-coding persona via the `system-prompt` row.
- **Estimate:**
  - 2-4 days for a JS port of the tree/hysteresis logic as a dsh backend, or 1-2 days if it shells out to the existing `optchat.py` for tree maintenance;
  - plus about half a day of profile tuning.

## 7. Gotchas (detailed)
1. **Prompt overhead.**
   - Stock headless sends 24 tools plus an English coding-agent persona ("You are a coding agent powered by the bonsai model"): 5835 tokens. The tools are create_goal, edit, exit_plan_mode, get_goal, glob, grep, interrupt_agent, job_kill, job_list, job_output, list_agents, pwsh, read, read_image, send_message, skill, subagent, subagent_fork, todo_write, update_goal, web_fetch, web_search, workflow and write.
   - `patches\lean.yml` disables tool-subagent, tool-subagent-fork, tool-subagent-control, tool-subagent-list-agents, tool-workflow, tool-goal, tool-web, tool-jobs, tool-skill and plan-mode. That leaves 9 tools (edit, glob, grep, pwsh, read, read_image, todo_write, write, zoom): 2758 tokens [R].
2. **Compaction defaults suit very large context windows.** At 12k you must set `modelPolicies` (section 2) or nothing compacts. A summary never wins over a span below ~600 framed tokens, and truncated summaries are rejected.
3. **Thinking control** needs the reasoning-declaration trick (section 2).
4. **Plugin import resolution** (section 5), with a terse "failed to import" diagnostic.
5. **Headless mode:**
   - one process per prompt (~3.5 s overhead);
   - approval policy `ask` with no answerer means approvals fail closed [D];
   - `DSH_PERMISSION_MODE=danger-full-access` would remove the sandbox [D];
   - under `workspace-write`, writing files in the workspace and running pwsh both worked [R].
6. **Log size:** each new process writes the full tool schemas in `request/header`, and `assistant/message` stores per-chunk stream timings: 85 KB for 3 short turns.
7. **Base defaults point at DeepSeek services:**
   - the default model is deepseek-official/deepseek-flash;
   - web_search uses DEEPSEEK_API_KEY;
   - the OTel exporter has a DeepSeek URL.
   All of these can be overridden, and telemetry can be turned off with an env var.
8. **Version pinning:** this is 0.1.7-rc.2, and plugin peer ranges are pinned to the exact runtime version. Plugins will need re-checking or exemptions on every dsh upgrade.
9. **My own tooling quirk (not dsh):** double backslashes collapsed in heredocs written through my Bash tool. Use forward slashes in Windows paths inside JS/YAML written that way.

## 8. Files (all under C:\Users\abdou\apothicaire\optchat\dsh-spike)
- `home\`: the isolated DSH_HOME (`profiles\headless`, `profiles\zoomtest`, `sessions`, `storages`).
- `patches\`: `bonsai.yml`, `mock.yml`, `mock-full.yml`, `lean.yml`, `zoom.yml`, `zoom-inprofile.yml`, `compact-*.yml`.
- `plugins\optchat-zoom\`: the plugin package.
- `tools\`:
  - `run.sh`: timed headless runs;
  - `mock-openai.mjs`: the no-GPU mock server;
  - `bin\pnpm.cmd`: the pnpm shim;
  - `mock-log-*`: captured request bodies.
- `runs\`: per-run event streams, stderr and timings; `runs\mock\`; the config dumps.
- `workspace\`: the sample files, plus `notes.txt` written by the agent.
