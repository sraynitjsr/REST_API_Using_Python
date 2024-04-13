from flask import Flask

app_hello = Flask(__name__)

@app_hello.route('/')
def welcome():
    return "Welcome to Hello World Service!"

if __name__ == '__main__':
    app_hello.run(debug=True, port=9000)
