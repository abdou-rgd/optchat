# Pi Durable as a host for OptChat memory - research note (2026-10-07)

## Verdict
1. **Can it host OptChat? Yes.** The hook you need exists, is in the normative spec and is unit-tested: `hook(GenerationTask, { beforeRequest })` receives the whole model context as `{ messages }` and may return a replacement list used for that one request only. It runs before every model request (later requests of a tool round, retries and crash recovery included). [V]
2. The other pieces are public API too: `defineTool({ replay: "safe" })` for zoom/read_message, `defineTask` + `background: true` for the compactor (create with `conversation.commit`, join with `harness.waitForTask`), JSONL storage, and local llama.cpp via `createProvider()` + `openAICompletionsApi()`. There is NO `openaiProvider({ baseURL })`: that factory takes no arguments and speaks the Responses API. [V]
3. Must-dos: `settings.compaction.enabled = false`; keep every `system` message when rewriting (they carry prompt sections AND tool schemas); cut the raw tail on a user-turn boundary; give the provider a dummy apiKey plus compat flags (`supportsDeveloperRole:false`, `maxTokensField:"max_tokens"`, `supportsStore:false`). [V/I]
4. Risks: the package README says "Experimental. The API changes without notice between releases" (npm 1.0.4, 2026-10-05; breaking changes already queued under Unreleased); TypeScript, Node >= 22.19 only, OptChat is Python so it is a port; I executed nothing (no npm install), so Windows and llama.cpp behaviour is read from source, not run-tested.
5. Effort (my estimate): spike (provider + `beforeRequest` view fed from your existing tree.jsonl + zoom/read_message + JSONL) 0.5-1 day; full port (tree/hysteresis compactor as background task, streaming REPL, bench parity) 2-4 days. Worth it only if you want the harness itself (durable tool loop, resume, multi-client); the memory algorithm gains nothing from it.

Legend: **[V]** verified by reading source/docs/tests; **[I]** inferred or not run. Paths below are under `https://github.com/earendil-works/pi/blob/a2eef9eb6/packages/` (main on 2026-10-07 20:41Z; `#L` = line). Blog (paraphrased): https://earendil.com/posts/pi-durable/ . Durable README: `durable/README.md`; normative spec: `durable/docs/spec.md`. Short code excerpts are from the MIT-licensed repo.

## 1. Rewriting the message list per request
**[V] API** (`durable/src/harness/types.ts#L629-L636`, identical in the published 1.0.4 `.d.ts`):
```ts
export interface GenerationHooks {
	/** Before every request attempt, including recovery; the result is used for that request only. */
	beforeRequest(request: { readonly messages: readonly Message[] }, api: HookApi, context: Context,
	): HookResult<{ readonly messages: readonly Message[] }>;
```
**[V] How it is applied** (`durable/src/harness/generation.ts#L195-L207`; `streamResponse` L402 then sends `{ messages: [...messages] }`):
```ts
const view = await runtime.context(conversationId, context, { at: cutoff });
let messages = view.messages;
await runtime.hooks.each("beforeRequest", async (hook) => {
	const replaced = await hook({ messages }, runtime, context);
	if (replaced !== undefined) messages = replaced.messages;
});
```
- **What the hook sees:** the committed context through the request cutoff. System prompt and tool schemas are NOT separate fields: they are `role:"system"` messages (`sections`, `toolsAdded`) in the same array (`ai/src/types.ts#L518-L544`, `durable/src/harness/prompt.ts`). Messages have a `timestamp` but no entry id. `api` is `HookApi`: `taskId`, `conversationId`, `memo()`, `snapshot()/snapshotAsOf()` (committed docs). `api.models` exists only on main (Unreleased), not in 1.0.4.
- **Per request, not persisted:** test "replaces request messages ..." asserts the injected message "was used for the request only" and never reaches the transcript (`durable/test/harness-tools.test.ts#L673-L702`). Spec: the `beforeRequest` chain "may replace the messages for this request only", recovery "reruns `beforeRequest`" (`spec.md#L3528-L3531`).
- **Chain:** hooks of all selected extensions run in extension order, each sees the previous replacement; an ordinary throw is reported via `onReport` and skipped (`spec.md#L2578-L2590`, `durable/src/harness/scheduler.ts#L1131-L1143`).
- **Tools are unaffected:** a call is accepted against the tool set of the committed context; "`beforeRequest` replacements do not change it" (`spec.md#L2932-L2934`). Dropping tool declarations only hides them from the model.
- **Built-in compaction ignores your rewrite:** thresholds are computed on the stored context (`generation.ts#L139-L155`, `compaction.ts#L307-L322`; it starts from the last assistant `usage`, so it may stay quiet, but do not rely on it). Set `settings: { compaction: { enabled: false } }` (`durable/README.md#L351-L362`); manual `compact()` still works.
- **Alternative [V]:** keep the harness mechanism and only supply the text: `hook(CompactionTask, { beforeCompact })` may return `{ summary }`, placed as a `pi.compaction` entry; trigger it yourself with `root.compact()` (`compaction.ts#L128-L133`). Token-based cut (`keepRecentTokens`) and ONE summary user message: weaker fit for the tree/hysteresis view.

