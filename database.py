import sqlite3

def connect_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
                faculty_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                ph_no TEXT UNIQUE
                   CHECK(length(ph_no) = 10),
                sub TEXT NOT NULL
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

def update_faculty(id, faculty_id, name, ph_no, sub):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE faculty
        SET faculty_id = ?, name = ?, ph_no = ?, sub = ?
        WHERE id = ?
    """, (faculty_id, name, ph_no, sub, id))

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected

def delete_faculty(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM faculty WHERE id = ?", (id,))
    conn.commit()

    affected = cursor.rowcount
    conn.close()

    return affected


def get_db_connection():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

