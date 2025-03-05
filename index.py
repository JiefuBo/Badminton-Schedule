from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 初始数据
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
    app.run(debug=True)

    #Jiefu Bo© 2025    版权所有    违者必究