Sketch **[I, not compiled]** of the OptChat view (`[system + <memory>] + raw tail`):
```ts
import { defineExtension, GenerationTask, hook } from "@earendil-works/pi-durable";
import type { SystemMessage } from "@earendil-works/pi-ai";
export const OptChatMemory = defineExtension({ name: "optchat-memory", hooks: [hook(GenerationTask, {
	beforeRequest: async ({ messages }, api, context) => {
		const system = messages.filter((m): m is SystemMessage => m.role === "system"); // keep: prompt + tool schemas
		const rest = messages.filter((m) => m.role !== "system");
		const { text, coveredTs } = await loadDigest(api, context);  // own tree.jsonl, or a defineDoc via api.snapshot(...)
		let from = rest.findIndex((m) => m.timestamp > coveredTs);   // raw tail = everything the digest does not cover
		if (from < 0) from = rest.length - 1;
		while (from > 0 && rest[from]!.role !== "user") from--;       // never start on assistant/toolResult
		const memory: SystemMessage = { role: "system", content: "", timestamp: Date.now(),
			sections: { memory: `<memory>\n${text}\n</memory>` } };
		return { messages: [...system, memory, ...rest.slice(from)] };
	} })] });
```
- Why a `system` message with `sections`: for llama.cpp the compat default `supportsMidConvoSystemMessages:false` makes pi-ai collapse ALL system messages into one leading prompt (`ai/src/utils/transcript.ts#L104-L120`, used at `ai/src/api/openai-completions.ts#L310`), so the digest lands inside the system prompt as in today's optchat.py.
- Cut rules: pi-ai adds synthetic "No result provided" results for orphan tool CALLS but passes orphan tool RESULTS through (`ai/src/api/transform-messages.ts#L158-L234`), so never start the tail on a `toolResult`; the tail must include the whole current run (assistant toolCall + results) or the model loses its in-flight work. Chat templates that demand strict user/assistant alternation may reject two consecutive user messages [I].
- Test without the GPU: `fauxProvider()` (`@earendil-works/pi-ai/providers/faux`) scripts replies and receives `request.messages` (same test file).

## 2. Registering a custom tool
**[V]** `durable/src/harness/types.ts#L143-L154,L212-L236` (+ `defineTool`/`defineExtension` in `harness/define.ts`):
```ts
type ToolRegistration<P extends TSchema, D> = Tool<P> /* name, description, parameters (TypeBox) */ & {
	readonly replay?: "safe" | "unsafe";          // default unsafe
	readonly executionMode?: "parallel" | "sequential";
	readonly outputLimits?: { maxBytes?; maxLines?; retain?: "head" | "tail" };   // default 50 KB / 2000 lines
	execute(args: Static<P>, api: ToolExecutionApi<D>, context: Context): Promise<ToolExecutionResult<D>>;
};  // ToolExecutionResult = { content?: (TextContent|ImageContent)[]; isError?; details?; diagnostics?; usage?; control? }
```
```ts
const zoom = defineTool({ name: "zoom", description: "Open a memory line (id like n42) into its children",
	parameters: Type.Object({ id: Type.String() }),   // Type is re-exported by @earendil-works/pi-ai
	replay: "safe",                                     // read-only
	execute: async (args, api, context) => ({ content: [{ type: "text", text: await tree.zoom(args.id) }] }) });
registry.install(defineExtension({ name: "optchat-tools", tools: [zoom, readMessage] }));
```
- **Results:** return `content`, or stream with `api.output(text)` and return `{}` (retained output becomes the content). A throw becomes an error result (`isError`, diagnostic `tool_error`) and the task ends `failed` (`durable/src/harness/tool.ts#L264-L274`). `control: { terminate: true }` ends the run without another model call when every result of the round asks for it; `control: { handoff }` = reset with a note.
- **`replay: "safe"` [V]** (`tool.ts#L85-L111`): final args + policy are committed as "intent" BEFORE `execute()`. After a crash `execute` reruns only if the stored policy AND the currently installed tool are both `safe`; otherwise the model receives an `interrupted` error result ("... was interrupted and may have partially run"). zoom/read_message are pure reads, so `safe`.
- Tools also get `api.commit(tx => ...)`, `api.createTask`, `api.waitForTask`, `api.snapshot`, `api.conversation(id)`, `api.env` (undefined unless `env` is passed to `Harness.open`; custom tools need none).

