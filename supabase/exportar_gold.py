# ==============================================
# PROJETO ARIA — Agient
# Exportação: Gold → Supabase
# Autor: Vitor Marinho
# ==============================================

import os
import requests
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def limpar_dados(df):
    for coluna in df.columns:
        # Converte float que são inteiros para int
        if df[coluna].dtype == 'float64':
            if df[coluna].dropna().apply(lambda x: x == int(x)).all():
                df[coluna] = df[coluna].fillna(0).astype(int)
    return df

def exportar_para_supabase(nome_tabela, caminho_csv):
    df = pd.read_csv(caminho_csv)
    df = limpar_dados(df)
    
    # Converte para dict removendo NaN
    dados = json.loads(df.to_json(orient="records"))

    # Limpa a tabela
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/{nome_tabela}",
        headers={**headers, "Prefer": "return=minimal"},
        params={"id": "gte.0"}
    )

    # Insere os dados
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{nome_tabela}",
        headers=headers,
        data=json.dumps(dados)
    )

    if response.status_code in [200, 201]:
        print(f"✅ {nome_tabela}: {len(dados)} registros exportados")
    else:
        print(f"❌ Erro em {nome_tabela}: {response.status_code} — {response.text}")

# ----------------------------------------------
# Exportando
# ----------------------------------------------
print("🥇 Iniciando exportação Gold → Supabase\n")

tabelas = {
    "gold_kpi_pacientes"    : "databricks/gold/aria_gold_kpis_pacientes.csv",
    "gold_kpi_atendimentos" : "databricks/gold/aria_gold_kpis_atendimentos.csv",
    "gold_kpi_clinico"      : "databricks/gold/aria_gold_kpis_clinico.csv",
    "gold_kpi_estoque"      : "databricks/gold/aria_gold_kpis_estoque.csv",
    "gold_kpi_financeiro"   : "databricks/gold/aria_gold_kpis_financeiro.csv"
}

for nome, caminho in tabelas.items():
    exportar_para_supabase(nome, caminho)

print("\n🚀 Exportação concluída!")