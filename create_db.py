import sqlite3
conn = sqlite3.connect("traffic.db")
cursor = conn.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS traffic(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                timestamp TEXT, 
                object_type TEXT
                )
            """)

conn.commit()
conn.close()
print("Database Created")
