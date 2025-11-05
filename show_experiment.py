from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, Blueprint,session
import pymysql
from configuration import connection

# experiment_bp = Flask(__name__)
experiment_bp = Blueprint('experiment', __name__)

def get_db_connection():
    """Create a database connection using pymysql."""
    # return pymysql.connect(
    #     host='localhost',
    #     user='root',
    #     password='',  # Update with your MySQL password
    #     database='asdw',  # Update with your database name # 数据修改
    #     charset='utf8mb4',
    #     cursorclass=pymysql.cursors.DictCursor
    # )
    return connection

def fetch_experiment_data():
    """Fetch data from the experiment table."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM experiment")
            entries = cursor.fetchall()
    finally:
        pass
    return entries

@experiment_bp.route('/experiment')
def show_experiments():
    """Render experiments.html template with fetched data."""
    ut = session.get('ut')

    email = session.get('email_address')
    if email:
        current_admin_email = email
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
        # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""

    # 全局搜索的代码
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT course_name FROM Course;"
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
    #111111111111111111
    try:
        entries = fetch_experiment_data()
        #print(entries)
        # return render_template('show_experiment.html', entries=entries)
        return render_template('show_experimentModel.html', entries=entries)
    except Exception as e:
        # 处理异常，例如打印错误信息或者返回错误页面
        print("An error occurred:", str(e))
        # return render_template('show_experiment.html', entries = entries,error_message=str(e),email=current_admin_email, content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
        return render_template('show_experimentModel.html', entries = entries,error_message=str(e),email=current_admin_email, content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)

@experiment_bp.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("a")
    print("Received search term:", search_term)
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 对e_id字段使用CAST将其转换为字符类型，并使用LIKE进行模糊匹配
            sql = """
            SELECT * FROM experiment WHERE 
                CAST(e_id AS CHAR) LIKE %s OR
                q_text LIKE %s OR 
                course_name LIKE %s OR 
                course_cat LIKE %s OR 
                answer LIKE %s OR 
                llmtype LIKE %s OR 
                r_explanation LIKE %s OR 
                score LIKE %s
            """
            search_like = f"%{search_term}%"
            cursor.execute(sql, (search_like,) * 8)  # 重复search_like参数八次
            results = cursor.fetchall()
            print(results)
            if results:
                # return render_template("search_experiment_results.html", results=results)
                return render_template("search_experiment_resultsModel.html", results=results)

            else:
                # return render_template("search_experiment_results.html", message="No matches found.")
                return render_template("search_experiment_resultsModel.html", message="No matches found.")
    except Exception as e:
        print("Error:", e)
        return render_template("error.html", error_message=str(e))
    finally:
        pass



