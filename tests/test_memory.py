"""Model-free tests of the memory (view, tree, compaction). A scripted fake replaces llama-server for both the chat
and the compactor, so these run anywhere: python -m unittest discover -s tests
"""
import json, os, re, shutil, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import optchat  # noqa: E402

# a realistic French summary sentence (~2.9 bytes per token with a Qwen3 tokenizer)
PROSE = ("L'utilisateur demande la NCA de l'exercice 3 par voie orale ; l'assistant importe la feuille 1, lance l'analyse et "
         "rapporte le Cmax de 12,4 mg/L et la demi-vie de 6,1 h, puis l'utilisateur demande de comparer les deux analyses. ")
TOOL_RESULT = json.dumps({"subjects": [{"subject": "1", "parameters": {f"p{k}": f"{1.23456 * k:.6g} mg/L" for k in range(40)}}]})[:2500]
ANSWER = ("Voici les résultats de la NCA : Cmax 12,4 mg/L à 1,5 h, AUC0-inf 98,2 h·mg/L, demi-vie 6,1 h. " * 8)[:700]


class FakeLLM:
    """Compactor calls (a JSON schema) get n lines of `line_chars` characters; chat calls get one tool call, then an
    answer. `context_bytes`: a chat call whose messages exceed it fails like llama-server (HTTP 400)."""
    total_slots = 2

    def __init__(self, line_chars=380, context_bytes=None, compactor_fails=False):
        self.line_chars, self.context_bytes, self.compactor_fails = line_chars, context_bytes, compactor_fails
        self.last, self.k = {}, 0
        self.compact_calls, self.chat_calls, self.overflows = 0, 0, 0

    def chat(self, messages, slot, tools=None, max_tokens=512, think=False, temperature=0.3, response_format=None):
        self.last = {"wall_s": 0, "prompt_tokens": 0, "completion_tokens": 0, "prompt_eval_n": 0, "cache_n": 0,
                     "prompt_ms": 0, "predicted_ms": 0, "gen_tps": None, "finish_reason": "stop"}
        if response_format:
            self.compact_calls += 1
            if self.compactor_fails: raise optchat.LLMError("HTTP 503: compactor down")
            n = response_format["json_schema"]["schema"]["properties"]["lines"]["minItems"]
            self.k += 1
            return {"content": json.dumps({"lines": [(f"[{self.k}.{j}] " + PROSE * 8)[:self.line_chars] for j in range(n)]})}
        self.chat_calls += 1
        if self.context_bytes is not None and prompt_bytes(messages) > self.context_bytes:
            self.overflows += 1
            raise optchat.LLMError("HTTP 400: the request exceeds the available context size")
        if messages[-1]["role"] == "user":
            return {"content": "", "tool_calls": [{"id": f"c{self.chat_calls}", "type": "function",
                                                   "function": {"name": "nca_run", "arguments": "{\"worksheet\": 1}"}}]}
        return {"content": ANSWER}


def prompt_bytes(messages):
    return sum(len((m.get("content") or "").encode("utf-8")) for m in messages)


def digest_bytes(store):
    return len(optchat.render_digest(store).encode("utf-8"))


class Session:
    """An optchat Agent on a temporary folder, with the fake model and a fake NCA tool."""
    def __init__(self, fake, **cfg):
        self.dir = tempfile.mkdtemp(prefix="optchat_test_")
        self.fake = fake
        real = optchat.LLM
        optchat.LLM = lambda cfg, base_url=None: fake
        try: self.ag = optchat.Agent(dict(optchat.CFG, data_dir=self.dir, **cfg))
        finally: optchat.LLM = real
        self.ag._tool = lambda name, args: TOOL_RESULT if name == "nca_run" else "?"

    def turns(self, n, check=None):
        for t in range(n):
            self.ag.turn(f"Tour {t} : lance la NCA sur la feuille 1 (400 mg, voie orale) et donne Cmax, AUC et demi-vie.",
                         verbose=False)
            self.ag.wait_bg()
            if check: check(t)

    def close(self):
        self.ag.close(); shutil.rmtree(self.dir, ignore_errors=True)


