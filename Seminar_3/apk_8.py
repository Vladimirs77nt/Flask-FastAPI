# Задание №8

# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

# -----------------------
import random
from flask import Flask, render_template, request
from forms_8 import LoginForm, RegistrationForm
from models import db, Students, Faculty, Users

from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '87c6005abb8e273831faa1b0b51c85f30f629193b0f2e35d7c2465e993d068b9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)
csrf = CSRFProtect(app)

# -----------------------
# инициализация базы
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Data Bases - инициализирована')

# добавление 10-ти новых студентов
@app.cli.command("add-db-students")
def add_students():
    for i in range(10):
        name_str = f"Jhon-{random.randint(1,9000)}"
        surname_str  = f"Smith-{random.randint(1,9000)+i*10}"
        age = random.randint(20,36)
        faculty = random.randint(1,3)
        student = Students(
            name = name_str,
            surname = surname_str,
            age = age,
            id_faculty = faculty,
            gender = "MALE",
            group = random.randint(1,15)
            )
        print(student)
        db.session.add(student)
        db.session.commit()
    print("10 студентов - добавлены!")

# удаление ВСЕХ студентов
@app.cli.command("delete-students")
def delete_students():
    students = Students.query.all()
    for i in students:
        db.session.delete(i)
        db.session.commit()

# добавление 3-х факультетов
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
    print ("Три факультета добавлены")

# добавление 10-ти новых пользователей
@app.cli.command("add-db-users")
def add_users():
    print ("add-users...")
    for i in range(10):
        name_str = f"Smith-{i}"
        surname_str = f"Foster-{random.randint(1,9)+i*10}"
        age = random.randint(20,36)
        user = Users(
            name = name_str,
            surname = surname_str,
            email=f"email_{random.randint(1,9000)}@mail.ru",
            password=f"password_{random.randint(1000000,90000000)}",
            age = age)
        print (user)
        db.session.add(user)
        db.session.commit()
    print("10 пользователей - добавлены!")


# -----------------------
# главная страница
@app.route("/")
@app.route('/page-main/')
def page_main():
    context = {'title': 'Главная страница'}
    return render_template('page-main.html', **context)
    
# студенты - для задания №1
@app.route('/students/')
def students():
    students = Students.query.all()
    context = {'students': students}
    return render_template('students.html', **context)

# факультеты - для задания №1
@app.route('/faculty/')
def faculty():
    faculty = Faculty.query.all()
    context = {'faculty': faculty}
    return render_template('faculty.html', **context)

# пользователи - для задания №8
@app.route('/users/')
def users():
    users = Users.query.all()
    context = {'users': users}
    return render_template('users.html', **context)

# форма регистрации - для задания №8
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        user = Users(
            name = form.name.data,
            surname = form.surname.data,
            email = form.email.data,
            password = form.password.data,
            age = form.age.data)
        print (user)
        db.session.add(user)
        db.session.commit()
        print("регистрация успешна!")
        return "--- РЕГИСТРАЦИЯ ОК ---<br><br><a href='/'>Вернутся на главную</a><br>"
    return render_template('register.html', form=form)

# форма авторизации - для задания №8
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = find_user(form.email.data)
        if user:
            if user.password == form.password.data:
                print("авторизация успешна!")
                return "--- АВТОРИЗАЦИЯ УСПЕШНА !!! ---<br><br><a href='/'>Вернутся на главную</a><br>"
            else:
                print("авторизация НЕ ПРОЙДЕНА")
                return "--- АВТОРИЗАЦИЯ НЕ ПРОЙДЕНА !!! ---<br><br><a href='/'>Вернутся на главную</a><br>"
    return render_template('login.html', form=form)

def find_user(email):
    users = Users.query.all()
    for user in users:
        if user.email == email:
            return user
    return False

    

# -----------------------
if __name__ == "__main__":
    app.run()