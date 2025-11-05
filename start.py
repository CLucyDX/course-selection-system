# 初始页面

from flask import Blueprint,render_template

start_bp = Blueprint('start', __name__)

@start_bp.route('/')
def login():
    # return render_template('login.html')
    return render_template('loginAndRegister.html')




