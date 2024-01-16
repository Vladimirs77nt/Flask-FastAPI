from flask import Flask
from flask import render_template

app = Flask(__name__)

# -----------------------
# ЗАДАНИЕ №1
# Напишите простое веб-приложение на Flask,
# которое будет выводить на экран текст "Hello, World!".
@app.route("/")
def hello_world():
    return "Hello, World!"

# -----------------------
# ЗАДАНИЕ №2
# Добавьте две дополнительные страницы в ваше веб-приложение:
#   - страницу "about"
#   - страницу "contact".

@app.route("/contact/")
def contact():
    return "--- КОНТАКТЫ ---"

@app.route("/about/")
def about():
    return "--- ОБО МНЕ ---"

# -----------------------
# ЗАДАНИЕ №3 - summ
# Написать функцию, которая будет принимать на вход два числа и выводить на экран их сумму.
@app.route("/summ/<int:a> <int:b>/")
def summ(a,b):
    return f"{a+b}"

# -----------------------
# ЗАДАНИЕ №4 - stroka
# Написать функцию, которая будет принимать на вход строку и выводить на экран ее длину.
@app.route("/stroka/<string:s>/")
def stroka(s):
    return f"{len(s)}"

# -----------------------
# ЗАДАНИЕ №5 - 
# Написать функцию, которая будет выводить на экран HTML страницу
#  с заголовком "Моя первая HTML страница" и абзацем "Привет, мир!".
@app.route("/html/")
def html_get():
    stroka = """
    <h1>Моя первая HTML страница</h1>
    <p>Привет, мир!</p>
    """
    return stroka

# -----------------------
# Задание №6
# Написать функцию, которая будет выводить на экран HTML страницу с таблицей,
# содержащей информацию о студентах.
# Таблица должна содержать следующие поля: "Имя", # "Фамилия", "Возраст", "Средний балл".
# Данные о студентах должны быть переданы в шаблон через контекст.
@app.route("/student/")
def student():
    data_student = [
        {"name": "Иван",
         "familia": "Федоров",
         "age": "20",
         "average": "4.5"},
         {"name": "Борис",
         "familia": "Мосеев",
         "age": "18",
         "average": "5"},
         {"name": "Дмитрий",
         "familia": "Гаврилов",
         "age": "25",
         "average": "3.5"},
    ]
    return render_template('student.html', data_student=data_student)

# -----------------------
# Задание №7
# Написать функцию, которая будет выводить на экран HTML страницу с блоками новостей.
# Каждый блок должен содержать заголовок новости, краткое описание и дату публикации.
# Данные о новостях должны быть переданы в шаблон через контекст.
@app.route("/news/<int:num>/")
def news(num):
    data_news = [
        {"title": "Новый год",
         "text_small": "Lorem ipsum dolor sit amet consectetur adipisicing elit. A laudantium repudiandae ut corporis quisquam pariatur adipisci. Beatae deserunt vero tenetur.",
         "date": "30.12.2023"},
         {"title": "Рождество",
         "text_small": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit ipsa molestias odio ducimus tenetur nam perferendis eos harum omnis inventore, fuga dolores aliquam quos officia ullam architecto maiores? Unde quo ex et modi dicta autem cum eveniet eum perspiciatis blanditiis",
         "date": "07.01.2024"},
         {"title": "Экономика",
         "text_small": "Lorem ipsum dolor sit amet consectetur adipisicing elit. A laudantium repudiandae ut corporis quisquam pariatur adipisci.",
         "date": "11.01.2024"},
         {"title": "ЖКХ",
         "text_small": "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Praesentium, velit! Unde animi deleniti inventore repudiandae! Suscipit corrupti, unde tempora assumenda aut dolore nam quo similique deserunt quasi sit, officia a.",
         "date": "12.01.2024"},
    ]
    return render_template('news.html', news=data_news[num-1])



# -----------------------
if __name__ == "__main__":
    app.run()