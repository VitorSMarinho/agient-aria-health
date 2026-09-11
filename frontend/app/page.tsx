"use client";

import { useState } from "react";
import {
  Activity,
  Boxes,
  LineChart,
  Send,
  Sparkles,
  Loader2,
} from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_ARIA_API_URL ?? "";

const FEATURES = [
  {
    icon: Activity,
    tag: "OPERAÇÕES",
    title: "Indicadores Operacionais",
    description:
      "Monitore ocupação, tempo médio de atendimento e produtividade clínica em tempo real.",
    gradient: "from-violet-500 to-blue-500",
  },
  {
    icon: Boxes,
    tag: "SUPRIMENTOS",
    title: "Análise de Estoque",
    description:
      "Identifique rupturas, vencimentos e otimize o consumo de insumos hospitalares.",
    gradient: "from-blue-500 to-cyan-400",
  },
  {
    icon: LineChart,
    tag: "FINANCEIRO",
    title: "Saúde Financeira",
    description:
      "Receita, glosas, ticket médio e margem por especialidade analisados de ponta a ponta.",
    gradient: "from-violet-500 to-fuchsia-500",
  },
];

export default function Home() {
  const [pergunta, setPergunta] = useState("");
  const [resposta, setResposta] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function consultarAria() {
    if (!pergunta.trim() || loading) return;

    if (!API_URL) {
      setError(
        "API do ARIA não configurada. Defina NEXT_PUBLIC_ARIA_API_URL no ambiente."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResposta("");

    try {
      const res = await fetch(`${API_URL}/consultar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pergunta }),
      });

      if (!res.ok) throw new Error(`Erro ${res.status}`);

      const data = await res.json();
      setResposta(data.resposta ?? "Sem resposta do ARIA.");
    } catch {
      setError("Não foi possível consultar o ARIA agora. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex flex-1 flex-col overflow-hidden">
      <div className="pointer-events-none absolute -top-40 -left-40 h-[32rem] w-[32rem] rounded-full bg-violet-700/25 blur-[120px]" />
      <div className="pointer-events-none absolute top-1/3 -right-40 h-[28rem] w-[28rem] rounded-full bg-cyan-500/15 blur-[120px]" />

      <main className="relative mx-auto flex w-full max-w-4xl flex-1 flex-col items-center px-6 py-20 sm:py-28">
        <div className="mb-8 flex items-center gap-2 rounded-full border border-card-border bg-card/80 px-4 py-1.5 text-sm text-muted">
          <Sparkles className="h-3.5 w-3.5 text-blue-400" />
          Powered by <span className="font-semibold text-foreground">Agient</span>
        </div>

        <h1 className="bg-gradient-to-b from-blue-400 to-indigo-500 bg-clip-text text-center text-7xl font-extrabold tracking-tight text-transparent sm:text-8xl">
          ARIA
        </h1>
        <p className="mt-4 max-w-xl text-center text-lg text-muted">
          Agente de Raciocínio e Inteligência em Análise Clínica
        </p>

        <div className="mt-14 grid w-full gap-4 sm:grid-cols-3">
          {FEATURES.map((feature) => (
            <div
              key={feature.title}
              className="rounded-2xl border border-card-border bg-card p-6"
            >
              <div
                className={`mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br ${feature.gradient}`}
              >
                <feature.icon className="h-5 w-5 text-white" />
              </div>
              <p className="mb-1 text-xs font-medium tracking-wide text-muted">
                {feature.tag}
              </p>
              <h3 className="mb-2 font-semibold text-foreground">
                {feature.title}
              </h3>
              <p className="text-sm leading-relaxed text-muted">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-8 w-full rounded-2xl border border-card-border bg-card p-6">
          <h2 className="mb-4 font-semibold text-foreground">
            Converse com o ARIA
          </h2>
          <div className="flex gap-3">
            <input
              value={pergunta}
              onChange={(e) => setPergunta(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && consultarAria()}
              placeholder="Faça uma pergunta ao ARIA..."
              className="flex-1 rounded-xl border border-card-border bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-blue-500/50"
            />
            <button
              onClick={consultarAria}
              disabled={loading}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-blue-500 px-5 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              Consultar ARIA
            </button>
          </div>

          <div className="mt-4 min-h-[7rem] rounded-xl border border-card-border bg-background p-4 text-sm leading-relaxed whitespace-pre-wrap text-muted">
            {error ? (
              <span className="text-red-400">{error}</span>
            ) : resposta ? (
              <span className="text-foreground">{resposta}</span>
            ) : (
              "A resposta do ARIA aparecerá aqui. Pergunte sobre indicadores, estoque ou desempenho financeiro."
            )}
          </div>
        </div>

        <p className="mt-10 max-w-xl text-center text-xs text-muted">
          O ARIA é um suporte à decisão baseado em dados. Não substitui o
          julgamento clínico médico.
        </p>
      </main>

      <footer className="relative border-t border-card-border py-6 text-center text-xs text-muted">
        Desenvolvido por Agient
      </footer>
    </div>
  );
}
