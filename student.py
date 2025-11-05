from flask import Flask, request, jsonify,render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from database import Course,Topic,LLM, Question
from configuration import connection
import pymysql
student_bp = Blueprint('student', __name__)


@student_bp.route('/studenthome')
def studentHomePage():
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
            print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 01"
    return render_template('studentHomePageModel.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)


@student_bp.route('/search')
def search():
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 02"
    # return render_template('search.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    return render_template('searchModel.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)

@student_bp.route('/course')
def course():
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 03"

    # return render_template('search_course.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    return render_template('search_courseModel.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)

@student_bp.route('/category')
def category():
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 04"
    # return render_template('search_category.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    return render_template('search_categoryModel.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)




@student_bp.route("/search_course", methods=["GET"])
def search_course():
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 05"
    course_name = request.args.get('course_name')
    if not course_name:
        return render_template('errormessage.html')
    topics_set = set()
    courses = Topic.query.filter(Topic.course_name == course_name).all()
    if courses:
        for course in courses:
            topics_set.add(course.topic)

        # return render_template('topic.html', topics=list(topics_set),ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
        return render_template('topicModel.html', topics=list(topics_set),ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    else:
        return render_template('errormessage.html',ut=ut,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)


@student_bp.route("/search_category", methods=["GET"])
def search_category():
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 06"

    course_category = request.args.get('course_cat')
    if not course_category:
        return jsonify(message="No course category provided"), 400

    # Fetch all courses that match the given category
    courses = Course.query.filter(Course.course_cat == course_category).all()
    if not courses:
        return render_template('errormessage.html')

    # Initialize a set to hold unique topics
    topics_set = set()

    # Loop over each course and fetch topics
    for course in courses:
        course_topics = Topic.query.filter(Topic.course_name == course.course_name).all()
        for topic in course_topics:
            topics_set.add(topic.topic)

    # Check if any topics were found
    if topics_set:
        # return render_template('topic.html',ut=ut, topics=list(topics_set),email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
        return render_template('topicModel.html',ut=ut, topics=list(topics_set),email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    else:
        return jsonify(message="No topics found for this category"), 404


@student_bp.route("/show_subtopics/<topic>", methods=["GET"])
def show_subtopics(topic):
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 07"

    subtopics = Topic.query.filter_by(topic=topic).all()
    if subtopics:
        # return render_template('subtopics.html', ut=ut,subtopics=subtopics, topic=topic,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
        return render_template('subtopicsModel.html', ut=ut,subtopics=subtopics, topic=topic,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)
    else:
        return jsonify(message="No subtopics found for this topic"), 404


@student_bp.route("/topic_details/<topic>/<subtopic>", methods=["GET"])
def topic_details(topic, subtopic):
    ut = session.get('ut')
    # 查询topic和subtopic对应的Topic对象
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
    try:
        with connection.cursor() as cursor:
            sql = "SELECT course_name FROM course;"
            cursor.execute(sql)
            course_names = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称
    try:
        with connection.cursor() as cursor:
            sql = "SELECT subtopic FROM topic"
            cursor.execute(sql)
            assignments_list = cursor.fetchall()
    except Exception as e:
        print("Error:", e)  # 课程名称 # 只要名称 # assi # 要id
        return "Error occurred while submit infront of question. 08"

    topic_obj = Topic.query.filter_by(topic=topic, subtopic=subtopic).first()
    if not topic_obj:
        return render_template('errortopic.html')

    questions = Question.query.filter_by(topic_id = topic_obj.topic_id)
    if not questions:
        return render_template('errorquestion.html')

    # Fetch all LLM information using q_ids from the questions
    llm_infos = []
    for question in questions:
        llm_info = LLM.query.filter_by(q_id=question.q_id).first()
        if llm_info:
            llm_infos.append({
                'answer': llm_info.answer,
                'score': llm_info.score
            })

    if not llm_infos:
        return render_template('errorllm.html')

    # return render_template('topic_details.html',ut=ut, llm_info=llm_info,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)  # # 查询topic对应的LLM对象
    return render_template('topic_detailsModel.html',ut=ut, llm_info=llm_info,email=email,content = avatar_content, name=name, course_names=course_names,assignments_list=assignments_list)  # # 查询topic对应的LLM对象