def check_view(tc, store):
    """The view covers every message exactly once, in order, and its levels never increase left to right."""
    covered, levels = [], []
    for it in store.view["items"]:
        if it["kind"] == "node":
            n = store.nodes[it["id"]]; covered.append((n["first"], n["last"])); levels.append(n["level"])
        else:
            covered.append((it["i"], it["i"])); levels.append(-1)
    tc.assertEqual(covered[0][0], 0)
    for (a0, a1), (b0, b1) in zip(covered, covered[1:]): tc.assertEqual(b0, a1 + 1)
    tc.assertEqual(covered[-1][1], len(store.log) - 1)
    tc.assertEqual(levels, sorted(levels, reverse=True))
    for n in store.nodes.values():                                   # every node opens on its children or its message
        if "children" in n:
            a, b = (store.nodes[c] for c in n["children"])
            tc.assertEqual((a["first"], b["last"], a["last"] + 1), (n["first"], n["last"], b["first"]))
        else:
            tc.assertEqual(n["msg"], n["first"])


class TestByteGuard(unittest.TestCase):
    def tearDown(self): self.s.close()

    def test_long_session_stays_within_the_byte_budgets(self):
        # 600 messages of NCA turns: without the guard the digest reaches ~24 KB (~8.9k tokens) at 380-char lines
        self.s = Session(FakeLLM(line_chars=380))
        cfg, st = self.s.ag.cfg, self.s.ag.store
        peak = {"digest": 0, "view": 0}
        def check(t):
            d, v = digest_bytes(st), digest_bytes(st) + optchat.raw_view_bytes(st, cfg)
            peak["digest"], peak["view"] = max(peak["digest"], d), max(peak["view"], v)
            self.assertLessEqual(d, cfg["digest_max_bytes"], t)
            self.assertLessEqual(v, cfg["view_max_bytes"], t)
        self.s.turns(150, check)
        self.assertEqual(len(st.log), 600)
        self.assertGreater(self.s.ag.compactor.stats["guard_merges"], 0)
        self.assertGreater(peak["digest"], cfg["digest_max_bytes"] * 0.8)    # the guard did bind
        check_view(self, st)

    def test_without_the_guard_the_digest_outgrows_the_budget(self):
        # the defect the guard fixes, reproduced with the guard switched off
        self.s = Session(FakeLLM(line_chars=380), view_max_bytes=10 ** 9, digest_max_bytes=10 ** 9)
        self.s.turns(150)
        self.assertGreater(digest_bytes(self.s.ag.store), 20000)
        self.assertEqual(self.s.ag.compactor.stats["guard_merges"], 0)

    def test_overflow_recovery_shrinks_the_digest(self):
        # a context that holds ~15 KB of messages: the normal view (up to 18 KB) overflows it on some turns; the
        # recovery (raw zone promoted, digest at half its budget) must make every retry fit
        fake = FakeLLM(line_chars=380, context_bytes=15000)
        self.s = Session(fake)
        self.s.turns(150)
        self.assertGreater(fake.overflows, 0)
        answers = [m for m in self.s.ag.store.log if m["role"] == "assistant"]
        self.assertEqual(len(answers), 150)                        # every turn answered: no retry failed
        check_view(self, self.s.ag.store)

    def test_a_failing_compactor_stops_the_guard(self):
        self.s = Session(FakeLLM(compactor_fails=True), digest_max_bytes=1000)
        self.s.turns(10)                                           # returns: no endless loop when no merge succeeds
        check_view(self, self.s.ag.store)

    def test_fit_digest_merges_the_coarsest_lines_first(self):
        self.s = Session(FakeLLM(line_chars=380), view_max_bytes=10 ** 9, digest_max_bytes=10 ** 9)
        self.s.turns(40)
        st, comp = self.s.ag.store, self.s.ag.compactor
        before = [st.nodes[it["id"]]["level"] for it in st.view["items"] if it["kind"] == "node"]
        budget = digest_bytes(st) - 1500
        self.assertGreater(comp.fit_digest(budget), 0)
        self.assertLessEqual(digest_bytes(st), budget)
        after = [st.nodes[it["id"]]["level"] for it in st.view["items"] if it["kind"] == "node"]
        self.assertGreater(max(after), max(before))                # the oldest, coarsest lines were merged
        self.assertEqual(after.count(0), before.count(0))          # the newest lines were left alone
        check_view(self, st)


if __name__ == "__main__":
    unittest.main()
