from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    bg_color = StringField('Укажите цвет фона', validators=[DataRequired()])
    text_color = StringField('Укажите цвет текста', validators=[DataRequired()])
    theme = BooleanField('Темная тема')
    city = StringField('Укажите свой город:', default='Не_указан')
    submit = SubmitField('Применить')