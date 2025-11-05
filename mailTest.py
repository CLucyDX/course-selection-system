from flask import Flask, render_template, request, flash, redirect, url_for  
from flask_mail import Mail, Message  
import os  
  
app = Flask(__name__)  
# 设置 secret_key，这里只是一个示例，你应该使用随机生成的密钥  
app.secret_key = os.urandom(24)

  
# 配置邮件服务器（这里使用SMTP服务器，你需要替换成你自己的SMTP服务器信息）  
app.config.update(  
    MAIL_SERVER='smtp.163.com',  
    MAIL_PORT=465,  
    MAIL_USE_SSL=True,  
    MAIL_USERNAME='pyx2632763373@163.com',  
    MAIL_PASSWORD='TKWZQOQASVTKGYUD'  # 授权的密码
)  
  
mail = Mail(app)  
  
@app.route('/', methods=['GET', 'POST'])  
def mailTest():  
    if request.method == 'POST':  
        email = request.form.get('email')  
        if not email:  
            flash('请输入电子邮件地址', 'error')  
        else:  
            msg = Message('测试邮件', sender='pyx2632763373@163.com', recipients=[email])  
            # msg.body = "function success"  
            # msg.body = "这是一段普通文本。点击以下链接: localhost:2020/teacherMain"
            msg.html = '''  
                <p>这是一段普通文本。</p>  
                <p>这是一个链接: <a href="localhost:5000/teacherMain">点击这里</a></p>  
                '''
            try:  
                mail.send(msg)  
                flash('邮件已发送', 'success')  
            except Exception as e:  
                flash('发送邮件时出错: ' + str(e), 'error')  
        return redirect(url_for('mailTest'))  
    return render_template('mailTest.html')  
  
if __name__ == '__main__':  
    # app.run(debug=True)
    app.run(port=2020,host="127.0.0.1",debug=True)