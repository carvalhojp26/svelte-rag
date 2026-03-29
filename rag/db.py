import psycopg2
from pgvector.psycopg2 import register_vector
from rag.config import DB_URL

def get_conn():
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn