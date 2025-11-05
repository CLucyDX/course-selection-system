"""
Author:       Clio
Date:         2024-4-28  11:03:01
Version:      1.0
LastEditors:  Clio
LaetEditTime: 2024-4-30  19:38:01
FilePath:     N
"""


from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from flask import Blueprint
from flask import session
from flask_mail import Mail, Message
from configuration import mail, connection

request_bp = Blueprint('request', __name__)

requests = [] # 所有请求


# 申请类型选项
request_types = ["","ADD_COURSE", "UPDATE_SCORE","CHANGE"] # ,"ADD_QUESTION" 暂时不要添加问题
course_type = ["","Writing","Math","Computers and programming"]

@request_bp.route("/")
def index(): # 暂时的入口
    tip = ''
    if request.args.get("tip"):
        tip = request.args.get("tip")
    return render_template("to_request.html",tip = tip)


# 渲染请求填写页面
@request_bp.route("/make_request",methods=["GET", "POST"])
def make_request():
    """
    渲染
    :param tip: 确定是否成功
    :return: {"Error occurred while create a request.", render_template}
    """
    email = request.args.get("email")
    if email:
        pass
    else:
        email = request.form.get("email")
    # 这里传递用户信息
    current_admin_email = email
    avatar_content = current_admin_email.split('@')[0][:2] # 头像
    name = current_admin_email.split('@')[0] # 全名
    
    tip = ''
    if request.args.get("tip"):
        tip = request.args.get("tip")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    
    if user_type:
        pass
    else:
        user_type = session.get("ut")
    # pyx: 设置 make request 下拉框中的选项
    if user_type["user_type"] == "A":
        request_types =  ["","None"] 
    elif user_type["user_type"] == 'S':
        request_types = ["","UPDATE_SCORE"] 
    else:
        request_types = ["","ADD_COURSE", "UPDATE_SCORE","CHANGE"] 
    ut = user_type["user_type"]
    course = None
    
    # 得到当前问题
    try:
        with connection.cursor() as cursor:
            sql = "SELECT q_text FROM question;"
            cursor.execute(sql)
            questions1 = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    try:
        with connection.cursor() as cursor:
            sql = "SELECT q_text FROM variation;"
            cursor.execute(sql)
            questions2 = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of variation."
    questions = questions1 + questions2
    #questions_json = json.dumps(questions)

    # 得到当前课程
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM course;"
            cursor.execute(sql)
            courses = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            sub = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 07"
    
    # return render_template("request.html", sub=sub, ut=ut,request_types=request_types, course_types=course_type, tip=tip, questions = questions, courses=courses,email=current_admin_email, content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    return render_template("requestModel.html", sub=sub, ut=ut,request_types=request_types, course_types=course_type, tip=tip, questions = questions, courses=courses,email=current_admin_email, content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)


