from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.debug = True
app.secret_key = 'super_secret_key_!_123'

db = config.dbserver2

#login page
@app.route('/', methods=['GET', 'POST'])
def base():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):
            #store session data
            session['loggedin'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            session['linked_id'] = user[4]

            #redirect based on role
            if user[3] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user[3] == "instructor":
                return redirect(url_for("instructor_dashboard"))
            elif user[3] == "student":
                return redirect(url_for("student_dashboard"))
        else:
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)

#different dashboards
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return "Unauthorized!"
    return render_template("admin.html")

@app.route("/instructor")
def instructor_dashboard():
    if session.get("role") != "instructor":
        return "Unauthorized!"
    return render_template("instructor.html")

@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return "Unauthorized!"
    return render_template("student.html")

#################################################################
# --------------------- CRUD EXAMPLES --------------------------
#################################################################

############ ADMIN CRUD COURSE (as example)
@app.route("/admin/course/create", methods=["POST"])
def admin_course_create():
    if session.get("role") != "admin":
        return "Unauthorized!"

    data = request.form
    cursor = db.cursor()
    cursor.execute("INSERT INTO course VALUES (%s,%s,%s,%s)",
                   (data["course_id"], data["title"], data["dept_name"], data["credits"]))
    db.commit(); cursor.close()
    return redirect("/admin")

@app.route("/admin/course/delete/<cid>")
def admin_course_delete(cid):
    if session.get("role") != "admin":
        return "Unauthorized!"
    cursor = db.cursor()
    cursor.execute("DELETE FROM course WHERE course_id=%s", [cid])
    db.commit(); cursor.close()
    return redirect("/admin")

@app.route('/admin/create_user', methods=['GET', 'POST'])
def admin_create_user():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # admin/instructor/student
        linked_id = request.form.get('linked_id')  # student_id or instructor_id

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s;", [username])
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        else:
            hashed = generate_password_hash(password)
            cursor.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s)", 
                (None, username, hashed, role, linked_id))
            db.commit()
            msg = "Registration successful!"
            cursor.close()

    return render_template("register.html", msg=msg)


############ INSTRUCTOR: SUBMIT GRADE
@app.route("/instructor/grade/submit", methods=["POST"])
def instructor_grade_submit():
    if session.get("role") != "instructor":
        return "Unauthorized!"

    data = request.form
    cursor = db.cursor()
    cursor.execute("""
        UPDATE enrollment SET grade=%s 
        WHERE student_id=%s AND section_id=%s
    """, (data["grade"], data["student_id"], data["section_id"]))
    db.commit(); cursor.close()
    return redirect("/instructor")

############ STUDENT: REGISTER FOR CLASS
@app.route("/student/register/<section_id>")
def student_register_class(section_id):
    if session.get("role") != "student":
        return "Unauthorized!"

    cursor = db.cursor()
    cursor.execute("INSERT INTO enrollment(student_id, section_id) VALUES (%s,%s)",
                   (session["linked_id"], section_id))
    db.commit(); cursor.close()
    return redirect("/student")

#################################################################
# ------------------------ LOGOUT ------------------------------
#################################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#################################################################
# ----------------------- RUN APP ------------------------------
#################################################################
app.run(host='localhost', port=4500)
