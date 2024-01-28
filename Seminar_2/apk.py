# СЕМИНАР №1
# -----------------------

from flask import Flask
from flask import render_template

app = Flask(__name__)

# -----------------------
# Задание №1
# Создать страницу, на которой будет кнопка "Нажми меня", при
# нажатии на которую будет переход на другую страницу с
# приветствием пользователя по имени.

@app.route("/")
@app.route('/main/')
def main():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)