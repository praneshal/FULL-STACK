from flask import Flask, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import bcrypt

# Load environment variables
load_dotenv()

# Build DB URI from .env
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DB_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

# Initialize Flask App
app = Flask(__name__, static_folder='frontend/static')
CORS(app)
app.secret_key = 'jeya'

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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


@app.route('/login', methods=['POST'])
def login():
    # Expect JSON input: { "uname": "...", "pword": "..." }
    data = request.json
    uname = data.get('uname')
    pword = data.get('pword')

    # Set greeting based on current time
    current_time = datetime.now().hour
    if current_time < 12:
        greet = "Good Morning"
        greet_img = "img/mng.jpg"
    elif 12 <= current_time < 17:
        greet = "Good Afternoon"
        greet_img = "img/aftn.jpg"
    elif 17 <= current_time < 19:
        greet = "Good Evening"
        greet_img = "img/evng.jpg"
    else:
        greet = "Good Evening"
        greet_img = "img/evng.jpg"

    if uname and pword:
        user = Student.query.filter_by(uname=uname).first()
        if user and bcrypt.checkpw(pword.encode('utf-8'), user.pword.encode('utf-8')):
            gender_normalized = user.gender.strip().upper() if user.gender else "UNKNOWN"
            if gender_normalized not in ['M', 'F']:
                gender_normalized = "UNKNOWN"

            # Set session variables
            session['user_id'] = user.id
            session['fname'] = user.fname.strip()
            session['email'] = user.email
            session['dob'] = str(user.dob)
            session['gender'] = gender_normalized
            session['uname'] = user.uname
            session['img'] = f"/static/img/{'mp.png' if gender_normalized == 'M' else 'fp.png'}"
            session['greet'] = greet
            session['greet_img'] = f"/static/{greet_img}"

            return jsonify({
                'message': 'Login successful',
                'fname': user.fname,
                'email': user.email,
                'dob': str(user.dob),
                'gender': gender_normalized,
                'uname': user.uname,
                'img': session['img'],
                'greet': greet,
                'greet_img': session['greet_img']
            }), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    return jsonify({'error': 'Missing credentials'}), 400

@app.route('/students/dash', methods=['GET'])
def dashboard():
    if 'fname' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    total_exams = db.session.query(func.count(Exam.exid)).scalar()
    total_attempts = db.session.query(func.count(Attempt.id)).filter(Attempt.student_id == session['user_id']).scalar()
    total_messages = db.session.query(func.count(Message.id)).filter(Message.student_id == session['user_id']).scalar()

    return jsonify({
        'fname': session['fname'],
        'email': session.get('email'),
        'dob': session.get('dob'),
        'gender': session.get('gender'),
        'uname': session.get('uname'),
        'img': session.get('img'),
        'greet': session.get('greet'),
        'greet_img': session.get('greet_img'),
        'total_exams': total_exams,
        'total_attempts': total_attempts,
        'total_messages': total_messages
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)