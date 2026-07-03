import sqlite3

# =========================
# KONEKSI DATABASE
# =========================
conn = sqlite3.connect("database/survey_sentimen.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# =========================
# RESPONDEN BELUM KOMENTAR
# =========================
print("\n" + "=" * 80)
print("RESPONDEN BELUM MENGISI KOMENTAR")
print("=" * 80)

cursor.execute("""
SELECT r.id_responden,
       r.nama,
       r.sekolah,
       r.kelas
FROM responden r
LEFT JOIN komentar k
ON r.id_responden = k.id_responden
WHERE k.id_komentar IS NULL
ORDER BY r.id_responden
""")

belum = cursor.fetchall()

if belum:
    for row in belum:
        print(
            f"ID: {row['id_responden']} | "
            f"{row['nama']} | "
            f"{row['sekolah']} | "
            f"{row['kelas']}"
        )
else:
    print("Tidak ada.")

# =========================
# RESPONDEN SUDAH KOMENTAR
# =========================
print("\n" + "=" * 80)
print("RESPONDEN SUDAH MENGISI KOMENTAR")
print("=" * 80)

cursor.execute("""
SELECT DISTINCT
       r.id_responden,
       r.nama,
       r.sekolah,
       r.kelas
FROM responden r
INNER JOIN komentar k
ON r.id_responden = k.id_responden
ORDER BY r.id_responden
""")

sudah = cursor.fetchall()

if sudah:
    for row in sudah:
        print(
            f"ID: {row['id_responden']} | "
            f"{row['nama']} | "
            f"{row['sekolah']} | "
            f"{row['kelas']}"
        )
else:
    print("Tidak ada.")

# =========================
# INPUT ID
# =========================
print("\n" + "=" * 80)
print("HAPUS DATA RESPONDEN")
print("=" * 80)

input_id = input(
    "\nMasukkan ID responden yang ingin dihapus\n"
    "(contoh: 5 atau 5,7,10) : "
)

id_list = [
    x.strip()
    for x in input_id.split(",")
    if x.strip()
]

if not id_list:
    print("Tidak ada ID yang dimasukkan.")
    conn.close()
    exit()

# =========================
# PREVIEW DATA
# =========================
print("\n" + "=" * 80)
print("DATA YANG AKAN DIHAPUS")
print("=" * 80)

total_responden = 0
total_komentar = 0
total_sentimen = 0

valid_ids = []

for id_responden in id_list:

    cursor.execute("""
    SELECT *
    FROM responden
    WHERE id_responden = ?
    """, (id_responden,))

    responden = cursor.fetchone()

    if not responden:
        print(f"ID {id_responden} tidak ditemukan")
        continue

    valid_ids.append(id_responden)

    cursor.execute("""
    SELECT id_komentar
    FROM komentar
    WHERE id_responden = ?
    """, (id_responden,))

    komentar = cursor.fetchall()

    jumlah_komentar = len(komentar)
    jumlah_sentimen = 0

    for k in komentar:

        cursor.execute("""
        SELECT COUNT(*) AS total
        FROM hasil_sentimen
        WHERE id_komentar = ?
        """, (k["id_komentar"],))

        jumlah_sentimen += cursor.fetchone()["total"]

    total_responden += 1
    total_komentar += jumlah_komentar
    total_sentimen += jumlah_sentimen

    print(f"\nID              : {responden['id_responden']}")
    print(f"Nama            : {responden['nama']}")
    print(f"Sekolah         : {responden['sekolah']}")
    print(f"Kelas           : {responden['kelas']}")
    print(f"Jumlah Komentar : {jumlah_komentar}")
    print(f"Jumlah Sentimen : {jumlah_sentimen}")

if not valid_ids:
    print("\nTidak ada ID valid.")
    conn.close()
    exit()

print("\n" + "-" * 80)
print(f"Total Responden : {total_responden}")
print(f"Total Komentar  : {total_komentar}")
print(f"Total Sentimen  : {total_sentimen}")

# =========================
# KONFIRMASI
# =========================
konfirmasi = input(
    "\nYakin ingin menghapus data tersebut? (y/n) : "
)

if konfirmasi.lower() != "y":
    print("\nPenghapusan dibatalkan.")
    conn.close()
    exit()

# =========================
# PROSES HAPUS
# =========================
hapus_responden = 0
hapus_komentar = 0
hapus_sentimen = 0

for id_responden in valid_ids:

    cursor.execute("""
    SELECT id_komentar
    FROM komentar
    WHERE id_responden = ?
    """, (id_responden,))

    komentar = cursor.fetchall()

    for k in komentar:

        cursor.execute("""
        SELECT COUNT(*) AS total
        FROM hasil_sentimen
        WHERE id_komentar = ?
        """, (k["id_komentar"],))

        hapus_sentimen += cursor.fetchone()["total"]

        cursor.execute("""
        DELETE FROM hasil_sentimen
        WHERE id_komentar = ?
        """, (k["id_komentar"],))

    hapus_komentar += len(komentar)

    cursor.execute("""
    DELETE FROM komentar
    WHERE id_responden = ?
    """, (id_responden,))

    cursor.execute("""
    DELETE FROM responden
    WHERE id_responden = ?
    """, (id_responden,))

    hapus_responden += 1

conn.commit()

# =========================
# HASIL
# =========================
print("\n" + "=" * 80)
print("HASIL PENGHAPUSAN")
print("=" * 80)

print(f"✓ {hapus_responden} responden berhasil dihapus")
print(f"✓ {hapus_komentar} komentar berhasil dihapus")
print(f"✓ {hapus_sentimen} hasil sentimen berhasil dihapus")

conn.close()