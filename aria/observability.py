"""Observabilidade: registra cada chamada ao agente (tokens, latência, tools usadas).

Sempre grava localmente em JSONL (funciona em qualquer ambiente, sem
dependência externa). Se o Supabase estiver configurado, também grava na
tabela agent_traces (ver supabase/01-knowledge-base-pgvector.sql), assim dá
pra consultar custo/latência em produção via SQL/dashboard.

Preços aproximados do Groq para o modelo default (openai/gpt-oss-120b),
usados só pra estimativa de custo em observabilidade, não é cobrança real.
"""

import json
import os
import time
from dataclasses import asdict, dataclass

import requests

from aria.agent import AgentResult
from aria.config import CONFIG

_PRICE_PER_1M_INPUT_TOKENS_USD = 0.15
_PRICE_PER_1M_OUTPUT_TOKENS_USD = 0.75


@dataclass
class Trace:
    agent: str
    question: str
    answer: str
    tool_calls: list
    input_tokens: int
    output_tokens: int
    latency_ms: int
    estimated_cost_usd: float
    timestamp: float


def _estimate_cost(input_tokens: int, output_tokens: int) -> float:
    return round(
        (input_tokens / 1_000_000) * _PRICE_PER_1M_INPUT_TOKENS_USD
        + (output_tokens / 1_000_000) * _PRICE_PER_1M_OUTPUT_TOKENS_USD,
        6,
    )


def record_trace(agent_slug: str, question: str, result: AgentResult) -> Trace:
    trace = Trace(
        agent=agent_slug,
        question=question,
        answer=result.answer,
        tool_calls=[asdict(tc) for tc in result.tool_calls],
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        latency_ms=result.latency_ms,
        estimated_cost_usd=_estimate_cost(result.input_tokens, result.output_tokens),
        timestamp=time.time(),
    )
    _write_local(trace)
    if CONFIG.has_supabase:
        _write_supabase(trace)
    return trace


def _write_local(trace: Trace) -> None:
    os.makedirs(os.path.dirname(CONFIG.traces_path) or ".", exist_ok=True)
    with open(CONFIG.traces_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(trace), ensure_ascii=False) + "\n")


def _write_supabase(trace: Trace) -> None:
    headers = {
        "apikey": CONFIG.supabase_key,
        "Authorization": f"Bearer {CONFIG.supabase_key}",
        "Content-Type": "application/json",
    }
    try:
        requests.post(
            f"{CONFIG.supabase_url}/rest/v1/agent_traces",
            headers=headers,
            json={
                "agent": trace.agent,
                "question": trace.question,
                "answer": trace.answer,
                "tool_calls": trace.tool_calls,
                "input_tokens": trace.input_tokens,
                "output_tokens": trace.output_tokens,
                "latency_ms": trace.latency_ms,
            },
            timeout=10,
        )
    except requests.RequestException:
        pass  # observabilidade nunca deve derrubar a resposta ao usuário
