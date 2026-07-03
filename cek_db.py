import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "survey_sentimen.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("DB YANG DIPAKAI:", DB_PATH)
print("\n=== DAFTAR TABEL ===")

for t in tables:
    print(t[0])

print("\n=== ISI TABEL ===")

for t in tables:
    print(f"\n-- {t[0]} --")
    cursor.execute(f"SELECT * FROM {t[0]}")
    rows = cursor.fetchall()

    if not rows:
        print(" (kosong)")
    else:
        for r in rows:
            print(r)

conn.close()