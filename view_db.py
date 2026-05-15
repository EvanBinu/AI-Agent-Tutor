import sqlite3

conn = sqlite3.connect("student_memory.db")

cursor = conn.cursor()

# View results table
print("Agent Messages:")
cursor.execute("SELECT * FROM agent_messages")
rows = cursor.fetchall()

for row in rows:
    print(row)
print("\n")
print("Outputting results:")
cursor.execute("SELECT * FROM results")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()