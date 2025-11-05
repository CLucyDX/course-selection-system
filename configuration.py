from flask import Flask
from start import start_bp
import os
import pymysql
from flask_mail import Mail

app = Flask(__name__)
app.register_blueprint(start_bp)
"""
Preparation: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@localhost/<database name>'
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/sdw'  # 数据修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')

app.secret_key = os.urandom(24)

# 配置邮件服务器（这里使用SMTP服务器）  
app.config.update(  
    MAIL_SERVER='smtp.163.com',  
    MAIL_PORT=465,  
    MAIL_USE_SSL=True,  
    MAIL_USERNAME='15153875323@163.com',  
    MAIL_PASSWORD='FOKFHWYPZCNODGVH'  # 授权的密码
) 
mail = Mail(app)

"""
Preparation:
    change the variables if needed, data needs to be the same as the previous database connection
"""
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='sdw',
                             charset='utf8mb4',
                             #passwd='yennie',
                             cursorclass=pymysql.cursors.DictCursor)