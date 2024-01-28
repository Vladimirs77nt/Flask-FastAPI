# СЕМИНАР №1
# -----------------------

from flask import Flask, request
from flask import render_template

app = Flask(__name__)

# -----------------------
# Задание №1
# Создать страницу, на которой будет кнопка "Нажми меня", при
# нажатии на которую будет переход на другую страницу с
# приветствием пользователя по имени.

@app.route("/")
@app.route('/page-1/')
def page_1():
    context = {'title': 'Страница 1'}
    return render_template('page-1.html', **context)

@app.route('/page-2/')
def page_2():
    context = {'title': 'Страница 2'}
    return render_template('page-2.html', **context)


# -----------------------
# Задание №2
# Создать страницу, на которой будет изображение и ссылка на другую страницу,
# на которой будет отображаться форма для загрузки изображений.

@app.get('/page-3/')
def load_image():
    context = {'title': 'Загрузка изображения'}
    return render_template('page-3.html', **context)

@app.post('/page-3/')
def upload():
    if request.method == "POST":
        f = request.files["file"]
        print (f)
    return 'Изображение загружено!'
    # context = {'title': 'Изображение загружено!'}
    # return render_template('page-3.html', **context)


# -----------------------
# Задание №3
# Создать страницу, на которой будет форма для ввода логина и пароля.
# При нажатии на кнопку "Отправить" будет произведена проверка соответствия логина
# и пароля и переход на страницу приветствия пользователя или страницу с ошибкой.

@app.route('/login/', methods=["POST", "GET"])
def auth():
    if request.method == "POST":
        user_name = request.form.get["login"]
        user_pass = request.form.get["password"]
        if user_name == "admin" & user_pass == "qwerty":
            return render_template('page-4-succ.html', **context)
        return render_template('page-4-error.html', **context)
    context = {'title': 'Авторизация'}
    return render_template('page-4.html', **context)

@app.post('/user/')
def auth_true():
    context = {'title': 'Успешная авторизация'}
    return render_template('page-4-succ.html', **context)

@app.post('/user_error/')
def auth_false():
    context = {'title': 'Нет авторизации!!!'}
    return render_template('page-4-error.html', **context)


# -----------------------
if __name__ == "__main__":
    app.run()