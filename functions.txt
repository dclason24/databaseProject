#this is where we write the queries

#! /usr/bin/python3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import config

#for the pymysql look at the faculty url, on that the two ways to access the CS database will be shown


#Configuration for pymysql
db = config.dbserver1



app = Flask(__name__)
app.debug = True
app.secret_key = "secretsecret"

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

        teacher_name = result[0]
        return render_template("student.html", name = teacher_name)
    else:
        return redirect(url_for('login_page'))
   
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    # Redirect back to login page
    return redirect(url_for('login_page'))

@app.route('/users')
def users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")  # or your table name
    users = cursor.fetchall()  # fetch all rows
    cursor.close()
    return render_template('users.html', users=users)

@app.route('/search',  methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        myName = request.form['name']
        myId = request.form['id']
        values = {
            'name': myName,
            'id': myId }
        return render_template('results.html', **values)
    if request.method == 'GET':
        return render_template('form.html')

@app.route('/values')
def values():
    myInteger = 3
    return render_template('values.html', value = myInteger)

@app.route('/student', methods = ['GET','POST'])
def displayStudent():
        if request.method == 'GET':
            #Function with pymysql
            cursor = db.cursor()
            sql = "SELECT * from student;"
            cursor.execute(sql)            
            data = cursor.fetchall()
            cursor.close()
            print(data)
            #return f"Done!! Query Result is {data}"
            return render_template('student.html', data=data)
        if request.method == 'POST':
            data = request.form['ID']
            print(data)
            cursor = db.cursor()
            sql = "delete from student where student_id = %s"
            cursor.execute(sql, [data])
            #get new faculty data     
            sql = "select * from student"
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()    
            return render_template('student.html',data= data)
        
@app.route('/searchStudent',  methods = ['GET','POST'])
def searchStudent():
    if request.method == 'GET':
        return render_template('searchStudent.html')
    
    if request.method == 'POST':
        myName = request.form['name']
        myId = request.form['id']
        print(myName, myId)    

        if myId != "":
            print("Goin for ID")
            cursor = db.cursor()
            pattern = f"%{myId}%"
            sql = "SELECT * from student where CAST(student_id AS CHAR) LIKE %s"
            cursor.execute(sql,[pattern])
            data = cursor.fetchall()
            cursor.close()
        elif myName != "":
            print("Goin for Name")
            cursor = db.cursor()
            pattern = f"%{myName}%"
            sql = "SELECT * FROM student WHERE first_name LIKE %s"
            cursor.execute(sql, [pattern])
            data = cursor.fetchall()
            cursor.close()         
  
        else:
            return render_template('searchStudent.html')
        return render_template('student.html', data=data)
    
@app.route('/schedule/<int:student_id>', methods=['GET', 'POST'])
def viewSchedule(student_id):
    cursor = db.cursor()

    sql = """select s.student_id, concat(s.first_name, ' ', s.last_name) as full_name, c.course_id, sec.semester, sec.year
        from enrollment e 
        join student s on e.student_id = s.student_id 
        join section sec on e.section_id = sec.section_id
        join course c on sec.course_id = c.course_id
        where s.student_id = %s
        order by sec.year, sec.semester
    """
    cursor.execute(sql, [student_id])
    schedule_data = cursor.fetchall()
    cursor.close()

    years = sorted({row[4] for row in schedule_data})
    filter_year = None
    if request.method == 'POST':
        filter_year = request.form.get('year')
        if filter_year:
            schedule_data = [row for row in schedule_data if str(row[4]) == filter_year]

    return render_template('schedule.html', schedule_data=schedule_data, years=years, filter_year=filter_year)

        
@app.route('/newStudent',  methods = ['GET','POST'])
def newStudent():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('newStudent.html', data = edited)
    if request.method == 'POST':
        myFName = request.form['first_name']
        myLName = request.form['last_name']
        myDept = request.form['dept']        
        myCredits = int(request.form['tot_credits'])
        cursor = db.cursor()
        sql = "Insert into student(first_name, last_name, dept_name, tot_credits) values(%s, %s, %s, %s)"    
        cursor.execute(sql,[myFName, myLName, myDept, myCredits])
        data = cursor.fetchall()
        #cursor.execute("CALL pp(%s, %s, %s, %s);",[myId, myName, myDept, mySalary])
        #reload page with all student members        
        cursor = db.cursor()
        sql = "select * from student"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('student.html', data=data)
       
@app.route('/faculty', methods = ['GET','POST'])
def displayFaculty():
        if request.method == 'GET':
            #Function with pymysql
            cursor = db.cursor()
            sql = "SELECT * from instructor;"
            cursor.execute(sql)            
            data = cursor.fetchall()
            cursor.close()
            print(data)
            #return f"Done!! Query Result is {data}"
            return render_template('faculty.html', data=data)
        if request.method == 'POST':
            data = request.form['ID']
            print(data)
            cursor = db.cursor()
            sql = "delete from instructor where instructor_id = %s"
            cursor.execute(sql, [data])
            #get new faculty data     
            sql = "select * from instructor"
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()    
            return render_template('faculty.html',data= data)

@app.route('/facultysearch', methods = ['GET','POST'])
def facultySearch():        
        if request.method == 'GET':
            return render_template('facultysearch.html')
        if request.method == 'POST':
            myName = request.form['name']
            myId = request.form['id']
            print(myName, myId)    
            if myId != "":
                print("Goin for ID")
                cursor = db.cursor()
                sql = "SELECT * from instructor where instructor_id = %s"
                cursor.execute(sql,[myId])
                data = cursor.fetchall()
                cursor.close()
            elif myName != "":
                print("Goin for Name")
                cursor = db.cursor()
                sql = "SELECT * FROM instructor WHERE CONCAT(first_name,' ',last_name) = %s"
                cursor.execute(sql, [myName])
                data = cursor.fetchall()
                cursor.close()            
            else:
                 return render_template('facultysearch.html')
            return render_template('faculty.html', data=data)

@app.route('/newfaculty',  methods = ['GET','POST'])
def newFaculty():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('newfaculty.html', data = edited)
    if request.method == 'POST':
        myName = request.form['name']
        myId = request.form['id']
        myDept = request.form['dept']        
        mySalary = request.form['salary']
        cursor = db.cursor()
        sql = "Insert into instructor values(%s, %s, %s, %s)"    
        cursor.execute(sql,[myId, myName, myDept, mySalary])
        data = cursor.fetchall()
        #cursor.execute("CALL pp(%s, %s, %s, %s);",[myId, myName, myDept, mySalary])
        #reload page with all favulty members        
        cursor = db.cursor()
        sql = "select * from instructor"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('faculty.html', data=data)
    
@app.route('/countfaculty',  methods = ['GET','POST'])
def countFaculty():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT dept_name as dept_name from department;"
        cursor.execute(sql)        
        data = cursor.fetchall()        
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('count.html', data = edited)
    if request.method == 'POST':
        dept = request.form['depts']  
        cursor = db.cursor()      
        sql = "SELECT dept_count(%s);"
        cursor.execute(sql,[dept])
        data = cursor.fetchall()
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('total.html', data=edited[0])

    
@app.route('/function',  methods = ['GET','POST'])
def countdeptfuntion():
    if request.method == 'POST':
        if request.method == 'POST':
            dept = request.form['dept']        
            cursor = db.cursor()
            sql = "SELECT dept_count(%s);"
            cursor.execute(sql, [dept])
            data = cursor.fetchall()
            cursor.close()
            edited = []
            for i in data:
                edited.append(i[0])
        return render_template('countdept.html', data = edited[0])
    if request.method == 'GET':
        cursor = db.cursor()
        sql ="SELECT dept_name as dept_name from department;"
        cursor.execute(sql)
        data = cursor.fetchall()        
        cursor.close()
        edited = []
        print(data)
        for i in data:
            edited.append(i[0])
        return render_template('function.html', data = edited)

if __name__ == '__main__':    
    cursor = db.cursor()
    sql = "SELECT * from instructor;"
    cursor.execute(sql)            
    data = cursor.fetchall()    
    cursor.close()
    finalList = []
    dictionary = {}
    for item in data:        
        dictionary = {}
        dictionary['_id'] = item[0]
        dictionary['name'] = f"{item[1]} {item[2]}"
        dictionary['dept_name'] = item[3]
        dictionary['salary'] = float(item[4])
        finalList.append(dictionary)
    
    pretty_json = json.dumps(finalList, indent=4)
    #print(pretty_json)
    cursor = db.cursor()
    sql = "SELECT * from student;"
    cursor.execute(sql)            
    data = cursor.fetchall()    
    cursor.close()
    finalList = []
    dictionary = {}
    for item in data:        
        dictionary = {}
        dictionary['_id'] = item[0]
        dictionary['name'] = f"{item[1]} {item[2]}"
        dictionary['dept_name'] = item[3]
        dictionary['tot_cred'] = int(item[4])
        finalList.append(dictionary)
    
    pretty_json = json.dumps(finalList, indent=4)
    #print(pretty_json)
    app.run(port = 4500)