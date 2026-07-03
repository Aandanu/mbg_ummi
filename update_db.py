import sqlite3

conn = sqlite3.connect("database/survey_sentimen.db")
cursor = conn.cursor()

# Buat tabel baru
cursor.execute("""
CREATE TABLE responden_baru (
    id_responden INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    sekolah TEXT,
    kelas TEXT,
    username TEXT UNIQUE,
    password TEXT,
    tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Salin data lama
cursor.execute("""
INSERT INTO responden_baru
(id_responden, nama, sekolah, kelas, username, password)
SELECT
id_responden, nama, sekolah, kelas, username, password
FROM responden
""")

# Hapus tabel lama
cursor.execute("DROP TABLE responden")

# Ganti nama tabel baru
cursor.execute("""
ALTER TABLE responden_baru
RENAME TO responden
""")

conn.commit()
conn.close()

print("Berhasil")