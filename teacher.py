# from user import User 
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for,session
from gevent import pywsgi
from flask_sqlalchemy import SQLAlchemy
from configuration import connection
from flask import Blueprint
from database import Course, Question, LLM,db

teacher_bp = Blueprint('teacher',__name__)
# 连接数据库

# 渲染初始化界面 -- 教师
@teacher_bp.route('/teacherhome')
def teacherhome():  
    # 从 session 中获取 email_address  
    email_address = session.get('email_address')
    # 构造头像
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""
    session['avatar_content'] = avatar_content
    session['name'] = name
    # 全局搜索的代码
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_name_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)# 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT q_text FROM question;"
            cursor.execute(sql)
            questions= cursor.fetchall()
    except Exception as e:
        print("Error:", e)# 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question."
    session['course_name_list'] = course_name_list
    session['questions'] = questions
    # return render_template("teacherMain.html", email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions)
    return render_template("teacherMainModel.html", email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions)

    # 全局搜索的代码
    

# 渲染搜索的初始化界面 
@teacher_bp.route('/teacherSelection')
def teacherSelection():
    email_address = session.get('email_address')
    # 搜索所有course name
    courses = Course.query.with_entities(Course.course_name).all()  
    course_name_list = [{'course_name': c.course_name} for c in courses]  # 直接转换为列表  
    # 搜索所有q_text
    q_texts = Question.query.with_entities(Question.q_text).all()
    questions = [{'q_text': qt.q_text} for qt in q_texts]  # 直接转换为列表  
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""
    # return render_template('teacherSelection.html', email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions)  
    return render_template('teacherSelectionModel.html', email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions)  


# 用户选择“使用course name进行搜索后”，获取所有课程名称
@teacher_bp.route('/courseList', methods=['GET'])
def courseList():  
    if request.args.get('type') == 'course_name':  
        # 搜索所有course name
        courses = Course.query.with_entities(Course.course_name).all()  
        return jsonify([{'name': c.course_name} for c in courses])  
    else:
        return "No course name"

# 用户选择了“使用课程类别进行搜索”后，搜索所有课程类别并以无序列表的形式输出
@teacher_bp.route('/categoryList', methods=['GET'])
def categoryList():
    if request.args.get('type') == 'course_category':  
        # 搜索所有category
        categories = Course.query.with_entities(Course.course_cat).distinct().all()  
        return jsonify([{'category': c.course_cat} for c in categories])  
    else:
        return "no course category"

# 用户选择了“使用score range进行搜索”且”选择了某个score range“后，获取该range的问题列表
@teacher_bp.route('/scoreRangeQ', methods=['GET'])
def scoreRangeQ():
    if request.args.get('type') == '03':  
        results = LLM.query.filter(LLM.score.between(0, 3)).order_by(LLM.score).all() 
    elif request.args.get('type') == '35':
        results = LLM.query.filter(LLM.score.between(3, 5)).order_by(LLM.score).all()
    else:
        return jsonify({'error': 'selection error'})
    
    # 将结果转换为字典列表
    result_dicts = []
    for result in results:
        # Fetch the related AssignQ object based on assq_id
        assignq = Question.query.get(result.q_id)
        if assignq:
            result_dict = {
                'llm_id': result.llm_id,
                'score': result.score,
                'q_text': assignq.q_text
            }
            result_dicts.append(result_dict)

    # Return the results as JSON
    return jsonify({'results': result_dicts})
  
