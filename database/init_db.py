import bcrypt
from koneksi import get_db

conn = get_db()
cursor = conn.cursor()

# =====================
# TABEL ADMIN
# =====================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id_admin SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nama_admin VARCHAR(150)
)
""")

# =====================
# TABEL RESPONDEN
# =====================

cursor.execute("""
CREATE TABLE IF NOT EXISTS responden(
    id_responden SERIAL PRIMARY KEY,
    nama VARCHAR(150),
    sekolah VARCHAR(200),
    kelas VARCHAR(50),
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
)
""")

# =====================
# TABEL KOMENTAR
# =====================

cursor.execute("""
CREATE TABLE IF NOT EXISTS komentar(
    id_komentar SERIAL PRIMARY KEY,
    id_responden INTEGER,
    isi_komentar TEXT,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_responden
    FOREIGN KEY(id_responden)
    REFERENCES responden(id_responden)
    ON DELETE CASCADE
)
""")

# =====================
# TABEL HASIL SENTIMEN
# =====================

cursor.execute("""
CREATE TABLE IF NOT EXISTS hasil_sentimen(
    id_hasil SERIAL PRIMARY KEY,
    id_komentar INTEGER,
    hasil VARCHAR(30),
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_komentar
    FOREIGN KEY(id_komentar)
    REFERENCES komentar(id_komentar)
    ON DELETE CASCADE
)
""")

# =====================
# ADMIN DEFAULT
# =====================

cursor.execute(
    "SELECT * FROM admin WHERE username=%s",
    ("admin",)
)

admin = cursor.fetchone()

if admin is None:

    password = bcrypt.hashpw(
        "admin123".encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute("""
        INSERT INTO admin
        (username,password,nama_admin)
        VALUES(%s,%s,%s)
    """,(
        "admin",
        password,
        "Administrator"
    ))

    print("Admin berhasil dibuat.")

conn.commit()

cursor.close()
conn.close()

print("Database berhasil dibuat.")
