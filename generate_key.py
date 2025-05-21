from flask import Flask, render_template, request, url_for, send_file
import hashlib
import os
import json
import datetime
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/generate_key', methods=['GET', 'POST'])
def generate_key():
    if request.method == 'POST':
        key = request.form.get('key')
        start_datetime = request.form.get('start_datetime')
        end_datetime = request.form.get('end_datetime')
        gen_date = datetime.datetime.now().isoformat(timespec='seconds')
        if not (key and start_datetime and end_datetime):
            return render_template('generate_key.html', error="所有字段均为必填")
        key_md5 = hashlib.md5(key.encode()).hexdigest()
        raw = f"{key_md5}|{gen_date}|{start_datetime}|{end_datetime}"
        checksum = hashlib.md5(raw.encode()).hexdigest()
        key_data = {
            "key": key_md5,
            "generated": gen_date,
            "start": start_datetime,
            "end": end_datetime,
            "checksum": checksum
        }
        filename = f"key_{gen_date.replace(':', '').replace('-', '').replace('T', '_')}.txt"
        filepath = os.path.join("keys", filename)
        os.makedirs("keys", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(key_data, ensure_ascii=False, indent=2))
        return render_template('generate_key.html', download_link=url_for('download_key', filename=filename))
    return render_template('generate_key.html')

@app.route('/download_key/<filename>')
def download_key(filename):
    return send_file(os.path.join("keys", filename), as_attachment=True)

@app.route('/')
def index():
    return '<a href="/generate_key">生成密钥文件</a><br><a href="/analyze_key">解析密钥文件</a>'

@app.route('/analyze_key', methods=['GET', 'POST'])
def analyze_key():
    if request.method == 'POST':
        auth_info = request.form.get('auth_info')
        if not auth_info:
            return render_template('analyze_key.html', error="请输入授权信息")
        if 'keyfile' not in request.files:
            return render_template('analyze_key.html', error="请上传密钥文件")
        file = request.files['keyfile']
        try:
            key_data = json.load(io.TextIOWrapper(file.stream, encoding='utf-8'))
            auth_md5 = hashlib.md5(auth_info.encode()).hexdigest()
            if auth_md5 != key_data.get('key'):
                return render_template('analyze_key.html', error="授权信息与密钥文件不匹配")
            start = key_data.get('start')
            end = key_data.get('end')
            result = f"密钥有效期：{start} 至 {end}"
            return render_template('analyze_key.html', result=result)
        except Exception as e:
            return render_template('analyze_key.html', error="密钥文件格式错误")
    return render_template('analyze_key.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)