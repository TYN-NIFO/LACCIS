-- ================================================================
-- LACCIS – Add missing tables to Neon
-- Run this in Neon SQL Editor if clause_embeddings and
-- clause_suggestions were not created by the main schema script.
-- ================================================================

-- Step 1: Enable the vector extension (required for clause_embeddings)
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Use dedicated schema only
CREATE SCHEMA IF NOT EXISTS laccis;
SET search_path TO laccis;

-- Step 3: Create the sequence for clause_embeddings auto-increment id
CREATE SEQUENCE IF NOT EXISTS laccis.clause_embeddings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- Step 4: clause_embeddings (pgvector table)
CREATE TABLE IF NOT EXISTS laccis.clause_embeddings (
    id          integer     NOT NULL DEFAULT nextval('laccis.clause_embeddings_id_seq'::regclass),
    clause_id   text        NOT NULL,
    clause      text        NOT NULL,
    content_id  text        NOT NULL,
    content     text        NOT NULL,
    embedding   vector(384),
    document    text,
    document_id text,
    created_at  timestamptz DEFAULT now(),
    page_number integer,
    CONSTRAINT clause_embeddings_pkey           PRIMARY KEY (id),
    CONSTRAINT clause_embeddings_content_id_key UNIQUE (content_id)
);

CREATE INDEX IF NOT EXISTS idx_clause_embeddings_clause     ON laccis.clause_embeddings(clause);
CREATE INDEX IF NOT EXISTS idx_clause_embeddings_content_id ON laccis.clause_embeddings(content_id);

-- Step 5: clause_suggestions
CREATE TABLE IF NOT EXISTS laccis.clause_suggestions (
    id             text        NOT NULL,
    clause_id      text        NOT NULL,
    clause         text        NOT NULL,
    content_id     text        NOT NULL,
    content        text        NOT NULL,
    page_number    integer     NOT NULL DEFAULT 1,
    document       text        NOT NULL,
    document_id    text,
    change_type    text        NOT NULL CHECK (change_type = ANY (ARRAY['insert'::text, 'delete'::text, 'replace'::text])),
    original_text  text        NOT NULL,
    suggested_text text        NOT NULL DEFAULT ''::text,
    author         text        NOT NULL,
    timestamp      timestamptz NOT NULL DEFAULT now(),
    status         text        NOT NULL DEFAULT 'pending'::text CHECK (status = ANY (ARRAY['pending'::text, 'accepted'::text, 'rejected'::text])),
    CONSTRAINT clause_suggestions_pkey             PRIMARY KEY (id),
    CONSTRAINT clause_suggestions_document_id_fkey FOREIGN KEY (document_id) REFERENCES laccis.documents(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_suggestions_document_id ON laccis.clause_suggestions(document_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_content_id  ON laccis.clause_suggestions(content_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_status      ON laccis.clause_suggestions(status);

-- Verify all 10 tables now exist:
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'laccis' AND table_type = 'BASE TABLE'
ORDER BY table_name;

