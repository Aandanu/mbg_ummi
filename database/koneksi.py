import os
import psycopg

print("SEMUA ENV:", list(os.environ.keys()))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

def get_db():
    conn = psycopg.connect(
        os.getenv("DATABASE_URL"),
        autocommit=False
    )
    return conn
