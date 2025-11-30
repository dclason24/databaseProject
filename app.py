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
    
# @app.route('/index.html')
# def home():
#     # Check if user is logged in
#     if 'user_id' in session:
#         role = session.get('role')
#         if role == 'student':
#             return redirect(url_for('student'))
#         elif role == 'instructor':
#             return redirect(url_for('instructor'))
#         elif role == 'admin':
#             return redirect(url_for('admin'))
#         else: 
#             return "Role not recognized"

#     else:
#         return redirect(url_for('login'))

# ================================================Admin================================================
# -----------------------
# CRUD: Courses
# -----------------------
@app.route('/admin/courses', methods=['GET'])
def admin_courses():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT course_id, title, dept_name, credits FROM course")
    courses = cursor.fetchall()

    cursor.execute("SELECT dept_name FROM department")
    departments = [row[0] for row in cursor.fetchall()]

    return render_template("admin/courses.html", courses=courses, departments=departments)


@app.route('/admin/courses/create', methods=['POST'])
def create_course():
    course_id = request.form['course_id']
    title = request.form['title']
    dept_name = request.form['dept_name']
    credits = request.form['credits']

    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO course (course_id, title, dept_name, credits) VALUES (%s, %s, %s, %s)",
            (course_id, title, dept_name, credits)
        )
        db.commit()
        flash("Course created successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error creating course: {e}", "danger")

    return redirect(url_for('admin_courses'))


@app.route('/admin/courses/update/<string:course_id>', methods=['POST'])
def update_course(course_id):
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
    except Exception as e:
        db.rollback()
        flash(f"Error updating course: {e}", "danger")

    return redirect(url_for('admin_courses'))


@app.route('/admin/courses/delete/<string:course_id>', methods=['POST'])
def delete_course(course_id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM course WHERE course_id=%s", (course_id,))
        db.commit()
        flash("Course deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting course: {e}", "danger")

    return redirect(url_for('admin_courses'))


# -----------------------
# CRUD: Sections
# -----------------------
@app.route('/admin/sections', methods=['GET', 'POST'])
def admin_sections():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()

    cursor.execute("SELECT course_id FROM course")
    courses = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT instructor_id, CONCAT(first_name, ' ', last_name) FROM instructor")
    instructors = cursor.fetchall()

    cursor.execute("SELECT room_number, building FROM classroom")
    rooms = cursor.fetchall()

    cursor.execute("SELECT DISTINCT building FROM classroom")
    buildings = [row[0] for row in cursor.fetchall()]

    cursor.execute(
        "SELECT time_slot_id, CONCAT(days, ' ', start_hr, ':', start_min, '-', end_hr, ':', end_min) FROM time_slot"
    )
    time_slots = cursor.fetchall()

    if request.method == 'POST':
        course_id = request.form['course_id']
        instructor_id = request.form['instructor_id']
        semester = request.form['semester']
        year = request.form['year']
        building = request.form['building']
        time_slot_id = request.form['time_slot_id']
        room_number = request.form['room_number']

        try:
            cursor.execute(
                "INSERT INTO section (course_id, instructor_id, semester, year, building, time_slot_id, room_number) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (course_id, instructor_id, semester, year, building, time_slot_id, room_number)
            )
            db.commit()
            flash("Section created successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error creating section: {e}", "danger")

        return redirect(url_for('admin_sections'))

    cursor.execute(
        "SELECT section_id, course_id, instructor_id, semester, year, building, time_slot_id, room_number "
        "FROM section"
    )
    sections = cursor.fetchall()

    return render_template("admin/sections.html",
                           sections=sections,
                           courses=courses,
                           instructors=instructors,
                           rooms=rooms,
                           buildings=buildings,
                           time_slots=time_slots)


@app.route('/admin/sections/update/<int:section_id>', methods=['POST'])
def update_section(section_id):
    course_id = request.form['course_id']
    instructor_id = request.form['instructor_id']
    semester = request.form['semester']
    year = request.form['year']
    building = request.form['building']
    time_slot_id = request.form['time_slot_id']
    room_number = request.form['room_number']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE section SET course_id=%s, instructor_id=%s, semester=%s, year=%s, "
            "building=%s, time_slot_id=%s, room_number=%s WHERE section_id=%s",
            (course_id, instructor_id, semester, year, building, time_slot_id, room_number, section_id)
        )
        db.commit()
        flash("Section updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating section: {e}", "danger")

    return redirect(url_for('admin_sections'))


