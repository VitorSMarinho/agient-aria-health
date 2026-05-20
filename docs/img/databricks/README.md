# ⚙️ Documentação Técnica — Pipeline Databricks

Esta documentação detalha a orquestração do fluxo de dados do **Projeto ARIA**, construída utilizando **Databricks Workflows** e **Apache Spark**.

---

## 🎯 Objetivo do Workflow

Automatizar a arquitetura Medallion garantindo que:
- Os **Agentes de IA** do ARIA consumam dados validados
- Os **painéis de BI** sempre reflitam a versão mais atual
- Não haja intervenção manual no pipeline
- Todos os dados sejam auditáveis e rastreáveis

---

## 🏗️ Arquitetura Medallion

### Estrutura de Pastas

<p align="center">
  <img src="images/databricks/medallion.png" width="70%" alt="Estrutura Medallion">
</p>
/FileStore/tables/aria/
├── bronze/ # 🥉 Dados brutos (imutáveis)
│ ├── pacientes/
│ ├── atendimentos/
│ ├── estoque/
│ └── financeiro/
│
├── silver/ # 🥈 Dados limpos e padronizados
│ ├── pacientes/
│ ├── atendimentos/
│ ├── estoque/
│ └── financeiro/
│
└── gold/ # 🥇 KPIs e agregações
├── kpi_clinico/
├── kpi_operacional/
└── kpi_financeiro/

text


---

## 🗄️ Unity Catalog — Governança

<p align="center">
  <img src="images/databricks/catalog.png" width="90%" alt="Unity Catalog">
</p>

### Tabelas Catalogadas

| Schema | Tabela | Descrição |
|--------|--------|-----------|
| `bronze` | `pacientes_raw` | Dados brutos de pacientes |
| `bronze` | `atendimentos_raw` | Histórico completo de atendimentos |
| `bronze` | `estoque_raw` | Movimentações de estoque |
| `bronze` | `financeiro_raw` | Transações financeiras |
| `silver` | `pacientes_clean` | Pacientes validados (CPF, data nascimento) |
| `silver` | `atendimentos_clean` | Atendimentos com timestamps corretos |
| `silver` | `estoque_clean` | Estoque com validades futuras |
| `silver` | `financeiro_clean` | Financeiro sem duplicatas |
| `gold` | `kpi_volume_atendimentos` | Agregação por período |
| `gold` | `kpi_inadimplencia` | Análise de convênios |
| `gold` | `kpi_estoque_critico` | Medicamentos abaixo do mínimo |

---

## 🔄 Fluxo do Workflow (DAG)

### 1. 🥉 Camada Bronze (Ingestion)

**Notebooks:**
- `bronze/ingest_pacientes.py`
- `bronze/ingest_atendimentos.py`
- `bronze/ingest_estoque.py`
- `bronze/ingest_financeiro.py`

**Responsabilidade:**
- Leitura direta dos arquivos CSV
- Validação de schema básico
- Append only (dados imutáveis)
- Registro de metadata (timestamp de ingestão)

**Tecnologia:** PySpark com schema enforcement

---

### 2. 🥈 Camada Silver (Transformation)

**Dependência:** ✅ Sucesso da camada Bronze

**Notebooks:**
- `silver/clean_pacientes.py`
- `silver/clean_atendimentos.py`
- `silver/clean_estoque.py`
- `silver/clean_financeiro.py`

**Transformações aplicadas:**

```python
# Exemplo: Limpeza de pacientes
df_silver = (
    df_bronze
    .dropDuplicates(["cpf"])
    .filter(col("cpf").isNotNull())
    .withColumn("cpf_hash", sha2(col("cpf"), 256))  # LGPD
    .withColumn("data_nascimento", to_date(col("data_nascimento")))
    .filter(col("data_nascimento") < current_date())
)
Validações:

Remoção de duplicatas
Tratamento de nulos
Mascaramento de dados sensíveis (LGPD)
Conversão de tipos de dados
Validação de regras de negócio
3. 🥇 Camada Gold (KPI Generation)
Dependência: ✅ Sucesso da camada Silver

Notebooks:

gold/kpi_clinico.py
gold/kpi_operacional.py
gold/kpi_financeiro.py
Métricas geradas:

KPI	Descrição	Agregação
Volume de Atendimentos	Quantidade por período/unidade	GROUP BY data, unidade
Taxa de Ocupação	Percentual de agenda preenchida	COUNT(agendados) / capacidade
Inadimplência	Percentual por convênio	SUM(atraso) / total_faturado
Estoque Crítico	Medicamentos abaixo do mínimo	FILTER(qtd < estoque_minimo)
Custo por Atendimento	Média de custos	AVG(valor_procedimento)
4. ✅ Gold Validation Layer
Dependência: ✅ Sucesso da camada Gold

Notebook: gold/data_quality_check.py

Validações executadas:

Python

# Exemplo: Validação de qualidade
assert df_kpi_financeiro.filter(col("receita") < 0).count() == 0, \
    "❌ Erro: Receita negativa detectada"

assert df_atendimentos.filter(col("paciente_id").isNull()).count() == 0, \
    "❌ Erro: Atendimento sem paciente vinculado"

assert df_estoque.filter(col("validade") < current_date()).count() == 0, \
    "❌ Erro: Medicamentos vencidos no estoque ativo"
Se todas as validações passarem, os dados são liberados para o Supabase.

🚀 Execução do Workflow
Job em Execução
<p align="center"> <img src="images/pipeline/job_run.png" width="100%" alt="Job rodando"> </p>
Características:

Paralelização automática das tarefas independentes
Retry automático em caso de falha transitória
Logs detalhados de cada etapa
Monitoramento de performance em tempo real
Job Concluído com Sucesso
<p align="center"> <img src="images/pipeline/job_success.png" width="100%" alt="Job concluído"> </p>
Resultado:

✅ Todas as 4 camadas executadas
✅ Dados validados e prontos para consumo
✅ Lineage registrado no Unity Catalog
✅ Agentes de IA podem ser acionados
🛠️ Configuração do Workflow
Cluster Configuration
YAML

Cluster Mode: Single Node (Databricks Community)
Runtime: 13.3 LTS (Scala 2.12, Spark 3.4.1)
Driver: 15.3 GB Memory, 2 Cores
Auto Termination: 120 minutes
Schedule
text

Trigger: Manual (demonstração)
Produção: Cron Schedule (diário às 2h AM)
Notifications
text

On Success: Email para time de dados
On Failure: Email + Slack alert
📊 Métricas de Performance
Etapa	Tempo Médio	Dados Processados
Bronze Ingestion	~2 min	4 arquivos CSV
Silver Transformation	~3 min	~50k registros
Gold KPI Generation	~2 min	12 KPIs calculados
Validation Layer	~1 min	15 testes executados
Total	~8 min	Pipeline completo
🔗 Próximos Passos
 Migrar para Delta Lake (ACID transactions)
 Implementar Streaming com Auto Loader
 Adicionar Unity Catalog com controle granular de acesso
 Configurar alertas automáticos via Databricks SQL
 Integrar com dbt para transformações mais complexas
📚 Referências
Databricks Workflows Documentation
Medallion Architecture
Unity Catalog
⬅️ Voltar para a documentação principal