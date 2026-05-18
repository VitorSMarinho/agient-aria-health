# ==============================================
# PROJETO ARIA — Agient
# Camada: BRONZE | Ingestão Raw
# Descrição: Ingestão dos CSVs do GitHub
#            para a camada raw do Delta Lake
# Autor: Vitor Marinho
# ==============================================

import pandas as pd

# URLs dos CSVs no GitHub (raw)
BASE_URL = "https://raw.githubusercontent.com/VitorSMarinho/agient-aria-health/main/data/raw"

arquivos = {
    "pacientes"             : f"{BASE_URL}/pacientes.csv",
    "atendimentos"          : f"{BASE_URL}/atendimentos.csv",
    "atendimentos_clinicos" : f"{BASE_URL}/atendimentos_clinicos.csv",
    "estoque"               : f"{BASE_URL}/estoque.csv",
    "financeiro"            : f"{BASE_URL}/financeiro.csv"
}

# ==============================================
# Leitura dos CSVs e conversão para Spark
# ==============================================

dfs = {}

for nome, url in arquivos.items():
    print(f"📥 Carregando: {nome}...")
    
    df_pandas = pd.read_csv(url)
    if len(df_pandas.columns) == 1:
        df_pandas = pd.read_csv(url, sep=";")
    
    dfs[nome] = spark.createDataFrame(df_pandas)
    print(f"   ✅ {nome}: {dfs[nome].count()} registros | {len(df_pandas.columns)} colunas")

print("\n🎉 Todos os arquivos carregados com sucesso!")

# ==============================================
# Salvando na camada Bronze — Delta Lake
# ==============================================

spark.sql("CREATE DATABASE IF NOT EXISTS aria_health")
spark.sql("USE aria_health")

for nome, df in dfs.items():
    tabela = f"aria_health.bronze_{nome}"
    
    df.write \
      .format("delta") \
      .mode("overwrite") \
      .saveAsTable(tabela)
    
    print(f"✅ Bronze salvo: {tabela}")

print("\n🥉 Camada Bronze concluída com sucesso!")