"""Validate-and-repair (self-correction) loop in AgentRunner: offline, MockLLM only."""
import copy

from conftest import T
from helpers import default_responses, make_pipeline

from ict_pipeline.agents.base import REPAIR_INSTRUCTION, AgentRunner, MockLLM, validate_envelope
from ict_pipeline.guardrails import FOOTER
from ict_pipeline.observability import RunLog

CYCLE = T("14:05")
PAYLOAD = {"run_id": "r1", "as_of": CYCLE.isoformat(), "data_source": "TV:OANDA", "fallback_used": False}


def _good_bias():
    return default_responses()["bias"]


def _flaky(bad_first: int, mutate):
    """Return a MockLLM callable that is invalid for the first ``bad_first`` calls, then valid."""
    good = _good_bias()
    state = {"n": 0, "prompts": []}

    def f(prompt):
        state["n"] += 1
        state["prompts"].append(prompt)
        d = copy.deepcopy(good(prompt))   # fixtures share nested dicts; never mutate them
        if state["n"] <= bad_first:
            mutate(d)
        return d
    return f, state


def _price_as_string(d):
    d["instruments"]["NAS100"]["dealing_range"]["high"] = "31000"


def test_repair_fixes_schema_error_on_second_attempt():
    f, state = _flaky(1, _price_as_string)
    log = RunLog("r1")
    res = AgentRunner("bias", MockLLM({"bias": f}), lambda x: validate_envelope(x, "bias"), log).run(PAYLOAD, CYCLE)
    assert res.ok and res.repaired and res.attempts == 2
    assert res.data["instruments"]["NAS100"]["dealing_range"]["high"] == 31000.0
    rec = log.records[0]
    assert rec["valid"] is True and rec["attempts"] == 2 and rec["repaired"] is True


def test_repair_prompt_carries_exact_validation_errors():
    f, state = _flaky(1, _price_as_string)
    AgentRunner("bias", MockLLM({"bias": f}), lambda x: validate_envelope(x, "bias")).run(PAYLOAD, CYCLE)
    first, second = state["prompts"]
    assert "failed schema validation" not in first
    assert REPAIR_INSTRUCTION.split("\n")[0] in second
    assert "- dealing_range.high: Input should be a valid number" in second     # field path the model must fix
    assert second.startswith(first)                               # same system rule + untrusted-wrapped snapshot


def test_repair_handles_non_json_answer():
    good = _good_bias()
    calls = {"n": 0}

    def f(prompt):
        calls["n"] += 1
        return "Sure! Here is my read of the market." if calls["n"] == 1 else good(prompt)
    res = AgentRunner("bias", MockLLM({"bias": f}), lambda x: validate_envelope(x, "bias")).run(PAYLOAD, CYCLE)
    assert res.ok and res.attempts == 2


def test_repair_is_bounded_then_discarded():
    f, state = _flaky(99, _price_as_string)          # never fixes itself
    log = RunLog("r1")
    res = AgentRunner("bias", MockLLM({"bias": f}), lambda x: validate_envelope(x, "bias"), log).run(PAYLOAD, CYCLE)
    assert not res.ok and res.attempts == 2 and state["n"] == 2 and "ValidationError" in res.error
    assert log.records[0]["valid"] is False and log.records[0]["repaired"] is False


def test_max_repairs_zero_keeps_single_shot_behaviour():
    f, state = _flaky(1, _price_as_string)
    res = AgentRunner("bias", MockLLM({"bias": f}), lambda x: validate_envelope(x, "bias"), max_repairs=0).run(PAYLOAD, CYCLE)
    assert not res.ok and res.attempts == 1 and state["n"] == 1


def test_stale_output_is_never_repaired():
    calls = {"n": 0}

    def stale(prompt):
        calls["n"] += 1
        return {"agent": "bias", "run_id": "r", "as_of": "2026-10-14T13:30:00+02:00", "data_source": "TV:OANDA",
                "fallback_used": False, "instruments": {}, "notes": "", "errors": []}
    res = AgentRunner("bias", MockLLM({"bias": stale}), lambda x: validate_envelope(x, "bias")).run(PAYLOAD, CYCLE)
    assert not res.ok and "stale" in res.error and calls["n"] == 1


def test_transport_errors_are_not_retried_as_repairs():
    res = AgentRunner("bias", MockLLM({}), lambda x: validate_envelope(x, "bias")).run(PAYLOAD, CYCLE)
    assert not res.ok and res.attempts == 1 and "RuntimeError" in res.error


def test_tokens_are_summed_across_attempts():
    f, _ = _flaky(1, _price_as_string)
    res = AgentRunner("bias", MockLLM({"bias": f}, tokens=40), lambda x: validate_envelope(x, "bias")).run(PAYLOAD, CYCLE)
    assert res.tokens == 80                          # repairs count against the daily token budget


def test_pipeline_uses_repaired_output_and_still_sends_one_call(settings, writer, calendar):
    resp = default_responses()
    f, _ = _flaky(1, _price_as_string)
    resp["bias"] = f
    pipe, llm, out = make_pipeline(settings, writer, calendar, resp)
    res = pipe.run_cycle(CYCLE)
    bias = [r for r in res["log"] if r["kind"] == "agent_call" and r["agent"] == "bias"][0]
    assert bias["valid"] is True and bias["repaired"] is True and bias["attempts"] == 2
    assert len(out.outbox) == 1 and FOOTER in out.outbox[0]
