import bcrypt
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, jsonify

from flask_cors import CORS
import sqlite3

from authentication import send_verification_code, verify_code
from database import get_db_connection, insert_faculty, update_faculty

from flask import Flask, render_template, request, jsonify
from flask_bcrypt import Bcrypt
from details import db, User

# 1. Tell Flask to look in "templetes" instead of the default "templates"
app = Flask(__name__)
CORS(app) # This allows your JS to connect without security blocks

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/send-code", methods=["POST"])
def send_code():
    email = request.json.get("email")
    send_verification_code(email)
    return jsonify({"message": "Verification code sent"})

@app.route("/verify-code", methods=["POST"])
def verify_code_route():

    email = request.json.get("email")
    entered_code = request.json.get("code")

    if verify_code(email, entered_code):
        return jsonify({
            "message": "Code correct",
            "status": "success"
        })

    else:
        return jsonify({
            "message": "Wrong code",
            "status": "fail"
        })

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

bcrypt = Bcrypt(app)

# create table
with app.app_context():
    db.create_all()

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("/pages/register.html")
    
    if request.method == "POST":
        data = request.get_json()

        dept = data.get("dept")
        email = data.get("email")
        phno2 = data.get("phno2")
        phno1 = data.get("phno1")
        password = data.get("password")

        # hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # store in database
        new_user = User(
            dept = dept,
            email = email,
            phno2 = phno2,
            phno1 = phno1,
            password = hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Registered successfully"
        })

from flask import request, jsonify
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("pages/login.html")
    
    if request.method == "POST":
        data = request.get_json()

        dept = data.get("dept")
        phno2 = data.get("phno2")
        password = data.get("password")

        # SELECT * FROM users WHERE dept=? AND ph2=?
        user = User.query.filter_by(dept=dept, phno2=phno2).first()

        # check if row exists AND password matches
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({
                "status": "success",
                "message": "Login successful"
            })

        else:
            return jsonify({
                "status": "error",
                "message": "Invalid department / phone / password"
            })

@app.route("/dashboard")
def dashboard():
    return render_template("pages/main.html")

@app.route("/extract", methods=["POST"])
def extract():
    print("Pipeline started")
    return {"status":"ok"}

@app.route("/dashboard_content")
def dashboard_content():
    return render_template("pages/dash_cont.html")

@app.route("/hod")
def hod():
    return render_template("pages/hod.html", segment = "hod")

@app.route("/faculty")
def faculty():
    return render_template("pages/faculty.html", segment = "faculty")

@app.route("/setting")
def setting():
    return render_template("pages/setting.html", segment = "setting")

@app.route("/templates")
def templates():
    return render_template("pages/temp.html", segment = "payment")

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





