from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
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
# -----------------------
# Manage grades
# -----------------------
@app.route('/instructor/grades', methods=['GET', 'POST'])
def instructor_grades():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    instructor_id = session['instructor_id']
    cursor = db.cursor()

    try:
        if request.method == 'POST':
            section_id = request.form['section_id']

            cursor.execute("SELECT instructor_id FROM section WHERE section_id=%s", (section_id,))
            sec = cursor.fetchone()
            if not sec or sec[0] != instructor_id:
                flash("Unauthorized access to this section.", "danger")
                return redirect(url_for('instructor_grades'))

            for key, value in request.form.items():
                if key.startswith("grade_"):
                    student_id = key.split("_")[1]
                    grade = value.strip() if value else None
                    cursor.execute("""
                        UPDATE enrollment
                        SET grade=%s
                        WHERE student_id=%s AND section_id=%s
                    """, (grade, student_id, section_id))
            db.commit()
            flash("Grades updated successfully.", "success")

        cursor.execute("""
            SELECT s.section_id, c.course_id, c.title, s.semester, s.year
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            WHERE s.instructor_id = %s
            ORDER BY s.year DESC, s.semester DESC
        """, (instructor_id,))
        sections = cursor.fetchall()

        section_students = {}
        for sec in sections:
            section_id = sec[0]
            cursor.execute("""
                SELECT e.student_id, st.first_name, st.last_name, e.grade
                FROM enrollment e
                JOIN student st ON e.student_id = st.student_id
                WHERE e.section_id = %s
            """, (section_id,))
            students = cursor.fetchall()
            section_students[section_id] = students

    except Exception as e:
        db.rollback()
        flash(f"Error accessing or updating grades: {e}", "danger")
        sections = []
        section_students = {}

    finally:
        cursor.close()

    return render_template("instructor/grades.html", sections=sections, section_students=section_students)

# -----------------------
# Manage section enrollment
# -----------------------
@app.route('/instructor/enrollment', methods=['GET', 'POST'])
def instructor_enrollment():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    instructor_id = session['instructor_id']
    cursor = db.cursor()

    try:
        if request.method == 'POST':
            student_id = request.form['student_id']
            section_id = request.form['section_id']

            cursor.execute("SELECT instructor_id FROM section WHERE section_id=%s", (section_id,))
            sec = cursor.fetchone()
            if not sec or sec[0] != instructor_id:
                flash("Unauthorized access to this section.", "danger")
                return redirect(url_for('instructor_enrollment'))

            cursor.execute("DELETE FROM enrollment WHERE student_id=%s AND section_id=%s",
                           (student_id, section_id))
            db.commit()
            flash("Student removed from section successfully.", "success")

        cursor.execute("""
            SELECT s.section_id, c.course_id, c.title, s.semester, s.year
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            WHERE s.instructor_id = %s
            ORDER BY s.year DESC, s.semester DESC
        """, (instructor_id,))
        sections = cursor.fetchall()

        section_students = {}
        for sec in sections:
            section_id = sec[0]
            cursor.execute("""
                SELECT e.student_id, st.first_name, st.last_name
                FROM enrollment e
                JOIN student st ON e.student_id = st.student_id
                WHERE e.section_id = %s
            """, (section_id,))
            students = cursor.fetchall()
            section_students[section_id] = students

    except Exception as e:
        db.rollback()
        flash(f"Error managing enrollment: {e}", "danger")
        sections = []
        section_students = {}

    finally:
        cursor.close()

    return render_template("instructor/enrollments.html", sections=sections, section_students=section_students)

