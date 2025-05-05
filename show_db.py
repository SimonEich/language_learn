import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate through all tables and print their contents
for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")
    
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print(f"Columns: {', '.join(column_names)}")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)

# Close the connection
conn.close()
