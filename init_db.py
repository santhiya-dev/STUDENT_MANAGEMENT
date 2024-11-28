import sqlite3

# Create/connect to the database file
conn = sqlite3.connect('students.db')

# Create a cursor object
cursor = conn.cursor()

# Create students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        course TEXT NOT NULL
    )
''')

# Create teacher/admin login table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# Add an admin user to start with
cursor.execute('''
    INSERT OR IGNORE INTO users (username, password, role) 
    VALUES ('admin', 'admin123', 'admin')
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully!")
