# dsh integration notes for OptChat (research, 2026-10-07)

**Verdict**
1. **Feasibility: high.** Local route, compaction seam, tool plugin and third-party plugin loading were each exercised end-to-end against the live llama-server, in a scratch `DSH_HOME` (the real `~/.dsh` was not touched).
2. **Effort:** v1 about 1-2 days (lean preset + `BasicCompactionEngine` subclass overriding `summarize()` + `zoom` tool + tree sidecar file); a faithful OptChat (own trigger/hysteresis/transaction) about 3-5 days more.
3. **Risk 1 (blocking if ignored):** dsh's fixed prompt+tools envelope is 6012 input tokens for a one-word reply (headless) and about 7.5k on the Desktop `standard` preset, against a 12288 window. A lean preset (persona + zoom) is mandatory.
4. **Risk 2:** `compaction-basic` re-fires on every step while envelope+digest stays above its threshold (my low-threshold test made 48 checkpoints in one turn), so cadence/hysteresis must be your own policy; Bonsai thinking eats `maxTokens` unless disabled (recipe in 1.4); never append custom event types to the session log; a plugin outside the profile tree cannot import `@deepseek-ai/*`.
5. **Version trap:** the installed Desktop is 0.2.0-rc.2 (embeds dsh 0.2.0-rc.2); the npx cache is 0.1.7-rc.2. Files used here are byte-identical across the two (compaction, compaction-basic, tool-present). Declare peers `^0.1.7-rc.2 || ^0.2.0-rc.2`. Nothing was run on the Desktop itself.

Legend: **RUN** = executed here; **CODE** = read in source; **INFERRED** = not executed. Experiments used `DSH_HOME=<scratchpad>\dshhome`, `DSH_PERMISSION_MODE=read-only`, `DSH_TELEMETRY_DISABLED=1`, node 22.23 running `C:\Users\abdou\AppData\Local\npm-cache\_npx\1e7f6d9597241db0\node_modules\@deepseek-ai\dsh\lib\bin.js`. About 9 requests hit the shared llama-server (slot caches perturbed). `.credentials.yaml` was never opened.

## 1. Local OpenAI-compatible route (`@deepseek-ai/dsh-llm-pi-ai`)

**1.1 Where config lives (CODE + RUN `--dump-config`).** The format is a YAML patch list, not JSON.
- Desktop: `C:\Users\abdou\.dsh\profiles\desktop\cordis.patch.yml`. `npx @deepseek-ai/dsh web`: `C:\Users\abdou\.dsh\profiles\web\cordis.patch.yml`. Both profiles: `C:\Users\abdou\.dsh\cordis.patch.yml` (absent today; outranks the profile patch; an empty or comment-only file fails boot, use `[]`). CLI only: `--patch file.yml` (repeatable, applied last). `DSH_HOME` relocates everything.
- Order: bundle patches (`package.json` `dsh.profile.bundles`) -> profile patch -> home patch -> `--patch`. A patch entry `- id: X / name: <assertion> / config: {...}` REPLACES the row's whole `config`; `- insert: [rows]` adds rows; `!!js` expressions are allowed. Source: `dsh-app-boot/README.md#profiles`, `dsh-app-boot/lib/index.js` `applyEntryPatches`.
- The row already exists, dormant, in `@deepseek-ai/dsh-base/cordis.patch.yml`: `- id: llm-pi-ai / name: '@deepseek-ai/dsh-llm-pi-ai'`. The Models settings page writes the same place (`dsh-settings` persists through the profile patch).
- `dsh-hmr` is mounted by the base (`root: []`); headless/sdk/acp disable it, web/desktop keep it, so patch edits should apply live (2 s write-stability delay). INFERRED for the Desktop. Plugin code changes need a restart unless `hmr.config.root` lists the plugin dir.

