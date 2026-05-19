# 🥈 Camada Silver — Transformação e Limpeza

## Sobre esta camada

A camada Silver é a segunda etapa da arquitetura Medallion do **Projeto ARIA**.
Aqui os dados brutos da camada Bronze passam por transformações de qualidade:
padronização, limpeza, remoção de duplicatas e validação de tipos — garantindo
dados confiáveis para análises e consumo pelos agentes de IA.

---

## O que foi feito nesta camada

| Transformação | Descrição |
|---|---|
| `trim()` | Remove espaços em branco no início e fim dos textos |
| `upper()` | Padroniza campos categóricos em maiúsculo |
| `parse_date()` | Trata múltiplos formatos de data com `try_to_date` |
| `cast(IntegerType)` | Converte campos numéricos inteiros corretamente |
| `cast(DoubleType)` | Converte campos de valor monetário corretamente |
| `dropDuplicates()` | Remove registros duplicados por chave primária |
| `filter isNotNull` | Remove registros sem chave primária |

---

## Tabelas geradas no Delta Lake
aria_health.silver_pacientes
aria_health.silver_atendimentos
aria_health.silver_atendimentos_clinicos
aria_health.silver_estoque
aria_health.silver_financeiro

---

## Resultado das transformações

| Tabela | Bronze | Silver | Registros removidos |
|---|---|---|---|
| pacientes | 50 | 50 | 0 |
| atendimentos | 50 | 49 | 1 duplicata |
| atendimentos_clinicos | 50 | 49 | 1 duplicata |
| estoque | 50 | 50 | 0 |
| financeiro | 51 | 50 | 1 nulo |

---

## Decisão técnica — parse_date

Os CSVs chegaram com formatos de data inconsistentes:
2024-03-10  →  formato ISO padrão
23-05-24    →  formato abreviado
28-02-23    →  formato abreviado

A solução foi criar uma função `parse_date` usando `try_to_date` com
múltiplos formatos em cascata via `coalesce` — tornando a ingestão
resiliente a variações sem quebrar o pipeline.

---

## Processo desta camada
Delta Lake — aria_health.bronze_*
↓
Leitura via spark.table()
↓
Transformações PySpark
(trim, upper, cast, parse_date, dropDuplicates, filter)
↓
Delta Lake — aria_health.silver_*
(saveAsTable — mode overwrite)

---

## Próxima etapa

➡️ [Camada Gold](../gold/README.md) — agregações, KPIs e métricas prontas para consumo