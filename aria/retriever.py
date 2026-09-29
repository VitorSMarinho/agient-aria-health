"""Retriever: junta embeddings + vector store num único ponto de acesso ao RAG."""

from aria.config import CONFIG
from aria.embeddings import embed_query
from aria.vectorstore import RetrievedChunk, get_vector_store


def retrieve(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    store = get_vector_store()
    query_embedding = embed_query(query)
    return store.search(query_embedding, top_k or CONFIG.top_k_retrieval)


def format_context(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "(nenhum documento relevante encontrado na base de conhecimento)"
    partes = [f"[Fonte: {c.source} | similaridade: {c.score:.2f}]\n{c.text}" for c in chunks]
    return "\n\n---\n\n".join(partes)