**1.2 Working config (RUN: headless reply "OK", `inputTokens` 6012, `request/context.contextWindow` 12288).**
```yaml
- id: llm-pi-ai
  name: '@deepseek-ai/dsh-llm-pi-ai'
  config:
    providers:
      llama-local:                      # route key; not a pi-ai catalog id
        displayName: Bonsai 27B (llama.cpp)
        api: openai-completions         # also openai-responses, anthropic-messages
        baseURL: http://127.0.0.1:18435/v1
        headers: { Authorization: Bearer none }     # keyless server, see 1.3
        compat: { supportsStore: false, supportsDeveloperRole: false, maxTokensField: max_tokens, thinkingFormat: qwen-chat-template }
        models:
          - id: bonsai                  # llama-server ignores it; /v1/models lists the GGUF path
            name: Bonsai 27B ternary
            contextWindow: 12288
            maxTokens: 1536             # becomes request/header.config.maxTokens
            input: [text]
            reasoningEfforts: { off: , high: high }   # empty `off:` = supported, send nothing
- id: agent-default-model
  name: '@deepseek-ai/dsh-agent-default-model'
  config: { provider: llama-local, model: bonsai }    # no reasoningEffort => thinking off
```
Other profile fields (`dsh-llm-pi-ai/lib/types/config.d.ts`): `apiKeyEnv, displayName, api, baseURL, models[{id,name,contextWindow,maxTokens,input,reasoningEfforts,compat}], modelOverrides, compat, defaultContextWindow (262144), defaultMaxTokens (32768), defaultInput, headers, reasoning, retryPolicy, timeoutMs, streamIdleTimeoutMs (300000)`. `GenerateOptions.stop` is rejected (`UNSUPPORTED_OPTION`).

**1.3 Credentials with no key (CODE + RUN).**
- `apiKeyEnv` is a credential reference (`/^[A-Za-z_][A-Za-z0-9_]*$/`) resolved per request by `dsh-credentials-local`: launch environment > `~/.dsh/.credentials.yaml` `refs:` > `<cwd>/.env` > `~/.dsh/.env`. Unresolved -> `MISSING_CREDENTIAL`. Omitted -> "keyless".
- Keyless is not enough: pi-ai `dist/api/openai-completions.js getClientApiKey()` throws `No API key for provider` unless an apiKey or an `authorization` header exists. dsh forwards profile `headers` on every request, so `headers.Authorization` works with no secret store (RUN).
- Alternative (INFERRED, not run): `apiKeyEnv: LLAMA_LOCAL_KEY` plus `LLAMA_LOCAL_KEY=none` in `C:\Users\abdou\.dsh\.env`.

**1.4 Thinking (RUN).** `reasoningEfforts: false` is not enough: Bonsai still returns reasoning, and the compactor (`maxTokens` 450) died with `compaction/end.error = "summarization truncated at the token cap (incomplete checkpoint)"`. The `off/high` + `thinkingFormat: qwen-chat-template` recipe makes pi-ai send `chat_template_kwargs {enable_thinking: !!reasoningEffort}`: no reasoning block, 2 output tokens, and compaction then succeeded. These pi-ai branches only fire for a model declared reasoning-capable (`openai-completions.js` ~line 654).

**1.5 Envelope numbers.** Headless: system ~744 tok + 24 tool schemas ~4.9k tok (first request 6012 input tokens). Desktop `standard` (sizes only, from an existing real log): system 5965 chars + 28 tools 24172 chars, about 7.5k tok. Server `/props`: `n_ctx` 12288 per slot, 2 slots, chat template supports tools.

**1.6 Observed cross-client bleed (RUN, cause INFERRED).** In 2 of my 3 agentic runs the model's reasoning quoted text that is not in dsh's request: "[#22] En une phrase, c'est quoi un cache KV ?" (present in `optchat\data\log.jsonl`, absent from my session log). Likely slot/prompt-cache reuse on the shared server (`--cache-reuse 256`, PrismML build). Use a separate llama-server port for dsh, or retest with the prototype stopped.

## 2. Compaction backend contract (`@deepseek-ai/dsh-compaction`)

