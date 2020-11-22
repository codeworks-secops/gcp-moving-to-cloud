from flask import Flask
from flask import render_template
import socket

app = Flask(__name__)

count = 0

@app.route('/hello/', methods=["GET"])
@app.route('/hello/<name>', methods=["GET"])
def hello(name=None):
    global count
    count += 1

    return render_template('hello.html', host=socket.gethostname(), name=name, count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0')