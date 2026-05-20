# ⚙️ Databricks Architecture — ARIA

Esta documentação apresenta a arquitetura de engenharia de dados do projeto ARIA utilizando:

- Databricks Workflows
- Apache Spark
- Arquitetura Medallion
- Unity Catalog
- Processamento distribuído
- Governança analítica

---

# 🏗️ Arquitetura Medallion

A plataforma ARIA utiliza o padrão Medallion para organizar os dados em camadas progressivas de refinamento.

<p align="center">
  <img src="../img/medallion.svg" width="80%" alt="Arquitetura Medallion">
</p>

---

# 🗄️ Unity Catalog

Todas as tabelas são catalogadas e rastreadas automaticamente utilizando Unity Catalog.

<p align="center">
  <img src="../img/unity_catalog.svg" width="90%" alt="Unity Catalog">
</p>

---

# ⚙️ Workflow Orquestrado

O pipeline executa automaticamente todas as etapas da arquitetura.

<p align="center">
  <img src="../img/job_run.svg" width="100%" alt="Workflow Databricks">
</p>

---

# ✅ Pipeline Executado com Sucesso

Execução finalizada com sucesso após validações da camada Gold.

<p align="center">
  <img src="../img/job_success.svg" width="100%" alt="Pipeline Success">
</p>

---

# 📚 Documentações Complementares

| Documento | Descrição |
|---|---|
| [Pipeline Workflow](pipeline_workflow_job/README.md) | Orquestração detalhada do workflow |