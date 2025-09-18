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