@app.route('/admin/sections/delete/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM section WHERE section_id=%s", (section_id,))
        db.commit()
        flash("Section deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting section: {e}", "danger")

    return redirect(url_for('admin_sections'))


# -----------------------
# CRUD: Classrooms
# -----------------------
@app.route('/admin/classrooms', methods=['GET', 'POST'])
def admin_classrooms():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT building FROM classroom")
    buildings = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        building = request.form['building']
        room_number = request.form['room_number']
        capacity = request.form['capacity']

        try:
            cursor.execute(
                "INSERT INTO classroom (building, room_number, capacity) VALUES (%s, %s, %s)",
                (building, room_number, capacity)
            )
            db.commit()
            flash("Classroom added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error adding classroom: {e}", "danger")

        return redirect(url_for('admin_classrooms'))

    cursor.execute("SELECT building, room_number, capacity FROM classroom")
    classrooms = cursor.fetchall()

    return render_template("admin/classrooms.html", classrooms=classrooms, buildings=buildings)


@app.route('/admin/classrooms/update', methods=['POST'])
def update_classroom():
    original_building = request.form['original_building']
    original_room_number = request.form['original_room_number']
    building = request.form['building']
    room_number = request.form['room_number']
    capacity = request.form['capacity']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE classroom SET building=%s, room_number=%s, capacity=%s "
            "WHERE building=%s AND room_number=%s",
            (building, room_number, capacity, original_building, original_room_number)
        )
        db.commit()
        flash("Classroom updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating classroom: {e}", "danger")

    return redirect(url_for('admin_classrooms'))


@app.route('/admin/classrooms/delete', methods=['POST'])
def delete_classroom():
    building = request.form['building']
    room_number = request.form['room_number']

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM classroom WHERE building=%s AND room_number=%s", (building, room_number))
        db.commit()
        flash("Classroom deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting classroom: {e}", "danger")

    return redirect(url_for('admin_classrooms'))

# -----------------------
# CRUD: Departments
# -----------------------
@app.route('/admin/departments', methods=['GET', 'POST'])
def admin_departments():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()

    if request.method == 'POST':
        dept_name = request.form['dept_name']
        building = request.form['building']
        budget = request.form['budget']

        try:
            cursor.execute(
                "INSERT INTO department (dept_name, building, budget) VALUES (%s, %s, %s)",
                (dept_name, building, budget)
            )
            db.commit()
            flash("Department added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error adding department: {e}", "danger")

        return redirect(url_for('admin_departments'))

    cursor.execute("SELECT dept_name, building, budget FROM department")
    departments = cursor.fetchall()
    return render_template("admin/departments.html", departments=departments)


@app.route('/admin/departments/update', methods=['POST'])
def update_department():
    original_dept_name = request.form['original_dept_name']
    dept_name = request.form['dept_name']
    building = request.form['building']
    budget = request.form['budget']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE department SET dept_name=%s, building=%s, budget=%s WHERE dept_name=%s",
            (dept_name, building, budget, original_dept_name)
        )
        db.commit()
        flash("Department updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating department: {e}", "danger")

    return redirect(url_for('admin_departments'))


@app.route('/admin/departments/delete', methods=['POST'])
def delete_department():
    dept_name = request.form['dept_name']

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM department WHERE dept_name=%s", (dept_name,))
        db.commit()
        flash("Department deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting department: {e}", "danger")

    return redirect(url_for('admin_departments'))


# -----------------------
# CRUD: Time Slots
# -----------------------
@app.route('/admin/time_slots', methods=['GET', 'POST'])
def admin_time_slots():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()

    if request.method == 'POST':
        time_slot_id = request.form['time_slot_id']
        days = request.form['days']
        start_hr = request.form['start_hr']
        start_min = request.form['start_min']
        end_hr = request.form['end_hr']
        end_min = request.form['end_min']

        try:
            cursor.execute(
                "INSERT INTO time_slot (time_slot_id, days, start_hr, start_min, end_hr, end_min) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (time_slot_id, days, start_hr, start_min, end_hr, end_min)
            )
            db.commit()
            flash("Time slot added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error adding time slot: {e}", "danger")

        return redirect(url_for('admin_time_slots'))

    cursor.execute("SELECT time_slot_id, days, start_hr, start_min, end_hr, end_min FROM time_slot")
    time_slots = cursor.fetchall()
    return render_template("admin/time_slots.html", time_slots=time_slots)


