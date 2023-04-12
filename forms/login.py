from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

# Как видно из примера, мы импортируем класс
# FlaskForm из модуля flask_wtf — основной класс,
# от которого мы будем наследоваться при создании своей формы.
# Из модуля wtforms (flask_wtf — обертка для этого модуля)
# мы импортируем типы полей, которые нам пригодятся для создания
# нашей формы: текстовое поле, поле ввода пароля, булевое поле
# (из него получается чекбокс), и кнопку отправки данных.