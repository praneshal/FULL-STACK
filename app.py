from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text
import logging
from datetime import datetime
import bcrypt

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'jeya'

# Configure Database for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pranesh:jeya@localhost:5432/FULL_STACK'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User Model
# Define User Model
class Student(db.Model):
    __tablename__ = 'student'  # Ensure this matches the table name in your database
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    uname = db.Column(db.String(50), unique=True, nullable=False)
    pword = db.Column(db.String(200), nullable=False)
    attempts = db.relationship('Attempt', backref='student', lazy=True)

# Define Teacher Model
class Teacher(db.Model):
    __tablename__ = 'teacher'  # Matches the table name in your database
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    uname = db.Column(db.String(100), unique=True, nullable=False)  # Unique username
    pword = db.Column(db.String(255), nullable=False)  # Password
    fname = db.Column(db.String(100), nullable=False)  # Full name
    dob = db.Column(db.Date, nullable=False)  # Date of birth
    gender = db.Column(db.String(10), nullable=False)  # Gender
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email
    subject = db.Column(db.String(100), nullable=False) 

# Define Exams Model
class Exam(db.Model):
    __tablename__ = 'exm_list'
    exid = db.Column(db.Integer, primary_key=True)  # Use 'exid' as the primary key
    exname = db.Column(db.String(100))
    nq = db.Column(db.Integer)
    desp = db.Column(db.String(100))
    subt = db.Column(db.DateTime)
    extime = db.Column(db.DateTime)
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp())
    subject = db.Column(db.String(100))

    # Define relationship with attempts, enabling cascading deletes
    attempts = db.relationship('Attempt', backref='exam', cascade='all, delete-orphan')


class Attempt(db.Model):
    __tablename__ = 'atmpt_list'
    id = db.Column(db.Integer, primary_key=True)
    exid = db.Column(db.Integer, db.ForeignKey('exm_list.exid'), nullable=False)  # Foreign key to Exam
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))  # Foreign key to Student
    uname = db.Column(db.String(100), nullable=False)  # Username associated with the attempt
    nq = db.Column(db.Integer, nullable=False)  # Number of questions
    cnq = db.Column(db.Integer, nullable=False)  # Correct answers
    ptg = db.Column(db.Integer, nullable=False)  # Percentage
    status = db.Column(db.Integer, nullable=False)  # Status of the attempt
    subtime = db.Column(db.DateTime, default=db.func.current_timestamp())  # Submission time

# Define Messages Model
class Message(db.Model):
    __tablename__ = 'message'  # Ensure this matches the actual table name in your database
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)  # Name of the sender
    date = db.Column(db.DateTime, default=db.func.current_timestamp())  # Date and time of the message, default to current timestamp
    feedback = db.Column(db.String(1000), nullable=False)  # The actual message content
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  # Foreign key to the Student table
    student = db.relationship('Student', backref=db.backref('message', lazy=True))  # Relationship with the Student model


# Define Question Model
class Question(db.Model):
    __tablename__ = 'qstn_list'
    qid = db.Column(db.Integer, primary_key=True)
    exid = db.Column(db.Integer, db.ForeignKey('exm_list.exid'))
    qstn = db.Column(db.String(500))
    qstn_o1 = db.Column(db.String(100))
    qstn_o2 = db.Column(db.String(100))
    qstn_o3 = db.Column(db.String(100))
    qstn_o4 = db.Column(db.String(100))
    qstn_ans = db.Column(db.Integer)
    sno = db.Column(db.Integer, nullable=False, autoincrement=True)


# Route for Login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'fname' in session:
        return redirect(url_for('dashboard'))

    uname = None
    pword = None

    if request.method == 'POST':
        uname = request.form.get('uname')
        pword = request.form.get('pword')
    elif request.method == 'GET':
        uname = request.args.get('uname')
        pword = request.args.get('pword')

    # Set a default greeting before processing login
    current_time = datetime.now().hour
    if current_time < 12:
        session['greet'] = "Good Morning"
        session['greet_img'] = url_for('static', filename='img/mng.jpg')
    elif 12 <= current_time < 17:
        session['greet'] = "Good Afternoon"
        session['greet_img'] = url_for('static', filename='img/aftn.jpg')
    elif 17 <= current_time < 19:
        session['greet'] = "Good Evening"
        session['greet_img'] = url_for('static', filename='img/evng.jpg')
    else:
        session['greet'] = "Good Evening"
        session['greet_img'] = url_for('static', filename='img/evng.jpg')

    if uname and pword:
        # Check user credentials
        user = Student.query.filter_by(uname=uname).first()
        if user and bcrypt.checkpw(pword.encode('utf-8'), user.pword.encode('utf-8')):
            gender_normalized = user.gender.strip().upper()
            if gender_normalized not in ['M', 'F']:
                gender_normalized = "UNKNOWN"

            # Set session variables
            session['user_id'] = user.id
            session['fname'] = user.fname.strip()
            session['email'] = user.email
            session['dob'] = str(user.dob)
            session['gender'] = gender_normalized
            session['uname'] = user.uname
            session['img'] = url_for(
                'static',
                filename=f'img/{"mp.png" if gender_normalized == "M" else "fp.png"}'
            )

            return redirect(url_for('dashboard'))
        else:
            logging.debug("Invalid username or password")
            return "Invalid username or password", 401

    # Pass greeting to the template
    return render_template('login.html', greet=session['greet'], greet_img=session['greet_img'])

