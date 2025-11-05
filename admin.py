"""
Author:       Clio
Date:         2024-4-22  22:03:01
Version:      1.0
LastEditors:  Clio
LaetEditTime: 2024-4-22  22:03:01
FilePath:     N
"""
import string
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from configuration import connection
import pymysql
from flask import Blueprint
admin_bp = Blueprint('admin', __name__)

# create a login api
@admin_bp.route("/Admin_login")
def begin():
    return render_template('A_Login.html')
    

# 这个函数可以放外面
@admin_bp.route("/admin_page/<email>")
def admin_pages(email):
    if email:
        current_admin_email = email
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
        # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    if user_type["user_type"] == "A":
        request_types =  ["","None"] 
    elif user_type["user_type"] == 'S':
        request_types = ["","UPDATE_SCORE","CHANGE"] 
    else:
        request_types = ["","ADD_COURSE", "UPDATE_SCORE","CHANGE"] 
    ut = user_type["user_type"]
    # 全局搜索的代码
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)# 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT q_text FROM question;"
            cursor.execute(sql)
            assignments_list= cursor.fetchall()
    except Exception as e:
        print("Error:", e)# 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question."
    # return render_template("admin.html", ut=ut,email=current_admin_email, content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    return render_template("adminModel.html", ut=ut,email=current_admin_email, content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)

@admin_bp.route("/handle",methods=["POST"])
def Handle():
    """Verifying Request's information
    :param:  Q_ID: question number
                Score: the score of LLMs's answer
                email: request from user which emailaddress is email
    :return: VERIFY_HANDLE = {WRONG_Q_ID, Wrong_email, Wrong_Score, OK};
    """
    return redirect(url_for("request.to_handle"))