# -----------------------
# Advisor portal
# -----------------------
@app.route('/instructor/advisor', methods=['GET', 'POST'])
def advisor():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    instructor_id = session['instructor_id']
    cursor = db.cursor()

    try:
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'add':
                student_id = request.form['student_id']
                cursor.execute("""
                    SELECT * FROM advisor 
                    WHERE student_id=%s AND instructor_id=%s
                """, (student_id, instructor_id))
                exists = cursor.fetchone()
                if exists:
                    flash("This student is already your advisee.", "warning")
                else:
                    cursor.execute("""
                        INSERT INTO advisor (student_id, instructor_id)
                        VALUES (%s, %s)
                    """, (student_id, instructor_id))
                    db.commit()
                    flash("Student added as an advisee successfully.", "success")

            elif action == 'remove':
                student_id = request.form['student_id']
                cursor.execute("""
                    DELETE FROM advisor
                    WHERE student_id=%s AND instructor_id=%s
                """, (student_id, instructor_id))
                db.commit()
                flash("Advisee removed successfully.", "success")

        cursor.execute("""
            SELECT student_id, first_name, last_name 
            FROM student
            WHERE dept_name = (SELECT dept_name FROM instructor WHERE instructor_id=%s)
            ORDER BY last_name, first_name
        """, (instructor_id,))
        students = cursor.fetchall()

        cursor.execute("""
            SELECT a.student_id, s.first_name, s.last_name
            FROM advisor a
            JOIN student s ON a.student_id = s.student_id
            WHERE a.instructor_id = %s
            ORDER BY s.last_name, s.first_name
        """, (instructor_id,))
        advisees = cursor.fetchall()

    except Exception as e:
        db.rollback()
        flash(f"Error managing advisees: {e}", "danger")
        students = []
        advisees = []

    finally:
        cursor.close()

    return render_template("instructor/advisor.html", students=students, advisees=advisees)

# -----------------------
# Manage prerequisites
# -----------------------
@app.route('/instructor/prereqs', methods=['GET', 'POST'])
def prereqs():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    instructor_id = session['instructor_id']
    cursor = db.cursor()

    try:
        if request.method == 'POST':
            action = request.form.get('action')
            course_id = request.form['course_id']

            if action == 'add':
                prereq_id = request.form['prereq_id']

                cursor.execute("""
                    SELECT * FROM prereq
                    WHERE course_id=%s AND prereq_id=%s
                """, (course_id, prereq_id))
                exists = cursor.fetchone()
                if exists:
                    flash("This course is already a prereq.", "warning")
                else:
                    cursor.execute("""
                        INSERT INTO prereq (course_id, prereq_id)
                        VALUES (%s, %s)
                    """, (course_id, prereq_id))
                    db.commit()
                    flash("Prerequisite added successfully.", "success")

            elif action == 'remove':
                prereq_id = request.form['prereq_id']
                cursor.execute("""
                    DELETE FROM prereq
                    WHERE course_id=%s AND prereq_id=%s
                """, (course_id, prereq_id))
                db.commit()
                flash("Prerequisite removed successfully.", "success")

        cursor.execute("""
            SELECT DISTINCT c.course_id, c.title
            FROM course c
            JOIN section s ON c.course_id = s.course_id
            WHERE s.instructor_id=%s
            ORDER BY c.course_id
        """, (instructor_id,))
        courses = cursor.fetchall()

        cursor.execute("SELECT course_id, title FROM course ORDER BY course_id")
        all_courses = cursor.fetchall()

        course_prereqs = {}
        for c in courses:
            cursor.execute("""
                SELECT p.prereq_id, c2.title
                FROM prereq p
                JOIN course c2 ON p.prereq_id = c2.course_id
                WHERE p.course_id=%s
            """, (c[0],))
            course_prereqs[c[0]] = cursor.fetchall()

    except Exception as e:
        db.rollback()
        flash(f"Error managing prerequisites: {e}", "danger")
        courses = []
        all_courses = []
        course_prereqs = {}

    finally:
        cursor.close()

    return render_template("instructor/prereqs.html", courses=courses, all_courses=all_courses, course_prereqs=course_prereqs)

