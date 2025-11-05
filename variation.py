from flask import Flask, render_template, request, jsonify
import pymysql.cursors
from flask import Blueprint
from configuration import connection


variation_bp = Blueprint('variation',__name__)

def get_db_connection():
    return connection

@variation_bp.route('/variation/<int:q_id>')
def variation(q_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT q_text, llmstype, answer, score FROM variation WHERE q_id = %s"
            cursor.execute(sql, (q_id,))
            rows = cursor.fetchall()

            if not rows:
                # return "No data found for q_id: {}".format(q_id)
                return render_template('display_variationModel.html', q_id=q_id, variations=0)


            data = [dict(row) for row in rows]  # 将结果转换成字典列表
            return render_template('display_variationModel.html', q_id=q_id, variations=data)
    finally:
        pass