#  根据选中的课程名称获取课程相关问题列表
@teacher_bp.route('/course/<course_name>')
def course(course_name): 
    # 查找course name对应的c_id 
    course = Course.query.filter_by(course_name=course_name).first()  
    if not course:  
        return 'No course found with the given name', 404  
    # 查找对应的所有q_text  
    q_texts = Question.query.filter_by(course_name=course.course_name).with_entities(Question.q_text,Question.q_id).all()  
    q_text_list = [qt[0] for qt in q_texts]  # 将查询结果转换为列表 
    q_code_list = [qt[1] for qt in q_texts] 

    # 获取需要的参数
    email_address = session.get('email_address')
    # 搜索所有course name
    courses = Course.query.with_entities(Course.course_name).all()  
    course_name_list = [{'course_name': c.course_name} for c in courses]  # 直接转换为列表  
    # 搜索所有q_text
    q_texts = Question.query.with_entities(Question.q_text).all()
    questions = [{'q_text': qt.q_text} for qt in q_texts]  # 直接转换为列表  
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""
    # 传参给disText输出
    return render_template('teacherQuestionListModel.html', course_name_or_category=course_name, q_texts=q_text_list, q_ids = q_code_list, email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions) 

@teacher_bp.route('/teacher/courseQuestionScore', methods=['POST'])
def courseQuestionScore():
    data = request.get_json()
    course_name_or_category = data.get('course_name_or_category')
    score_range = data.get('score_range')

    # 确认course_name_or_category是course_name还是course_cat
    course = Course.query.filter((Course.course_name == course_name_or_category) | 
                                 (Course.course_cat == course_name_or_category)).first()

    if not course:
        return jsonify({"error": "Invalid course name or category"}), 400

    # 设置分数范围
    if score_range == '03':
        min_score, max_score = 0, 3
    elif score_range == '35':
        min_score, max_score = 3, 5
    else:
        return jsonify({"error": "Invalid score range"}), 400

    # 查询符合条件的问题，并按照q_id排序
    if course.course_name == course_name_or_category:
        questions = db.session.query(Question.q_id, Question.q_text).join(LLM, Question.q_id == LLM.q_id) \
                              .filter(Question.course_name == course_name_or_category) \
                              .filter(LLM.score >= min_score, LLM.score <= max_score) \
                              .order_by(Question.q_id.asc()).distinct().all()
    elif course.course_cat == course_name_or_category:
        questions = db.session.query(Question.q_id, Question.q_text).join(LLM, Question.q_id == LLM.q_id) \
                              .join(Course, Question.course_name == Course.course_name) \
                              .filter(Course.course_cat == course_name_or_category) \
                              .filter(LLM.score >= min_score, LLM.score <= max_score) \
                              .order_by(Question.q_id.asc()).distinct().all()
    else:
        return jsonify({"error": "Invalid course identifier"}), 400

    question_list = [{'q_id': q.q_id, 'q_text': q.q_text} for q in questions]

    # 获取需要的参数
    email_address = session.get('email_address')
    # 搜索所有course name
    courses = Course.query.with_entities(Course.course_name).all()  
    course_name_list = [{'course_name': c.course_name} for c in courses]  # 直接转换为列表  
    # 搜索所有q_text
    q_texts = Question.query.with_entities(Question.q_text).all()
    questions = [{'q_text': qt.q_text} for qt in q_texts]  # 直接转换为列表  
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""

    return render_template('teacherQuestionListModel.html', questions=question_list, 
                        course_name_or_category=course_name_or_category,
                        email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions)

# 用户选中具体的某个课程类别后，获取此类别下的所有问题并输出问题的无序列表
@teacher_bp.route('/category/<course_category>')
def category(course_category):
    if not course:
        return 'No course found with the given name', 404 
    # 查找对应的q_text
    q_texts = Question.query.join(Course).filter(Course.course_cat == course_category).with_entities(Question.q_text, Question.q_id).all()  # 注意：我添加了q_id，因为通常你可能需要这个主键    
    q_text_list = [qt[0] for qt in q_texts] 
    q_code_list = [qt[1] for qt in q_texts]

    # 获取需要的参数
    email_address = session.get('email_address')
    # 搜索所有course name
    courses = Course.query.with_entities(Course.course_name).all()  
    course_name_list = [{'course_name': c.course_name} for c in courses]  # 直接转换为列表  
    # 搜索所有q_text
    q_texts = Question.query.with_entities(Question.q_text).all()
    questions = [{'q_text': qt.q_text} for qt in q_texts]  # 直接转换为列表  
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""

    return render_template('teacherQuestionListModel.html', course_name_or_category=course_category, q_texts=q_text_list, q_ids = q_code_list, email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions) 

