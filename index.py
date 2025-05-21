from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import os
import io
import json
import datetime
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

def check_key():
    # 校验密钥是否已通过验证且在有效期内
    key = session.get('key')
    start = session.get('start')
    end = session.get('end')
    if not key or not start or not end:
        return redirect(url_for('verify'))
    now = datetime.datetime.now().isoformat(timespec='seconds')
    if not (start <= now <= end):
        session.clear()
        return redirect(url_for('verify'))
    return None

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        auth_info = request.form.get('auth_info')
        if not auth_info:
            return render_template('verify.html', error="请输入授权信息")
        if 'keyfile' not in request.files:
            return render_template('verify.html', error="请上传密钥文件")
        file = request.files['keyfile']
        try:
            key_data = json.load(io.TextIOWrapper(file.stream, encoding='utf-8'))
            # 授权信息MD5校验
            auth_md5 = hashlib.md5(auth_info.encode()).hexdigest()
            if auth_md5 != key_data['key']:
                return render_template('verify.html', error="授权信息或密钥文件不匹配")
            raw = f"{key_data['key']}|{key_data['generated']}|{key_data['start']}|{key_data['end']}"
            checksum = hashlib.md5(raw.encode()).hexdigest()
            now = datetime.datetime.now().isoformat(timespec='seconds')
            if checksum != key_data['checksum']:
                return render_template('verify.html', error="密钥校验失败")
            if not (key_data['start'] <= now <= key_data['end']):
                return render_template('verify.html', error="密钥已过期或未到生效期")
            # 保存密钥和有效期到session
            session['key'] = key_data['key']
            session['start'] = key_data['start']
            session['end'] = key_data['end']
            session['next_check'] = (datetime.datetime.now() + datetime.timedelta(
                seconds=random.randint(600, 1800))).timestamp()
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('verify.html', error="密钥文件格式错误")
    return render_template('verify.html')

@app.before_request
def before_request():
    # 除验证页面外，其他页面都要校验密钥和有效期
    if request.endpoint not in ('verify', 'static'):
        result = check_key()
        if result:
            return result
        next_check = session.get('next_check')
        if next_check and datetime.datetime.now().timestamp() > next_check:
            session.clear()
            return redirect(url_for('verify'))

courts = [
    {"name": "Court 1", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 2", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 3", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 6", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 5", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 4", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 7", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 8", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 9", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 10", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 11", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 12", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 15", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 14", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 13", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 16", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 17", "type": "Forbidden", "time": "8-11 pm"},
    {"name": "Court 18", "type": "Forbidden", "time": "8-11 pm"}
]

@app.route('/')
def index():
    return render_template('index.html', courts=courts)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        for i, court in enumerate(courts):
            court['type'] = request.form.get(f'type{i}')
            court['time'] = request.form.get(f'time{i}')
        return redirect(url_for('index'))
    return render_template('edit.html', courts=courts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)