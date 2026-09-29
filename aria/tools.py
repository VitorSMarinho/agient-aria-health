"""Tools reais que o agente ARIA pode chamar (function calling).

Antes desta mudança, o /consultar enfiava todos os dados do Supabase dentro
do prompt em toda chamada. Agora o LLM decide, por pergunta, qual dado buscar:
reduz tokens, generaliza melhor e é o padrão real de "AI Agents" do roadmap.
"""

import os

import requests

from aria.config import CONFIG
from aria.retriever import format_context, retrieve

# Dado de demonstração, usado como fallback enquanto as tabelas gold_kpi_*
# do Supabase de produção não estiverem populadas (pendência conhecida do projeto).
_DADOS_DEMO = {
    "gold_kpi_atendimentos": [
        {"total_atendimentos": 49, "melhora": 18, "estavel": 15, "piora": 12, "em_avaliacao": 4}
    ],
    "gold_kpi_pacientes": [{"total_pacientes": 50, "idade_media": 52}],
    "gold_kpi_estoque": [{"itens_criticos": 8, "itens_vencendo": 5}],
    "gold_kpi_financeiro": [
        {"receitas": 87432.00, "despesas": 124876.00, "pendentes": 12, "atrasados": 5}
    ],
}


def buscar_kpis(tabela: str) -> dict:
    """Busca indicadores (KPIs) de uma tabela gold do Supabase.

    tabela deve ser uma de: gold_kpi_pacientes, gold_kpi_atendimentos,
    gold_kpi_clinico, gold_kpi_estoque, gold_kpi_financeiro.
    """
    if CONFIG.has_supabase:
        headers = {
            "apikey": CONFIG.supabase_key,
            "Authorization": f"Bearer {CONFIG.supabase_key}",
        }
        try:
            response = requests.get(
                f"{CONFIG.supabase_url}/rest/v1/{tabela}",
                headers=headers,
                params={"limit": 10},
                timeout=15,
            )
            if response.status_code == 200 and response.json():
                return {"tabela": tabela, "fonte": "supabase", "dados": response.json()}
        except requests.RequestException:
            pass

    return {
        "tabela": tabela,
        "fonte": "demo (Supabase indisponível ou tabela vazia)",
        "dados": _DADOS_DEMO.get(tabela, []),
    }


def buscar_protocolo_clinico(pergunta: str) -> dict:
    """Busca (RAG) em protocolos, políticas e manuais internos do Instituto Oncológico."""
    try:
        chunks = retrieve(pergunta)
        return {"contexto": format_context(chunks), "fontes": [c.source for c in chunks]}
    except requests.RequestException:
        return {
            "contexto": "(base de conhecimento indisponível no momento)",
            "fontes": [],
        }


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_kpis",
            "description": (
                "Busca indicadores (KPIs) reais do Instituto Oncológico numa tabela gold "
                "específica. Use sempre que a pergunta envolver números, métricas ou status atuais."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tabela": {
                        "type": "string",
                        "enum": [
                            "gold_kpi_pacientes",
                            "gold_kpi_atendimentos",
                            "gold_kpi_clinico",
                            "gold_kpi_estoque",
                            "gold_kpi_financeiro",
                        ],
                    }
                },
                "required": ["tabela"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_protocolo_clinico",
            "description": (
                "Busca por similaridade semântica em protocolos, políticas de estoque e "
                "manuais internos (fictícios) do Instituto Oncológico. Use quando a pergunta "
                "pedir um procedimento, uma política ou uma recomendação, não apenas um número."
            ),
            "parameters": {
                "type": "object",
                "properties": {"pergunta": {"type": "string"}},
                "required": ["pergunta"],
            },
        },
    },
]

TOOL_IMPLEMENTATIONS = {
    "buscar_kpis": buscar_kpis,
    "buscar_protocolo_clinico": buscar_protocolo_clinico,
}