**2.1 Contract (CODE, `lib/types/index.d.ts`).** `abstract class CompactionEngine extends Service` (`super(ctx, 'compaction')`, exposed as `ctx.compaction`, one per context).
```ts
abstract compactIfNeeded(agent: CompactionAgentContext, trigger: 'pressure'|'context-overflow', signal: AbortSignal): Promise<CompactionResult|null>
abstract compactNow(agent: ManualCompactAgentContext, signal: AbortSignal, sourceCommandId?: CommandId): Promise<CompactionResult|null>
abstract compactRegion(start: SessionSeq, end: SessionSeq, agent: CompactionAgentContext, signal?: AbortSignal): Promise<CompactionResult>
```
- Input: no message list. `CompactionAgentContext = { session: Session, options: {provider?, model?} }`; `ManualCompactAgentContext` adds `runMaintenance(task)`. The backend reads the `Session` (`surface.nodes`, `eventAt`, `deriveEventMessage`, `requestHeader()`, `id`, `append`) and may use `ctx.tokenMeter`, `ctx.llm`, `ctx.sessions.flush`.
- Return: `CompactionResult { compactionId, startSeq, summarySeq, endSeq, summary: ContentBlock[], shadowedRange, shadowedSeqs, shadowedTokenCount, sourceCommandId? }`, or `null` (nothing safe to compact). Manual failures throw `ManualCompactionError(code: busy|cancelled|changed|summary|commit|persistence)`.
- Marker: the replacement message's `source = compactCheckpointSource(compactionId, sourceCommandId?)` = `{kind:'compact-checkpoint', compactionId}`; test with `isCompactCheckpointSource`. Other packages (session-reference, token-meter) key on it.
- Also exported: `toolPairingBalancedBefore/After(session, seq)`; waterfall event `compaction/summary-error` for retry hooks.

**2.2 What the shipped backend writes (RUN, real events produced with Bonsai).**
```
17 compaction/start   {compactionId, turn}
18 compaction/summary {compactionId, summary:[text], rawOutput, llmStreamCall:true, shadowedRange:{start:8,end:8}, shadowedSeqs:[8],
                       shadowedTokenCount:1387, provider, model, maxTokens, usage}
19 user/message       data:{role:'user', id:<uuid>, source:{kind:'compact-checkpoint', compactionId},
                       content:[text(preamble + "<compacted-summary>"), text(summary), text("</compacted-summary>")]}
                      surfaceOp:{op:'replace', startSeq:8, endSeq:8}, sourceEventSeqs:[17,18,8]
20 compaction/end     {compactionId, turn}      (failure: this event carries `error`, and 18/19 are absent)
```
Code: `dsh-compaction-basic/lib/index.js` `compactSurfaceRegion` (the lock is an unmatched `compaction/start`; append start; summarize; revalidate; append summary then the replacement synchronously; append end). The next request gets a new `request/header` with `reason: series`.

**2.3 How basic works (CODE).** `BasicCompactionEngine extends CompactionEngine`, `static inject = ['llm','tokenMeter','sessions']`. Triggers: `ctx.on('agent/pre-step')` -> `compactIfNeeded(agent,'pressure')`, and `agent/request-error` on `CONTEXT_WINDOW_EXCEEDED`. Range = first non-system surface node up to the tail kept by `retainTokens`, never splitting a tool call/result pair. Summarizer `summarizeWithLlm`: `ctx.llm.stream({provider, model, messages:[system head, ...shadowed messages, user: COMPACTION_INSTRUCTION], tools, toolHistory, maxTokens, sessionId, purpose:'compaction'})`; keeps only text blocks; fixed 8-section Markdown prompt ("Primary Request and Intent" ... "Critical Context"; merges a prior `<compacted-summary>`); framed by a fixed preamble + tags (`frameSummary`, not overridable). `summarize(input, agent, signal)` is the sole subclass hook. It rejects a summary not smaller than the shadowed span ("summary is not smaller than the shadowed content"). Pressure trigger = `floor(min(W*thresholdRatio, W - reservedOutput - headroomTokens))`; the default `headroomTokens` 65536 is impossible at W=12288 (plugin warns once and skips proactive compaction). `retainTokens` and `retainRatio` are mutually exclusive.

