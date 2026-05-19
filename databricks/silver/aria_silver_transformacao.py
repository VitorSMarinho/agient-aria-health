# ==============================================
# PROJETO ARIA — Agient
# Camada: SILVER | Transformação e Limpeza
# Descrição: Padronização, tratamento de nulos
#            e validação dos dados Bronze
# Autor: Vitor Marinho
# ==============================================

from pyspark.sql.functions import col, trim, upper, coalesce, expr
from pyspark.sql.types import IntegerType, DoubleType

spark.sql("USE aria_health")

# Função para tratar múltiplos formatos de data
def parse_date(coluna):
    return coalesce(
        expr(f"try_to_date(`{coluna}`, 'yyyy-MM-dd')"),
        expr(f"try_to_date(`{coluna}`, 'dd/MM/yyyy')"),
        expr(f"try_to_date(`{coluna}`, 'MM/dd/yyyy')"),
        expr(f"try_to_date(`{coluna}`, 'dd-MM-yy')"),
        expr(f"try_to_date(`{coluna}`, 'yy-MM-dd')"),
        expr(f"try_to_date(`{coluna}`, 'dd-MM-yyyy')"),
        expr(f"try_to_date(`{coluna}`, 'MM-dd-yy')")
    )

print("✅ Imports e configuração carregados!")

# ==============================================
# Carregando tabelas da camada Bronze
# ==============================================

tabelas_bronze = [
    "bronze_pacientes",
    "bronze_atendimentos",
    "bronze_atendimentos_clinicos",
    "bronze_estoque",
    "bronze_financeiro"
]

dfs = {}
for tabela in tabelas_bronze:
    dfs[tabela] = spark.table(f"aria_health.{tabela}")
    print(f"📥 Carregado: {tabela} → {dfs[tabela].count()} registros")

print("\n🥉 Dados Bronze prontos para transformação!")

# ==============================================
# Transformação — Pacientes
# ==============================================

df_silver_pacientes = dfs["bronze_pacientes"] \
    .withColumn("nome_ficticio", trim(col("nome_ficticio"))) \
    .withColumn("genero", upper(trim(col("genero")))) \
    .withColumn("tipo_cancer", trim(col("tipo_cancer"))) \
    .withColumn("estadiamento", trim(col("estadiamento"))) \
    .withColumn("convenio", trim(col("convenio"))) \
    .withColumn("status_tratamento", trim(col("status_tratamento"))) \
    .withColumn("data_entrada", parse_date("data_entrada")) \
    .withColumn("idade", col("idade").cast(IntegerType())) \
    .dropDuplicates(["id_paciente"]) \
    .filter(col("id_paciente").isNotNull())

print(f"✅ Pacientes: {df_silver_pacientes.count()} registros limpos")

# ==============================================
# Transformação — Atendimentos
# ==============================================

df_silver_atendimentos = dfs["bronze_atendimentos"] \
    .withColumn("tipo_atendimento", trim(col("tipo_atendimento"))) \
    .withColumn("medico_responsavel", trim(col("medico_responsavel"))) \
    .withColumn("data_atendimento", parse_date("data_atendimento")) \
    .withColumn("evolucao_quadro", trim(col("evolucao_quadro"))) \
    .withColumn("status_quadro", trim(col("status_quadro"))) \
    .withColumn("procedimento_realizado", trim(col("procedimento_realizado"))) \
    .withColumn("medicacao_aplicada", trim(col("medicacao_aplicada"))) \
    .dropDuplicates(["id_atendimento"]) \
    .filter(col("id_atendimento").isNotNull())

print(f"✅ Atendimentos: {df_silver_atendimentos.count()} registros limpos")

# ==============================================
# Transformação — Atendimentos Clínicos
# ==============================================

df_silver_atendimentos_clinicos = dfs["bronze_atendimentos_clinicos"] \
    .withColumn("tipo_atendimento", trim(col("tipo_atendimento"))) \
    .withColumn("medico_responsavel", trim(col("medico_responsavel"))) \
    .withColumn("data_atendimento", parse_date("data_atendimento")) \
    .withColumn("evolucao_quadro", trim(col("evolucao_quadro"))) \
    .withColumn("status_quadro", trim(col("status_quadro"))) \
    .withColumn("procedimento_realizado", trim(col("procedimento_realizado"))) \
    .withColumn("medicacao_aplicada", trim(col("medicacao_aplicada"))) \
    .dropDuplicates(["id_atendimento"]) \
    .filter(col("id_atendimento").isNotNull())

print(f"✅ Atendimentos Clínicos: {df_silver_atendimentos_clinicos.count()} registros limpos")

# ==============================================
# Transformação — Estoque
# ==============================================

df_silver_estoque = dfs["bronze_estoque"] \
    .withColumn("nome_medicamento", trim(col("nome_medicamento"))) \
    .withColumn("categoria", trim(col("categoria"))) \
    .withColumn("fornecedor", trim(col("fornecedor"))) \
    .withColumn("unidade", trim(col("unidade"))) \
    .withColumn("quantidade_atual", col("quantidade_atual").cast(IntegerType())) \
    .withColumn("quantidade_minima", col("quantidade_minima").cast(IntegerType())) \
    .withColumn("valor_unitario", col("valor_unitario").cast(DoubleType())) \
    .withColumn("data_validade", parse_date("data_validade")) \
    .withColumn("data_ultima_compra", parse_date("data_ultima_compra")) \
    .dropDuplicates(["id_item"]) \
    .filter(col("id_item").isNotNull())

print(f"✅ Estoque: {df_silver_estoque.count()} registros limpos")

# ==============================================
# Transformação — Financeiro
# ==============================================

df_silver_financeiro = dfs["bronze_financeiro"] \
    .withColumn("tipo", trim(col("tipo"))) \
    .withColumn("categoria", trim(col("categoria"))) \
    .withColumn("status_pagamento", trim(col("status_pagamento"))) \
    .withColumn("convenio", trim(col("convenio"))) \
    .withColumn("descricao", trim(col("descricao"))) \
    .withColumn("valor", col("valor").cast(DoubleType())) \
    .withColumn("data", parse_date("data")) \
    .dropDuplicates(["id_transacao"]) \
    .filter(col("id_transacao").isNotNull())

print(f"✅ Financeiro: {df_silver_financeiro.count()} registros limpos")

# ==============================================
# Salvando na camada Silver — Delta Lake
# ==============================================

tabelas_silver = {
    "silver_pacientes"             : df_silver_pacientes,
    "silver_atendimentos"          : df_silver_atendimentos,
    "silver_atendimentos_clinicos" : df_silver_atendimentos_clinicos,
    "silver_estoque"               : df_silver_estoque,
    "silver_financeiro"            : df_silver_financeiro
}

for nome, df in tabelas_silver.items():
    tabela = f"aria_health.{nome}"
    df.write \
      .format("delta") \
      .mode("overwrite") \
      .saveAsTable(tabela)
    print(f"✅ Silver salvo: {tabela}")

print("\n🥈 Camada Silver concluída com sucesso!")