@app.route('/admin/time_slots/update', methods=['POST'])
def update_time_slot():
    original_id = request.form['original_time_slot_id']
    time_slot_id = request.form['time_slot_id']
    days = request.form['days']
    start_hr = request.form['start_hr']
    start_min = request.form['start_min']
    end_hr = request.form['end_hr']
    end_min = request.form['end_min']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE time_slot SET time_slot_id=%s, days=%s, start_hr=%s, start_min=%s, end_hr=%s, end_min=%s "
            "WHERE time_slot_id=%s",
            (time_slot_id, days, start_hr, start_min, end_hr, end_min, original_id)
        )
        db.commit()
        flash("Time slot updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating time slot: {e}", "danger")

    return redirect(url_for('admin_time_slots'))


@app.route('/admin/time_slots/delete', methods=['POST'])
def delete_time_slot():
    time_slot_id = request.form['time_slot_id']

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM time_slot WHERE time_slot_id=%s", (time_slot_id,))
        db.commit()
        flash("Time slot deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting time slot: {e}", "danger")

    return redirect(url_for('admin_time_slots'))


# -----------------------
# CRUD: Instructors
# -----------------------
@app.route('/admin/instructors', methods=['GET', 'POST'])
def admin_instructors():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT dept_name FROM department")
    departments = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dept_name = request.form['dept_name'] or None
        salary = request.form['salary']

        try:
            cursor.execute(
                "INSERT INTO instructor (first_name, last_name, dept_name, salary) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, dept_name, salary)
            )
            db.commit()
            flash("Instructor added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error adding instructor: {e}", "danger")

        return redirect(url_for('admin_instructors'))

    cursor.execute("SELECT instructor_id, first_name, last_name, dept_name, salary FROM instructor")
    instructors = cursor.fetchall()
    return render_template("admin/instructors.html", instructors=instructors, departments=departments)


@app.route('/admin/instructors/update', methods=['POST'])
def update_instructor():
    instructor_id = request.form['original_instructor_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dept_name = request.form['dept_name'] or None
    salary = request.form['salary']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE instructor SET first_name=%s, last_name=%s, dept_name=%s, salary=%s WHERE instructor_id=%s",
            (first_name, last_name, dept_name, salary, instructor_id)
        )
        db.commit()
        flash("Instructor updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating instructor: {e}", "danger")

    return redirect(url_for('admin_instructors'))


@app.route('/admin/instructors/delete', methods=['POST'])
def delete_instructor():
    instructor_id = request.form['instructor_id']

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM instructor WHERE instructor_id=%s", (instructor_id,))
        db.commit()
        flash("Instructor deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting instructor: {e}", "danger")

    return redirect(url_for('admin_instructors'))


# -----------------------
# CRUD: Students
# -----------------------
@app.route('/admin/students', methods=['GET', 'POST'])
def admin_students():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT dept_name FROM department")
    departments = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dept_name = request.form['dept_name'] or None
        tot_credits = request.form['tot_credits']

        try:
            cursor.execute(
                "INSERT INTO student (first_name, last_name, dept_name, tot_credits) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, dept_name, tot_credits)
            )
            db.commit()
            flash("Student added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error adding student: {e}", "danger")

        return redirect(url_for('admin_students'))

    cursor.execute("SELECT student_id, first_name, last_name, dept_name, tot_credits FROM student")
    students = cursor.fetchall()
    return render_template("admin/students.html", students=students, departments=departments)


@app.route('/admin/students/update', methods=['POST'])
def update_student():
    student_id = request.form['original_student_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dept_name = request.form['dept_name'] or None
    tot_credits = request.form['tot_credits']

    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE student SET first_name=%s, last_name=%s, dept_name=%s, tot_credits=%s WHERE student_id=%s",
            (first_name, last_name, dept_name, tot_credits, student_id)
        )
        db.commit()
        flash("Student updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating student: {e}", "danger")

    return redirect(url_for('admin_students'))


@app.route('/admin/students/delete', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM student WHERE student_id=%s", (student_id,))
        db.commit()
        flash("Student deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting student: {e}", "danger")

    return redirect(url_for('admin_students'))

# ================================================Instructor================================================

# ================================================Student================================================
@app.route('/enrollment')
def enrollment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    student_id = session['student_id']
    
    cursor = db.cursor()
    cursor.execute("select course_id, grade from enrollment where student_id = %s", (student_id,))
    grades = cursor.fetchall()
    cursor.close()

    return render_template("enrollment.html", grades = grades)


    

# ================================================Logout================================================
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    # Redirect back to login page
    return redirect(url_for('login'))

if __name__ == '__main__':    
    app.run(port = 4500)