## 3. Background task after each turn
- **No per-turn hook can commit** (`HookApi` is read-only + memos), but a public, documented mechanism exists (blog "Tasks"; `durable/README.md#L450-L486`; working example `coding-agent/src/experimental/vacation/vacation.ts#L60-L127`): `defineTask`, listed in an extension's `tasks: [...]`, created inside a commit with `{ ownership: { kind: "conversation" }, background: true }`. Background = belongs to the conversation but not to its current work: the conversation goes idle while it runs, Esc/`abort()` leaves it alone, `abort(ctx, { background: true })` stops it. Phases are checkpointed, so it resumes after a crash.
```ts
// DigestDoc = defineDoc<{ text: string; coveredTs: number }>({ kind: "app.digest", version: 1, scope: "conversation", history: "latest", fork: "current", initial: () => ({ text: "", coveredTs: 0 }) })
const Compact = defineTask<{ upTo: number }, { phase: "run" }, null>({ name: "optchat.compact", version: 1,
	initial: () => ({ phase: "run" }),
	phases: { run: async (task, runtime, context) => {
		const digest = await buildDigest(task.input.upTo, runtime);    // e.g. runtime.models.completeSimple(compactor, { messages }, opts)
		await runtime.commit(async (tx) => { (await tx.doc(DigestDoc, runtime.conversationId)).text = digest;
			return { status: "terminal", outcome: { status: "completed", result: null } }; }, context);
	} },
	abort: (_t, rt, ctx) => rt.commit(() => ({ status: "terminal", outcome: { status: "aborted" } }), ctx) });
// extension: defineExtension({ name: "optchat-compact", tasks: [Compact] })
const settled = await submission.wait(context);                         // after each answered turn:
const id = await root.commit((tx) => tx.createTask(Compact, { upTo }, { ownership: { kind: "conversation" }, background: true }), context);
await harness.waitForTask(id, context);                                 // "join before next turn" (optchat.py thread.join)
```
- **Where to trigger "after each turn" [V/I]:** (a) host code after `submission.wait()` (simplest); (b) from a tool via `api.createTask`; (c) from `afterTools`/`onYield` using a captured `harness.commit(...)` - a test does this from a `beforeRequest` hook (`durable/test/harness-structured.test.ts#L1143-L1147`) although typed `HookApi` does not expose it; (d) `harness.subscribeCommits()` for passive observation (per its doc the listener must not throw, block or call Session APIs, so defer the work). `Conversation.waitForIdle()` ignores background tasks, hence `harness.waitForTask(id)`.
- **Constraint [V]:** a background task must not `appendEntry` into a busy conversation: built-in compaction places its summary through a write submission "at once when idle, otherwise at the next boundary" (`compaction.ts#L402-L436`, REMINDER L405). Keep the digest in a `defineDoc` (the hook reads it via `api.snapshot`) or use `conversation.submit({ type: "write", entry })`.
- Built-in compaction is the template to copy: conversation-owned, `background` unless manual (`compaction.ts#L234-L247`), summarises with `runtime.models.completeSimple(model, { messages }, options)` (L174). `runtime.models` exists in 1.0.4; `HookApi.models` / `ToolExecutionApi.models` do not yet.

