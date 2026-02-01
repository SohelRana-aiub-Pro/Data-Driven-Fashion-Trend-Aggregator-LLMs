import sqlite3


def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = c.fetchone()

    if table_exists:
        # Check schema columns
        c.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in c.fetchall()]

        required_columns = ["id", "name", "gender", "style_pref", "budget", "currency", "occasion"]

        # If schema mismatch, drop and recreate
        if set(required_columns) != set(columns):
            c.execute("DROP TABLE users")
            conn.commit()

    # Create table if not exists (or after drop)
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    gender TEXT,
                    style_pref TEXT,
                    budget REAL,
                    currency TEXT,
                    occasion TEXT
                )""")
    conn.commit()
    conn.close()


def add_user(name, gender, style_pref, budget, currency, occasion):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (name, gender, style_pref, budget, currency, occasion) VALUES (?, ?, ?, ?, ?, ?)",
        (name, gender, style_pref, budget, currency, occasion)
    )
    conn.commit()
    conn.close()




def get_user(user_id: int):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user