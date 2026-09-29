"""Camada de embeddings: modelo local via fastembed (ONNX, sem chave de API).

Multilíngue (PT-BR incluso) e leve o suficiente para rodar no free tier do Render,
ao contrário de sentence-transformers (que traz PyTorch como dependência).
"""

from functools import lru_cache

import numpy as np

from aria.config import CONFIG


@lru_cache(maxsize=1)
def _model():
    from fastembed import TextEmbedding

    return TextEmbedding(model_name=CONFIG.embedding_model)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = _model().embed(texts)
    return [np.asarray(v, dtype=np.float32).tolist() for v in vectors]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
