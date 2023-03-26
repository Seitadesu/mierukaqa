from flask import Flask, render_template ,request, redirect, session
import psycopg2
from word import create_cloud
from html import escape
import os

app = Flask(__name__, static_folder='static')


DATABASE_URL = os.environ['DATABASE_URL']

@app.route('/')
def index():
    return render_template('index.html') #index.htmlを表示

@app.route("/result",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def insert():
    if request.method == 'POST':
        # index.htmlのフォームから質問文を入手する
        page_question = escape(request.form['page_question'])
        
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        # page_questionを保存する
        cursor.execute(
            '''INSERT INTO question (q_text) VALUES (%s)''',
            (page_question,)
        )
        conn.commit()

        # 最大のidを取得
        cursor.execute("SELECT MAX(id) FROM question")
        q_id = cursor.fetchone()[0]

        # your.htmlにリダイレクト
        return redirect(f'/question/{q_id}')

@app.route('/question/<int:q_id>')
def your(q_id):
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    # idがq_idの行を取得
    cursor.execute("SELECT q_text FROM question WHERE id=%s", (q_id,))
    q_text = cursor.fetchone()[0]


    # your.htmlを表示
    return render_template('your.html', q_text=q_text, q_id=q_id)

@app.route("/result2",  methods=['GET', 'POST'])
def insert2():
    if request.method == 'POST':
        # 質問文とpage_id、page_question_nameを取得
        page_answer = escape(request.form['page_answer'])
        page_id = escape(request.form['page_id'])
        page_question_name = escape(request.form['page_question_name'])

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        # page_answer、page_id、page_question_nameを保存する
        cursor.execute(
            '''INSERT INTO answer (q_answer, question_id, question_name) VALUES (%s, %s, %s)''',
            (page_answer, page_id, page_question_name)
        )
        conn.commit()

        # データベースを閉じる
        conn.close()
        return redirect(f'/answer/{page_id}')

@app.route('/answer/<int:page_id>')
def insert3(page_id):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()    

    # question_idがpage_idの行を取得
    cursor.execute("SELECT q_answer FROM answer WHERE question_id=%s", (page_id,))
    q_answer = cursor.fetchall()
    word_q_answer = q_answer

    cursor.execute("SELECT question_name FROM answer WHERE question_id=%s", (page_id,))
    q_name = cursor.fetchone()
    # データベースを閉じる    
    conn.close()

    if len(q_answer) == 0:
        return render_template('no_answer.html', page_id=page_id)
    else:
        create_cloud(word_q_answer, page_id)
        return render_template('result_wordcloud.html', q_name=q_name, page_id=page_id)

@app.route('/emb/<int:q_id>')
def emb(q_id):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    # idがq_idの行を取得
    cursor.execute("SELECT q_text FROM question WHERE id=%s", (q_id,))
    q_text = cursor.fetchone()[0]

    # データベースを閉じる
    cursor.close()
    conn.close()

    # your.htmlを表示
    return render_template('youremb.html', q_text=q_text, q_id=q_id)
    
@app.route('/htmlemb/<int:q_id>')
def htmlemb(q_id):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    # idがq_idの行を取得
    cursor.execute("SELECT q_text FROM question WHERE id=%s", (q_id,))
    q_text = cursor.fetchone()[0]

    # データベースを閉じる
    conn.close()

    # your.htmlを表示
    return render_template('emb.html', q_text=q_text, q_id=q_id)

@app.route("/result4",  methods=['GET', 'POST'])
def insert4():
    if request.method == 'POST':
        # 質問文とpage_id、page_question_nameを取得
        page_answer = escape(request.form['page_answer'])
        page_id = escape(request.form['page_id'])
        page_question_name = escape(request.form['page_question_name'])

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
    
        cursor.execute(
            '''INSERT INTO answer (q_answer, question_id, question_name) VALUES (%s, %s, %s)''',
            (page_answer, page_id, page_question_name)
        )
        conn.commit()

        # データベースを閉じる
        cursor.close()
        conn.close()
        return redirect(f'/answeremb/{page_id}')


@app.route('/answeremb/<int:page_id>')
def insert5(page_id):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    # question_idがpage_idの行を取得
    cursor.execute("SELECT q_answer FROM answer WHERE question_id=%s", (page_id,))
    q_answer = cursor.fetchall()
    word_q_answer = q_answer

    cursor.execute("SELECT question_name FROM answer WHERE question_id=%s", (page_id,))
    q_name = cursor.fetchone()
    # データベースを閉じる    
    conn.close()

    if len(q_answer) == 0:
        return render_template('emb_no_answer.html', page_id=page_id)
    else:
        create_cloud(word_q_answer, page_id)
        return render_template('emb_result_wordcloud.html', q_name=q_name, page_id=page_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