## 4. pi-ai -> local llama.cpp (http://127.0.0.1:18435/v1, model "bonsai", no key)
**[V]** `openaiProvider()` (`ai/src/providers/openai.ts`) has no parameters: fixed `https://api.openai.com/v1`, Responses API, `OPENAI_API_KEY`. Local servers use `createProvider()` (`ai/README.md#L1220-L1332`; there is no built-in llama.cpp/Ollama chat provider):
```ts
import { createModels, createProvider, type Model } from "@earendil-works/pi-ai";
import { openAICompletionsApi } from "@earendil-works/pi-ai/api/openai-completions.lazy";
const bonsai: Model<"openai-completions"> = { id: "bonsai", name: "Ternary Bonsai 27B", api: "openai-completions",
	provider: "llamacpp", baseUrl: "http://127.0.0.1:18435/v1", reasoning: false, input: ["text"],
	cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
	contextWindow: 12288,  // the PER-SLOT n_ctx you actually run [I]
	maxTokens: 1200,
	compat: { supportsDeveloperRole: false, supportsReasoningEffort: false, supportsStore: false, maxTokensField: "max_tokens" },
	samplingParams: { temperature: 0.3, cache_prompt: true, id_slot: 0, chat_template_kwargs: { enable_thinking: false } } };
	// samplingParams = free-form Record<string,unknown>, Object.assign-ed into the request body (openai-completions.ts#L1003-L1007)
const llamacpp = createProvider({ id: "llamacpp", name: "llama.cpp", baseUrl: "http://127.0.0.1:18435/v1",
	auth: { apiKey: { name: "llama.cpp", resolve: async () => ({ auth: { apiKey: "local" } }) } },   // dummy key, see below
	models: [bonsai], api: openAICompletionsApi() });
const models = createModels(); models.setProvider(llamacpp);   // Harness.open(storage, { models, registry, settings }, ctx)
// root conversation agent: { model: { provider: "llamacpp", modelId: "bonsai" } }
```
- **Dummy key is needed [V]:** the README example resolves `{ auth: {} }`, but `ai/src/api/openai-completions.ts#L87-L91` throws "No API key for provider" when there is neither `apiKey` nor an Authorization header, and nothing injects a placeholder (`ai/src/models.ts#L864-L872`, `auth/resolve.ts`). pi-ai's llama-cpp-classify test passes `apiKey: "local"`; your README notes the same for dsh.
- **Compat [V]:** for an unknown host `detectCompat` assumes OpenAI (`developer` role for `reasoning:true` models, `store:false`, `max_completion_tokens`, `stream_options.include_usage`) (`openai-completions.ts#L1593-L1690`, `buildParams` L802-L871). llama.cpp's documented limit parameter is `max_tokens`, hence the override [I]. optchat.py already sends `cache_prompt`, `id_slot`, `chat_template_kwargs` to `/v1/chat/completions`, so the server takes them; pi-ai sends none of them by itself (a `reasoning:false` model gets no thinking switch), hence `samplingParams`. For per-request routing use two `Model`s with different `samplingParams.id_slot` (chat vs compactor), or wrap `api` and set `onPayload` (`ai/README.md#L1287-L1304`, `ai/src/types.ts#L159`).
- **Output cap [V]:** pi-ai sends `min(model.maxTokens, contextWindow - estimatedPrompt - 4096)`, floor 1 (`ai/src/api/simple-options.ts#L15-L22`): with a 12k window keep the view well under ~7k tokens or answers shrink to a few tokens.
- **Tool calling [V client, I model]:** tools go out as `{type:"function", function:{name, description, parameters}}` (`openai-completions.ts#L1482-L1517`), streamed `delta.tool_calls` are assembled incrementally (L640-L668), llama.cpp `reasoning_content` becomes thinking blocks (L607-L638), `finish_reason` is mandatory (L701-L703). Server side: llama.cpp docs say OpenAI-style function calling "is supported with the `--jinja` flag" (default-on in current master; may need `--chat-template-file`). optchat.py already sends the same `tools` format to this server, so Bonsai's template copes; BUT pi-ai always streams (`stream:true`, `buildParams` L822-L826) while optchat.py does not, so streamed `tool_calls` from the PrismML fork are untested [I] - curl that first.

