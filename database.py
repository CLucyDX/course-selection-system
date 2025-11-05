# database.py
from sqlalchemy import Text, Integer,String
from flask_sqlalchemy import SQLAlchemy 

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Comment(db.Model):
    __tablename__ = 'comment'
    llm_id = db.Column(db.Integer)
    comment_content = db.Column(db.Text, nullable=True, primary_key=True)
    email = db.Column(db.String(255), nullable=True)

class Course(db.Model):
    __tablename__ = 'course'
    course_name = db.Column(db.String(255), primary_key=True)
    course_cat = db.Column(db.String(100), nullable=True)

class Experiment(db.Model):
    __tablename__ = 'experiment'
    e_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_text = db.Column(db.Text, nullable=True)
    course_name = db.Column(db.String(255), nullable=True)
    course_cat = db.Column(db.String(100), nullable=True)
    answer = db.Column(db.Text, nullable=True)
    llmtype = db.Column(db.String(50), nullable=True)
    score = db.Column(db.Float, nullable=True)

class LLM(db.Model):
    __tablename__ = 'llm'
    llm_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_id = db.Column(db.Integer, db.ForeignKey('question.q_id'), nullable=True)
    answer = db.Column(db.Text, nullable=True)
    llmtype = db.Column(db.String(100), nullable=True)
    score = db.Column(db.Float, nullable=True)

class Question(db.Model):
    __tablename__ = 'question'
    q_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_text = db.Column(db.Text, nullable=True)
    course_name = db.Column(db.String(255), db.ForeignKey('course.course_name'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'), nullable=True)

class Request(db.Model):
    __tablename__ = 'requests'
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    r_type = db.Column(db.String(50), nullable=True)
    course_name = db.Column(db.String(255), nullable=True)
    r_status = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    q_id = db.Column(db.Integer, db.ForeignKey('question.q_id'), nullable=True)
    course_cat = db.Column(db.String(100), nullable=True)
    q_text = db.Column(db.Text, nullable=True)
    r_explanation = db.Column(db.Text, nullable=True)
    llmtype = db.Column(db.String(50), nullable=True)
    e_id = db.Column(db.Integer, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)

class Score(db.Model):
    __tablename__ = 'score'
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_text = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    score = db.Column(db.Float, nullable=True)

class Topic(db.Model):
    __tablename__ = 'topic'
    course_name = db.Column(db.String(100), db.ForeignKey('course.course_name'), nullable=True)
    topic = db.Column(db.String(255), nullable=True)
    subtopic = db.Column(db.String(255), unique=True, nullable=True)
    topic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Users(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(1), nullable=False)

class Variation(db.Model):
    __tablename__ = 'variation'
    v_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_id = db.Column(db.Integer, db.ForeignKey('question.q_id'), nullable=True)
    q_text = db.Column(db.Text, nullable=True)
    llmstype = db.Column(db.String(255), nullable=True)
    answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()