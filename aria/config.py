"""Configuração central do ARIA, lida a partir de variáveis de ambiente."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    groq_api_key: str | None
    supabase_url: str | None
    supabase_key: str | None
    llm_model: str
    embedding_model: str
    max_tool_iterations: int
    top_k_retrieval: int
    traces_path: str

    @property
    def has_supabase(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)


def load_config() -> Config:
    return Config(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
        llm_model=os.getenv("ARIA_LLM_MODEL", "openai/gpt-oss-120b"),
        embedding_model=os.getenv(
            "ARIA_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        ),
        max_tool_iterations=int(os.getenv("ARIA_MAX_TOOL_ITERATIONS", "4")),
        top_k_retrieval=int(os.getenv("ARIA_TOP_K", "4")),
        traces_path=os.getenv("ARIA_TRACES_PATH", "logs/aria_traces.jsonl"),
    )


CONFIG = load_config()