# -----------------------
# Sections
# -----------------------
@app.route('/instructor/sections', methods=['GET', 'POST'])
def instructor_sections():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    instructor_id = session['instructor_id']
    cursor = db.cursor()
    selected_semester = None
    selected_year = None

    try:
        if request.method == 'POST':
            selected_semester = request.form.get('semester')
            selected_year = request.form.get('year')

        query = """
            SELECT s.section_id, c.course_id, c.title, s.semester, s.year, s.building, s.room_number,
                   ts.days, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            LEFT JOIN time_slot ts ON s.time_slot_id = ts.time_slot_id
            WHERE s.instructor_id = %s
        """
        params = [instructor_id]

        if selected_semester:
            query += " AND s.semester = %s"
            params.append(selected_semester)
        if selected_year:
            query += " AND s.year = %s"
            params.append(selected_year)

        query += " ORDER BY s.year DESC, s.semester DESC"

        cursor.execute(query, tuple(params))
        sections_raw = cursor.fetchall()

        # Convert to readable time format
        sections = []
        for s in sections_raw:
            section_id, course_id, title, semester, year, building, room_number, days, start_hr, start_min, end_hr, end_min = s
            if start_hr is not None:
                start_time = f"{int(start_hr):02}:{int(start_min):02}"
                end_time = f"{int(end_hr):02}:{int(end_min):02}"
                display_time = f"{days} {start_time}-{end_time}"
            else:
                display_time = "TBD"

            sections.append({
                "section_id": section_id,
                "course_id": course_id,
                "title": title,
                "semester": semester,
                "year": year,
                "building": building,
                "room_number": room_number,
                "display_time": display_time
            })

    except Exception as e:
        flash(f"Error fetching sections: {e}", "danger")
        sections = []

    finally:
        cursor.close()

    return render_template(
        "instructor/sections.html",
        sections=sections,
        selected_semester=selected_semester,
        selected_year=selected_year
    )