# （score range情况中）用户选中某个question后，跳转到对应的question详情界面 -- scoreQuestionDetail
@teacher_bp.route('/score/<llm_id>')
def score(llm_id):
    # results = LLM.query.filter(LLM.llm_id == llm_id).all()  
    results = LLM.query.join(Question, LLM.q_id == Question.q_id).join(Course, Question.course_name == Course.course_name).filter(LLM.llm_id == llm_id).with_entities(LLM.llm_id, LLM.score, Question.q_text, Question.q_id, Course.course_cat, LLM.answer).all() 
    # 将结果转换为字典列表
    result_dicts = []
    for result in results:
        # Fetch the related AssignQ object based on assq_id
        assignq = Question.query.get(result[0])
        if assignq:
            result_dict = {
                'llm_id': result.llm_id,
                'LLM_score': result.score,
                'q_text': assignq.q_text,
                'q_id': assignq.q_id,
                'q_categ': result.course_cat,
                'LLM_answerImg': result.answer
                # 'comments':result.comments
            }
            result_dicts.append(result_dict)
    if not results:
        return 'No course found with the given name', 404
    
    # 获取需要的参数
    email_address = session.get('email_address')
    # 搜索所有course name
    courses = Course.query.with_entities(Course.course_name).all()  
    course_name_list = [{'course_name': c.course_name} for c in courses]  # 直接转换为列表  
    # 搜索所有q_text
    q_texts = Question.query.with_entities(Question.q_text).all()
    questions = [{'q_text': qt.q_text} for qt in q_texts]  # 直接转换为列表  
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""

    # return render_template('teacherScoreQDetail.html', results=result_dicts, email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions) 
    return render_template('teacherScoreQDetailModel.html', results=result_dicts, email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions) 

# （course name或 category情况中）用户选中具体的问题后，根据问题的id获取所有问题信息并在questionDetail页面输出  
@teacher_bp.route('/questionDetail/<int:q_id>')
def questionDetail(q_id):
    # 从 Question 表中查询 q_id 列的值等于 q_id 的所有记录，并获取 q_text  
    question = Question.query.filter_by(q_id=q_id).first()  
    if question:  
        q_text = question.q_text  
        
        # 通过 Question 表中的 course_name，从 Course 表中获取对应的 course_cat 和 course_name  
        course = Course.query.filter_by(course_name=question.course_name).first()  
        if course:  
            course_name = course.course_name  
            course_cat = course.course_cat  
        else:  
            # 如果找不到对应的 Course，可以设置默认值或抛出异常  
            course_name = None  
            course_cat = None

    llms = LLM.query.filter_by(q_id=q_id).all() 
  
    # 获取数据
    email_address = session.get('email_address')
    # 搜索所有course name
    courses = Course.query.with_entities(Course.course_name).all()  
    course_name_list = [{'course_name': c.course_name} for c in courses]  # 直接转换为列表  
    # 搜索所有q_text
    q_texts = Question.query.with_entities(Question.q_text).all()
    questions = [{'q_text': qt.q_text} for qt in q_texts]  # 直接转换为列表  
    if email_address:
        current_admin_email = email_address
        avatar_content = current_admin_email.split('@')[0][:2]
        name = current_admin_email.split('@')[0]
    else:
         # 处理 email 为空的情况，例如设置默认值或者返回错误信息
        current_admin_email = ""
        avatar_content = ""
        name = ""
    # 将数据传递给网页  
    return render_template('teacherQuestionDetailModel.html', q_id = q_id,
                           q_text = q_text, course_cat = course_cat, course_name = course_name,llms = llms, 
                           email=email_address, content = avatar_content, name=name, course_names=course_name_list,assignments_list=questions) 

if __name__=="__main__":
    teacher_bp.run(port=5000,host="127.0.0.1",debug=True)
    # server = pywsgi.WSGIServer(('0.0.0.0',5000),teacher)
    # server.serve_forever()