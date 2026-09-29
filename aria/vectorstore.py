"""Vector store plugável: Supabase/pgvector em produção, JSON local em dev/eval/CI.

A troca é automática: se SUPABASE_URL e SUPABASE_KEY estiverem configurados,
usa Supabase; caso contrário cai para o LocalVectorStore, o que permite rodar
ingestão, retrieval e a suíte de evals sem depender de infraestrutura externa.
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass

import numpy as np
import requests

from aria.chunking import Chunk
from aria.config import CONFIG


@dataclass
class RetrievedChunk:
    text: str
    source: str
    score: float


class VectorStore(ABC):
    @abstractmethod
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...

    @abstractmethod
    def search(self, query_embedding: list[float], top_k: int) -> list[RetrievedChunk]: ...


class LocalVectorStore(VectorStore):
    """Armazena embeddings em um JSON local e faz similaridade de cosseno em memória."""

    def __init__(self, path: str = "data/vector_store.json"):
        self.path = path
        self._rows: list[dict] = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self._rows = json.load(f)

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        for chunk, embedding in zip(chunks, embeddings):
            self._rows.append({**asdict(chunk), "embedding": embedding})
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._rows, f, ensure_ascii=False)

    def clear(self) -> None:
        self._rows = []
        if os.path.exists(self.path):
            os.remove(self.path)

    def search(self, query_embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        if not self._rows:
            return []
        query = np.asarray(query_embedding, dtype=np.float32)
        query_norm = query / (np.linalg.norm(query) + 1e-8)

        scored = []
        for row in self._rows:
            vec = np.asarray(row["embedding"], dtype=np.float32)
            vec_norm = vec / (np.linalg.norm(vec) + 1e-8)
            score = float(np.dot(query_norm, vec_norm))
            scored.append((score, row))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            RetrievedChunk(text=row["text"], source=row["source"], score=score)
            for score, row in scored[:top_k]
        ]


class SupabaseVectorStore(VectorStore):
    """Usa duas funções RPC no Postgres (ver supabase/01-knowledge-base-pgvector.sql):

    - insert_document(content text, embedding vector, source text, chunk_index int)
    - match_documents(query_embedding vector, match_count int)
    """

    def __init__(self, url: str, key: str):
        self.url = url.rstrip("/")
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        for chunk, embedding in zip(chunks, embeddings):
            response = requests.post(
                f"{self.url}/rest/v1/rpc/insert_document",
                headers=self.headers,
                json={
                    "content": chunk.text,
                    "embedding": embedding,
                    "source": chunk.source,
                    "chunk_index": chunk.chunk_index,
                },
                timeout=30,
            )
            response.raise_for_status()

    def search(self, query_embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        response = requests.post(
            f"{self.url}/rest/v1/rpc/match_documents",
            headers=self.headers,
            json={"query_embedding": query_embedding, "match_count": top_k},
            timeout=30,
        )
        response.raise_for_status()
        return [
            RetrievedChunk(text=row["content"], source=row["source"], score=row["similarity"])
            for row in response.json()
        ]


def get_vector_store() -> VectorStore:
    if CONFIG.has_supabase:
        return SupabaseVectorStore(CONFIG.supabase_url, CONFIG.supabase_key)
    return LocalVectorStore()
