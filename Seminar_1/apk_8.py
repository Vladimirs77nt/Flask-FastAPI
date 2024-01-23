# СЕМИНАР №1
# -----------------------

from flask import Flask
from flask import render_template

app = Flask(__name__)


# Задание №8
# Создать базовый шаблон для всего сайта, содержащий общие элементы
# дизайна (шапка, меню, подвал), и дочерние шаблоны для каждой отдельной страницы.
# Например, создать страницу "О нас" и "Контакты", используя базовый шаблон.

@app.route('/main/')
def main():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)

@app.route('/about/')
def about():
    context = {'title': 'О нас'}
    return render_template('about.html', **context)

@app.route('/contact/')
def contact():
    context = {'title': 'Контакты'}
    return render_template('contact.html', **context)

# -----------------------
if __name__ == "__main__":
    app.run()
