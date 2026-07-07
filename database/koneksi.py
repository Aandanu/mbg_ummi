import os
import psycopg

def get_db():
    conn = psycopg.connect(
        os.environ["DATABASE_PUBLIC_URL"],
        autocommit=False
    )
    return conn
