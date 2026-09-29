-- ARIA: Base de conhecimento vetorial (RAG) + tabela de observabilidade
-- Rodar manualmente no SQL Editor do Supabase do projeto ARIA.
-- Pré-requisito: extensão pgvector disponível (padrão nos projetos Supabase).

create extension if not exists vector;

-- ---------------------------------------------------------------------
-- Tabela de documentos (chunks) da base de conhecimento do ARIA
-- ---------------------------------------------------------------------
create table if not exists knowledge_base (
    id bigint generated always as identity primary key,
    content text not null,
    source text not null,
    chunk_index int not null default 0,
    embedding vector(384) not null,
    created_at timestamptz not null default now()
);

-- Índice para busca por similaridade (cosine distance)
create index if not exists knowledge_base_embedding_idx
    on knowledge_base
    using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);

-- ---------------------------------------------------------------------
-- RPC: inserir um chunk já embedado (usado pelo script de ingestão)
-- ---------------------------------------------------------------------
create or replace function insert_document(
    content text,
    embedding vector(384),
    source text,
    chunk_index int
)
returns void
language sql
as $$
    insert into knowledge_base (content, embedding, source, chunk_index)
    values (content, embedding, source, chunk_index);
$$;

-- ---------------------------------------------------------------------
-- RPC: busca semântica (top-k por similaridade de cosseno)
-- ---------------------------------------------------------------------
create or replace function match_documents(
    query_embedding vector(384),
    match_count int default 4
)
returns table (
    content text,
    source text,
    similarity float
)
language sql
stable
as $$
    select
        knowledge_base.content,
        knowledge_base.source,
        1 - (knowledge_base.embedding <=> query_embedding) as similarity
    from knowledge_base
    order by knowledge_base.embedding <=> query_embedding
    limit match_count;
$$;

-- ---------------------------------------------------------------------
-- Observabilidade: traço de cada chamada ao agente (tokens, latência, tools)
-- ---------------------------------------------------------------------
create table if not exists agent_traces (
    id bigint generated always as identity primary key,
    agent text not null,
    question text not null,
    answer text,
    tool_calls jsonb not null default '[]'::jsonb,
    input_tokens int,
    output_tokens int,
    latency_ms int,
    created_at timestamptz not null default now()
);

-- RLS: leitura/escrita apenas via service_role (chamado pelo backend, nunca pelo frontend)
alter table knowledge_base enable row level security;
alter table agent_traces enable row level security;
