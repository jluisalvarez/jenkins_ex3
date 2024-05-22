# file app.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def holamundo():
    return "Hola Mundo"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080)

