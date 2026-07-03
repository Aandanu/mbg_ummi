import streamlit as st
from database.koneksi import get_db


def reset_data():

    st.title("🔄 Reset Data")

    st.error(
        "PERINGATAN! Semua data responden, komentar, dan hasil sentimen akan dihapus permanen."
    )

    st.warning(
        "Data admin tidak akan dihapus."
    )

    konfirmasi = st.checkbox(
        "Saya yakin ingin menghapus seluruh data"
    )

    if konfirmasi:

        if st.button(
            "🗑️ Hapus Semua Data",
            type="primary",
            use_container_width=True
        ):

            conn = get_db()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "DELETE FROM hasil_sentimen"
                )

                cursor.execute(
                    "DELETE FROM komentar"
                )

                cursor.execute(
                    "DELETE FROM responden"
                )

                conn.commit()

                st.success(
                    "Seluruh data berhasil dihapus."
                )

            except Exception as e:

                st.error(str(e))

            finally:

                conn.close()