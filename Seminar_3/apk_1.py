# Задание №1

# Создать базу данных для хранения информации о студентах университета.

# База данных должна содержать две таблицы: "Студенты" и "Факультеты".
# В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, возраст, пол, группа и id факультета.
# В таблице "Факультеты" должны быть следующие поля: id и название факультета.
# Необходимо создать связь между таблицами "Студенты" и "Факультеты".
# Написать функцию-обработчик, которая будет выводить список всех
# студентов с указанием их факультета.

import random
from flask import Flask, render_template
from Seminar_3.models import db, Students, Faculty

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)

@app.route("/")
@app.route('/page-main/')
def page_main():
    context = {'title': 'Главная страница'}
    return render_template('page-main.html', **context)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')

@app.cli.command("add-students")
def add_students():
    for i in range(10):
        name = f"Jhon-{i+1}"
        surname = f"Smith-{random.randint(1,9)+i*10}"
        age = random.randint(20,36)
        faculty = random.randint(1,3)
        print (name, age, faculty)
        student = Students(id = i+1, name = name, surname = surname, age = age, id_faculty = faculty, gender = "MALE")
        db.session.add(student)
        db.session.commit()

@app.cli.command("delete-students")
def delete_students():
    students = Students.query.all()
    for i in students:
        db.session.delete(i)
        db.session.commit()

@app.cli.command("add-faculty")
def add_faculty():
    faculty = Faculty(id = 1, name_faculty="Финансовый")
    db.session.add(faculty)
    db.session.commit()
    faculty = Faculty(id = 2, name_faculty="Юридический")
    db.session.add(faculty)
    db.session.commit()
    faculty = Faculty(id = 3, name_faculty="Экономический")
    db.session.add(faculty)
    db.session.commit()

@app.route('/students/')
def students():
    students = Students.query.all()
    context = {'students': students}
    return render_template('students.html', **context)

@app.route('/faculty/')
def faculty():
    faculty = Faculty.query.all()
    context = {'faculty': faculty}
    return render_template('faculty.html', **context)

# -----------------------
if __name__ == "__main__":
    app.run()