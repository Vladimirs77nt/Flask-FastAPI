# Задание 1

# Разработать API для управления списком пользователей с использованием базы данных SQLite.
#   Для этого создайте модель User со следующими полями:
#       - id: int (идентификатор пользователя, генерируется автоматически)
#       - username: str (имя пользователя)
#       - email: str (электронная почта пользователя)
#       - password: str (пароль пользователя)

# API должно поддерживать следующие операции:
#       - Получение списка всех пользователей: GET /users/
#       - Получение информации о конкретном пользователе: GET /users/{user_id}/
#       - Создание нового пользователя: POST /users/
#       - Обновление информации о пользователе: PUT /users/{user_id}/
#       - Удаление пользователя: DELETE /users/{user_id}/

# Для валидации данных используйте параметры Field модели User.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.

import random
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

DATABASE_URL = "sqlite:///Seminar_6/users_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("username", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("password", sqlalchemy.String(32)), )
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

# Первая модель нужна для получения информации о пользователе от клиента
class UserIn(BaseModel):
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)

# Вторая модель используется для возврата данных о пользователе из БД клиенту (содержит ID)
class User(UserIn):
    id: int

# Добавление тестовых (фейковых) пользователей в БД
@app.get("/fake_users/{count}")
async def create_fake_users(count: int):
    for i in range(count):
        query = users.insert().values(username=f'user{i+1}',
                                      email=f'mail_{i+1}_{random.randint(101,1000)}@mail.ru',
                                      password=f'password_{i+1}_{random.randint(10001,1000000000)}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}

# Создание пользователя в БД, create
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(username=user.username, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

# Чтение ВСЕХ пользователей из БД, read
@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

# Чтение одного пользователя из БД, read
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

# Обновление одного пользователя в БД, update
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

# Удаление пользователя из БД, delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}
