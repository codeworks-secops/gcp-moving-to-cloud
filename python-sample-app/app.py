from flask import Flask
app = Flask(__name__)

#for demo purposes only to see different requests handled by instances of the application
count = 0

@app.route('/')
def index():
    global count
    count += 1
    return 'Hello Hamza ' + str(count)
    #return 'Goodbye Hamza ' + str(count)

if __name__ == '__main__':
    app.run(host='0.0.0.0')