**2.4 Can a backend keep one multi-line digest updated every turn? Yes (RUN), with costs.**
- RUN: `class OptChatEngineProbe extends BasicCompactionEngine { async summarize(input, agent, signal) { return { summary: [{ type: 'text', text: '<memory>\n[L0-0] user: ...\n</memory>' }], provider: 'optchat', model: 'digest-probe' } } }`, loaded from a linked package. The digest landed inside the checkpoint (`<memory>` between the preamble and `</compacted-summary>`) and `compaction/summary` recorded `provider: optchat` with no `llmStreamCall`. 48 successive replace cycles ran, each replacing [previous digest + newly aged nodes]; the old digest arrives in the replayed `input.messages`.
- Costs: every replace invalidates the KV prefix from the digest position and starts a new header series; the span must be contiguous, tool-pair balanced and start after node 0; the automatic path only works inside an open turn; the shrink check can fail on tiny spans (that failure leaves `compaction/start` + `compaction/end{error}`).
- Loop trap (RUN): my threshold (0.3 x 12288 = 3686) was below the envelope, so basic compacted on every step until the 330 s timeout (exit 124). Set the threshold above envelope + digest, or write your own trigger.
- No request-time rewrite exists: the `agent/request` waterfall "cannot mutate messages" (CODE). Do not put the digest in the system prompt: pi-ai routes have no `systemPromptUpdate: 'in-history'` (RUN: absent from `request/context`), so a prompt change rewrites node 0 and the whole prefix.
- Background compaction like the prototype (INFERRED, untested): on `agent/status === 'idle'` call `compactNow()`; it runs under `agent.runMaintenance` and later prompts queue FIFO until it settles.

**2.5 Config-only baseline (RUN, produced a real checkpoint; values were test values).** Headless/sdk host row:
```yaml
- id: compaction-basic
  name: '@deepseek-ai/dsh-compaction-basic'
  config: { thresholdRatio: 0.3, headroomTokens: 256, retainTokens: 100, summarizationProvider: llama-local, summarizationModel: bonsai, maxTokens: 700, compactionRetries: 0 }
```

**2.6 Web/Desktop wiring (CODE; the preset YAML below is INFERRED, not run).** `dsh-web-app` disables the host rows `compaction-basic`, `command-compact`, `tool-result-pruner`, `tool-todo` and mounts them inside agent presets (`presets/standard.patch.yml`: a `compaction` group with `isolate: {compaction: true, toolResultPruner: true}`). The session header records `agentPreset`. Define a new preset in the profile patch (modelled on `presets/minimal.patch.yml`):
```yaml
- insert:
    - id: preset-optchat
      name: '@deepseek-ai/dsh-agent-preset'
      config:
        id: optchat
        order: 5
        plugins:
          - { id: persona, name: '@deepseek-ai/dsh-persona', config: { prefix: '<prompt incl. zoom directive>', complete: true, includeRuntimeContext: false } }
          - id: compaction
            name: cordis:group
            group: true
            isolate: { compaction: true }
            config:
              - { id: optchat-compaction, name: optchat-dsh/engine }
              - { id: command-compact, name: '@deepseek-ai/dsh-command-compact' }
          - { id: optchat-zoom, name: optchat-dsh/zoom }
- { id: agent-preset-registry, name: '@deepseek-ai/dsh-agent-preset-registry', config: { default: optchat } }
```
`persona.complete: true` makes the prefix the entire system prompt (extra `systemPrompt.section()` calls are dropped), so put the zoom directive in the prefix and in the tool description.

## 3. Registering a tool

