import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS hospital_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("DELETE FROM hospital_users")

cursor.execute(
    "INSERT INTO hospital_users (name, password) VALUES (?, ?)",
    ("City Hospital", "city123")
)

cursor.execute(
    "INSERT INTO hospital_users (name, password) VALUES (?, ?)",
    ("Green Care Hospital", "green123")
)

conn.commit()
conn.close()

print("Hospital users created")
