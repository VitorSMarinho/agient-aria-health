"""Runner de evals do ARIA.

Eval determinístico (sempre roda): a tool certa foi chamada? a resposta
contém alguma das keywords esperadas?

Eval baseado em modelo (--judge, opcional): usa o próprio LLM como juiz pra
notar se a resposta está fundamentada nos dados retornados pelas tools
(0 chamadas extra de LLM por padrão, só roda se pedido, porque custa tokens).

Uso:
    python eval/run_evals.py
    python eval/run_evals.py --judge
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.cases import CASES, EvalCase

from aria.agents import ask
from aria.observability import record_trace


def _normalize(text: str) -> str:
    # LLMs às vezes usam espaços tipográficos (ex: narrow no-break space antes
    # de unidades, "48 horas") em vez de espaço comum. Normaliza antes de comparar.
    return re.sub(r"\s+", " ", text).lower()


def _keyword_hit(answer: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    normalized = _normalize(answer)
    return any(_normalize(k) in normalized for k in keywords)


def _judge(case: EvalCase, answer: str, tool_results: list[dict]) -> str:
    from langchain_core.messages import HumanMessage, SystemMessage

    from aria.agent import _llm

    llm = _llm()
    prompt = (
        "Voce e um avaliador de qualidade de respostas de IA. Dado o resultado das tools "
        "chamadas e a resposta final do agente, diga em uma palavra se a resposta esta "
        "FUNDAMENTADA nos dados das tools ou se parece INVENTADA (nao usa os dados). "
        "Responda so com 'FUNDAMENTADA' ou 'INVENTADA'."
    )
    content = f"Pergunta: {case.question}\nDados das tools: {tool_results}\nResposta: {answer}"
    resposta = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=content)])
    return resposta.content.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", action="store_true", help="roda também o eval baseado em modelo")
    args = parser.parse_args()

    if not os.getenv("GROQ_API_KEY"):
        print("GROQ_API_KEY não configurada: não dá pra rodar os evals (precisam do LLM real).")
        sys.exit(1)

    results = []
    for case in CASES:
        profile, result = ask(case.agent, case.question)
        record_trace(case.agent, case.question, result)

        tool_used = {tc.name for tc in result.tool_calls}
        tool_ok = case.expect_tool is None or case.expect_tool in tool_used
        keyword_ok = _keyword_hit(result.answer, case.expect_keywords)
        passed = tool_ok and keyword_ok

        judge_verdict = None
        if args.judge:
            judge_verdict = _judge(case, result.answer, [tc.result for tc in result.tool_calls])

        results.append((case, passed, tool_ok, keyword_ok, judge_verdict, result))

    print(f"\n{'CASO':<32} {'TOOL':<6} {'KEYWORD':<8} {'STATUS':<8} JUIZ")
    print("-" * 80)
    failures = 0
    for case, passed, tool_ok, keyword_ok, judge_verdict, result in results:
        status = "PASS" if passed else "FAIL"
        failures += 0 if passed else 1
        print(
            f"{case.name:<32} {str(tool_ok):<6} {str(keyword_ok):<8} {status:<8} "
            f"{judge_verdict or '-'}"
        )
        if not passed:
            print(f"   -> tools chamadas: {[tc.name for tc in result.tool_calls]}")
            print(f"   -> resposta: {result.answer[:200]}")

    print(f"\n{len(results) - failures}/{len(results)} casos passaram.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
