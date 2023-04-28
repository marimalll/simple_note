from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NotesForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    image = FileField('Выберите изображение', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Применить')