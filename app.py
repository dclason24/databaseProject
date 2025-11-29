#this is where we write the queries

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from MySQLdb import OperationalError
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
        return render_template("admin/dashboard.html", name= 'Admin')
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
        return render_template("instructor/dashboard.html", name = instructor_name)
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
        return render_template("student/dashboard.html", name = student_name)
    else:
        return redirect(url_for('login'))
    
@app.route('/index.html')
def home():
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

# ================================================Admin================================================
@app.route('/admin/courses')
def admin_courses():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT course_id, title, dept_name, credits FROM course")
    courses = cursor.fetchall()
    cursor.execute("SELECT dept_name FROM department")
    dept_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return render_template("admin/courses.html", courses=courses, dept_names=dept_names)

# ================================================
# Create a new course
# ================================================
@app.route('/admin/courses/create', methods=['POST'])
def create_course():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    course_id = request.form['course_id']
    title = request.form['title']
    dept_name = request.form['dept_name']
    credits = request.form['credits']

    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO course (course_id, title, dept_name, credits) VALUES (%s,%s,%s,%s)",
            (course_id, title, dept_name, credits)
        )
        db.commit()
        flash("Course added successfully.", "success")
    except OperationalError as e:
        db.rollback()
        flash(f"Error adding course: {e}", "danger")
    finally:
        cursor.close()

    return redirect(url_for('admin_courses'))

# ================================================
# Update a course
# ================================================
@app.route('/admin/courses/update/<course_id>', methods=['POST'])
def update_course(course_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    title = request.form['title']
    dept_name = request.form['dept_name']
    credits = request.form['credits']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE course SET title=%s, dept_name=%s, credits=%s WHERE course_id=%s",
            (title, dept_name, credits, course_id)
        )
        db.commit()
        flash("Course updated successfully.", "success")
    except OperationalError as e:
        db.rollback()
        flash(f"Error updating course: {e}", "danger")
    finally:
        cursor.close()

    return redirect(url_for('admin_courses'))

# ================================================
# Delete a course
# ================================================
@app.route('/admin/courses/delete/<course_id>', methods=['POST'])
def delete_course(course_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM course WHERE course_id=%s", (course_id,))
        db.commit()
        flash("Course deleted successfully.", "success")
    except OperationalError as e:
        db.rollback()
        flash(f"Error deleting course: {e}", "danger")
    finally:
        cursor.close()

    return redirect(url_for('admin_courses'))

# ================================================
# Get sections
# ================================================
@app.route('/admin/sections')
def admin_sections():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("""
        SELECT section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id 
        FROM section
    """)
    sections = cursor.fetchall()
    cursor.close()
    return render_template("admin/sections.html", sections=sections)

# ================================================
# Create a section
# ================================================
@app.route('/admin/sections/create', methods=['POST'])
def create_section():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    course_id = request.form['course_id']
    instructor_id = request.form['instructor_id']
    semester = request.form['semester']
    year = request.form['year']
    building = request.form['building']
    room_number = request.form['room_number']
    time_slot_id = request.form['time_slot_id']

    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO section 
            (course_id, instructor_id, semester, year, building, room_number, time_slot_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (course_id, instructor_id, semester, year, building, room_number, time_slot_id))
        db.commit()
        flash("Section added successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error adding section: {e}", "danger")
    finally:
        cursor.close()

    return redirect(url_for('admin_sections'))

# ================================================
# Update a section
# ================================================
@app.route('/admin/sections/update/<int:section_id>', methods=['POST'])
def update_section(section_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    course_id = request.form['course_id']
    instructor_id = request.form['instructor_id']
    semester = request.form['semester']
    year = request.form['year']
    building = request.form['building']
    room_number = request.form['room_number']
    time_slot_id = request.form['time_slot_id']

    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE section
            SET course_id=%s, instructor_id=%s, semester=%s, year=%s, building=%s, room_number=%s, time_slot_id=%s
            WHERE section_id=%s
        """, (course_id, instructor_id, semester, year, building, room_number, time_slot_id, section_id))
        db.commit()
        flash("Section updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating section: {e}", "danger")
    finally:
        cursor.close()

    return redirect(url_for('admin_sections'))

# ================================================
# Delete a section
# ================================================
@app.route('/admin/sections/delete/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM section WHERE section_id=%s", (section_id,))
        db.commit()
        flash("Section deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting section: {e}", "danger")
    finally:
        cursor.close()

    return redirect(url_for('admin_sections'))

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