from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, current_app,session
import pymysql
#图片
import os
from flask import Blueprint
from werkzeug.utils import secure_filename
from configuration import connection
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from flask import Blueprint
from flask import session
from flask_mail import Mail, Message
from configuration import mail, connection

subequest_bp = Blueprint('subrequest', __name__)

def get_db_connection():
    return connection

class CourseDetailsNotFoundError(Exception):
    """Exception raised when course details are not found in the database."""
    def __init__(self, message="Course details not found"):
        self.message = message
        super().__init__(self.message)

def get_course_details(q_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 首先从 question 表中获取 course_name
            cursor.execute("SELECT course_name FROM question WHERE q_id = %s", (q_id,))
            question_result = cursor.fetchone()
            if question_result and 'course_name' in question_result:
                course_name = question_result['course_name']
                # 使用获取到的 course_name 从 course 表中获取 course_cat
                cursor.execute("SELECT course_cat FROM course WHERE course_name = %s", (course_name,))
                course_result = cursor.fetchone()
                if course_result and 'course_cat' in course_result:
                    return {'course_name': course_name, 'course_cat': course_result['course_cat']}
                else:
                    # 如果 course_cat 找不到，抛出异常
                    raise CourseDetailsNotFoundError(f"Course category not found for course: {course_name}")
            else:
                # 如果 course_name 找不到，抛出异常
                raise CourseDetailsNotFoundError(f"Course name not found for q_id: {q_id}")
    finally:
        pass




def insert_request(data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO requests (r_type, course_name, r_status, email, q_id, score, course_cat, q_text, r_explanation, llmtype, answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (data['r_type'], data['course_name'], data['r_status'], data['email'], data['q_id'], data['score'], data['course_cat'], data['q_text'], data['r_explanation'], data['llmtype'], data['answer']))
            connection.commit()
    finally:
        pass







@subequest_bp.route('/sub_request', methods=['GET', 'POST'])
def submit_request():
    email = request.form.get("email")
    if email:
        pass
    else:
        email = session.get("email_address")
    print(email)
    current_admin_email = email
    avatar_content = current_admin_email.split('@')[0][:2] # 头像
    name = current_admin_email.split('@')[0] # 全名
    
    if email:
        pass
    else:
        email = session.get("email_address")
    print(email)
    if request.method == 'POST':
        q_id = request.form['q_id']
        file = request.files.get('answer_image')  # 获取上传的文件对象
        try:
            if file:
                # 生成安全的文件名
                filename = secure_filename(file.filename)
                
                # 生成文件的完整路径
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file_path = os.path.join(upload_folder, filename).replace("\\", "/")
                
                # 保存文件到指定路径
                file.save(file_path)
                
                # 获取相对路径
                relative_path = os.path.join('/static', filename).replace("\\", "/")
        #图片
        except Exception as e:  
            # 这里捕获所有异常，但最好只捕获你期望的异常类型  
            return f"文件上传失败: {e}", 500  # 返回500错误和错误信息

        # Additional validation on the server-side for q_id presence
        try:
            course_details = get_course_details(q_id)
        except CourseDetailsNotFoundError as e:
            return f"<script>alert('The question does not exist. Please try again.'); setTimeout(() => {{ window.location = '/sub_request'; }}, 1000);</script>"

        data = {
            'r_type': 'EXPERIMENT',
            'course_name': course_details['course_name'],
            'r_status': 'In Review',
            'email': email,
            'q_id': q_id,
            'score': request.form.get('score', 0),
            'course_cat': course_details['course_cat'],
            'q_text': request.form['q_text'],
            'r_explanation': request.form.get('r_explanation', ''),
            'llmtype': request.form.get('llmtype', ''),
            'answer': relative_path#图片
        }

        insert_request(data)
        return "<script>alert('The request was successfully submitted'); setTimeout(() => { window.location = '/sub_request'; }, 300);</script>"

    return render_template('sub_requestsModel.html', name= name,email=email)













# 修改 这里的代码直接复制 pyx 你要改改你的 return 
@subequest_bp.route("/search",methods=["POST"])
def search():
    search_term = request.form.get("a")
    print("Received search term:", search_term)
    print("3")
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor: 
            print("Received search term1:", search_term)
            sql = "SELECT course_name FROM course WHERE course_name = %s;"
            cursor.execute(sql,(search_term))
            course_names = cursor.fetchall()
            if course_names:
                print("1")
                course_name = [course_name1['course_name'] for course_name1 in course_names]
                print(course_name[0])
                url = "http://127.0.0.1:2020/course/"+course_name[0]
                print(url)
                return redirect(url_for("teacher.course", course_name=course_name[0]))
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)

    try:
        with connection.cursor() as cursor: 
            print("Received search term2:", search_term)
            sql = "SELECT q_text FROM question WHERE q_text = %s;"
            cursor.execute(sql,(search_term))
            q_codes = cursor.fetchall()
            if q_codes:
                print("2")
                q_code = [row['q_code'] for row in q_codes]
                print(q_code[0])
                url = "http://127.0.0.1:2020/questionDetail/"+q_code[0]
                print(url)
                return redirect(url)
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)
    return render_template("error.html")

# if __name__ == '__main__':
#     subequest_bp.run(debug=False, port=5000)


