from flask import Flask
from flask import render_template
app = Flask(__name__)

count = 0

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    global count
    count += 1

    return render_template('hello.html', name=name, count=count)
