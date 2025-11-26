#this is where we write the queries

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
def base():
    # Check if user is logged in
    if 'user_id' in session:
        role = session.get('role')
        if role == 'student':
            return redirect(url_for('student'))
        elif role == 'instructor':
            return redirect(url_for('instructor'))
        elif role == 'admin':
            return redirect(url_for('admin'))
        else: 
            return "Role not recognized"

    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("""SELECT user_id, email, password, role, student_id, instructor_id 
                          FROM user WHERE email=%s""", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):  # user[2] is hashed password
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['role'] = user[3]
            session['student_id'] = user[4]
            session['instructor_id'] = user[5]

            if user[3] == 'student':
                return redirect(url_for('student'))
            elif user[3] == 'instructor':
                return redirect(url_for('instructor'))
            elif user[3] == 'admin':
                return redirect(url_for('admin'))
            else:
                return "Role not recognized."
        
        else:
            return "Invalid credentials. Please try again."
        
    return render_template("login.html")

# ================================================Dashboards================================================
@app.route('/admin')
def admin():
    if 'user_id' in session:
        return render_template("admin.html", name= 'admin')
    else:
        return redirect(url_for('login'))

@app.route('/instructor')
def instructor():
    if 'user_id' in session:
        user_id = session['instructor_id']

        cursor = db.cursor()
        cursor.execute("select first_name from instructor where instructor_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()

        instructor_name = result[0]
        return render_template("instructor.html", name = instructor_name)
    else:
        return redirect(url_for('login'))

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
        return redirect(url_for('login'))

# ================================================Admin================================================
# Register route

# ================================================Instructor================================================

# ================================================Student================================================

# ================================================Logout================================================
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    # Redirect back to login page
    return redirect(url_for('login'))

if __name__ == '__main__':    
    app.run(port = 4500)