## ⚙️ Pipeline Orquestrado — Databricks Workflows

O ARIA utiliza workflows orquestrados no Databricks para automatizar toda a jornada de dados da plataforma, garantindo qualidade e rastreabilidade desde a ingestão até a camada analítica.

---

### 🔄 Fluxo Automatizado

O pipeline é executado em **4 etapas sequenciais**:

1. **🥉 Bronze Ingestion** → Ingestão de dados brutos sem transformação
2. **🥈 Silver Transformation** → Limpeza, padronização e validação
3. **🥇 Gold KPI Generation** → Agregação de métricas clínicas e operacionais
4. **✅ Gold Validation Layer** → Auditoria de qualidade dos dados

---

### 📊 Arquitetura Medallion

A estrutura de dados segue o padrão **Medallion Architecture** com camadas progressivas de refinamento:

<p align="center">
  <img src="docs/img/medallion.svg" width="80%" alt="Estrutura de pastas Medallion">
  <br>
  <em>Organização física das camadas Bronze, Silver e Gold no Databricks</em>
</p>

---

### 🗄️ Unity Catalog — Governança de Dados

Todas as tabelas são catalogadas e rastreadas pelo **Unity Catalog**, garantindo lineage automático e auditoria completa:

<p align="center">
  <img src="docs/img/Catalog.svg" width="90%" alt="Unity Catalog - Tabelas ARIA">
>>>>>>> 19f2660b53f60cf79c4675d2fba2e77ed22deb01
  <br>
  <em>Visão completa das tabelas nas camadas Bronze, Silver e Gold</em>
</p>

---

### 🚀 Execução do Workflow

O workflow orquestra todos os notebooks de forma automatizada, com dependências claras entre as tarefas:

<p align="center">
  <img src="docs/img/job_run.svg" width="100%" alt="Databricks Job em execução">
  <br>
  <em>Pipeline em execução — processamento distribuído com Apache Spark</em>
</p>

---

### ✅ Pipeline Concluído com Sucesso

Após a validação final, o pipeline confirma que todos os dados estão prontos para consumo:

<p align="center">
  <img src="docs/img/job_success.svg" width="100%" alt="Job concluído com sucesso">
  <br>
  <em>Todas as etapas executadas com sucesso ✓</em>
</p>

---

### 🛠️ Recursos Implementados

| Recurso | Descrição |
|---------|-----------|
| **Arquitetura Medallion** | Bronze → Silver → Gold com separação lógica |
| **Orquestração de Notebooks** | DAG com dependências entre tarefas |
| **Processamento Distribuído** | Apache Spark para escala horizontal |
| **Data Lineage Automático** | Rastreabilidade completa via Unity Catalog |
| **Governança Analítica** | Controle de acesso e auditoria |
| **Validação de Qualidade** | Testes automatizados antes da camada Gold |
| **Escalabilidade** | Pronto para processar Big Data |

---

> 📖 **Quer ver os detalhes técnicos?**  
> Confira a [Documentação Completa do Pipeline](docs/databricks/README.md)
