import os
from dotenv import load_dotenv

# Load .env from the backend root directory
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
DB_SCHEMA = os.getenv("DB_SCHEMA", "laccis")

# LLM Provider: "bedrock" or "mistral"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "bedrock")

# AWS Bedrock
AWS_REGION = os.getenv("AWS_REGION", os.getenv("REGION", "ap-south-1"))
BEDROCK_MODEL = os.getenv("BEDROCK_MODEL", "mistral.mistral-large-2402-v1:0")

# Mistral fallback
MISTRAL_API_KEY = os.getenv("MISTRAL_API")
MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_TEMPERATURE = 0.2

# Backward-compatible aliases for legacy callers that still use the generic config names.
LLM_MODEL = os.getenv("LLM_MODEL", BEDROCK_MODEL if LLM_PROVIDER == "bedrock" else MISTRAL_MODEL)
LLM_API_KEY = os.getenv("LLM_API_KEY", MISTRAL_API_KEY or "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", str(MISTRAL_TEMPERATURE)))

# Embedding
EMBEDDING_MODEL = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
EMBEDDING_DEVICE = "cpu"
EMBEDDING_NORMALIZE = True

# Pipeline
TOP_K = 5
SBERT_HIGH_RISK_THRESHOLD = 0.80
SBERT_MEDIUM_RISK_THRESHOLD = 0.90


def get_db_connection():
    import psycopg2

    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute(f'SET search_path TO "{DB_SCHEMA}"')
    conn.commit()
    return conn
