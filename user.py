from flask import Flask, request, jsonify,render_template,redirect, url_for,flash,session
from gevent import pywsgi
import uuid  # 用于生成唯一的令牌
from flask import Blueprint
from flask_mail import Mail, Message  
import re  
import os
from database import Course, LLM, Question,db,Users
from configuration import mail

login_bp = Blueprint('login',__name__)

class User:  
    def __init__(self, email_address, password, user_type):  
        self._email_address = email_address
        self._password = password
        self.user_type = user_type
        
    def validate_password_complexity(self):
        if len(self._password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", self._password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", self._password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", self._password):
            return False, "Password must contain at least one digit."
        return True, "Password is strong."
    
 
    def register(self):
        # Check if email_address is empty or contains illegal characters
        if self._email_address is None or any(char in "()[]{}" for char in self._email_address):
            return 1001, "WRONG_Register_email_address"
        
        # 检查用户是否存在
        user_list = Users.query.filter_by(email=self._email_address).all()
        if user_list:
            return 1001, "User already exists"
        
        # Validate email_address format
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(self._email_address):  
            return 1001, "WRONG_Register_email_address"
        
        # Check if password is empty or contains illegal characters
        if self._password is None or any(char in "()[]{}" for char in self._password):
            return 1002, "WRONG_Register_Password"
        
        # Validate password complexity
        valid, message = self.validate_password_complexity()
        if not valid:
            return 1002, message
        else:
            return 0, "OK"
  

    def login(self):
        # 检查用户是否存在
        user_list = Users.query.filter_by(email=self._email_address).with_entities(Users.email, Users.password, Users.user_type).all()
        if user_list:
            if user_list[0][1]==self._password and user_list[0][2]==self.user_type:
                return 0, "OK"
            else:
                return 1004,"WRONG_Login_Password_or_Identity"
        else:
            return 1003, "WRONG_Login_Email"

@login_bp.route("/loginAndRegister", methods=["POST","GET"])
def loginAndRegister():
    if request.method == 'POST':
        email_address = request.form.get('email')  
        role = request.form.get('role')
        password = request.form.get('password')  
        
        if email_address:
            if password:  # login
                user = User(email_address, password, role)  
                res, message = user.login()
                # 将 email_address 添加到 session 中  
                session['email_address'] = email_address

                if res==0:
                    # 根据角色重定向到主页  
                    if role == 'T':  
                        return redirect(url_for('teacher.teacherhome'))  
                    elif role == 'S':  
                        return redirect(url_for('student.studentHomePage'))
                    elif role=='A':
                        return redirect(url_for('admin.admin_pages', email=email_address))
                else:
                    return redirect(url_for('login.loginRegisterFail', res=res, message=message))
            else:  # register
                # 检查用户是否存在
                user_list = Users.query.filter_by(email=email_address).all()
                if user_list: # 存在
                    return render_template('loginRegisterFail.html', res=1001, msg='Email Address Exits')
                else: # 不存在
                    # 发送邮件
                    msg = Message('Register Mail', sender='15153875323@163.com', recipients=[email_address]) 
                    msg.html = '''  
                        <p>Go to the following page and enter your password: </p>  
                        <p><a href="http://localhost:5000/registerPassword">Click here to enter</a></p>  
                        '''
                    try:  
                        mail.send(msg)  
                        flash('email has been sent', 'success')  
                        print("mail success")
                        return render_template('loginRegisterFail.html', res=0, msg='The registration link has been sent, please check your email')
                    except Exception as e:  
                        flash('Error sending email: ' + str(e), 'error')
                        return render_template('loginRegisterFail.html', res=1, msg='Error sending email: ' + str(e))
        
    return render_template('loginAndRegister.html')

        
@login_bp.route("/registerPassword", methods=["POST","GET"])
def registerPassword():
    if request.method == 'POST':  
        email_address = request.form.get('email')  
        password = request.form.get('password')  
        role = request.form.get('role') 

        user = User(email_address, password, role)
        res, message = user.register()

        if res==0:
            
            # 插入 Users 数据  
            new_user = Users(email=email_address, password=password, user_type = role)  
            db.session.add(new_user)  
            db.session.commit()

            if role == 'T':  
                return redirect(url_for('teacher.teacherhome'))  
            elif role == 'S':  
                return redirect(url_for('student.studentHomePage')) 
            elif role == 'A':
                return redirect(url_for('admin'))
        else:
            return redirect(url_for('login.loginRegisterFail', res=res, message=message))
            
    return render_template('registerPasswordModel.html')

@login_bp.route('/loginRegisterFail', methods=['GET'])  
def loginRegisterFail():  
    res = request.args.get('res', type=int, default=None)  
    message = request.args.get('message', default='')  
      
    return render_template('loginRegisterFail.html', res=res, msg=message)