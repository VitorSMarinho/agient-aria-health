"""Chunking de documentos para ingestão no RAG."""

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    chunk_index: int


def chunk_markdown(text: str, source: str, chunk_size: int = 800, overlap: int = 120) -> list[Chunk]:
    """Divide o texto em blocos por parágrafo, respeitando um tamanho máximo.

    Simples de propósito: parágrafos curtos (como os do conhecimento do ARIA)
    não precisam de um text splitter recursivo mais sofisticado.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(paragraph) <= chunk_size:
            current = paragraph
        else:
            for i in range(0, len(paragraph), chunk_size - overlap):
                chunks.append(paragraph[i : i + chunk_size])
            current = ""
    if current:
        chunks.append(current)

    return [Chunk(text=c, source=source, chunk_index=i) for i, c in enumerate(chunks)]
