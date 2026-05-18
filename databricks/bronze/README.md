# 🥉 Camada Bronze — Ingestão Raw

## Sobre esta camada

A camada Bronze é a primeira etapa da arquitetura Medallion do **Projeto ARIA**.
Aqui os dados são ingeridos **sem transformação**, preservando o estado original
das fontes — garantindo rastreabilidade e auditabilidade completa.

---

## Fonte dos dados

Os dados são ingeridos diretamente do repositório GitHub via URL raw,
simulando um processo de ingestão de arquivos entregues por parceiros
ou sistemas legados do **Instituto Oncológico**.

| Arquivo | Registros | Colunas | Descrição |
|---|---|---|---|
| `pacientes.csv` | 50 | 10 | Cadastro de pacientes oncológicos |
| `atendimentos.csv` | 50 | 12 | Histórico de atendimentos |
| `atendimentos_clinicos.csv` | 50 | 12 | Evolução clínica por atendimento |
| `estoque.csv` | 50 | 10 | Controle de medicamentos e insumos |
| `financeiro.csv` | 51 | 10 | Movimentações financeiras |

---

## Tabelas geradas no Delta Lake
aria_health.bronze_pacientes
aria_health.bronze_atendimentos
aria_health.bronze_atendimentos_clinicos
aria_health.bronze_estoque
aria_health.bronze_financeiro

---

## Processo de ingestão
GitHub (CSV raw)
↓
Pandas (read_csv + detecção de separador)
↓
Spark DataFrame (createDataFrame)
↓
Delta Lake (saveAsTable — mode overwrite)
↓
Unity Catalog — aria_health.bronze_*

---

## Decisões técnicas

- **Formato Delta Lake** — permite versionamento, time travel e ACID transactions
- **Mode overwrite** — garante idempotência, reprocessamento seguro
- **Unity Catalog** — governança e controle de acesso centralizado
- **Detecção automática de separador** — resiliência a variações de formato CSV
- **Sem transformações** — dados preservados exatamente como recebidos

---

## Próxima etapa

➡️ [Camada Silver](../silver/README.md) — limpeza, padronização e validação dos dados