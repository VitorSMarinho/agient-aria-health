# 🥇 Camada Gold — KPIs e Agregações

## Sobre esta camada

A camada Gold é a etapa final da arquitetura Medallion do **Projeto ARIA**.
Aqui os dados limpos da camada Silver são agregados em KPIs e métricas
prontas para consumo — pelos agentes de IA, time de DataViz e área de negócios.

---

## O que foi feito nesta camada

| Transformação | Descrição |
|---|---|
| `groupBy()` | Agrupamento por dimensões de negócio |
| `agg()` | Cálculo de métricas: count, sum, avg, min, max |
| `when()` | Classificação inteligente de status de estoque e validade |
| `datediff()` | Cálculo de dias para vencimento de medicamentos |
| `round()` | Arredondamento de valores monetários e médias |
| `countDistinct()` | Contagem de valores únicos por dimensão |

---

## Tabelas geradas no Delta Lake
aria_health.gold_kpi_pacientes
aria_health.gold_kpi_atendimentos
aria_health.gold_kpi_clinico
aria_health.gold_kpi_estoque
aria_health.gold_kpi_financeiro

---

## KPIs por domínio

### 🧬 Pacientes
| KPI | Descrição |
|---|---|
| total_pacientes | Total por tipo de câncer e estadiamento |
| idade_media | Média de idade por grupo |
| idade_minima / maxima | Faixa etária por grupo |
| total_convenios | Convênios distintos atendidos |
| total_medicos | Médicos responsáveis por grupo |

### 📋 Atendimentos
| KPI | Descrição |
|---|---|
| total_atendimentos | Volume por tipo e evolução do quadro |
| total_medicos | Médicos envolvidos por categoria |
| total_pacientes_atendidos | Pacientes únicos atendidos |

### 🩺 Clínico
| KPI | Descrição |
|---|---|
| total_atendimentos | Atendimentos por médico e status |
| total_pacientes | Pacientes únicos por médico |
| tipos_procedimentos | Variedade de procedimentos realizados |
| tipos_medicacoes | Variedade de medicações aplicadas |

### 💊 Estoque
| KPI | Descrição |
|---|---|
| status_estoque | Classificação: Normal, Atenção, Crítico, Sem estoque |
| status_validade | Classificação: OK, Vence em breve, Vencido |
| valor_total_estoque | Valor total por categoria |
| quantidade_media | Quantidade média em estoque |

### 💰 Financeiro
| KPI | Descrição |
|---|---|
| total_transacoes | Volume de transações por tipo e categoria |
| valor_total | Soma total por grupo |
| valor_medio | Ticket médio por grupo |
| valor_maximo / minimo | Faixa de valores por grupo |

---

## Resultado desta camada

| Tabela Gold | Registros |
|---|---|
| gold_kpi_pacientes | 44 |
| gold_kpi_atendimentos | 38 |
| gold_kpi_clinico | 34 |
| gold_kpi_estoque | 18 |
| gold_kpi_financeiro | 22 |

---

## Processo desta camada
Delta Lake — aria_health.silver_*
↓
Leitura via spark.table()
↓
Agregações PySpark
(groupBy, agg, when, datediff, round)
↓
Delta Lake — aria_health.gold_kpi_*
(saveAsTable — mode overwrite)
↓
Disponível para:
├── Agentes ARIA (Claude API + LangChain)
├── Time de DataViz (dashboards)
└── Time de Negócios (decisões estratégicas)