@request_bp.route("/submit", methods=["GET", "POST"])
def  Submit(): # 提交request
    """
    点击提交后
    :param request_type: 请求类型
    :param course_type: 课程类型
    :param request_id: 请求编号
    :return: {"Error occurred while create a request.", render_template}
    """

    # 得到前面页面传来的q_id
    q_id = int(request.form.get("q_id", "0"))
    # 得到当前所有请求
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM requests;"
            cursor.execute(sql)
            requests = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront."
    
    # 得到当前问题
    try:
        with connection.cursor() as cursor:
            sql = "SELECT q_text FROM question;"
            cursor.execute(sql)
            questions1 = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    try:
        with connection.cursor() as cursor:
            sql = "SELECT q_text FROM variation;"
            cursor.execute(sql)
            questions2 = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of variation."
    questions = questions1 + questions2
    
    # 得到当前课程
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM course;"
            cursor.execute(sql)
            courses = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    
    # 得到用户在页面填写的内容 # 如有添加在下方添加的到的数据
    if request.method == "POST":
        request_type = request.form["request_type"] # 请求类型
        # add course
        course_type = request.form.get("course_type", "NULL") # 选择的课程类型
        course_name = request.form.get("course", "NULL") # 添加课程名称
        # add question  名字 答案 lms course_name(这个上面得到啦)
        request_question2 = request.form.get("question2", "NULL") # 添加问题题目
        request_q_description = request.form.get("q_describe","NULL") # 添加问题描述
        # request_answer = request.form.get("answer","NULL") # 添加问题 答案
        # update score 问题名字 分数 和理由
        request_question = request.form.get("question", "NULL")
        request_score = request.form.get("q_score") # 修改分数
        print(request_score)
        print(type(request_score))
        if request_score is not None and request_score != '':
            try:
                request_score = float(request_score)
            except ValueError:
                return 'Invalid value for score!'
        else:
            request_score = 0
        # variation q_text llms answer
        request_question3 = request.form.get("question3", "NULL")
        request_llmstype = request.form.get("request_llmstype", "NULL")
        request_answer = request.files['answer2']
        request_answer = request_answer.filename
        request_llms = request.form.get("llms","NULL")
        email = request.form.get("email")
        # 这里传递用户信息
        current_admin_email = email
        avatar_content = current_admin_email.split('@')[0][:2] # 头像
        name = current_admin_email.split('@')[0] # 全名
        # pyx: 设置 make request 下拉框中的选项
        try:
            with connection.cursor() as cursor:
                sql = "SELECT user_type FROM users WHERE email=%s;"
                cursor.execute(sql,(email))
                user_type = cursor.fetchone()
        except Exception as e:
            print("Error1:", e)
            return "Error occurred while submit infront of question."
        if user_type:
            pass
        else:
            user_type = session.get("ut")
        if user_type["user_type"] == "A":
            request_types =  ["","None"] 
        elif user_type["user_type"] == 'S':
            request_types = ["","UPDATE_SCORE","CHANGE"] 
        else:
            request_types = ["","ADD_COURSE", "UPDATE_SCORE","CHANGE"] 
        ut = user_type["user_type"]
        # 所有请求共用
        request_explanation = request.form.get("explanation", "NULL") # 分数理由

        

        # 检查是否和当前已有请求重复 # 如有添加和修改在下方进行 # 这里缺少对分数修改的次数限制，数据库完成后添加
        for req in requests:
            if req["r_type"] == request_type:

                if request_type == "ADD_COURSE":
                    for course in courses:
                        if course["course_name"] == course_name  and course["course_cat"] == course_type:
                            error = "Fail1"
                            tip = "The Course already exists"
                            return redirect(url_for("request.make_request",tip = tip, email=email))
                        elif req["course_name"] == course_name and req["email"] == email:
                            error = "Fail1"
                            tip = "The request already exists"
                            return redirect(url_for("request.make_request",tip = tip,email=email))
                
                if request_type == "UPDATE_SCORE" and req["q_text"] == request_question and req["score"] == request_score and req["email"] == email:
                    # 检查用户是否修改过该问题，如果改过，就返回错误 # zcy
                    # 用户提供的q_text和email示例
                    user_q_text = 'example_question_text'  # 替换为用户实际的q_text
                    user_email = 'example@example.com'  # 替换为用户实际的email

                    try:
                        # 建立到数据库的连接
                        with connection.cursor() as cursor: 

                        # 查询语句，检查q_text与email是否已存在于score表中
                            query = """
                            SELECT EXISTS (
                            SELECT 1
                            FROM score
                            WHERE q_text = %s AND email = %s
                            )
                            """
                            cursor.execute(query, (user_q_text, user_email))

                        # 获取查询结果，返回值是((0,),)或((1,),)，表示不存在或存在
                            (exists,) = cursor.fetchone()

                            # 根据查询结果打印信息
                            if exists:
                                print(f"警告：q_text与email的组合已存在于数据库中。")
                                error = "Fail1"
                                tip = "The request already exists"
                                return redirect(url_for("request.make_request",tip = tip,email=email))
                            else:
                                print(f"q_text与email的组合未在数据库中出现，可以安全修改。")

                    except pymysql.MySQLError as error:
                        print(f"Something went wrong: {error}")
                        return "Error: in score time"
                    

                if request_type == "CHANGE": # 没有判断
                    request_question = request_question3
                if request_type == "None":
                    tip = "You can not do this way!"
                    return redirect(url_for("request.make_request",tip = tip,email=email))

                # add question 暂时不用修改
                if request_type == "ADD_QUESTION":
                    for question in questions:
                        if question["question"] == request_question and question["course_type"] == course_type:
                            error = "Fail1"
                            tip = "The Question already exists"
                            return redirect(url_for("request.make_request",tip = tip,email=email))
                        elif req["question"] == request_question and req["course_type"] == course_type:
                            error = "Fail1"
                            tip = "The request already exists"
                            return redirect(url_for("make_request",tip = tip,email=email))
            
        # 如果不存在相同的请求，执行通过 进行数据插入
        try:
            with connection.cursor() as cursor:                                                                                      # 这里的course 放 answer 
                sql = "INSERT INTO requests (r_type, course_name, email, q_id, score, course_cat, q_text, r_explanation, llmtype, e_id, answer) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (request_type, course_name, email, q_id, request_score, course_type,  request_question, request_explanation, request_llmstype, 0, request_answer))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error2 occurred: {e}")
            return "Error occurred while submitting request."
        
        #return "Success" 如果成功 返回进入请求页的页面
        tip = "Success"
        return redirect(url_for("request.make_request",tip = tip,email=email,ut=ut))


