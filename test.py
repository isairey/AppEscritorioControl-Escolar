conn = conectar()
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(asistencia)")
print(cursor.fetchall())

conn.close()