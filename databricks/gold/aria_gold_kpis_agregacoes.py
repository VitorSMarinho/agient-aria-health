# ==============================================
# PROJETO ARIA — Agient
# Camada: GOLD | KPIs e Agregações
# Descrição: Dados agregados e prontos para
#            consumo pelos agentes e DataViz
# Autor: Vitor Marinho
# ==============================================

from pyspark.sql.functions import (
    col, count, avg, sum, max, min,
    when, lit, round, countDistinct,
    current_date, datediff
)
from pyspark.sql.types import IntegerType, DoubleType

spark.sql("USE aria_health")

print("✅ Imports e configuração carregados!")

# ==============================================
# Carregando tabelas da camada Silver
# ==============================================

tabelas_silver = [
    "silver_pacientes",
    "silver_atendimentos",
    "silver_atendimentos_clinicos",
    "silver_estoque",
    "silver_financeiro"
]

dfs = {}
for tabela in tabelas_silver:
    dfs[tabela] = spark.table(f"aria_health.{tabela}")
    print(f"📥 Carregado: {tabela} → {dfs[tabela].count()} registros")

print("\n🥈 Dados Silver prontos para agregação!")

# ==============================================
# GOLD — KPIs de Pacientes
# ==============================================

gold_kpi_pacientes = dfs["silver_pacientes"] \
    .groupBy("tipo_cancer", "estadiamento", "status_tratamento") \
    .agg(
        count("id_paciente").alias("total_pacientes"),
        round(avg("idade"), 1).alias("idade_media"),
        min("idade").alias("idade_minima"),
        max("idade").alias("idade_maxima"),
        countDistinct("convenio").alias("total_convenios"),
        countDistinct("medico_responsavel").alias("total_medicos")
    ) \
    .orderBy("tipo_cancer", "estadiamento")

gold_kpi_pacientes.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("aria_health.gold_kpi_pacientes")

print(f"✅ gold_kpi_pacientes: {gold_kpi_pacientes.count()} registros")

# ==============================================
# GOLD — KPIs de Atendimentos
# ==============================================

gold_kpi_atendimentos = dfs["silver_atendimentos"] \
    .groupBy("tipo_atendimento", "evolucao_quadro", "status_quadro") \
    .agg(
        count("id_atendimento").alias("total_atendimentos"),
        countDistinct("medico_responsavel").alias("total_medicos"),
        countDistinct("id_paciente").alias("total_pacientes_atendidos")
    ) \
    .orderBy("tipo_atendimento")

gold_kpi_atendimentos.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("aria_health.gold_kpi_atendimentos")

print(f"✅ gold_kpi_atendimentos: {gold_kpi_atendimentos.count()} registros")

# ==============================================
# GOLD — KPIs Clínicos por Médico
# ==============================================

gold_kpi_clinico = dfs["silver_atendimentos_clinicos"] \
    .groupBy("medico_responsavel", "evolucao_quadro", "status_quadro") \
    .agg(
        count("id_atendimento").alias("total_atendimentos"),
        countDistinct("id_paciente").alias("total_pacientes"),
        countDistinct("procedimento_realizado").alias("tipos_procedimentos"),
        countDistinct("medicacao_aplicada").alias("tipos_medicacoes")
    ) \
    .orderBy("medico_responsavel")

gold_kpi_clinico.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("aria_health.gold_kpi_clinico")

print(f"✅ gold_kpi_clinico: {gold_kpi_clinico.count()} registros")

# ==============================================
# GOLD — KPIs de Estoque
# ==============================================

gold_kpi_estoque = dfs["silver_estoque"] \
    .withColumn("status_estoque",
        when(col("quantidade_atual") <= 0, "Sem estoque")
        .when(col("quantidade_atual") < col("quantidade_minima"), "Crítico")
        .when(col("quantidade_atual") < col("quantidade_minima") * 1.5, "Atenção")
        .otherwise("Normal")
    ) \
    .withColumn("status_validade",
        when(datediff(col("data_validade"), current_date()) < 0, "Vencido")
        .when(datediff(col("data_validade"), current_date()) <= 30, "Vence em breve")
        .otherwise("OK")
    ) \
    .groupBy("categoria", "status_estoque", "status_validade") \
    .agg(
        count("id_item").alias("total_itens"),
        round(sum("valor_unitario"), 2).alias("valor_total_estoque"),
        round(avg("quantidade_atual"), 1).alias("quantidade_media")
    ) \
    .orderBy("status_estoque", "categoria")

gold_kpi_estoque.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("aria_health.gold_kpi_estoque")

print(f"✅ gold_kpi_estoque: {gold_kpi_estoque.count()} registros")

# ==============================================
# GOLD — KPIs Financeiros
# ==============================================

gold_kpi_financeiro = dfs["silver_financeiro"] \
    .groupBy("tipo", "categoria", "status_pagamento") \
    .agg(
        count("id_transacao").alias("total_transacoes"),
        round(sum("valor"), 2).alias("valor_total"),
        round(avg("valor"), 2).alias("valor_medio"),
        round(max("valor"), 2).alias("valor_maximo"),
        round(min("valor"), 2).alias("valor_minimo")
    ) \
    .orderBy("tipo", "categoria")

gold_kpi_financeiro.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("aria_health.gold_kpi_financeiro")

print(f"✅ gold_kpi_financeiro: {gold_kpi_financeiro.count()} registros")

# ==============================================
# Resumo final da camada Gold
# ==============================================

tabelas_gold = [
    "gold_kpi_pacientes",
    "gold_kpi_atendimentos",
    "gold_kpi_clinico",
    "gold_kpi_estoque",
    "gold_kpi_financeiro"
]

print("🥇 CAMADA GOLD — Resumo:\n")
for tabela in tabelas_gold:
    df = spark.table(f"aria_health.{tabela}")
    print(f"   ✅ {tabela}: {df.count()} registros")

print("\n🏆 Arquitetura Medallion completa!")
print("   Bronze → Silver → Gold ✅")