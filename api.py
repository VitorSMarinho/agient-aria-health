# ==============================================
# PROJETO ARIA — Agient
# API: FastAPI — Backend dos Agentes
# Descrição: Recebe perguntas do frontend
#            e retorna respostas do ARIA
#            com dados reais do Supabase
# Autor: Vitor Marinho
# ==============================================

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import requests

load_dotenv()

app = FastAPI(
    title="ARIA API",
    description="Agente de Raciocinio e Inteligencia em Analise Clinica",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers_supabase = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

# ----------------------------------------------
# Função para buscar dados do Supabase
# ----------------------------------------------
def buscar_dados_supabase():
    tabelas = [
        "gold_kpi_pacientes",
        "gold_kpi_atendimentos",
        "gold_kpi_clinico",
        "gold_kpi_estoque",
        "gold_kpi_financeiro"
    ]
    
    dados = {}
    for tabela in tabelas:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/{tabela}",
            headers=headers_supabase
        )
        if response.status_code == 200:
            dados[tabela] = response.json()
    
    return dados

# ----------------------------------------------
# Formata dados para o agente
# ----------------------------------------------
def formatar_dados(dados):
    texto = "DADOS REAIS DO INSTITUTO ONCOLOGICO:\n\n"
    
    for tabela, registros in dados.items():
        texto += f"=== {tabela.upper()} ===\n"
        for registro in registros[:5]:  # Limita 5 registros por tabela
            texto += str(registro) + "\n"
        texto += "\n"
    
    return texto

# ----------------------------------------------
# Modelo da requisição
# ----------------------------------------------
class Pergunta(BaseModel):
    pergunta: str

# ----------------------------------------------
# Rotas
# ----------------------------------------------
@app.get("/")
def health_check():
    return {"status": "ARIA API online", "versao": "1.0.0"}

@app.post("/consultar")
def consultar_aria(body: Pergunta):
    # Busca dados reais do Supabase
    dados = buscar_dados_supabase()
    contexto = formatar_dados(dados)
    
    mensagens = [
        SystemMessage(content="Voce e o ARIA, agente de inteligencia "
        "do Instituto Oncologico desenvolvido pela Agient. "
        "Analise os dados fornecidos e responda de forma clara e objetiva. "
        "Sempre aponte pontos de atencao e sugira melhorias quando relevante. "
        "Responda sempre em portugues brasileiro."),
        HumanMessage(content=f"{contexto}\n\nPergunta: {body.pergunta}")
    ]
    
    resposta = llm.invoke(mensagens)
    
    return {
        "pergunta": body.pergunta,
        "resposta": resposta.content,
        "agente": "ARIA v1.0",
        "disclaimer": "O ARIA e um suporte a decisao baseado em dados. Nao substitui o julgamento clinico medico."
    }