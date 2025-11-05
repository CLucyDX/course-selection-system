"""
Preparation:
    Please confirm that the database configuration in the configuration.py file is correct. 
    Our MySQL database file is sdw.sql. If the database is not configured, please import the relevant data into MySQL
"""


# 测试使用蓝图进行统筹
from flask import Flask
from student import student_bp
from teacher import teacher_bp
from user import login_bp
from admin import admin_bp
from request import request_bp
from variation import variation_bp
from sub_requests import subequest_bp
from show_experiment import experiment_bp
from database import db, Course, Question, LLM, init_db
from configuration import app


# 注册蓝图
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(request_bp)
app.register_blueprint(variation_bp)
app.register_blueprint(subequest_bp)
app.register_blueprint(experiment_bp)

# 初始化数据库
init_db(app)
if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)
