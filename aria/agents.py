"""Os 5 agentes especializados do ARIA, cada um com prompt, tools e papel de acesso próprios.

Antes, esses 5 agentes existiam só como descrição no README (apenas
`aria_indicadores` tinha código). Agora todos compartilham o mesmo loop de
tool-calling (aria.agent.run_agent), diferenciados por persona e escopo.
"""

from dataclasses import dataclass

from aria.agent import AgentResult, run_agent

_BASE_PROMPT = (
    "Voce e o ARIA, sistema multi-agente de inteligencia de dados do Instituto "
    "Oncologico (cliente ficticio, usado como demonstracao tecnica). "
    "Use as tools disponiveis para buscar dados reais antes de responder. Nunca "
    "invente numeros. Responda de forma clara e objetiva, e aponte pontos de "
    "atencao quando relevante. "
    "Voce e suporte a decisao: nunca substitui julgamento clinico ou financeiro humano."
)


@dataclass(frozen=True)
class AgentProfile:
    slug: str
    nome: str
    acesso: str
    foco: str


AGENT_PROFILES: dict[str, AgentProfile] = {
    "indicadores": AgentProfile(
        slug="indicadores",
        nome="Agente de Indicadores de Atendimento",
        acesso="Gestão operacional",
        foco=(
            "Volume de atendimentos, gargalos, performance medica e operacional, "
            "metas nao atingidas. Foque em gold_kpi_atendimentos e gold_kpi_pacientes."
        ),
    ),
    "clinico": AgentProfile(
        slug="clinico",
        nome="Agente Clínico de Quadro do Paciente",
        acesso="Médicos autorizados",
        foco=(
            "Resumo clinico, evolucao por estadiamento, padroes clinicos, alertas. "
            "Foque em gold_kpi_clinico e nos protocolos internos (RAG)."
        ),
    ),
    "financeiro": AgentProfile(
        slug="financeiro",
        nome="Agente Financeiro",
        acesso="Diretoria e financeiro",
        foco=(
            "Monitoramento financeiro, anomalias, inadimplencia, projecoes. "
            "Foque em gold_kpi_financeiro."
        ),
    ),
    "estoque": AgentProfile(
        slug="estoque",
        nome="Agente de Estoque",
        acesso="Farmácia e suprimentos",
        foco=(
            "Estoque minimo, validade, reposicao, criticidade. "
            "Foque em gold_kpi_estoque e na politica de estoque (RAG)."
        ),
    ),
    "estrategico": AgentProfile(
        slug="estrategico",
        nome="Agente Estratégico",
        acesso="Liderança executiva",
        foco=(
            "Cruza dados clinicos, operacionais e financeiros para insights e "
            "recomendacoes priorizadas. Pode usar qualquer tabela gold e o RAG."
        ),
    ),
}

DEFAULT_AGENT = "indicadores"

# Idioma da resposta escolhido no frontend; os dados e as tools seguem em portugues.
LANGUAGE_INSTRUCTIONS = {
    "pt": "Responda sempre em portugues brasileiro.",
    "en": (
        "Always answer in English, even though the data, table names and "
        "internal documents are in Portuguese."
    ),
}
DEFAULT_LANGUAGE = "pt"


def _system_prompt(profile: AgentProfile, language: str = DEFAULT_LANGUAGE) -> str:
    instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS[DEFAULT_LANGUAGE])
    return (
        f"{_BASE_PROMPT} {instruction}\n\nVoce e especificamente o {profile.nome} "
        f"(acesso: {profile.acesso}). Seu foco: {profile.foco}"
    )


def ask(
    agent_slug: str, question: str, language: str = DEFAULT_LANGUAGE
) -> tuple[AgentProfile, AgentResult]:
    profile = AGENT_PROFILES.get(agent_slug, AGENT_PROFILES[DEFAULT_AGENT])
    result = run_agent(_system_prompt(profile, language), question)
    return profile, result
