import flask
from flask import Flask, url_for
from flask import Flask, render_template, session
from flask import redirect, request, make_response
from flask import make_response
from data import db_session
from data.users import User
from forms.login import LoginForm
from forms.user import RegisterForm
from weather import weather_forecast

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

    global color_value, dark_theme_value, city_value
    data = []
    if request.method == 'GET':
        if dark_theme_value == 'on':
            return render_template('settings.html', color_value=color_value, dark_theme_value='on', city_value=city_value)
        else:
            return render_template('settings.html', color_value=color_value, dark_theme_value='off', city_value=city_value)
    elif request.method == 'POST':
        color_value = request.form['color']
        city_value = request.form['city']
        if len(request.form) == 2:
            dark_theme_value = 'on'
        else:
            dark_theme_value = 'off'
        if city_value != 'Не_указан':
            data = weather_forecast(city_value)
        else:
            data = ['Не указан']
    return redirect(url_for('main_page', data=data))


@app.route('/main_page/<data>')
def main_page(data):
    data = data[1:-1].split(', ')
    reformat = []
    for i in data:
        reformat.append(i[1:-1])
    return render_template('main_page.html', data=reformat)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # мы зашли в наш личный дневник
        # можно сделать отдельную страницу с выбором: настройки, мои записи, создать новую
        # а можно после успешного входа перекинуть пользователя на главную страницу,
        # но теперь сверху будет доступна новая кнопка - мои записи. или две кнопки. еще "создать новую запись"
        return redirect('/index')
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    dark_theme_value = 'off'
    color_value = '#0000ff'
    city_value = "Не_указан"
    db_session.global_init("db/simple_note.db")
    app.run(port=8080, host='127.0.0.1', debug=True)
