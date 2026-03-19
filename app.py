from flask import Flask, render_template, request, jsonify

from flask_cors import CORS
import sqlite3

from database import get_all_faculty, insert_faculty

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

@app.route('/api/faculty', methods=['GET'])
def get_faculty_api():
    faculty = get_all_faculty()
    return jsonify(faculty)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)







# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def main():
#     return render_template("templetes\index.html")

# @app.route("/login")
# def login():
#     return render_template("templetes\pages\login.html")

# @app.route("/register")
# def register():
#     return render_template("templetes\pages\register.html")

# if __name__ == "__main__":
#     app.run(debug=True)


# @app.route("/register", methods=["POST"])
# def register():
#     password = request.form.get("password")
    
#     # Re-verify the requirements in Python
#     if len(password) < 8 or not any(char.isdigit() for char in password):
#         # Send them back to the page with an error message
#         return render_template("pages/register.html", error="Password did not meet requirements.")
    
#     # If it's strong, proceed to save to database
#     return "Registration Successful!"




# def insert_faculty(faculty_id, name, dept, sub, ph_no):
#     conn = sqlite3.connect("faculty.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#     INSERT INTO faculty(faculty_id, name, dept, sub, ph_no)
#     VALUES (?, ?, ?, ?, ?) """, (faculty_id, name, dept, sub, ph_no))
#     conn.commit()
#     conn.close()
#     return "Saved successfully"

