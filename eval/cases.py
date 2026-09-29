"""Casos de teste do ARIA: evals determinísticos + um eval baseado em modelo (opcional).

Cada caso descreve o que esperamos do agente para uma pergunta real:
- expect_tool: a tool que deveria ter sido chamada (eval determinístico)
- expect_keywords: palavras que devem aparecer na resposta final
"""

from dataclasses import dataclass, field


@dataclass
class EvalCase:
    name: str
    agent: str
    question: str
    expect_tool: str | None = None
    expect_keywords: list[str] = field(default_factory=list)


CASES: list[EvalCase] = [
    EvalCase(
        name="indicadores_volume_atendimentos",
        agent="indicadores",
        question="Qual o total de atendimentos registrados hoje?",
        expect_tool="buscar_kpis",
        expect_keywords=["atendimento"],
    ),
    EvalCase(
        name="estoque_itens_criticos",
        agent="estoque",
        question="Quantos itens estão em estoque crítico agora?",
        expect_tool="buscar_kpis",
        expect_keywords=["crítico", "critico", "estoque"],
    ),
    EvalCase(
        name="estoque_politica_reposicao",
        agent="estoque",
        question="Qual o prazo pra repor um quimioterápico que entrou em criticidade?",
        expect_tool="buscar_protocolo_clinico",
        expect_keywords=["48h", "48 h", "48 horas"],
    ),
    EvalCase(
        name="financeiro_saude_geral",
        agent="financeiro",
        question="Como está a saúde financeira do instituto?",
        expect_tool="buscar_kpis",
        expect_keywords=["financ"],
    ),
    EvalCase(
        name="financeiro_fluxo_cobranca",
        agent="financeiro",
        question="A partir de quantos dias de atraso um pagamento entra no fluxo de cobrança?",
        expect_tool="buscar_protocolo_clinico",
        expect_keywords=["16", "dia"],
    ),
]
