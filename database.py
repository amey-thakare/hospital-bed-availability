import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    available_beds INTEGER NOT NULL
)
""")

cursor.execute("DELETE FROM hospitals")

cursor.execute("INSERT INTO hospitals (name, available_beds) VALUES (?, ?)",
               ("City Hospital", 12))
cursor.execute("INSERT INTO hospitals (name, available_beds) VALUES (?, ?)",
               ("Green Care Hospital", 0))
cursor.execute("INSERT INTO hospitals (name, available_beds) VALUES (?, ?)",
               ("Sunrise Medical Center", 5))

conn.commit()
conn.close()

print("Database created and data inserted")
