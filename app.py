from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            mining_status TEXT DEFAULT '未开始'
        )''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect('/login')
        except:
            return "用户名已存在"
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "用户名或密码错误"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>挖矿页面</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 100px; }
            #mineBtn { padding: 10px 20px; font-size: 20px; }
            #counter { font-size: 40px; color: green; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>挖矿模拟器</h1>
        <button id="mineBtn">开始挖矿</button>
        <div id="counter">0</div>

        <script>
            let mining = false;
            let counter = 0;
            let interval;

            document.getElementById("mineBtn").onclick = function () {
                if (!mining) {
                    mining = true;
                    this.innerText = "挖矿中...";
                    interval = setInterval(() => {
                        counter += Math.floor(Math.random() * 5 + 1); // 每次增加 1~5
                        document.getElementById("counter").innerText = counter;
                    }, 1000); // 每秒增加
                }
            };
        </script>
    </body>
    </html>
    """)

@app.route('/mine')
def mine():
    if 'user' not in session:
        return redirect('/login')
    username = session['user']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET mining_status='正在挖矿' WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=10000)


    
