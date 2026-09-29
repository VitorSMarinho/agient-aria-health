# ==============================================
# PROJETO ARIA: Agient
# API: FastAPI, Backend dos Agentes
# Descrição: Recebe perguntas do frontend e roteia
#            pro agente ARIA certo (tool-calling real,
#            RAG e observabilidade, ver pasta aria/)
# Autor: Vitor Marinho
# ==============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from aria.agents import AGENT_PROFILES, DEFAULT_AGENT, ask
from aria.observability import record_trace

app = FastAPI(
    title="ARIA API",
    description="Agente de Raciocinio e Inteligencia em Analise Clinica",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pergunta(BaseModel):
    pergunta: str
    agente: str = DEFAULT_AGENT


@app.get("/")
def health_check():
    return {"status": "ARIA API online", "versao": "2.0.0"}


@app.get("/agentes")
def listar_agentes():
    return {
        slug: {"nome": profile.nome, "acesso": profile.acesso}
        for slug, profile in AGENT_PROFILES.items()
    }


@app.post("/consultar")
def consultar_aria(body: Pergunta):
    profile, result = ask(body.agente, body.pergunta)
    record_trace(profile.slug, body.pergunta, result)

    return {
        "pergunta": body.pergunta,
        "resposta": result.answer,
        "agente": profile.nome,
        "tools_utilizadas": [tc.name for tc in result.tool_calls],
        "latencia_ms": result.latency_ms,
        "disclaimer": "O ARIA e um suporte a decisao baseado em dados. Nao substitui o julgamento clinico medico.",
    }
