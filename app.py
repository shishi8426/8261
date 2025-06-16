
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 假装这是数据库
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username not in users:
            users[username] = {
                'level': 1,
                'mined': 0,
                'last_mine_time': None
            }
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_data = users[username]
    return render_template('dashboard.html', username=username, mined=user_data['mined'], level=user_data['level'])

@app.route('/mine', methods=['POST'])
def mine():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_data = users[username]

    now = datetime.now()
    last_time = user_data['last_mine_time']
    
    cooldown = timedelta(hours=3) if user_data['level'] == 1 else timedelta(hours=6)

    if last_time is None or now - last_time >= cooldown:
        speed = 1 if user_data['level'] == 1 else 2
        user_data['mined'] += speed * 3  # 模拟每次点击“挖矿”获得数量
        user_data['last_mine_time'] = now
        message = '挖矿成功！'
    else:
        message = '冷却中，请稍后再来。'

    return render_template('dashboard.html', username=username, mined=user_data['mined'], level=user_data['level'], message=message)

# 适配 Render 的端口
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
