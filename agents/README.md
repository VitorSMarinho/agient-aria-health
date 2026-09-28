# 🤖 Agentes ARIA — Agient

## O que é o ARIA?

O ARIA é um sistema multi-agent de inteligência clínica desenvolvido 
pela **Agient** para transformar dados hospitalares em decisões estratégicas.

---

## Agentes disponíveis

Todos os 5 agentes estão implementados em `aria/agents.py`, sobre o mesmo
loop de tool-calling (`aria/agent.py`) — a diferença entre eles é o system
prompt, o foco de análise e o papel de acesso pretendido.

| Agente | Descrição | Papel de acesso |
|---|---|---|
| `indicadores` | Análise de KPIs operacionais | Gestão operacional — **demo pública** (default da API) |
| `clinico` | Resumo e evolução clínica do paciente | Médicos autorizados |
| `financeiro` | Saúde financeira e anomalias | Diretoria e financeiro |
| `estoque` | Controle de medicamentos e criticidade | Farmácia e suprimentos |
| `estrategico` | Cruzamento de dados e insights priorizados | Liderança executiva |

Hoje o controle de acesso é apenas descritivo (o `slug` do agente é passado
no corpo do `POST /consultar`); RBAC de verdade (autenticação + permissão
por usuário) está no roadmap do projeto, não implementado ainda.

---

## 🟢 Teste ao vivo — Agente de Indicadores

O agente de indicadores operacionais é o default da API pública. Acesse e
faça sua pergunta:

👉 **[Acessar demo do ARIA](https://agient-aria-health.vercel.app)**

Pra testar qualquer um dos 5 agentes, chame a API diretamente:

```bash
curl -X POST https://agient-aria-health-conection.onrender.com/consultar \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Quantos itens estao em estoque critico?", "agente": "estoque"}'
```

---

## Arquitetura dos agentes

```
Databricks Gold (Delta Lake)          Base de conhecimento (RAG)
        ↓                                      ↓
Supabase (PostgreSQL)  ←──────────  Supabase (pgvector)
        ↓                                      ↓
              FastAPI (Backend) — aria/agents.py
                        ↓
        Agente ARIA (LangChain tool-calling + Groq)
                        ↓
              Interface Web (Next.js/Vercel)
```

---

> *"Dados são a matéria-prima. Inteligência é o produto."*
> — Agient