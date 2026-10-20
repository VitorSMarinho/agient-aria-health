"use client";

import { useEffect, useState } from "react";
import {
  Activity,
  Boxes,
  LineChart,
  Send,
  Sparkles,
  Loader2,
} from "lucide-react";

const API_URL =
  process.env.NEXT_PUBLIC_ARIA_API_URL ??
  "https://agient-aria-health-conection.onrender.com";

type Lang = "pt" | "en";

const COPY = {
  pt: {
    badge: "Projeto de portfólio · dados fictícios",
    subtitle: "Agente de Raciocínio e Inteligência em Análise Clínica",
    features: [
      {
        tag: "OPERAÇÕES",
        title: "Indicadores Operacionais",
        description:
          "Monitore ocupação, tempo médio de atendimento e produtividade clínica em tempo real.",
      },
      {
        tag: "SUPRIMENTOS",
        title: "Análise de Estoque",
        description:
          "Identifique rupturas, vencimentos e otimize o consumo de insumos hospitalares.",
      },
      {
        tag: "FINANCEIRO",
        title: "Saúde Financeira",
        description:
          "Receita, glosas, ticket médio e margem por especialidade analisados de ponta a ponta.",
      },
    ],
    chatTitle: "Converse com o ARIA",
    placeholder: "Faça uma pergunta ao ARIA...",
    button: "Consultar ARIA",
    empty:
      "A resposta do ARIA aparecerá aqui. Pergunte sobre indicadores, estoque ou desempenho financeiro.",
    noAnswer: "Sem resposta do ARIA.",
    noApi:
      "API do ARIA não configurada. Defina NEXT_PUBLIC_ARIA_API_URL no ambiente.",
    error:
      "Não foi possível consultar o ARIA agora. O servidor gratuito pode levar até um minuto para acordar; tente novamente.",
    disclaimer:
      "O ARIA é um suporte à decisão baseado em dados. Não substitui o julgamento clínico médico.",
    footer: "Desenvolvido por",
    langLabel: "Idioma",
  },
  en: {
    badge: "Portfolio project · fictional data",
    subtitle: "Reasoning and Intelligence Agent for Clinical Analytics",
    features: [
      {
        tag: "OPERATIONS",
        title: "Operational Indicators",
        description:
          "Track occupancy, average service time and clinical productivity in real time.",
      },
      {
        tag: "SUPPLY",
        title: "Inventory Analysis",
        description:
          "Spot stockouts and expiring items, and optimize the use of hospital supplies.",
      },
      {
        tag: "FINANCE",
        title: "Financial Health",
        description:
          "Revenue, claim denials, average ticket and margin by specialty, analyzed end to end.",
      },
    ],
    chatTitle: "Talk to ARIA",
    placeholder: "Ask ARIA a question...",
    button: "Ask ARIA",
    empty:
      "ARIA's answer will appear here. Ask about indicators, inventory or financial performance.",
    noAnswer: "No answer from ARIA.",
    noApi: "ARIA API is not configured. Set NEXT_PUBLIC_ARIA_API_URL in the environment.",
    error:
      "Could not reach ARIA right now. The free server can take up to a minute to wake up; please try again.",
    disclaimer:
      "ARIA is a data-driven decision support tool. It does not replace medical clinical judgment.",
    footer: "Built by",
    langLabel: "Language",
  },
} as const;

const FEATURE_STYLE = [
  { icon: Activity, gradient: "from-violet-500 to-blue-500" },
  { icon: Boxes, gradient: "from-blue-500 to-cyan-400" },
  { icon: LineChart, gradient: "from-violet-500 to-fuchsia-500" },
];