@request_bp.route("/CheckScoreUpdate", methods=["GET", "POST"])
def CheckScoreUpdate(): # 学生和老师共用 #老师通过对题目的改变来改变分数或上报分数，学生上报分数进行改变
    """
    点击分数检查，所有用户都可以使用 并渲染页面
    :param user["email"]: 当前用户邮箱
    :return: {"Error occurred while check scoreUpdate.", render_template("check_score.html",requests_s=request_s)}
    """
    email = request.args.get("email")
    # 这里传递用户信息
    current_admin_email = email
    avatar_content = current_admin_email.split('@')[0][:2] # 头像
    name = current_admin_email.split('@')[0] # 全名
    if email:
        pass
    else:
        email = session.get("email_address")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error3:", e)
        return "Error occurred while submit infront of question."
    if user_type:
        pass
    else:
        user_type = session.get("ut")
    if user_type["user_type"] == "A":
        request_types =  ["","None"] 
    elif user_type["user_type"] == 'S':
        request_types = ["","UPDATE_SCORE"] 
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
        print("Error4:", e)# 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT q_text FROM question;"
            cursor.execute(sql)
            assignments_list= cursor.fetchall()
    except Exception as e:
        print("Error:", e)# 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question."
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            sub = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 07"
    # 这里的到邮件相关的请求数据，类型为UPDATE_SCORE的请求以及修改的问题本身
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM requests WHERE email = %s AND r_type IN ('UPDATE_SCORE', 'EXPERIMENT');"# and q_id = ? 
            cursor.execute(sql,(email))
            request_s = cursor.fetchall()
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while check scoreUpdate."
    
    return render_template("check_scoreModel.html",sub=sub, ut=ut,requests_s=request_s,email=current_admin_email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)


@request_bp.route("/CheckRequest", methods=["GET", "POST"])
def CheckRequest(): # 只有老师使用 这里的数据来源于数据库中与email相关连的请求
    """
    点击请求检查，所有只有老师类型的用户可以使用 并渲染页面
    :param user["email"]: 当前用户邮箱
    :return: {"Error occurred while check requests.", render_template("check_request.html",requests=requests)}
    """
    email = request.args.get("email")
    if email:
        pass
    else:
        email = session.get("email_address")
    # 这里传递用户信息
    current_admin_email = email
    avatar_content = current_admin_email.split('@')[0][:2] # 头像
    name = current_admin_email.split('@')[0] # 全名
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    if user_type:
        pass
    else:
        user_type = session.get("ut")
    if user_type["user_type"] == "A":
        request_types =  ["","None"] 
    elif user_type["user_type"] == 'S':
        request_types = ["","UPDATE_SCORE","CHANGE","EXPERIMENT"] 
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            sub = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 07"
    # email 相关所有请求
    try:
        with connection.cursor() as cursor:
            # 根据用户email进行查找
            sql = "SELECT * FROM requests WHERE email = %s;"
            cursor.execute(sql,(email))
            requests = cursor.fetchall()
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while check requests."
    
    # return render_template("check_request.html",sub=sub, ut=ut,requests=requests,email=current_admin_email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    return render_template("check_requestModel.html",sub=sub, ut=ut,requests=requests,email=current_admin_email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)