**3.1 Code (CODE: `dsh-tool-present/lib/index.js`, 4.2 KB; RUN with a probe plugin).** A plugin module exports `name`, `inject`, `Config` (schemastery) and `apply(ctx, config)`; the registry is `ctx.tools` (`@deepseek-ai/dsh-tools`). Smallest first-party packages: `dsh-tool-ask-user` and `dsh-tool-subagent-control` (3.3 KB), `dsh-tool-present`, `dsh-tool-todo` (appends `exec.agent.session.append('todo/write', ...)`).
```js
import z from '@deepseek-ai/schemastery'
import { defineTool } from '@deepseek-ai/dsh-tools'
export const name = 'optchat-zoom'
export const inject = ['tools']                    // add 'sessionQuery' to read originals
export const Config = z.object({ treeDir: z.string().default('') })
export function apply(ctx, config) {
  ctx.tools.register(defineTool({                  // returns a disposer
    name: 'zoom',
    description: 'Open a digest line by id ...',
    parameters: { id: { type: 'string', required: true, description: 'Line id, e.g. L2-14' } },
    output: { schema: { type: 'string' }, render: (_args, value) => [{ type: 'text', text: value }] },
    async execute(args, exec) { /* exec.agent.session.id, exec.signal, exec.callId */ return 'text for the model' },
  }))
}
```
**3.2 Schema DSL and results (CODE + RUN).** `parameters` is a property map with inline `required: true` (types string, number, integer, boolean, null, array, object, oneOf). The model receives standard JSON Schema: `{"name":"zoom_probe","description":"...","parameters":{"type":"object","properties":{"id":{"type":"string","description":"..."}},"required":["id"]}}`. `execute` returns a JSON value validated against `output.schema`; `render(args, value)` produces the `ContentBlock[]` the model sees. A throw becomes an error result and the turn continues. `exec` also offers `deferContext(msg)` and `concludeTurn()`; `timeoutMs` and `isConcurrencySafe` are optional.
RUN events: `16 tool/call {turn, step, callId, name:'zoom_probe', arguments:'{"id":"L0-7"}'}`, then `17 tool/result` with `sourceEventSeqs:[16]`, `surfaceOp:'append'`, `message.content:[{type:'text', text:'zoom_probe:L0-7:linked:agent=yes'}]`, `isError:false`. Bonsai called the tool correctly.

**3.3 Scope (CODE).** A bundle row registers on the host `ctx.tools` (global, every preset). A row inside `preset.plugins` registers in that agent scope only. Real third-party example: `profiles\desktop\node_modules\dsh-hindsight\lib\index.js` (`ctx.tools.register(defineTool(...))`, `ctx.systemPrompt.section(...)`). To read original messages use `ctx.sessionQuery.readEvent({sessionId, seq, before?, after?})` (returns `SessionEventWindow.target`); `session.eventAt()` is documented as deprecated for new code.

## 4. Session logs (CODE + RUN on structure only; no message text was read)

- Location: `C:\Users\abdou\.dsh\sessions\--<normalized-cwd>--\session-<uuid>\session.v4.jsonl.zstd` (`session-persistence-jsonl` row, `root: dshHomePath('sessions')`; format version 4 in both runtimes). Desktop and `dsh web` share this root. `compression: 'none'` exists but needs a separate root.
- Encoding: concatenated checksummed zstd frames (frame 1 = header only, then one frame per append batch). Node's `zlib.zstdDecompressSync` decodes only the first frame (RUN: it returned 210 bytes of a 55 KB file); scan frames first (see `scanZstdFrames` in `dsh-session-persistence-jsonl/lib/index.js`), then decode each. My reader: `<scratchpad>\zread.mjs`.
- Header row: `{type:'session', version:4, id:'session-<uuid>', createdAt, cwd, isSeeded, delegationDepth, agentPreset}`. Event row: `{type, seq, time, data, surfaceOp?, sourceEventSeqs?, ignorable?}`.
- IDs for the tree: `seq` is a dense per-session integer, stable and never reused (shadowed events stay in the log); message ids are UUIDs at `data.id` (`user/message`) or `data.message.id` (assistant, tool result, system); tools: `callId` on `tool/call`, `toolCallId` on the result message; checkpoints: `data.source.compactionId`. Reference nodes as `{sessionId, seq}`; key the sidecar `tree.jsonl` by `sessionId` + `compactionId` (forks copy the event prefix, compaction events included).
- Event types seen: `turn/start|end`, `step/start|end`, `system/message`, `user/message` (also synthetic `runtime-context`), `assistant/message` (embeds `usage` and the stream), `tool/call`, `tool/result`, `request/header|context`, `compaction/*`, `session/title`, plus runtime events.
- Do not append custom event types: `dsh-session-persistence-jsonl/lib/worker.cjs:6600` refuses to read a log containing an unknown type that lacks `ignorable: true`, and `Session.append()` has no way to set `ignorable` (CODE, not run). Keep the tree outside the log and only emit the official `compaction/*` events.
- Privacy aside (CODE): the default-on `session-log-deepseek` upload rides only requests to the official DeepSeek API routes, not pi-ai routes; `session-telemetry-otel` is feedback-only by default.