export default function Home() {
  const [lang, setLang] = useState<Lang>("pt");
  const [pergunta, setPergunta] = useState("");
  const [resposta, setResposta] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const t = COPY[lang];

  // ?lang=en no link tem prioridade; senão vale a última escolha do visitante
  useEffect(() => {
    const fromUrl = new URLSearchParams(window.location.search).get("lang");
    let saved: string | null = null;
    try {
      saved = localStorage.getItem("aria-lang");
    } catch {}
    const initial = fromUrl ?? saved;
    if (initial === "en" || initial === "pt") setLang(initial);
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang === "en" ? "en" : "pt-BR";
  }, [lang]);

  function changeLang(next: Lang) {
    setLang(next);
    setResposta("");
    setError("");
    try {
      localStorage.setItem("aria-lang", next);
    } catch {}
    const url = new URL(window.location.href);
    url.searchParams.set("lang", next);
    window.history.replaceState(null, "", url);
  }

  async function consultarAria() {
    if (!pergunta.trim() || loading) return;

    if (!API_URL) {
      setError(t.noApi);
      return;
    }

    setLoading(true);
    setError("");
    setResposta("");

    try {
      const res = await fetch(`${API_URL}/consultar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pergunta, idioma: lang }),
      });

      if (!res.ok) throw new Error(`Erro ${res.status}`);

      const data = await res.json();
      setResposta(data.resposta ?? t.noAnswer);
    } catch {
      setError(t.error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex flex-1 flex-col overflow-hidden">
      <div className="pointer-events-none absolute -top-40 -left-40 h-[32rem] w-[32rem] rounded-full bg-violet-700/25 blur-[120px]" />
      <div className="pointer-events-none absolute top-1/3 -right-40 h-[28rem] w-[28rem] rounded-full bg-cyan-500/15 blur-[120px]" />

      <div className="relative mx-auto flex w-full max-w-4xl justify-end px-6 pt-6">
        <div
          role="group"
          aria-label={t.langLabel}
          className="flex rounded-full border border-card-border bg-card/80 p-1 text-xs font-medium"
        >
          {(["pt", "en"] as const).map((code) => (
            <button
              key={code}
              type="button"
              onClick={() => changeLang(code)}
              aria-pressed={lang === code}
              lang={code === "en" ? "en" : "pt-BR"}
              className={`rounded-full px-3 py-1 transition-colors ${
                lang === code
                  ? "bg-foreground text-background"
                  : "text-muted hover:text-foreground"
              }`}
            >
              {code.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <main className="relative mx-auto flex w-full max-w-4xl flex-1 flex-col items-center px-6 py-14 sm:py-20">
        <div className="mb-8 flex items-center gap-2 rounded-full border border-card-border bg-card/80 px-4 py-1.5 text-sm text-muted">
          <Sparkles className="h-3.5 w-3.5 text-blue-400" />
          {t.badge}
        </div>

        <h1 className="bg-gradient-to-b from-blue-400 to-indigo-500 bg-clip-text text-center text-7xl font-extrabold tracking-tight text-transparent sm:text-8xl">
          ARIA
        </h1>
        <p className="mt-4 max-w-xl text-center text-lg text-muted">
          {t.subtitle}
        </p>

        <div className="mt-14 grid w-full gap-4 sm:grid-cols-3">
          {t.features.map((feature, i) => {
            const { icon: Icon, gradient } = FEATURE_STYLE[i];
            return (
              <div
                key={feature.tag}
                className="rounded-2xl border border-card-border bg-card p-6"
              >
                <div
                  className={`mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br ${gradient}`}
                >
                  <Icon className="h-5 w-5 text-white" />
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
            );
          })}
        </div>

        <div className="mt-8 w-full rounded-2xl border border-card-border bg-card p-6">
          <h2 className="mb-4 font-semibold text-foreground">{t.chatTitle}</h2>
          <div className="flex gap-3">
            <input
              value={pergunta}
              onChange={(e) => setPergunta(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && consultarAria()}
              placeholder={t.placeholder}
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
              {t.button}
            </button>
          </div>

          <div className="mt-4 min-h-[7rem] rounded-xl border border-card-border bg-background p-4 text-sm leading-relaxed whitespace-pre-wrap text-muted">
            {error ? (
              <span className="text-red-400">{error}</span>
            ) : resposta ? (
              <span className="text-foreground">{resposta}</span>
            ) : (
              t.empty
            )}
          </div>
        </div>

        <p className="mt-10 max-w-xl text-center text-xs text-muted">
          {t.disclaimer}
        </p>
      </main>

      <footer className="relative border-t border-card-border py-6 text-center text-xs text-muted">
        {t.footer}{" "}
        <a
          href="https://vitormarinho.vercel.app"
          target="_blank"
          rel="noopener noreferrer"
          className="text-foreground underline-offset-4 hover:underline"
        >
          Vitor Marinho | AI &amp; Data Engineer
        </a>
      </footer>
    </div>
  );
}
