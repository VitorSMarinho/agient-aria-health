"""Ingestão da base de conhecimento (RAG): chunk -> embed -> upsert no vector store.

Uso:
    python scripts/ingest_knowledge_base.py            # usa Supabase se configurado, senão local
    python scripts/ingest_knowledge_base.py --local     # força o vector store local (dev/eval)
"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aria.chunking import chunk_markdown
from aria.embeddings import embed_texts
from aria.vectorstore import LocalVectorStore, get_vector_store


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true", help="força o vector store local")
    parser.add_argument("--source-dir", default="knowledge_base")
    args = parser.parse_args()

    store = LocalVectorStore() if args.local else get_vector_store()
    if isinstance(store, LocalVectorStore):
        store.clear()
        store = LocalVectorStore()

    files = sorted(glob.glob(os.path.join(args.source_dir, "*.md")))
    if not files:
        print(f"Nenhum arquivo .md encontrado em {args.source_dir}/")
        return

    total_chunks = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_markdown(text, source=os.path.basename(path))
        embeddings = embed_texts([c.text for c in chunks])
        store.add(chunks, embeddings)
        total_chunks += len(chunks)
        print(f"  {os.path.basename(path)}: {len(chunks)} chunks")

    print(f"\nIngestão concluída: {total_chunks} chunks de {len(files)} documentos.")


if __name__ == "__main__":
    main()
