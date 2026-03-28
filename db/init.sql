CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id        SERIAL PRIMARY KEY,
    chunk_id  TEXT UNIQUE NOT NULL,
    url       TEXT NOT NULL,
    page      TEXT,
    section   TEXT,
    level     INTEGER,
    content   TEXT NOT NULL,
    embedding vector(768)
);

CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);