@app.route('/students/dash')
def dashboard():
    if 'fname' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    uname = session['uname']

    # Query counts from the database
    total_exams = db.session.query(func.count(Exam.exid)).scalar()  # Use 'exid' instead of 'id'
    total_attempts = db.session.query(func.count(Attempt.id)).filter(Attempt.student_id == session['user_id']).scalar()
    total_messages = db.session.query(func.count(Message.id)).filter(Message.student_id == session['user_id']).scalar()

    return render_template('student_dashbord.html', fname=session['fname'], total_exams=total_exams, total_attempts=total_attempts, total_messages=total_messages)

# Route for Logout
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))  # Redirect to login page

# Route for Teacher Login
@app.route('/teacher_login.html')
def teacher_login():
    if 'teacher_fname' in session:  # Check if teacher is already logged in
        return redirect(url_for('teacher_dashboard'))

    uname = None
    pword = None

    if request.method == 'POST':
        uname = request.form.get('uname')
        pword = request.form.get('pword')
    elif request.method == 'GET':
        uname = request.args.get('uname')
        pword = request.args.get('pword')

    current_time = datetime.now().hour
    if current_time < 12:
        session['greet'] = "Good Morning"
        session['greet_img'] = url_for('static', filename='img/mng.jpg')
    elif 12 <= current_time < 17:
        session['greet'] = "Good Afternoon"
        session['greet_img'] = url_for('static', filename='img/aftn.jpg')
    elif 17 <= current_time < 19:
        session['greet'] = "Good Evening"
        session['greet_img'] = url_for('static', filename='img/evng.jpg')
    else:
        session['greet'] = "Good Evening"
        session['greet_img'] = url_for('static', filename='img/evng.jpg')
    if uname and pword:
        # Check teacher credentials
        teacher = Teacher.query.filter_by(uname=uname).first()
        if teacher and bcrypt.checkpw(pword.encode('utf-8'), teacher.pword.encode('utf-8')):
            # Log full teacher record and gender field for debugging
            logging.debug(f"Teacher Record: {teacher}")
            logging.debug(f"Raw Gender from DB: '{teacher.gender}'")

            # Normalize gender to handle extra spaces and inconsistent casing
            gender_normalized = teacher.gender.strip().upper()
            logging.debug(f"Normalized Gender: '{gender_normalized}'")  # Debug normalized gender

            # Validate gender format (default to "UNKNOWN" if invalid)
            if gender_normalized not in ['M', 'F']:
                gender_normalized = "UNKNOWN"
                logging.debug(f"Invalid Gender Detected. Defaulting to '{gender_normalized}'")

            # Set session variables
            session['teacher_id'] = teacher.id
            session['teacher_fname'] = teacher.fname.strip()  # Trim any extra spaces from name
            session['teacher_email'] = teacher.email
            session['teacher_dob'] = str(teacher.dob)
            session['teacher_gender'] = gender_normalized  # Use normalized gender
            session['teacher_uname'] = teacher.uname

            # Assign profile image based on normalized gender
            session['teacher_img'] = url_for(
                'static',
                filename=f'img/{"mp.png" if gender_normalized == "M" else "fp.png"}'
            )

            return redirect(url_for('teacher_dashboard'))
        else:
            logging.debug("Invalid username or password for teacher")  # Debug invalid login attempt
            return "Invalid username or password", 401

    return render_template('teacher_login.html',greet=session['greet'], greet_img=session['greet_img'])

#Route for Teacher Dashbord
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'teacher_fname' not in session:  # Redirect to login if not logged in
        return redirect(url_for('teacher_login'))

    uname = session['teacher_uname']
    recent_results = db.session.query(
        Attempt.subtime,
        Attempt.uname,
        Exam.exname.label('exam_name'),
        Attempt.ptg
    ).join(Exam, Exam.exid == Attempt.exid) \
     .order_by(Attempt.subtime.desc()) \
     .limit(5).all()
    recent_results_dicts = [
    {
        'subtime': result.subtime.strftime("%Y-%m-%d"),  # Format as YYYY-MM-DD
        'uname': result.uname,
        'exam_name': result.exam_name,
        'ptg': result.ptg,
    }
    for result in recent_results
]
    # Query counts from the database
    total_students = db.session.query(func.count(Student.id)).scalar()
    total_exams = db.session.query(func.count(Exam.exid)).scalar()
    total_exams_created = db.session.query(func.count(Exam.exid)).filter(Exam.subject == session['teacher_uname']).scalar()
    total_students_attempted = db.session.query(func.count(Attempt.student_id.distinct())).join(
    Exam, Exam.exid == Attempt.exid
).join(
    Teacher, Teacher.uname == session['teacher_uname']
).filter(
    Exam.subject == Teacher.subject
).scalar()
    total_messages_received = db.session.query(func.count(Message.id)).join(
    Student, Student.id == Message.student_id
).join(
    Attempt, Attempt.student_id == Student.id
).join(
    Exam, Exam.exid == Attempt.exid
).filter(
    Exam.exname == session['teacher_uname']
).scalar()

    return render_template(
        'teacher_dashbord.html',
        fname=session['teacher_fname'],
        total_exams_created=total_exams_created,
        total_students_attempted=total_students_attempted,
        total_messages_received=total_messages_received,
        recent_results=recent_results_dicts,
        total_students=total_students,
        total_exams=total_exams
    ) 
#test_Connection
@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Query the first row from the 'student' table
        result = db.session.execute(text('SELECT * FROM student LIMIT 1')).fetchone()
        if result:
            return f"Database connection successful! First row: {result}", 200
        else:
            return "Database connection successful but no rows found in the 'student' table.", 200
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