## 5. Loading a third-party plugin (RUN unless noted)

| Case | Result |
|---|---|
| `name: C:\...\plug\index.js` in a patch `insert`, file outside the profile | path converted to `file:///C:/...` (`anchorInsertedPluginNames`, visible in `--dump-config`), but the import fails: `ERR_MODULE_NOT_FOUND @deepseek-ai/schemastery` |
| same file placed under `profiles\<p>\` | loads |
| junction `profiles\<p>\node_modules\<pkg>` -> external dir (what `pnpm add link:` creates), no `peerDependencies` | import fails |
| same, with `peerDependencies` on the `@deepseek-ai/*` packages it imports | loads; imports resolve to the runtime copies |
| peer range not matching the runtime (dsh-tools 9.9.9) | row disabled: "Plugin ... is incompatible with dsh 0.1.7-rc.2" (exemption: `dsh plugin allow-version`) |

- Mechanism (CODE): runtime resolution intercepts only modules under the profiles tree or under symlinked roots in the active profile's `node_modules`, and routes the names listed in that module's `package.json` `peerDependencies` to the installed runtime (`dsh-app-boot/lib/worker/profile-resolution-bootstrap.js`). Never ship a private copy of `@deepseek-ai/*`.
- Bundle manifest (CODE, same as the installed `dsh-hindsight`): `package.json` has `"dsh": {"bundle": {"patch": "./cordis.patch.yml"}}`; the patch is `- insert: [ {id, name: <pkg>, config} ]`. The profile lists the package in `package.json` `dependencies` and `dsh.profile.bundles` (see `profiles\desktop\package.json`: dshmarket, dsh-mnemon, dsh-free-search, dsh-hindsight). A row `name` may be a package name, absolute path, `file:` URL, or a subpath export.
- Install (CODE): `dsh plugin --profile <name> add <spec>` forwards to pnpm in the profile dir. Specs: registry name, absolute path (plain, `file:` or `link:`; relative paths are rejected), git, tarball. Use `link:C:\Users\abdou\apothicaire\optchat\dsh` so edits are live. The CLI refuses `--profile desktop` ("managed exclusively by the Electron application"), so for the Desktop edit `profiles\desktop\package.json` and its patch by hand, or use the in-app Plugins page (INFERRED, not tried). A package without `dsh.bundle` is refused ("not-a-bundle").
- Module shape (CODE): either named exports `name/inject/Config/apply` (tool-present) or a default-exported class extending `Service`/`CompactionEngine` with `static inject`/`static Config` (compaction-basic). A subclass inherits both statics (RUN: worked).
- Dev loop (CODE, not run): `npx @deepseek-ai/dsh web --patch C:\...\optchat.patch.yml`; module hot reload via `- id: hmr / disabled: false / config: { root: ["C:\\Users\\abdou\\optchat\\dsh"] }`.

## Suggested build order
1. Package `C:\Users\abdou\apothicaire\optchat\dsh\`: `package.json` (peers `^0.1.7-rc.2 || ^0.2.0-rc.2` on cordis, schemastery, dsh-tools, dsh-compaction, dsh-compaction-basic; `dsh.bundle.patch`), `engine.js`, `zoom.js`, `cordis.patch.yml`.
2. Add the route from 1.2; verify with a scratch `DSH_HOME` and `dsh --profile headless` first, then the Desktop.
3. Lean preset (2.6) + subclass engine with a threshold above envelope + digest; digest tree in a sidecar keyed by `{sessionId, compactionId}`, leaves pointing at `seq`.
4. `zoom` reads the sidecar and `ctx.sessionQuery.readEvent` for leaves. Re-test on the Desktop (0.2.0-rc.2).
