from flask import Flask, render_template  # render_template 추가
import pymysql
import os

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        # 데이터를 'index.html' 템플릿으로 전달
        return render_template('index.html', rows=rows)

    except Exception as e:
        return f"<h3>연결 에러 발생:</h3><p>{str(e)}</p>"
    
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)