import flask
from flask import Flask
from flask import Flask, render_template, session
from flask import redirect, request, make_response
from flask import make_response
from data import db_session
from data.users import User
from forms.login import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ourprojectsecretkey'


@app.route('/')
@app.route('/index')
def index():
    data = 'Простое заметки - это простой и удобный инструмент для создания собственных заметок. Вы можете легко создавать, редактировать и удалять заметки в любое время. Этот инструмент также позволяет создавать списки задач и отмечать их по мере выполнения.'
    # print(color_value, dark_theme_value)
    return render_template('index.html', data=data.split('. '))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data,
                    email = form.email.data,
                    about = form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/settings', methods=['GET', 'POST'])
def settings():

    global color_value, dark_theme_value
    if request.method == 'GET':
        if dark_theme_value == 'on':
            return render_template('settings.html', color_value=color_value, dark_theme_value='on')
        else:
            return render_template('settings.html', color_value=color_value, dark_theme_value='off')
    elif request.method == 'POST':
        color_value = request.form['color']
        if len(request.form) == 2:
            dark_theme_value = 'on'
        else:
            dark_theme_value = 'off'
    print(request.form['color'])
    print(dark_theme_value)
    return redirect('/index')




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    dark_theme_value = 'off'
    color_value = '#0000ff'
    db_session.global_init("db/simple_note.db")
    app.run(port=8080, host='127.0.0.1')