## 5. Storage (JSONL)
**[V]** `durable/README.md#L536-L546`; `durable/src/storage/jsonl/node.ts`:
```ts
import { openNodeJsonlStorage } from "@earendil-works/pi-durable/storage/jsonl/node";
const storage = await openNodeJsonlStorage("C:/Users/abdou/apothicaire/optchat/data/pi", context, { fsync: true }); // fsync default false
const harness = await Harness.open(storage, { models, registry, settings: { compaction: { enabled: false } } }, context);
const root = await harness.root(context, { agent: { model: { provider: "llamacpp", modelId: "bonsai" } } });
harness.resume();                                                            // finish a run a crashed process left
const settled = await (await root.submit({ type: "input", content: "hi", requestId: "turn-1" }, context)).wait(context);
const page = await root.entries({}, 50, undefined, context);                // Page<EntryRecord>, newest first, page.next = cursor
```
- **Layout [V]** (`durable/src/storage/jsonl/storage.ts#L28-L29,L100,L246,L277-L306`): `main.jsonl` = one JSON line per commit `{format:1,type:"commit",seq,writes:[{type:"entry",value:EntryRecord},...]}`, appended (sidecars first, then the marker; `fsync:true` flushes before the marker). Documents and live tasks go to `doc-<id>.jsonl` / `task-<id>.jsonl`, which are rewritten ("reclaimed" via `.reclaim` + rename, errors ignored). On open the whole store is replayed into an in-memory `MemoryStorage`: RAM and start-up grow with history (SQLite keeps only the working set). One process per storage, no locking (the experimental host uses `proper-lockfile`; optchat has its own `data/lock`).
- **Append-only [V]:** entries are immutable. Reset, compaction, context edits (`omit`/`replace`) and head markers are NEW entries; "older messages always stay in storage". Kinds: `pi.user`, `pi.assistant`, `pi.tool-result`, `pi.system`, `pi.reset`, `pi.compaction` + your own (`defineEntry`, `submit({ type: "write" })`) (`durable/src/entries.ts`).
- **Reading back [V]:** `Conversation.entries(query, limit, cursor, ctx)` with `EntryQuery { minEntryId, maxEntryId }` (`order` only on main); `Conversation.context(ctx)` returns `ContextView { entries, contributions, messages }`; tools can use `api.commit(tx => tx.scanEntries(...))` (blog "search_history" tool example). Entry ids are session-wide increasing integers, NOT message ordinals (system and tool-result entries consume ids), so optchat's `#n` needs its own `n -> EntryId` index (a `defineDoc`), or keep `log.jsonl` as source of truth and treat the harness transcript as a copy.

## 6. Maturity
| | |
|---|---|
| npm [V] | `@earendil-works/pi-durable` **1.0.4** (2026-10-05; 13 versions since 2026-09-19, 1.0.0 on 2026-10-01); `pi-ai` 1.0.4, `chord` 1.0.4. pi-ai hard-depends on openai, @anthropic-ai/sdk, @google/genai, @aws-sdk/client-bedrock-runtime (lazy-loaded but installed) |
| Repo [V] | github.com/earendil-works/pi: 113k stars, 284 open issues, HEAD 2026-10-07 20:41Z, last `packages/durable` commit 2026-10-06 19:10Z; releases v1.0.0 to v1.0.4 within 5 days, v1.1.0 changelog audit already in flight |
| License [V] | MIT (package.json, repo, Pi 1.0 post) |
| Stability [V] | `durable/README.md#L3`: "Experimental. The API changes without notice between releases." `durable/CHANGELOG.md` Unreleased: breaking `Storage` `order` contract and `TaskRuntime.context(.., { at })`; adds `HookApi.models`, `Conversation.context({ at })`. 38 issues mention pi-durable (open: #10411 wait-cycle deadlock, #10583 compaction retention). Pin exact versions |
| Node [V] | `engines.node >= 22.19.0` on all three; ESM only; this machine has v22.23.2 = OK. SQLite adapter uses `node:sqlite`; JSONL needs only `node:fs` |
| Windows [V/I] | Win32 is handled in `durable/src/env/node.ts` (Git-for-Windows bash lookup, taskkill, `windowsHide`, no O_NOFOLLOW); 1.0.3: `watch()` polls on Windows; 1.0.4 adds `createPowerShellTool()`. OptChat would use none of the shell/watch parts. No Windows-specific durable issue found in an issue search. Not run-tested by me |
