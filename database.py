import sqlite3

def create_db():
    conn = sqlite3.connect("history.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS translations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_text TEXT,
        translated_text TEXT,
        source_lang TEXT,
        target_lang TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_translation(original,
                     translated,
                     source,
                     target):

    conn = sqlite3.connect("history.db")

    conn.execute(
        """
        INSERT INTO translations(
        original_text,
        translated_text,
        source_lang,
        target_lang
        )
        VALUES(?,?,?,?)
        """,
        (original,
         translated,
         source,
         target)
    )

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("history.db")

    rows = conn.execute(
        "SELECT * FROM translations"
    ).fetchall()

    conn.close()

    return rows