# 以下操作只有管理员可进行
@request_bp.route("/handle_page", methods=["GET", "POST"])
def to_handle():
    """
    点击跳入处理，只有admin可以使用
    :param user["email"]: 当前用户邮箱
    :param page: 帮助页面进行渲染
    :return: {return "Error occurred while to handle page.", render_template("check_request.html",requests=requests)}
    """
    email = request.form.get("email")
    if email:
        # 这里传递用户信息
        current_admin_email = email
        avatar_content = current_admin_email.split('@')[0][:2] # 头像
        name = current_admin_email.split('@')[0] # 全名
    else:
        email = request.args.get("email")
    # 这里传递用户信息
    current_admin_email = email
    avatar_content = current_admin_email.split('@')[0][:2] # 头像
    name = current_admin_email.split('@')[0] # 全名
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    if user_type:
        pass
    else:
        user_type = session.get("ut")
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            sub = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 07"
    

    # 找到当前所有请求 按照 审核中 失败 已完成 和 空 进行排序
    try:
        with connection.cursor() as cursor:
            # sql = "SELECT * FROM requests;"
            sql = """
            SELECT * FROM requests
            WHERE r_status IN ('In Review', 'Fail', 'Completed','')
            ORDER BY 
            CASE 
                WHEN r_status = 'In Review' THEN 1
                WHEN r_status = 'Fail' THEN 2
                WHEN r_status = 'Complete' THEN 3
                ELSE 4  
            END;
            """
            cursor.execute(sql)
            requests = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while to handle page."
    
    # 由handle页面传回
    page = int(request.args.get("page", 1))
    # 设定每页10条数据
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    requests_page = requests[start_index:end_index]
    num_pages = len(requests) // per_page + (1 if len(requests) % per_page > 0 else 0)
    # return render_template("handle.html", sub=sub,ut=ut,requests=requests_page, page=page, num_pages=num_pages,content=avatar_content,name=name,course_names=course_names,assignments_list=assignments_list,email=current_admin_email)
    return render_template("handleModel.html", sub=sub,ut=ut,requests=requests_page, page=page, num_pages=num_pages,content=avatar_content,name=name,course_names=course_names,assignments_list=assignments_list,email=current_admin_email)

