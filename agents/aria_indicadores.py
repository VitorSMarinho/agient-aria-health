# ==============================================
# PROJETO ARIA — Agient
# Agente: Indicadores de Atendimento
# Descrição: Analisa KPIs operacionais do
#            Instituto Oncológico
# Autor: Vitor Marinho
# ==============================================

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# ----------------------------------------------
# Carregando variáveis de ambiente
# ----------------------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------------------------------------
# Configuração do modelo
# ----------------------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0.3
)

# ----------------------------------------------
# Dados Gold para o agente
# ----------------------------------------------
dados_kpi = """
INDICADORES DO INSTITUTO ONCOLOGICO:

ATENDIMENTOS:
- Total de atendimentos: 49
- Tipos: Consulta, Quimioterapia, Radioterapia, Exame, Imunoterapia
- Evolucoes: Melhora (18), Estavel (15), Piora (12), Em avaliacao (4)
- Status: Em tratamento (22), Remissao (14), Critico (8), Alta (5)

PACIENTES:
- Total: 50 pacientes
- Tipos de cancer: Mama, Pulmao, Leucemia, Linfoma, Prostata, Colorretal
- Estadiamentos: I, II, III, IV
- Idade media: 52 anos

ESTOQUE:
- Itens criticos (abaixo do minimo): 8
- Itens vencidos ou vencendo em breve: 5
- Categorias: Quimioterapico, Analgesico, Antieméetico, Insumo

FINANCEIRO:
- Receitas totais: R$ 87.432,00
- Despesas totais: R$ 124.876,00
- Pagamentos pendentes: 12 transacoes
- Pagamentos atrasados: 5 transacoes
"""

# ----------------------------------------------
# Funcao principal do agente
# ----------------------------------------------
def agente_indicadores(pergunta: str) -> str:
    mensagens = [
        SystemMessage(content="Voce e o ARIA, agente de inteligencia "
        "do Instituto Oncologico desenvolvido pela Agient. "
        "Analise os indicadores fornecidos e responda de forma clara e objetiva. "
        "Sempre aponte pontos de atencao e sugira melhorias quando relevante. "
        "Responda sempre em portugues brasileiro."),
        HumanMessage(content=f"Dados atuais do Instituto Oncologico:\n\n{dados_kpi}\n\nPergunta: {pergunta}")
    ]
    
    resposta = llm.invoke(mensagens)
    return resposta.content

# ----------------------------------------------
# Execucao do agente
# ----------------------------------------------
if __name__ == "__main__":
    print("🤖 ARIA — Agente de Indicadores")
    print("=" * 50)
    
    perguntas = [
        "Qual e a situacao geral do instituto hoje?",
        "Quais sao os principais pontos de atencao no estoque?",
        "Como esta a saude financeira do instituto?"
    ]
    
    for pergunta in perguntas:
        print(f"\n📊 {pergunta}")
        print("-" * 40)
        resposta = agente_indicadores(pergunta)
        print(resposta)
        print()