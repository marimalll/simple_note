
from flask import abort, url_for

from flask import Flask, render_template
from flask import redirect, request
from flask_login import LoginManager, login_user, \
    login_required, logout_user, current_user
import os
from data import db_session
from data.settings import Settings
from data.users import User
from data.notes import Notes
from forms.settings import SettingsForm
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.notes import NotesForm
import datetime

from weather import weather_forecast

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def main():
    db_session.global_init("db/notes.db")
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        settings = db_sess.query(Settings).filter(Settings.user == current_user).first()
        if settings:
            weather, icon_url = weather_forecast(settings.city)
        else:
            weather, icon_url = weather_forecast('не указан')
        print(weather, icon_url)
        notes = db_sess.query(Notes).filter(Notes.user == current_user)
        for i in notes:
            print(i)
        return render_template("index.html", notes=notes, weather=weather, icon_url=icon_url, settings=settings, title='Simple note')
    else:
        data = 'Простое заметки - это простой и удобный инструмент для создания собственных заметок. Вы можете легко создавать, редактировать и удалять заметки в любое время. Этот инструмент также позволяет создавать списки задач и отмечать их по мере выполнения.'
        return render_template('index.html', data=data.split('. '), title='Simple note')



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        settings = db_sess.query(Settings).filter(Settings.user == current_user).first()
        if settings:
            if settings.theme == '1':
                form.theme.data = True
            else:
                form.theme.data = False
            form.bg_color.data = settings.bg_color
            form.text_color.data = settings.text_color
            form.city.data = settings.city
            print('before submition:', form.bg_color.data, form.text_color.data, form.theme.data, form.city.data)
            db_sess.commit()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        settings = Settings()
        settings.bg_color = form.bg_color.data
        settings.text_color = form.text_color.data
        settings.theme = form.theme.data
        settings.city = form.city.data
        current_user.settings = [settings]
        db_sess.merge(current_user)
        db_sess.commit()
        print('after submition:', settings.bg_color, settings.text_color, settings.theme, settings.city)
        return redirect('/')

    return render_template('settings.html', title='Настройки', form=form, settings=settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/users_pictures', picture_name)
    picture_file.save(picture_path)
    return picture_name


@app.route('/notes',  methods=['GET', 'POST'])
@login_required
def add_notes():
    form = NotesForm()
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter(Settings.user == current_user).first()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        notes = Notes()
        notes.title = form.title.data
        notes.content = form.content.data
        if form.image.data:
            image = save_image(form.image.data)
            image_url = url_for('static', filename='users_pictures/' + image)
            notes.image = image_url
            print(notes.image)
        current_user.notes.append(notes)
        db_sess.merge(current_user)
        db_sess.commit()
        # image_url = url_for('static', filename='users_pictures/' + notes.image)
        return redirect('/')
    return render_template('notes.html', title='Добавление записи',
                           form=form, settings=settings)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/notes/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_notes(id):
    form = NotesForm()
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter(Settings.user == current_user).first()
    print(settings)
    if request.method == "GET":
        db_sess = db_session.create_session()
        notes = db_sess.query(Notes).filter(Notes.id == id, Notes.user == current_user).first()
        if notes:
            form.title.data = notes.title
            form.content.data = notes.content
            if notes.image:
                form.image.data = notes.image
        db_sess.commit()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        notes = db_sess.query(Notes).filter(Notes.id == id, Notes.user == current_user).first()
        notes.title = form.title.data
        notes.content = form.content.data
        if form.image.data:
            image = save_image(form.image.data)
            image_url = url_for('static', filename='users_pictures/' + image)
            notes.image = image_url
            print(notes.image)
        db_sess.commit()
        return redirect('/')
    return render_template('notes.html',
                           title='Редактирование записи',
                           form=form, settings=settings)


@app.route('/notes_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def notes_delete(id):
    db_sess = db_session.create_session()
    notes = db_sess.query(Notes).filter(Notes.id == id, Notes.user == current_user).first()
    if notes:
        db_sess.delete(notes)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')


@app.errorhandler(400)
def bad_request(error):
    return render_template('error400.html')


@app.errorhandler(401)
def unauthorized(error):
    return render_template('error401.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