@request_bp.route("/Approve", methods=["GET", "POST"])
def approve():# 这里采用handle的代码，原本的handle不应该属于admin
    """
    点击处理，只有admin可以使用
    :param request_id: 执行请求的id
    :param request_type: 执行请求的类型
    :param course_type: 执行请求的课程类型
    :return: {return "Error occurred while to request_bprove.", "Error occurred while to handle page2.", return redirect(url_for("to_handle"))}
    """
    email = request.form.get("email")
    print("1",email)
    # 这里传递用户信息
    current_admin_email = email
    avatar_content = current_admin_email.split('@')[0][:2] # 头像
    name = current_admin_email.split('@')[0] # 全名
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while submit infront of question."
    if user_type:
        pass
    else:
        user_type = session.get("ut")
    if user_type["user_type"] == "A":
        request_types =  ["","None"] 
    elif user_type["user_type"] == 'S':
        request_types = ["","UPDATE_SCORE","CHANGE"] 
    else:
        request_types = ["","ADD_COURSE", "UPDATE_SCORE","CHANGE"] 
    ut = user_type["user_type"]

    request_id = int(request.form.get("request_id"))
    request_type = request.form.get("request_type")
    course_type = request.form.get("course_type")
    request_course = request.form.get("request_course", "NULL") # 课程名
    request_explanation = request.form.get("request_explanation", "NULL")
    request_question = request.form.get("request_question", "NULL") # 修改分数的q\
    request_score = request.form.get("request_score")
    if request_score is not None and request_score != '':
            try:
                request_score = float(request_score)
            except ValueError:
                return 'Invalid value for score!'
    else:
        request_score = 0
    request_answer = request.form.get("request_answer", "NULL")
    request_q_id = request.form.get("request_q_id", "NULL")
    request_email = request.form.get("request_email")  # 请求的用户
    page = int(request.args.get("page", 1))
    request_llmstype = request.form.get("request_llms", "NULL")

    # 判断是否通过
    r_value = request.form.get('r',"1")
    print(r_value)
    if r_value == "0":
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE requests
                    SET r_status = 'Fail'
                    WHERE r_id = %s AND r_type = %s;
                """
                cursor.execute(sql,(request_id, request_type))
            connection.commit()
        except Exception as e:
            print("Error:", e)
            return "Error occurred while to request_bprove."
        
        real_email = request_email
        recipient_email_clean = real_email.strip().replace('\r', '').replace('\n', '')

        print(real_email)
        if real_email:
            msg = Message('Fail_request_Notification',sender='15153875323@163.com',recipients=[recipient_email_clean])
            msg.html = '''
                <p>Hello</p>
                <p>The request with Requset ID: {r_id} has been has been rejected uploaded to the database.</p>
                <p>This is an email sent by the system, please do not reply</p>
            '''.format(r_id=request_id)
            try:
                mail.send(msg)
            except Exception as e:
                return jsonify({"error": "Error sending email: " + str(e)}), 500
        # 更新状态到页面
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM requests;"
                cursor.execute(sql)
                requests = cursor.fetchall()
        except Exception as e:
            print("Error:", e)
            return "Error occurred while to handle page2."
        
        found_request = False
        for req in requests:
            if req["r_id"] == request_id and req["r_status"] == "Fail":
                print("hhhh2")
                found_request = True
                break
        if found_request:
            return redirect(url_for("request.to_handle", email=email,ut=ut))
        else:
        # 如果循环结束时没有找到满足条件的请求，则抛出异常或返回错误消息
            raise ValueError("No completed request found for the specified ID.")
    if request_type == "ADD_COURSE":
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `course`(`course_name`,`course_cat`) VALUES (%s, %s)"
                cursor.execute(sql, (request_course, course_type))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error occurred: {e}")
            return "Error occurred while excuet request."
        

        real_email = request_email
        recipient_email_clean = real_email.strip().replace('\r', '').replace('\n', '')

        print(real_email)
        if real_email:
            msg = Message('ADD_COURSE_Notification',sender='15153875323@163.com',recipients=[recipient_email_clean])
            msg.html = '''
                <p>Hello</p>
                <p>The request about adding course has been successfully uploaded to the database.</p>
                <p>This is an email sent by the system, please do not reply</p>
            '''
            try:
                mail.send(msg)
            except Exception as e:
                return jsonify({"error": "Error sending email: " + str(e)}), 500

    elif request_type == "UPDATE_SCORE":
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `score`(`q_text`, `email`, `score`) VALUES (%s, %s, %s);"
                cursor.execute(sql, (request_question, request_email, request_score))
            connection.commit()
        except Exception as e:
            print("Error:", e)
            return "Error occurred while excuet request."
        
        real_email = request_email
        recipient_email_clean = real_email.strip().replace('\r', '').replace('\n', '')

        print(real_email)
        if real_email:
            msg = Message('UPDATE_SCORE_Notification',sender='15153875323@163.com',recipients=[recipient_email_clean])
            msg.html = '''
                <p>Hello</p>
                <p>The request about updating score has been successfully uploaded to the database.</p>
                <p>This is an email sent by the system, please do not reply</p>
            '''
            try:
                mail.send(msg)
            except Exception as e:
                return jsonify({"error": "Error sending email: " + str(e)}), 500
    elif request_type == "EXPERIMENT":
        q_id = request_q_id # ybx
        r_id = request_id
        if not r_id or not q_id:
            return jsonify({"error": "Missing r_id or q_id parameter"}), 400
        global request_data
        request_data = fetch_request_by_id(r_id, q_id)
        print("1001",request_data)
        if not request_data:
            return jsonify({"error": "No data found for provided r_id and q_id1"}), 404

        print(request_data)
        # Insert data into experiment
        insert_into_experiment(
            request_data['q_text'], request_data['course_name'], request_data['course_cat'],
            request_data['answer'], request_data['llmtype'],  request_data['score']
        )
        #yin 5.11
        real_email = request_data['email']
        recipient_email_clean = real_email.strip().replace('\r', '').replace('\n', '')

        print(real_email)
        if real_email:
            msg = Message('Experiment_Update_Notification',sender='15153875323@163.com',recipients=[recipient_email_clean])
            msg.html = '''
                <p>Hello</p>
                <p>The request with Question ID: {q_id} has been successfully uploaded to the experiment database.</p>
                <p>This is an email sent by the system, please do not reply</p>
            '''.format(q_id=q_id)
            try:
                mail.send(msg)
            except Exception as e:
                return jsonify({"error": "Error sending email: " + str(e)}), 500
        #end yin 5.11
    elif request_type == "ADD_QUESTION":
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `question`( `q_text`, `course_name`) VALUES (%s, %s)"
                cursor.execute(sql, (request_question,request_course))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error occurred: {e}")
            return "Error occurred while excuet request."
    elif request_type == "CHANGE":
        # 你的代码
        try:
            with connection.cursor() as cursor:
            # 将查询到的数据插入到variation表中
                sql = """
                INSERT INTO variation (q_id, q_text, llmstype, answer, score)
                VALUES (%s, %s, %s, %s, %s)
                """
                new_request_answer = f"/static/{request_answer}"
                cursor.execute(sql, (request_q_id, request_question, request_llmstype, new_request_answer, request_score))

            # 提交事务
            connection.commit()

        except pymysql.MySQLError as error:
            print(f"Something went wrong: {error}")
        #######redirect(url_for)
        real_email = request_email
        recipient_email_clean = real_email.strip().replace('\r', '').replace('\n', '')

        print(real_email)
        if real_email:
            msg = Message('Experiment_Update_Notification',sender='15153875323@163.com',recipients=[recipient_email_clean])
            msg.html = '''
                <p>Hello</p>
                <p>The request about changing question has been successfully uploaded to the database.</p>
                <p>This is an email sent by the system, please do not reply</p>
            '''
            try:
                mail.send(msg)
            except Exception as e:
                return jsonify({"error": "Error sending email: " + str(e)}), 500
        
        
    else:
        return "System error1001"
    
    # 执行完毕改变请求状态
    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE requests
                SET r_status = 'Completed'
                WHERE r_id = %s AND r_type = %s;
            """
            cursor.execute(sql,(request_id, request_type))
        connection.commit()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while to request_bprove."

    # 更新状态到页面
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM requests;"
            cursor.execute(sql)
            requests = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
        return "Error occurred while to handle page2."
    
    found_request = False
    for req in requests:
        print(req["r_id"])
        print(request_id)
        print(req["r_status"])
        if req["r_id"] == request_id and req["r_status"] == "Completed":
            print("wwww")
            found_request = True
            break
    if found_request:
        return redirect(url_for("request.to_handle", email=email,ut=ut))
    else:
    # 如果循环结束时没有找到满足条件的请求，则抛出异常或返回错误消息
        raise ValueError("No completed request found for the specified ID.")
