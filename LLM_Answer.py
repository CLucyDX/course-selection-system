
from flask import Flask, request, jsonify, render_template_string
import pymysql
from configuration import connection

app = Flask(__name__)

class LLM_Answer:
    def __init__(self, LLM_Name, LLM_AnswerImg, LLM_Score, Comments):
        self.LLM_Name = LLM_Name
        self.LLM_AnswerImg = LLM_AnswerImg
        self.LLM_Score = LLM_Score
        self.Comments = Comments

    def change_score(self, new_score):
        if self.verify_score_range(new_score):
            self.LLM_Score = new_score
            return "Successfully Changed"
        else:
            return "INVALID_New_Score"

    def verify_score_range(self, score):
        return 0 <= score <= 100  # 有效范围

# 数据库连接配置
def get_db_connection():
    # connection = pymysql.connect(host='localhost',
    #                              user='root', 
    #                              password='', 
    #                              database='LLM_Answer',
    #                              cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/change_score', methods=['POST'])
def api_change_score():
    try:
        llm_name = request.form['LLM_Name']
        new_score = float(request.form['New_Score'])
    except ValueError:
        return jsonify(result="Invalid input."), 400  # 返回400错误表示客户端请求中有误

    # 检查传入的分数是否在有效范围内
    if not 0 <= new_score <= 100:
        return jsonify(result="New score is out of range."), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM LLM_Answer WHERE LLM_Name = %s", (llm_name,))
            row = cursor.fetchone()

            if not row:
                return jsonify(result="No such entry."), 404  # 如果找不到条目，返回404错误

            # LLM_Answer实例
            answer = LLM_Answer(row['LLM_Name'], row['LLM_AnswerImg'], row['LLM_Score'], row['Comment'])
            answer.change_score(new_score)  # 尝试更改分数

            # 更新数据库
            cursor.execute("UPDATE LLM_Answer SET LLM_Score = %s WHERE LLM_Name = %s", (new_score, llm_name))
            connection.commit()
    finally:
        # connection.close()
        pass

    return jsonify(result="Successfully changed."), 200

#@app.route('/display_question', methods=['GET'])
#def api_display_question():
#    answer = LLM_Answer(None, None, None, None)  # 使用空值初始化
#    result = answer.display_question()
#    return jsonify(result=result)

@app.route('/change_score_form')
def change_score_form():
    return render_template_string("""
    <html>
    <body>
        <h2>Change Score</h2>
        <form action="/change_score" method="post">
            <label for="LLM_Name">Name:</label><br>
            <input type="text" id="LLM_Name" name="LLM_Name"><br>
            <label for="New_Score">New Score:</label><br>
            <input type="text" id="New_Score" name="New_Score"><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """)

#@app.route('/display_question_form')
#def display_question_form():
#    return render_template_string("""
#    <html>
#    <body>
#        <h2>Display All Questions</h2>
#        <form action="/display_question" method="get">
#            <input type="submit" value="Display Questions">
#        </form>
#    </body>
#    </html>
#    """)

@app.route('/')
def home():
    return render_template_string("""
    <html>
    <body>
        <h1>Welcome to the LLM_Answer API!</h1>
        <p><a href="/change_score_form">Change Score</a></p>
        
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)