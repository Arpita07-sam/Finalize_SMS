import sqlite3

def connect_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty_id INTERGER,
                name TEXT,
                ph_no TEXT,
                sub TEXT
                )           
""")
    conn.commit()
    conn.close()

def insert_faculty(faculty_id, name, ph_no, sub):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO faculty(faculty_id, name, ph_no, sub)
    VALUES (?, ?, ?, ?) """, (faculty_id, name, ph_no, sub))

    conn.commit()
    conn.close()

    return "Saved successfully"

def get_all_faculty():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()
    
    # Convert rows to a list of dictionaries
    faculty_list = [dict(row) for row in rows]
    
    conn.close()
    return faculty_list

