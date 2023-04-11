import flask
from flask import Flask
from flask import Flask, render_template, session
from flask import redirect, request, make_response



app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Simple note')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')