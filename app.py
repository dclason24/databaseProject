#this is where we write the queries

#! /usr/bin/python3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json
import config

db = config.dbserver1

app = Flask(__name__)
app.debug = True
app.secret_key = "secretsecret"

# ================================================Login================================================
@app.route('/')
def home():
    # Check if user is logged in
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

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("""SELECT user_id, email, password, role, student_id, instructor_id 
                          FROM users WHERE email=%s""", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):  # user[2] is hashed password
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['role'] = user[3]
            session['student_id'] = user[4]
            session['teacher_id'] = user[5]

            if user[3] == 'student':
                return redirect(url_for('student'))
            elif user[3] == 'teacher':
                return redirect(url_for('teacher'))
            elif user[3] == 'admin':
                return redirect(url_for('admin'))
        
        return render_template("login.html", error="Invalid credentials. Please try again.")

# ================================================Dashboards================================================
@app.route('/admin')
def admin():
    if 'user_id' in session:
        return render_template("admin.html", name= 'admin')
    else:
        return redirect(url_for('login_page'))

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

@app.route('/student')
def student():
    if 'user_id' in session:
        user_id = session['student_id']

        cursor = db.cursor()
        cursor.execute("select first_name from student where student_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()

        student_name = result[0]
        return render_template("student.html", name = student_name)
    else:
        return redirect(url_for('login_page'))

# ================================================Admin================================================

# ================================================Instructor================================================

# ================================================Student================================================

# ================================================Logout================================================
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    # Redirect back to login page
    return redirect(url_for('login_page'))

if __name__ == '__main__':    
    app.run(port = 4500)