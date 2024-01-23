# СЕМИНАР №1 - ДОМАШНЕЕ ЗАДАНИЕ

#       Задание
#       Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал)
#       и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
#       Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.
# -----------------------

from flask import Flask
from flask import render_template

app = Flask(__name__)


# главная
@app.route('/main/')
def main():
    context = {'title': 'Интернет-магазин'}
    return render_template('main.html', **context)

# одежда
@app.route('/clothes/')
def clothes():
    context = {'title': 'Одежда'}
    return render_template('clothes.html', **context)

# обувь
@app.route('/shoes/')
def shoes():
    context = {'title': 'Обувь'}
    return render_template('shoes.html', **context)

# игрушки
@app.route('/toys/')
def toys():
    context = {'title': 'Игрушки'}
    return render_template('toys.html', **context)


# -----------------------
if __name__ == "__main__":
    app.run()