# 全局搜索
@request_bp.route("/search",methods=["POST"])
def search():
    search_term = request.form.get("a")
    print("Received search term:", search_term)
    print("3")
    email = session.get("email_address")
    print("e",email)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_type FROM users WHERE email=%s;"
            cursor.execute(sql,(email))
            user_type = cursor.fetchone()
    except Exception as e:
        print("Error3:", e)
        return "Error occurred while submit infront of question."
    if user_type:
        pass
    else:
        user_type = session.get("ut")
    ut = user_type["user_type"]
    print(ut)
    try:
        with connection.cursor() as cursor: 
            print("Received search term1:", search_term)
            sql = "SELECT course_name FROM course WHERE course_name = %s;"
            cursor.execute(sql,(search_term))
            course_names = cursor.fetchall()
            if course_names:
                course_name = [course_name1['course_name'] for course_name1 in course_names]
                print(course_name[0])
                if ut == "S":
                    url = f"http://localhost:5000/search_course?course_name={course_name[0]}"
                else:
                    url = "http://127.0.0.1:5000/course/"+course_name[0]
                print(url)
                return redirect(url)
                # return redirect("http://127.0.0.1:5000/make_request")
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)

    try:
        with connection.cursor() as cursor: 
            print("Received search term2:", search_term)
            sql = "SELECT q_id FROM question WHERE q_text = %s;"
            cursor.execute(sql,(search_term))
            q_codes = cursor.fetchall()
            if q_codes:
                q_code = [row['q_id'] for row in q_codes]
                print(q_code[0])
                return redirect(url_for("teacher.questionDetail", q_id=q_code[0]))
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)
    
    try:
        with connection.cursor() as cursor: 
            print("Received search term3:", search_term)
            sql = "SELECT topic, subtopic FROM topic WHERE subtopic = %s;"
            cursor.execute(sql,(search_term))
            result = cursor.fetchone()
            print(result)
            if result:
                topic = result['topic']
                subtopic = result['subtopic']
                print(topic)
                return redirect(url_for("student.topic_details",topic=topic,subtopic=subtopic))
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)
    return render_template("error.html")






def fetch_request_by_id(r_id,q_id):
    #connection = get_db_connection()
    print(r_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT q_text, course_name, course_cat, answer, llmtype, score, email
                FROM requests 
                WHERE r_id = %s AND q_id = %s
            """, (r_id, q_id))
            return cursor.fetchone()
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)




def insert_into_experiment(q_text, course_name, course_cat, answer, llmtype, score):
    #connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO experiment (q_text, course_name, course_cat, answer, llmtype, score) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (q_text, course_name, course_cat, answer, llmtype, score))
            connection.commit()
        
    except Exception as e:
        print("Error:", e)
        return print("Error:", e)
    