import flask
from flask import Flask
from flask import Flask, render_template, session
from flask import redirect, request, make_response
from flask import make_response



app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    data = 'Простое заметки - это простой и удобный инструмент для создания собственных заметок. Вы можете легко создавать, редактировать и удалять заметки в любое время. Этот инструмент также позволяет создавать списки задач и отмечать их по мере выполнения.'
    return render_template('index.html', data=data.split('. '))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register')
def register():
    return 'регистрация'


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
