from flask import Flask, render_template, request, jsonify

from flask_cors import CORS
import sqlite3

from database import get_db_connection, insert_faculty, update_faculty
import database

# 1. Tell Flask to look in "templetes" instead of the default "templates"
app = Flask(__name__, template_folder='templetes')
CORS(app) # This allows your JS to connect without security blocks

@app.route("/")
def main():
    # 2. Use ONLY the filename here. 
    # Flask already knows to look inside your "templetes" folder now.
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("pages/register.html")

@app.route("/login")
def login():
    # 3. Use forward slashes (/) for paths inside the folder
    return render_template("pages/login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("pages/main.html")

@app.route("/hod")
def hod():
    return render_template("pages/hod.html", segment = "hod")


@app.route("/faculty")
def faculty():
    return render_template("pages/faculty.html", segment = "faculty")

@app.route("/setting")
def setting():
    return render_template("pages/setting.html", segment = "setting")

@app.route("/payment")
def payment():
    return render_template("pages/payment.html", segment = "payment")

@app.route("/history")
def history():
    return render_template("pages/history.html", segment = "history")




@app.route('/add-faculty', methods=['POST'])
def add_faculty_api():
    data = request.json
    
    # These keys MUST match the ones in the facultyData object in JS
    msg = insert_faculty(
        data['faculty_id'], 
        data['name'], 
        data['ph_no'],
        data['sub']   
    )
    return jsonify({"message": msg})

@app.route('/get-faculty', methods=['GET'])
def get_faculty():
    conn = get_db_connection() 
    faculty = conn.execute("SELECT * FROM faculty").fetchall()
    conn.close()

    faculty_list = [dict(row) for row in faculty]
    return jsonify(faculty_list)

@app.route("/update-faculty/<int:id>", methods=["PUT"])
def update_faculty(id):
    data = request.json
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE faculty
        SET name=?, ph_no=?, sub=?
        WHERE faculty_id=?
    """, (data["name"], data["ph_no"], data["sub"], id))

    conn.commit()
    conn.close()

    return {"message":"updated"}

@app.route("/delete-faculty/<int:id>", methods=["DELETE"])
def delete_faculty(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faculty WHERE faculty_id=?", (id,))
    conn.commit()
    conn.close()

    return {"message":"deleted"}

if __name__ == '__main__':
    app.run(port=5000, debug=True)





