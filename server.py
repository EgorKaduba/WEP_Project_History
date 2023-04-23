from flask import Flask, redirect, render_template, request, flash
from requests import get, post
from flask_restful import Api
from random import shuffle
from pprint import pprint
from forms.post import LoginForm
import logging

from werkzeug.utils import secure_filename
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
import os

from tools import main_tools

from data import db_session

# Настройки web-приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = './static/images'
api = Api(app)
db_session.global_init("db/history.db")
logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)


# Главная страница
@app.route("/", methods=['GET', 'POST'])
def main():
    # Если пользователь нажал на кнопку "Поиск", вызываем функция поиска по всем ресурсам, иначе выводим все ресурсы
    if request.method == "POST":
        logging.info('Request: %r', request.json)
        search_text = request.form.get('text')
        res = main_tools.search_all(search_text)
        if not res:
            return render_template("not_found.html")
    else:
        res = main_tools.get_all_info_list()
    shuffle(res)
    return render_template('index.html', res=res)


# Страница одной из групп
@app.route("/main/<string:group>", methods=['GET', 'POST'])
def group_list(group):
    # Если пользователь нажал на кнопку "Поиск", вызываем функция поиска по всем ресурсам определенной группы,
    # иначе выводим все ресурсы этой группы
    if request.method == "POST":
        logging.info('Request: %r', request.json)
        search_text = request.form.get('text')
        res = main_tools.search_group(group, search_text)
        if not res:
            return render_template("not_found.html")
    else:
        res = main_tools.get_group_list(group)
    return render_template("index.html", res=res)


# Страница одного ресурса
@app.route('/main/<string:group>/<int:id>', methods=['GET', 'POST'])
def resourse_info(group, id):
    if request.method == "POST":
        logging.info('Request: %r', request.json)
        search_text = request.form.get('text')
        res = main_tools.search_group(group, search_text)
        if not res:
            return render_template("not_found.html")
    else:
        res = main_tools.get_for_id(group, id)
    return render_template("resourse_info.html", res=res)


@app.route('/main/post/new_zapis', methods=['GET', 'POST'])
def post_form():
    form = LoginForm()
    if form.validate_on_submit():
        logging.info('Request: %r', request.json)
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect('/main/post/new_zapis')
        title_image_file_name = None
        if form.title_image.data != '' and form.title_image.data:
            f = form.title_image.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            title_image_file_name = filename
        if form.content_image.data[0] != '' and form.content_image.data[0]:
            content_image_file_name = []
            for f in form.content_image.data:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                content_image_file_name.append(filename)
            content_image = " | ".join(content_image_file_name)
        if not form.year:
            post(f"http://127.0.0.1:8080/api/{form.group.data}",
                 json={"title": form.title.data, "content": form.content.data,
                       "title_image": title_image_file_name if title_image_file_name else None,
                       "content_image": content_image if form.content_image.data[0] else None})
        else:
            post(f"http://127.0.0.1:8080/api/{form.group.data}",
                 json={"title": form.title.data, "content": form.content.data, 'date': form.year.data,
                       "title_image": title_image_file_name if title_image_file_name else None,
                       "content_image": content_image if form.content_image.data[0] else None})
        return redirect('/main/post/new_zapis')
    return render_template('post.html', title='Авторизация', form=form)


def add_api():
    from api.personalities_resourse import PersonalitiesResourse, PersonalitiesListResourse, PersonalitiesRes
    from api.concepts_resourse import ConceptsResourse, ConceptsRes, ConceptsListResourse
    from api.events_dates import EventsResourse, DatesResourse, EventsRes, EventsDatesListResourse
    api.add_resource(EventsDatesListResourse, "/api/events_dates")
    api.add_resource(EventsRes, "/api/events/id/<int:id>")
    api.add_resource(DatesResourse, "/api/dates/date/<string:dates>")
    api.add_resource(EventsResourse, "/api/events/title/<string:title>")
    api.add_resource(PersonalitiesRes, "/api/personalities/id/<int:id>")
    api.add_resource(PersonalitiesResourse, "/api/personalities/title/<string:titles>")
    api.add_resource(PersonalitiesListResourse, "/api/personalities")
    api.add_resource(ConceptsRes, "/api/concepts/id/<int:id>")
    api.add_resource(ConceptsResourse, "/api/concepts/title/<string:titles>")
    api.add_resource(ConceptsListResourse, "/api/concepts")


if __name__ == '__main__':
    add_api()
    app.run(host='127.0.0.1', port=8080)
