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

@app.get('/page-4/')
def auth():
    context = {'title': 'Авторизация'}
    return render_template('page-4.html', **context)

@app.post('/page-4/')
def auth_true():
    if request.method == "POST":
        f = request.files["file"]
        print (f)
    return 'Изображение загружено!'
    # context = {'title': 'Изображение загружено!'}
    # return render_template('page-3.html', **context)

# -----------------------
if __name__ == "__main__":
    app.run()
