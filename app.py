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

# Route for Exam List
@app.route('/students/exams.html', methods=['GET'])
def exams():
    if 'uname' not in session:
        return redirect(url_for('login'))
    
    all_exams = Exam.query.all()
    return render_template('exams.html', exams=all_exams)

# Route for Add Exam (Teacher Functionality)
@app.route('/add_exams', methods=['GET', 'POST'])
def add_exams():
    if 'teacher_fname' not in session:
        return redirect(url_for('login_teacher'))

    exid = request.form.get('exid')
    nq = int(request.form.get('nq'))

    # Collect questions and their options
    questions = []
    for i in range(1, nq + 1):
        question_data = Question(
            exid=exid,
            qstn=request.form.get(f'q{i}'),
            qstn_o1=request.form.get(f'o1{i}'),
            qstn_o2=request.form.get(f'o2{i}'),
            qstn_o3=request.form.get(f'o3{i}'),
            qstn_o4=request.form.get(f'o4{i}'),
            qstn_ans=request.form.get(f'a{i}'),
            # sno=i  # Assuming the serial number is the question's order
        )
        questions.append(question_data)

    try:
        # Save all questions to the database
        db.session.bulk_save_objects(questions)
        db.session.commit()
        flash('Questions updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating questions: {str(e)}', 'danger')

    return redirect(url_for('teacher_dashboard'))


#Route for Take Exam
@app.route('/take_exam/<int:exid>', methods=['GET', 'POST'])
def take_exam(exid):
    if 'uname' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Fetch exam details using SQLAlchemy
    exam = Exam.query.get_or_404(exid)  # Get the exam using SQLAlchemy's ORM
    questions = Question.query.filter_by(exid=exid).all()  # Get questions for the exam

    # Convert subtime to ISO format (JavaScript-readable)
    exam_subtime = exam.subt.isoformat() if exam.subt else None  # Ensure it’s in ISO format

    if request.method == 'POST':
        # Process answers
        total_score = 0
        for question in questions:
            selected_option = request.form.get(f"o{question.qid}", None)  # Match radio button names
            if selected_option and int(selected_option) == question.qstn_ans:
                total_score += 1
        
        # Calculate percentage
        percentage = (total_score / len(questions)) * 100 if len(questions) > 0 else 0

        # Determine status based on score
        status = 1 if percentage >= 40 else 0  # Example logic, adjust as needed
        
        # Save attempt using SQLAlchemy
        attempt = Attempt(
            exid=exid,
            student_id=session['user_id'],
            uname=session.get('uname'),
            nq=exam.nq,
            cnq=total_score,  # Correct number of answers
            ptg=percentage,   # Percentage
            status=status,    # Assign status
        )
        db.session.add(attempt)
        db.session.commit()

        # Flash message for feedback
        if status == 1:
            flash(f"Congratulations! You passed the exam with a score of {total_score}/{len(questions)} ({percentage}%).", "success")
        else:
            flash(f"You failed the exam with a score of {total_score}/{len(questions)} ({percentage}%).", "danger")

        # Redirect to a results or another page
        return render_template('examportal.html', exam=exam, questions=questions, exam_subtime=exam_subtime)

    return render_template('examportal.html', exam=exam, questions=questions, exam_subtime=exam_subtime)


# Route for Submit Exam
@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    if 'uname' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Retrieve exam details and questions
    exid = request.form.get('exid')
    exam = Exam.query.get_or_404(exid)
    questions = Question.query.filter_by(exid=exid).all()

    if not questions:
        flash("There are no questions in this exam.", "error")
        return redirect(url_for('exams'))  # Redirect if no questions are available

    total_score = 0

    for question in questions:
        selected_option = request.form.get(f"o{question.qid}")
        if selected_option and selected_option == str(question.qstn_ans):  # Compare with correct answer
            total_score += 1

    # Calculate percentage and status
    percentage = (total_score / len(questions)) * 100 if questions else 0
    status = 1 if percentage >= 40 else 0  # You can change this threshold if needed

    # Save the attempt
    attempt = Attempt(
        exid=exid,
        student_id=session['user_id'],
        uname=session.get('uname'),
        nq=len(questions),
        cnq=total_score,
        ptg=percentage,
        status=status,
    )
    db.session.add(attempt)
    db.session.commit()

    flash(f"You scored {total_score}/{len(questions)}! Status: {'Passed' if status else 'Failed'}", "success")
    return redirect(url_for('exams'))


#Routr for Results
@app.route('/students/results.html', methods=['GET'])
def results():
    if 'uname' not in session:
        return redirect(url_for('login'))

    uname = session['uname']
    student = Student.query.filter_by(uname=uname).first()
    if student is None:
        return redirect(url_for('login'))

    # Query the attempts with exams
    attempts = (
        db.session.query(Attempt, Exam)
        .join(Exam, Attempt.exid == Exam.exid)  # Use outer join
        .filter(Attempt.student_id == student.id)
        .all()
    )
    for attempt, exam in attempts:
        if attempt.cnq is not None and exam.nq is not None:
            attempt.ptg = round((attempt.cnq / exam.nq) * 100, 2) # Calculate percentage
        else:
            attempt.ptg = 0
    return render_template('results.html', attempts=attempts, student=student)


