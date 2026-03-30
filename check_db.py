import sqlite3
conn = sqlite3.connect('brand_monitor.db')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT brand FROM mentions')
print(cursor.fetchall())
conn.close()