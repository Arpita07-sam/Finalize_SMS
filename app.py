import os

import bcrypt
from flask_bcrypt import Bcrypt
from flask import Flask, flash, redirect, render_template, request, jsonify, session, url_for

from flask_cors import CORS
import sqlite3

from authentication import send_verification_code, verify_code
from database import connect_db, get_db_connection, insert_faculty, update_faculty

from details import Signature, db, Department
import sign_cropper

from flask_bcrypt import Bcrypt

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
app.config["UPLOAD_FOLDER"] = "static/uploads"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

# create table
with app.app_context():
    db.create_all()

# @app.route('/signatures')
# def display_signatures():
#     # Fetch all signatures from the DB
#     signatures = Signature.query.all()
#     return render_template('pages/setting.html', signatures=signatures)


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return redirect(request.url)
    
#     file = request.files['file']
#     dept_id = request.form.get('dept_id', 1)
    
#     if file.filename != '':
#         os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(file_path)
        
#         # Call your cropper
#         cropped_paths = sign_cropper.process_page(file_path, dept_id)
        
#         # CORRECTED SECTION:
#         for path in cropped_paths:
#             new_sig = Signature(image_path=path, dept_id=dept_id)
#             db.session.add(new_sig) # Add to the session
        
#         db.session.commit() # Commit everything at once
        
#     return redirect(url_for('/signatures'))

# @app.route('/delete_signature/<int:sig_id>', methods=['POST'])
# def delete_signature(sig_id):
#     sig = Signature.query.get_or_404(sig_id)
#     # Remove file from folder
#     full_path = os.path.join('static', sig.image_path)
#     if os.path.exists(full_path):
#         os.remove(full_path)
#     # Remove from DB
#     db.session.delete(sig)
#     db.session.commit()
#     return jsonify({"success": True})

@app.route('/signatures')
def display_signatures():
    # Fetch all signatures from the DB
    signatures = Signature.query.all()
    # Ensure this path matches your templates folder structure
    return render_template('pages/setting.html', signatures=signatures)


@app.route("/upload", methods=["POST"])
def upload():
    dept_id = request.form.get("dept_id")
    files = request.files.getlist("files")
    total_files = len(files)
    all_saved = []
    for i, file in enumerate(files):

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        saved = sign_cropper.process_page(path, dept_id, i)
        all_saved.extend(saved)
    return jsonify({
        "images": all_saved
    })

# @app.route('/delete_signature/<int:sig_id>', methods=['POST'])
# def delete_signature(sig_id):
#     sig = Signature.query.get_or_404(sig_id)
    
#     # Construct the full path to delete the file from your computer
#     # Result: static/signatures/cropped_signatures/image.png
#     full_os_path = os.path.join(app.root_path, 'static', sig.image_path)
    
#     try:
#         if os.path.exists(full_os_path):
#             os.remove(full_os_path)
        
#         db.session.delete(sig)
#         db.session.commit()
#         return jsonify({"success": True})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

bcrypt = Bcrypt(app)
app.secret_key = "secret734"

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("/pages/register.html") 
    if request.method == "POST":
        data = request.get_json()
        dept_name = data.get("dept_name")
        dept_id = data.get("dept_id")
        hod_name = data.get("hod_name")
        tech_name = data.get("tech_name")
        email = data.get("email")
        tech_phno = data.get("tech_phno")
        hod_phno = data.get("hod_phno")
        password = data.get("password")

        # hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # store in database
        new_user = Department(
            dept_name = dept_name,
            dept_id = dept_id,
            hod_name = hod_name,
            tech_name = tech_name,
            email = email,
            tech_phno = tech_phno,
            hod_phno = hod_phno,
            password = hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Registered successfully"
        })

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("pages/login.html")
    
    if request.method == "POST":
        data = request.get_json()

        dept_id = data.get("dept_id")
        tech_phno = data.get("tech_phno")
        password = data.get("password")

        # SELECT * FROM users WHERE dept=? AND ph2=?
        user = Department.query.filter_by(dept_id=dept_id, tech_phno=tech_phno).first()

        # check if row exists AND password matches
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["dept_id"] = user.dept_id
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


@app.route("/get_department_details", methods=["GET"])
def get_department_details():
    dept_id = session.get("dept_id")
    if not dept_id:
        return jsonify({"error": "not logged in"}), 401
    user = Department.query.filter_by(dept_id=dept_id).first()
    if user:
        return jsonify({
            "dept_id": user.dept_id,
            "dept_name": user.dept_name,
            "hod_name": user.hod_name,
            "tech_name": user.tech_name,
            "email": user.email,
            "hod_phno": user.hod_phno,
            "tech_phno": user.tech_phno,
               
        })
    return jsonify({"error": "No data found"})

@app.route("/update_department", methods=["POST"])
def update_department():
    dept_id = session.get("dept_id")
    data = request.get_json()
    user = Department.query.filter_by(dept_id=dept_id).first()
    user.dept_name = data["dept_name"]
    user.hod_name = data["hod_name"]
    user.tech_name = data["tech_name"]
    user.email = data["email"]
    user.hod_phno = data["hod_phno"]
    user.tech_phno = data["tech_phno"]
    db.session.commit()
    return jsonify({"status":"updated"})

@app.route("/extract", methods=["POST"])
def extract():
    print("Pipeline started")
    return {"status":"ok"}

@app.route("/dashboard_content")
def dashboard_content():
    return render_template("pages/dash_cont.html")



@app.route("/faculty")
def faculty():
    return render_template("pages/faculty.html", segment = "faculty")

# @app.route("/setting")
# def setting():
#     return render_template("pages/setting.html", segment = "setting")

@app.route("/setting")
def settings():
    if "dept_id" not in session:
        return redirect("/")
    return render_template("pages/setting.html")

@app.route("/templates")
def templates():
    return render_template("pages/temp.html", segment = "payment")

@app.route("/history")
def history():
    return render_template("pages/history.html", segment = "history")


@app.route('/add-faculty', methods=['POST'])
def add_faculty_api(): 
    data = request.json

    user_id = session.get("user_id")
    
    # These keys MUST match the ones in the facultyData object in JS
    msg = insert_faculty(
        user_id,
        data['faculty_id'], 
        data['name'], 
        data['ph_no'],
        data['sub']   
    )
    return jsonify({"message": msg})

@app.route('/get-faculty', methods=['GET'])
def get_faculty():
    user_id = session.get("user_id")
    conn = get_db_connection() 
    faculty = conn.execute("SELECT * FROM faculty WHERE user_id=?",(user_id,)).fetchall()
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

def get_logged_user():
    if "user_id" not in session:
        return None
    return Department.query.get(session["user_id"])

if __name__ == '__main__':
    app.run(port=5000, debug=True)





