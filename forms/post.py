from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, MultipleFileField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    group = SelectField('Группа', choices=['concepts', 'personalities', 'events_dates'],
                           validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired()])
    content = StringField('Контент', validators=[DataRequired()])
    year = StringField('Год')
    title_image = FileField(u'Главное изображение', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    content_image = MultipleFileField(u'Изображения в контенте')
    submit = SubmitField('Отправить')
