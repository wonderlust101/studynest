-- An extension adds features to Postgres. pgvector adds a `vector` column type
-- for storing embeddings. IF NOT EXISTS makes this safe to run more than once.
CREATE EXTENSION IF NOT EXISTS vector;