# -----------------------
# Profile
# -----------------------
@app.route('/instructor/profile', methods=['GET', 'POST'])
def instructor_profile():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    instructor_id = session['instructor_id']
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT instructor_id, first_name, last_name, dept_name, salary 
            FROM instructor 
            WHERE instructor_id=%s
        """, (instructor_id,))
        instructor = cursor.fetchone()

        if not instructor:
            flash("Instructor not found.", "danger")
            return redirect(url_for('instructor'))

        if request.method == 'POST':
            first_name = request.form['first_name'].strip()
            last_name = request.form['last_name'].strip()
            dept_name = request.form['dept_name']

            try:
                cursor.execute("""
                    UPDATE instructor
                    SET first_name=%s, last_name=%s, dept_name=%s
                    WHERE instructor_id=%s
                """, (first_name, last_name, dept_name, instructor_id))
                db.commit()
                flash("Profile updated successfully.", "success")
            except Exception as e:
                db.rollback()
                flash(f"Error updating profile: {e}", "danger")

        cursor.execute("SELECT dept_name FROM department ORDER BY dept_name")
        departments = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        flash(f"Error loading profile: {e}", "danger")
        instructor = None
        departments = []

    finally:
        cursor.close()

    return render_template("instructor/profile.html", instructor=instructor, departments=departments)

# -----------------------
# Final additions
# -----------------------
@app.route('/instructor/avg_grades', methods=['GET', 'POST'])
def avg_grades():
    if 'user_id' not in session or session.get('role') != 'instructor':
        return redirect(url_for('login'))

    cursor = db.cursor()

    avg_by_dept = []
    class_avg = None
    class_selected = None
    courses = []

    try:
        cursor.execute("""
            SELECT d.dept_name,
                   ROUND(AVG(
                       CASE 
                           WHEN e.grade REGEXP '^[A-F][+-]?$' THEN
                               CASE
                                   WHEN e.grade = 'A' THEN 4.0
                                   WHEN e.grade = 'A-' THEN 3.7
                                   WHEN e.grade = 'B+' THEN 3.3
                                   WHEN e.grade = 'B' THEN 3.0
                                   WHEN e.grade = 'B-' THEN 2.7
                                   WHEN e.grade = 'C+' THEN 2.3
                                   WHEN e.grade = 'C' THEN 2.0
                                   WHEN e.grade = 'C-' THEN 1.7
                                   WHEN e.grade = 'D+' THEN 1.3
                                   WHEN e.grade = 'D' THEN 1.0
                                   WHEN e.grade = 'F' THEN 0.0
                               END
                       END
                   ), 2) AS avg_grade
            FROM student s
            JOIN department d ON s.dept_name = d.dept_name
            JOIN enrollment e ON s.student_id = e.student_id
            GROUP BY d.dept_name
            ORDER BY d.dept_name
        """)

        avg_by_dept = cursor.fetchall()

        cursor.execute("SELECT course_id, title FROM course ORDER BY course_id")
        courses = cursor.fetchall()

        if request.method == "POST":
            course_id = request.form["course_id"]
            sem_start = request.form["sem_start"]   
            sem_end = request.form["sem_end"]      

            class_selected = (course_id, sem_start, sem_end)

            # Split semester into components
            y1, s1 = sem_start.split('-')
            y2, s2 = sem_end.split('-')

            # For semester ordering
            sem_order = {
                "Winter": 1,
                "Spring": 2,
                "Summer": 3,
                "Fall":   4
            }

            # Query for average grade in a course over semester range
            cursor.execute(f"""
                SELECT ROUND(AVG(
                    CASE 
                        WHEN e.grade REGEXP '^[A-F][+-]?$' THEN
                            CASE
                                WHEN e.grade = 'A' THEN 4.0
                                WHEN e.grade = 'A-' THEN 3.7
                                WHEN e.grade = 'B+' THEN 3.3
                                WHEN e.grade = 'B' THEN 3.0
                                WHEN e.grade = 'B-' THEN 2.7
                                WHEN e.grade = 'C+' THEN 2.3
                                WHEN e.grade = 'C' THEN 2.0
                                WHEN e.grade = 'C-' THEN 1.7
                                WHEN e.grade = 'D+' THEN 1.3
                                WHEN e.grade = 'D' THEN 1.0
                                WHEN e.grade = 'F' THEN 0.0
                            END
                    END
                ), 2)
                FROM enrollment e
                JOIN section s ON e.section_id = s.section_id
                WHERE s.course_id = %s
                AND (
                    (s.year > %s AND s.year < %s)
                    OR (s.year = %s AND FIELD(s.semester, 'Winter','Spring','Summer','Fall') >= FIELD(%s,'Winter','Spring','Summer','Fall'))
                    OR (s.year = %s AND FIELD(s.semester, 'Winter','Spring','Summer','Fall') <= FIELD(%s,'Winter','Spring','Summer','Fall'))
                )
            """, (course_id, y1, y2, y1, s1, y2, s2))

            row = cursor.fetchone()
            class_avg = row[0] if row else None

    except Exception as e:
        flash(f"Error loading averages: {e}", "danger")

    finally:
        cursor.close()

    return render_template(
        "instructor/avg_grades.html",
        avg_by_dept=avg_by_dept,
        courses=courses,
        class_avg=class_avg,
        class_selected=class_selected
    )

@app.route('/instructor/best_worst', methods=['GET', 'POST'])
def best_worst():
    if 'user_id' not in session:
        return redirect(url_for('login'))


    cursor = db.cursor()

    # --- Get selected semester/year ---
    selected_semester = request.form.get('semester', 'Fall')
    selected_year = int(request.form.get('year', 2025))

    # --- Mapping grades to numeric values and calculating average ---
    cursor.execute("""
        SELECT 
            s.section_id,
            c.course_id,
            c.title,
            AVG(
                CASE e.grade
                    WHEN 'A' THEN 4.0
                    WHEN 'A-' THEN 3.7
                    WHEN 'B+' THEN 3.3
                    WHEN 'B' THEN 3.0
                    WHEN 'B-' THEN 2.7
                    WHEN 'C+' THEN 2.3
                    WHEN 'C' THEN 2.0
                    WHEN 'C-' THEN 1.7
                    WHEN 'D+' THEN 1.3
                    WHEN 'D' THEN 1.0
                    WHEN 'F' THEN 0.0
                END
            ) AS avg_grade
        FROM section s
        JOIN course c ON s.course_id = c.course_id
        LEFT JOIN enrollment e ON s.section_id = e.section_id
        WHERE s.semester = %s AND s.year = %s
        GROUP BY s.section_id, c.course_id, c.title
        HAVING avg_grade IS NOT NULL
        ORDER BY avg_grade DESC
    """, (selected_semester, selected_year))

    results = cursor.fetchall()  # List of tuples: (section_id, course_id, title, avg_grade)

    if results:
        best_class = results[0]
        worst_class = results[-1]
    else:
        best_class = None
        worst_class = None

    # --- Fetch distinct semesters and years for filter ---
    cursor.execute("SELECT DISTINCT semester FROM section ORDER BY FIELD(semester,'Fall','Summer','Spring');")
    semesters = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT year FROM section ORDER BY year DESC;")
    years = [row[0] for row in cursor.fetchall()]

    return render_template(
        'instructor/best_worst.html',
        semesters=semesters,
        years=years,
        selected_semester=selected_semester,
        selected_year=selected_year,
        best_class=best_class,
        worst_class=worst_class
    )

@app.route('/instructor/student_stat')
def student_stat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor()

    # Query total students and currently enrolled students per department
    cursor.execute("""
        SELECT 
            d.dept_name,
            COUNT(s.student_id) AS total_students,
            COUNT(DISTINCT e.student_id) AS current_students
        FROM department d
        LEFT JOIN student s ON d.dept_name = s.dept_name
        LEFT JOIN enrollment e ON s.student_id = e.student_id
        GROUP BY d.dept_name
        ORDER BY total_students DESC;
    """)
    results = cursor.fetchall()  # List of tuples: (dept_name, total_students, current_students)

    return render_template('instructor/student_stat.html', data=results)

# ================================================Student================================================
# -------------------------
# View grades
# -------------------------
@app.route('/student/grades')
def grades():
    if 'user_id' not in session:
        flash("You must be logged in to view grades.", "danger")
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()
    try:
        query = """
            SELECT 
                c.title AS course_name,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name,
                CONCAT(sec.semester, ' ', sec.year) AS semester,
                e.grade
            FROM enrollment e
            JOIN section sec ON e.section_id = sec.section_id
            JOIN course c ON sec.course_id = c.course_id
            JOIN instructor i ON sec.instructor_id = i.instructor_id
            WHERE e.student_id = %s;
        """
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading grades: {e}", "danger")
        results = []

    return render_template('/student/grades.html', grades=results)

# -------------------------
# View advisor
# -------------------------
@app.route('/student/advisor')
def student_advisor():
    if 'user_id' not in session:
        flash("You must be logged in.", "danger")
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()
    try:
        query = """
            SELECT 
                CONCAT(i.first_name, ' ', i.last_name) AS advisor_name,
                i.dept_name
            FROM advisor a
            JOIN instructor i ON a.instructor_id = i.instructor_id
            WHERE a.student_id = %s;
        """
        cursor.execute(query, (student_id,))
        advisor = cursor.fetchone()
        if advisor is None:
            flash("No advisor assigned.", "info")
    except Exception as e:
        flash(f"Error loading advisor: {e}", "danger")
        advisor = None

    return render_template('student/advisor.html', advisor=advisor)

# -------------------------
# Enrollment
# -------------------------
@app.route('/student/enrollment', methods=['GET', 'POST'])
def enrollment():
    if 'student_id' not in session:
        flash("You must be logged in.", "danger")
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()
    selected_semester = request.form.get('semester', 'Fall')
    selected_year = int(request.form.get('year', 2025))
    action = request.form.get('action')

    # --- Handle POST actions ---
    if request.method == 'POST' and action:
        try:
            section_id = request.form.get('section_id')
            if action == 'add':
                cursor.execute("""
                    INSERT INTO enrollment (student_id, course_id, section_id, grade)
                    SELECT %s, s.course_id, s.section_id, NULL
                    FROM section s
                    WHERE s.section_id = %s
                """, (student_id, section_id))
                db.commit()
                flash("Class added successfully.", "success")
            elif action == 'drop':
                cursor.execute("""
                    DELETE FROM enrollment
                    WHERE student_id = %s AND section_id = %s
                """, (student_id, section_id))
                db.commit()
                flash("Class dropped successfully.", "success")
            else:
                flash("Invalid action.", "danger")
        except Exception as e:
            db.rollback()
            flash(f"Database error: {e}", "danger")
        return redirect(url_for('enrollment'))

    # --- Load current enrollment and available sections ---
    try:
        # Current enrollment
        cursor.execute("""
            SELECT
                c.course_id, c.title,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name,
                s.semester, s.year,
                ts.days, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min,
                s.building, s.room_number, e.section_id
            FROM enrollment e
            JOIN section s ON e.section_id = s.section_id
            JOIN course c ON s.course_id = c.course_id
            LEFT JOIN instructor i ON s.instructor_id = i.instructor_id
            LEFT JOIN time_slot ts ON s.time_slot_id = ts.time_slot_id
            WHERE e.student_id = %s AND s.semester = %s AND s.year = %s
            ORDER BY ts.start_hr, ts.start_min
        """, (student_id, selected_semester, selected_year))
        current_enrollment = cursor.fetchall()

        # Available sections
        cursor.execute("""
            SELECT
                s.section_id, c.course_id, c.title,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name,
                ts.days, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min,
                s.building, s.room_number
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            LEFT JOIN instructor i ON s.instructor_id = i.instructor_id
            LEFT JOIN time_slot ts ON s.time_slot_id = ts.time_slot_id
            WHERE s.semester = %s AND s.year = %s
            AND s.section_id NOT IN (SELECT section_id FROM enrollment WHERE student_id = %s)
            ORDER BY c.title
        """, (selected_semester, selected_year, student_id))
        available_sections = cursor.fetchall()

        # Dropdowns
        cursor.execute("SELECT DISTINCT semester FROM section ORDER BY FIELD(semester,'Fall','Summer','Spring');")
        semesters = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT DISTINCT year FROM section ORDER BY year DESC;")
        years = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        flash(f"Error loading enrollment data: {e}", "danger")
        current_enrollment = []
        available_sections = []
        semesters = []
        years = []

    return render_template(
        'student/enrollment.html',
        selected_semester=selected_semester,
        selected_year=selected_year,
        semesters=semesters,
        years=years,
        current_enrollment=current_enrollment,
        available_sections=available_sections
    )

# -------------------------
# Schdeule
# -------------------------
@app.route('/student/schedule', methods=['GET', 'POST'])
def schedule():
    if 'student_id' not in session:
        flash("You must be logged in.", "danger")
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()
    selected_semester = request.form.get('semester', 'Fall')
    selected_year = int(request.form.get('year', 2025))

    try:
        cursor.execute("""
            SELECT
                c.course_id, c.title,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name,
                s.semester, s.year,
                ts.days, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min,
                s.building, s.room_number
            FROM enrollment e
            JOIN section s ON e.section_id = s.section_id
            JOIN course c ON s.course_id = c.course_id
            LEFT JOIN instructor i ON s.instructor_id = i.instructor_id
            LEFT JOIN time_slot ts ON s.time_slot_id = ts.time_slot_id
            WHERE e.student_id = %s AND s.semester = %s AND s.year = %s
            ORDER BY ts.start_hr, ts.start_min
        """, (student_id, selected_semester, selected_year))
        schedule_data = cursor.fetchall()

        cursor.execute("SELECT DISTINCT semester FROM section ORDER BY FIELD(semester,'Fall','Summer','Spring');")
        semesters = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT DISTINCT year FROM section ORDER BY year DESC;")
        years = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        flash(f"Error loading schedule: {e}", "danger")
        schedule_data = []
        semesters = []
        years = []

    return render_template(
        'student/schedule.html',
        schedule=schedule_data,
        semesters=semesters,
        years=years,
        selected_semester=selected_semester,
        selected_year=selected_year
    )

# -------------------------
# Profile
# -------------------------
@app.route('/student/profile', methods=['GET', 'POST'])
def profile():
    if 'student_id' not in session:
        flash("You must be logged in.", "danger")
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor()

    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            dept_name = request.form.get('dept_name')

            cursor.execute("""
                UPDATE student
                SET first_name=%s, last_name=%s, dept_name=%s
                WHERE student_id=%s
            """, (first_name, last_name, dept_name, student_id))
            db.commit()
            flash("Profile updated successfully.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error updating profile: {e}", "danger")
        return redirect(url_for('profile'))

    try:
        cursor.execute("SELECT student_id, first_name, last_name, dept_name, tot_credits FROM student WHERE student_id=%s", (student_id,))
        student_info = cursor.fetchone()
        cursor.execute("SELECT dept_name FROM department ORDER BY dept_name;")
        departments = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        flash(f"Error loading profile: {e}", "danger")
        student_info = None
        departments = []

    return render_template('student/profile.html', student=student_info, departments=departments)

# ================================================Logout================================================
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    # Redirect back to login page
    return redirect(url_for('login'))

if __name__ == '__main__':    
    app.run(port = 4500)