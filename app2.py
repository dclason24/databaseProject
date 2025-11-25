from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.debug = True
app.secret_key = 'secretsecret'

db = config.dbserver1

#home page, checks where the user should be rerouted to depending on role
@app.route('/')
def home():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'student':
            return redirect(url_for('student'))
        elif role == 'teacher':
            return redirect(url_for('teacher'))
        elif role == 'admin':
            return redirect(url_for('admin'))
        else: 
            return "role not recognized"

    else:
        return redirect(url_for('login_page'))

#login page, gets info from the user, searches database and stores it in a session
#so the user goes to the correct page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template("login.html")
     
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = db.cursor()
        cursor.execute("SELECT user_id, email, role, student_id, instructor_id FROM users WHERE email=%s AND password=%s", [email, password])
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            # Store user info in session
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['role'] = user[2]
            session['student_id'] = user[3]
            session['teacher_id'] = user[4]
            
            # Redirect based on role
            if user[2] == 'student':
                return redirect(url_for('student'))
            elif user[2] == 'teacher':
                return redirect(url_for('teacher'))
            elif user[2] == 'admin':
                return redirect(url_for('admin'))
            else:
                return "Role not recognized."
    else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")

#admin homepage
@app.route('/admin')
def admin():
    if 'user_id' in session:
        return render_template("admin.html", name= 'admin')
    else:
        return redirect(url_for('login_page'))

#teacher homepage
@app.route('/teacher')
def teacher():
    if 'user_id' in session:
        user_id = session['teacher_id']

        cursor = db.cursor()
        cursor.execute("select first_name from instructor where instructor_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()

        teacher_name = result[0]
        return render_template("teacher.html", name = teacher_name)
    else:
        return redirect(url_for('login_page'))

#student homepage
@app.route('/student')
def student():
    if 'user_id' in session:
        user_id = session['student_id']

        cursor = db.cursor()
        cursor.execute("select first_name from student where student_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()

        teacher_name = result[0]
        return render_template("student.html", name = teacher_name)
    else:
        return redirect(url_for('login_page'))

#=================================================ADMIN=================================================
#CRUD course  
# @app.route("/admin/course/create", methods=["POST"])
# def admin_course_create():
#     if session.get("role") != "admin":
#         return "Unauthorized!"

#     data = request.form
#     cursor = db.cursor()
#     cursor.execute("INSERT INTO course VALUES (%s,%s,%s,%s)",
#                    (data["course_id"], data["title"], data["dept_name"], data["credits"]))
#     db.commit(); cursor.close()
#     return redirect("/admin")

# @app.route("/admin/course/delete/<cid>")
# def admin_course_delete(cid):
#     if session.get("role") != "admin":
#         return "Unauthorized!"
#     cursor = db.cursor()
#     cursor.execute("DELETE FROM course WHERE course_id=%s", [cid])
#     db.commit(); cursor.close()
#     return redirect("/admin")
  
#CRUD section
#CRUD classroom
#CRUD department
#CRUD time slot
#CRUD instructor 
#CRUD student 
#Assign/modify/remove teachers to classes

#=================================================INSTRUCTOR=================================================
#Submit grades 
# @app.route("/instructor/grade/submit", methods=["POST"])
# def instructor_grade_submit():
#     if session.get("role") != "instructor":
#         return "Unauthorized!"

#     data = request.form
#     cursor = db.cursor()
#     cursor.execute("""
#         UPDATE enrollment SET grade=%s 
#         WHERE student_id=%s AND section_id=%s
#     """, (data["grade"], data["student_id"], data["section_id"]))
#     db.commit(); cursor.close()
#     return redirect("/instructor")

#Change grades
#Add students as advisor
#Remove students as advisor
#Modify course prerequisites
#Remove student from section
#Check section roster 
#Check sections teaching based on the semester
#Modify personal information, except ID

#=================================================STUDENT=================================================
#Register for classes
# @app.route("/student/register/<section_id>")
# def student_register_class(section_id):
#     if session.get("role") != "student":
#         return "Unauthorized!"

#     cursor = db.cursor()
#     cursor.execute("INSERT INTO enrollment(student_id, section_id) VALUES (%s,%s)",
#                    (session["linked_id"], section_id))
#     db.commit(); cursor.close()
#     return redirect("/student")

#Drop classes
#Check final grade for classes
#Check courses based on the semester, including status
#Check for section information
#Check for advisor’s information
#Modify personal information, except ID

#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

#run
app.run(host='localhost', port=4500)
