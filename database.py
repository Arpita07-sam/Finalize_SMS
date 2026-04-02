import sqlite3

def connect_db():
    conn = sqlite3.connect("instance/users.db")
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,      
                faculty_id INTEGER,
                name TEXT NOT NULL,
                ph_no TEXT UNIQUE
                   CHECK(length(ph_no) = 10),
                sub TEXT NOT NULL
                )           
""")
    conn.commit()
    conn.close()

def insert_faculty(user_id, faculty_id, name, ph_no, sub):
    conn = sqlite3.connect("instance/users.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO faculty(user_id, faculty_id, name, ph_no, sub)
    VALUES (?, ?, ?, ?, ?) """, (user_id, faculty_id, name, ph_no, sub))

    conn.commit()
    conn.close()

    return "Saved successfully"

def get_all_faculty():
    conn = sqlite3.connect("instance/users.db")
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()
    
    # Convert rows to a list of dictionaries
    faculty_list = [dict(row) for row in rows]
    
    conn.close()
    return faculty_list

def update_faculty(user_id, faculty_id, name, ph_no, sub):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE faculty
        SET faculty_id = ?, name = ?, ph_no = ?, sub = ?
        WHERE id = ?
    """, (faculty_id, name, ph_no, sub, user_id))

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
    conn = sqlite3.connect("instance/users.db")
    conn.row_factory = sqlite3.Row
    return conn



# import sqlite3

# conn = sqlite3.connect("instance/users.db")
# cursor = conn.cursor()

# cursor.execute("DROP TABLE faculty")

# conn.commit()
# conn.close()