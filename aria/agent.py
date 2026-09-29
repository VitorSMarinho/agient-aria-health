"""Loop de tool-calling (ReAct) do agente ARIA.

Substitui o padrão anterior de "enfiar tudo no prompt" por um agente real:
o LLM decide se e quais tools chamar, nós executamos e devolvemos o
resultado, até ele ter contexto suficiente pra responder.
"""

import json
import time
from dataclasses import dataclass, field

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq

from aria.config import CONFIG
from aria.tools import TOOL_IMPLEMENTATIONS, TOOL_SCHEMAS


@dataclass
class ToolCallTrace:
    name: str
    args: dict
    result: dict
    latency_ms: int


@dataclass
class AgentResult:
    answer: str
    tool_calls: list[ToolCallTrace] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0


def _llm():
    return ChatGroq(
        model=CONFIG.llm_model,
        api_key=CONFIG.groq_api_key,
        temperature=0.3,
    ).bind_tools(TOOL_SCHEMAS)


def run_agent(system_prompt: str, question: str) -> AgentResult:
    start = time.perf_counter()
    llm = _llm()
    messages: list = [SystemMessage(content=system_prompt), HumanMessage(content=question)]

    tool_traces: list[ToolCallTrace] = []
    input_tokens = 0
    output_tokens = 0

    for _ in range(CONFIG.max_tool_iterations):
        response: AIMessage = llm.invoke(messages)
        usage = getattr(response, "usage_metadata", None) or {}
        input_tokens += usage.get("input_tokens", 0)
        output_tokens += usage.get("output_tokens", 0)

        if not response.tool_calls:
            latency_ms = int((time.perf_counter() - start) * 1000)
            return AgentResult(
                answer=response.content,
                tool_calls=tool_traces,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
            )

        messages.append(response)
        for call in response.tool_calls:
            tool_start = time.perf_counter()
            implementation = TOOL_IMPLEMENTATIONS.get(call["name"])
            result = implementation(**call["args"]) if implementation else {"erro": "tool desconhecida"}
            tool_latency = int((time.perf_counter() - tool_start) * 1000)

            tool_traces.append(
                ToolCallTrace(name=call["name"], args=call["args"], result=result, latency_ms=tool_latency)
            )
            messages.append(
                ToolMessage(content=json.dumps(result, ensure_ascii=False), tool_call_id=call["id"])
            )

    latency_ms = int((time.perf_counter() - start) * 1000)
    return AgentResult(
        answer="Não consegui concluir o raciocínio dentro do limite de passos. Tente reformular a pergunta.",
        tool_calls=tool_traces,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
    )