#Route for Student Messages
@app.route('/students/messages.html')
def messages():
    if 'user_id' not in session:
        flash('Please log in to access messages.', 'warning')
        return redirect(url_for('login_student'))

    # Retrieve the logged-in user's ID from the session
    user_id = session['user_id']

    # Query messages for the logged-in user only
    messages = (
        Message.query.filter_by(student_id=user_id)
        .join(Student, Message.student_id == Student.id)
        .add_columns(
            Message.id,  # Ensure we fetch the message ID
            Message.fname,
            Message.date,
            Message.feedback,
            Student.fname.label('student_fname')
        )
        .all()
    )

    return render_template('messages.html', messages=messages)

#Route to Delete Message Student
@app.route('/students/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if 'user_id' not in session:
        flash('Please log in to delete messages.', 'warning')
        return redirect(url_for('login_student'))

    # Query the message to ensure it belongs to the logged-in user
    message = Message.query.get(message_id)
    if not message or message.student_id != session['user_id']:
        flash('You are not authorized to delete this message.', 'danger')
        return redirect(url_for('messages'))

    try:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting the message: {str(e)}', 'error')

    return redirect(url_for('messages'))


#Route For Settings
@app.route('/students/settings.html', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        flash('Please log in to access settings.', 'warning')
        return redirect(url_for('login'))
    
    student = Student.query.filter_by(id=session['user_id']).first()
    
    if request.method == 'POST':
        # Get form data
        fname = request.form.get('fname').strip()
        uname= request.form.get('uname').strip()
        email = request.form.get('email').strip()
        dob = request.form.get('dob').strip()
        gender = request.form.get('gender').strip().upper()

        # Update student details
        if student:
            student.fname = fname
            student.uname = uname
            student.email = email
            student.dob = datetime.strptime(dob, "%Y-%m-%d").date() if dob else student.dob
            student.gender = gender
            db.session.commit()

            # Update session variables
            session['fname'] = fname
            session['uname'] = uname
            session['email'] = email
            session['dob'] = dob
            session['gender'] = gender
            session['img'] = url_for(
                'static',
                filename=f'img/{"mp.png" if gender == "M" else "fp.png"}'
            )

            flash('Profile updated successfully! Kindly re-login to see the changes.', 'success')
            return redirect(url_for('logout'))  # Force re-login
        else:
            flash('Student record not found.', 'error')
            return redirect(url_for('dashboard'))

    return render_template('settings.html', student=student)


#Route for Help
@app.route('/students/help.html')
def help_page():
    # Ensure user is logged in
    if 'fname' not in session:
        return redirect(url_for('login'))
    
    # Pass session data to template
    return render_template('help.html')


def format_date(value, format="%b %d, %Y"):
    if value:
        return value.strftime(format)
    return ""

app.jinja_env.filters['date'] = format_date



#Route for Exam(Teacher)
@app.route('/exams', methods=['GET', 'POST'])
def manage_exams():
    if request.method == 'POST':
        exname = request.form.get('exname')
        desp = request.form.get('desp')
        extime = datetime.strptime(request.form.get('extime'), '%Y-%m-%dT%H:%M')
        subt = datetime.strptime(request.form.get('subt'), '%Y-%m-%dT%H:%M')
        nq = request.form.get('nq')
        exam = Exam(exname=exname, desp=desp, extime=extime, subt=subt, nq=nq)
        db.session.add(exam)
        db.session.commit()
        flash('Exam added successfully!', 'success')
        return redirect(url_for('manage_exams'))
    
    exams = Exam.query.all()  # Fetch all exams
    return render_template('teacher_exam.html', exams=exams)


@app.route('/delete_exam/<int:exid>', methods=['POST'])
def delete_exam(exid):
    exam = Exam.query.get(exid)
    if exam:
        db.session.delete(exam)  # This will also delete all related attempts due to cascade
        db.session.commit()
        flash('Exam and related attempts deleted successfully!', 'danger')
    else:
        flash('Exam not found!', 'warning')
    return redirect(url_for('exams'))


@app.route('/edit_exam/<int:exid>', methods=['GET', 'POST'])
def edit_exam(exid):
    exam = Exam.query.get_or_404(exid)
    
    if request.method == 'POST':
        exam.exname = request.form.get('exname')
        exam.desp = request.form.get('desp')
        exam.extime = datetime.strptime(request.form.get('extime'), '%Y-%m-%dT%H:%M')
        exam.subt = datetime.strptime(request.form.get('subt'), '%Y-%m-%dT%H:%M')
        exam.nq = request.form.get('nq')
        db.session.commit()
        flash('Exam updated successfully!', 'info')
        return redirect(url_for('manage_exams'))
    
    return render_template('edit_exam.html', exam=exam)


#Route for Records
@app.route('/records')
def records():
    if 'teacher_fname' not in session:
        return redirect(url_for('teacher_login'))
    students = Student.query.all()
    return render_template("records.html", students=students)

#Route for Help
@app.route('/help')
def help():
    if 'teacher_fname' not in session:
        return redirect(url_for('teacher_login'))
    return render_template("teacher_help.html")

app.jinja_env.globals.update(enumerate=enumerate)

