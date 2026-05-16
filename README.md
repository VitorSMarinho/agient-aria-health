# 🧬 ARIA — Agente de Raciocínio e Inteligência em Análise Clínica

> **Agient** | Agentes · Inteligência · Enterprise

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Stack](https://img.shields.io/badge/stack-Databricks%20%7C%20Claude%20AI%20%7C%20Supabase-blue)
![Setor](https://img.shields.io/badge/setor-Sa%C3%BAde%20%7C%20Oncologia-red)
![Método](https://img.shields.io/badge/m%C3%A9todo-ARIA-brightgreen)

---

## 🎯 Sobre o Projeto

O **Projeto ARIA** é uma solução de inteligência de dados desenvolvida pela **Agient** para transformar a operação de centros oncológicos brasileiros.

A maioria dos hospitais e clínicas no Brasil possui dados valiosos espalhados em planilhas, sistemas legados e arquivos isolados — sem estrutura, sem governança e sem inteligência. O resultado: decisões lentas, desperdício de recursos, atendimento comprometido.

O ARIA resolve isso. Com uma arquitetura moderna de dados combinada a agentes de IA, transformamos dados brutos em inteligência clínica e operacional — auditável, escalável e acessível para todos os times.

---

## 🏥 Contexto — Cliente Fictício

**Instituto Oncológico** — centro oncológico de médio porte com 3 unidades, 80 médicos e mais de 200 atendimentos/dia.

**Desafios identificados:**
- Dados de pacientes, estoque e financeiro em silos isolados
- Sem visibilidade de indicadores em tempo real
- Dificuldade em auditar processos e decisões clínicas
- Time médico sem acesso rápido a análises e literatura atualizada

**O que o ARIA entrega:**
- Organização e governança de todos os dados da instituição
- Melhoria de performance de entrega médica e atendimento
- Controle inteligente de estoque e financeiro
- Estratégias baseadas em dados para evolução contínua

---

## 🏗️ Arquitetura da Solução

```
📁 Fontes de Dados (CSV)
    pacientes.csv · atendimentos.csv · estoque.csv · financeiro.csv
            │
            ▼
🔶 DATABRICKS — Arquitetura Medallion
    ├── 🥉 Bronze  → Ingestão dos dados brutos (sem transformação)
    ├── 🥈 Silver  → Limpeza, padronização e validação
    └── 🥇 Gold    → Agregações, KPIs e métricas prontas para consumo
            │
            ▼
🤖 ARIA — Agentes de IA (Claude API + LangChain)
    ├── Agente Clínico       → Análise de indicadores de atendimento
    ├── Agente Financeiro    → Controle e anomalias financeiras
    ├── Agente de Estoque    → Monitoramento e alertas de insumos
    └── Agente Estratégico   → Insights e recomendações de melhoria
            │
            ▼
🗄️ SUPABASE — Camada de Disponibilização
    ├── Time de Data Viz     → Dashboards e painéis gerenciais
    └── Time de Negócios     → Decisões estratégicas auditáveis
```

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Função |
|---|---|---|
| Processamento | **Databricks Community** | Pipeline de dados + Medallion |
| Linguagem | **Python + PySpark** | Transformações e lógica |
| Agentes de IA | **LangChain + CrewAI** | Orquestração dos agentes |
| LLM | **Claude API (Anthropic)** | Raciocínio e análise clínica |
| Banco de Dados | **Supabase (PostgreSQL)** | Camada Gold + APIs |
| Versionamento | **Git + GitHub** | Controle e colaboração |
| IDE | **VS Code** | Desenvolvimento local |

> 💡 **Filosofia do projeto:** 100% em modo free/gratuito — provando que com as ferramentas certas, pequenas equipes entregam soluções enterprise.

---

## 📁 Estrutura do Repositório

```
agient-aria-health/
│
├── 📂 data/
│   ├── raw/                  # CSVs originais (dados fictícios)
│   └── samples/              # Amostras para testes
│
├── 📂 databricks/
│   ├── bronze/               # Notebooks de ingestão
│   ├── silver/               # Notebooks de limpeza
│   └── gold/                 # Notebooks de agregação e KPIs
│
├── 📂 agents/
│   ├── aria_clinico.py       # Agente de análise clínica
│   ├── aria_financeiro.py    # Agente financeiro
│   ├── aria_estoque.py       # Agente de estoque
│   └── aria_estrategico.py   # Agente de estratégia
│
├── 📂 supabase/
│   └── schema.sql            # Estrutura do banco de dados
│
├── 📂 docs/
│   └── arquitetura.md        # Documentação técnica detalhada
│
├── .env.example              # Variáveis de ambiente necessárias
├── requirements.txt          # Dependências do projeto
└── README.md
```

---

## 🚀 Roadmap do Projeto

- [x] Definição da arquitetura e stack
- [ ] Geração dos datasets fictícios
- [ ] Pipeline Bronze no Databricks
- [ ] Pipeline Silver no Databricks
- [ ] Pipeline Gold no Databricks
- [ ] Agente Clínico (ARIA v1)
- [ ] Agente Financeiro
- [ ] Agente de Estoque
- [ ] Agente Estratégico
- [ ] Integração com Supabase
- [ ] Documentação completa

---

## 💡 Método ARIA

O **ARIA** não é apenas um projeto — é um método replicável desenvolvido pela **Agient** para transformar dados em inteligência em qualquer setor.

Após saúde, o método será aplicado em:
- 🌱 Setor Agrícola
- 💰 Setor Financeiro
- 🍽️ Setor Alimentício
- ⚡ Setor de Energia

---

## 👨‍💻 Autor

**Vitor Marinho**
Engenheiro de Dados | AI Engineer | Fundador da Agient

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vitor%20Marinho-blue)](https://www.linkedin.com/in/vitor-marinho/)
[![GitHub](https://img.shields.io/badge/GitHub-VitorSMarinho-black)](https://github.com/VitorSMarinho)

---

> *"Com as ferramentas certas e o problema certo, pequenas equipes mudam setores inteiros."*
> — Agient
