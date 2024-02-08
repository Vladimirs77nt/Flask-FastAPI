# Задание 6 (Промежуточная аттестация)

# Необходимо создать базу данных для интернет-магазина.

#   ○ База данных должна состоять из трех таблиц: товары, заказы и пользователи.
#   ○ Таблица товары должна содержать информацию о доступных товарах, их описаниях и ценах.
#   ○ Таблица пользователи должна содержать информацию о зарегистрированных пользователях магазина.
#   ○ Таблица заказы должна содержать информацию о заказах, сделанных пользователями.
#   ○ Таблица пользователей должна содержать следующие поля:
#       id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
#   ○ Таблица товаров должна содержать следующие поля:
#       id (PRIMARY KEY), название, описание и цена.
#   ○ Таблица заказов должна содержать следующие поля:
#       id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.

# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц
#  (итого шесть моделей).

# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
#   ○ Чтение всех
#   ○ Чтение одного
#   ○ Запись
#   ○ Изменение
#   ○ Удаление
#--------------------------------------------------------------------------------------------------------

import datetime
import random
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import faker    # генерация фейковых имен и фамилий
from transliterate import translit  # транлирования русских букв в латиницу

#--------------------------------------------------------------------------------------------------------
DATABASE_URL = "sqlite:///Seminar_6/online_store_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
fake = faker.Faker('ru_RU')

# Таблица пользователей (users) содержит следующие поля:
#   id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), # ID номер товара
                         sqlalchemy.Column("name", sqlalchemy.String(32)),              # имя пользователя
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),           # фамилия
                         sqlalchemy.Column("email", sqlalchemy.String(64)),             # электронная почта
                         sqlalchemy.Column("password", sqlalchemy.String(32)), )        # пароль пользователя

# Таблица товаров (products) содержит следующие поля:
#   id (PRIMARY KEY), название, описание и цена.
products = sqlalchemy.Table("products", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), # ID номер товара
                         sqlalchemy.Column("product_name", sqlalchemy.String(32)),      # название товара
                         sqlalchemy.Column("description", sqlalchemy.String(32)),       # описание товара
                         sqlalchemy.Column("price", sqlalchemy.Integer), )              # цена

# Таблица заказов (orders) содержит следующие поля:
#   id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
orders = sqlalchemy.Table("orders", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),                 # ID номер заказа
                         sqlalchemy.Column("id_user", sqlalchemy.ForeignKey("users.id")),              # ID пользователя
                         sqlalchemy.Column("id_product", sqlalchemy.ForeignKey("products.id")),         # ID товара
                         sqlalchemy.Column("order_time", sqlalchemy.DateTime(), default=datetime.datetime.now),  # время создания заказа
                         sqlalchemy.Column("status", sqlalchemy.String(16)), )                          # статус заказа

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
app = FastAPI()

#--------------------------------------------------------------------------------------------------------
# Класс UserIn - первая модель нужна для получения информации о пользователе от клиента
class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=64)
    password: str = Field(max_length=32)

# Класс User - вторая модель используется для возврата данных о пользователе из БД клиенту (содержит ID пользователя)
class User(UserIn):
    id: int

#-----------------
# Класс ProductIn - первая модель нужна для получения информации о товаре от клиента
class ProductIn(BaseModel):
    product_name: str = Field(max_length=32)
    description: str = Field(max_length=32)
    price: int

# Класс Product - вторая модель используется для возврата данных о товаре из БД клиенту (содержит ID товара)
class Product(ProductIn):
    id: int

#-----------------
# Класс "OrderIn" - первая модель нужна для получения информации о заказе от клиента
class OrderIn(BaseModel):
    id_user: int
    id_product: int
    status: str = Field(max_length=32)

# Класс "Order" - вторая модель используется для возврата данных о заказе из БД клиенту (содержит ID заказа и время заказа)
class Order(OrderIn):
    id: int
    order_time: datetime.datetime.now()


#--------------------------------------------------------------------------------------------------------
# Добавление тестовых (фейковых) пользователей (users) в БД
@app.get("/fake_fake_users/{count}")
async def create_fake_users(count: int):
    for i in range(count):
        random_name=fake.first_name()
        random_surname=fake.last_name()
        name_lat = f"{random_surname}_{random_name}"
        random_email=f'{translit(name_lat, language_code="ru", reversed=True)}_{random.randint(100,1000)}@mail.ru'
        random_password=f"password_{i+1}_{random.randint(10001,1000000000)}"
        print (random_name, random_surname, random_email, random_password)
        query = users.insert().values(name=random_name,
                                      surname=random_surname,
                                      email=random_email,
                                      password=random_password)

        await database.execute(query)
    return {"message": f"{count} fake users create"}

# Добавление тестовых товаров (products) в БД
@app.get("/create_test_products/")
async def create_test_products():
    list_products = ["Телевизор", "Смарфтон", "Стол", "Мягкая игрушка", "Картина", "Сок", "Чай", "Конфеты", "Куртка", "Кеды", "Дрель", "Кресло", "Кепка"]
    for name_ in list_products:
        query = products.insert().values(product_name=name_,
                                         description=f"products {name_} {random.randint(10000,1000000)}",
                                         price=random.randint(10,1000))
        await database.execute(query)
        print (name_)
    return {"message": f"test products create"}

# Добавление тестовых заказов (orders) в БД
@app.get("/create_test_orders/{count}")
async def create_test_orders(count: int):
    # 1 Формируем список (множество!) ID номеров пользователей
    query = users.select()
    list_users = await database.fetch_all(query)  # получаем список пользователей
    list_users_id = set()   # множество - id номера пользователей
    for user_ in list_users:
        list_users_id.add(user_[0])

    # 2 Формируем список ID номеров товаров
    query = products.select()
    list_products = await database.fetch_all(query)
    list_products_id = []   # список id номера товаров
    for product_ in list_products:
        list_products_id.append(product_[0])

    # 3 Формируем закааы по ID номерам пользователей и товаров
    status_list = ["в сборке", "доставка", "ждет оплаты", "получен", "отменен", "решение спора", "в корзине"]
    for count_ in range(count):  # цикл по пользователям
        if not list_users_id:
            break
        id_user_ = random.choice(list(list_users_id))
        list_users_id.remove(id_user_)
        for count2_ in range(random.randint(2,10)):  # для кажлого ползователя - несколько заказов
            id_product_ = random.choice(list_products_id)
            status_=random.choice(status_list)
            query = orders.insert().values(id_user=id_user_,
                                           id_product=id_product_,
                                           status=status_)
            await database.execute(query)
            print(id_user_, id_product_, status_)
    return {"message": "test orders create"}


#--------------------------------------------------------------------------------------------------------
# 1. CRUD операции для таблицы "users" (пользователи)
#--------------------------------------------------------------------------------------------------------

# 1.1. Создание пользователя в БД, create
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

# 1.2. Чтение ВСЕХ пользователей из БД, read
@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

# 1.3. Чтение одного пользователя из БД, read
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

# 1.4. Обновление одного пользователя в БД, update
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

# 1.5. Удаление пользователя из БД, delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


#--------------------------------------------------------------------------------------------------------
# 2. CRUD операции для таблицы "products" (товары)
#--------------------------------------------------------------------------------------------------------

# 2.1. Создание товара в БД, create
@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(product_name=product.product_name,
                                     description=product.description,
                                     price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}

# 2.2. Чтение ВСЕХ товаров из БД, read
@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)

# 2.3. Чтение одного товара из БД, read
@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)

# 2.4. Обновление одного товара в БД, update
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}

# 2.5. Удаление товара из БД, delete
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}

#--------------------------------------------------------------------------------------------------------
# 3. CRUD операции для таблицы "orders" (заказы)
#--------------------------------------------------------------------------------------------------------

# 3.1. Создание заказа в БД, create
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(id_user=order.id_user,
                                   id_product=order.id_product,
                                   status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}

# 3.2. Чтение ВСЕХ заказов из БД, read
@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)

# 3.3. Чтение одного заказа из БД, read
@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)

# 3.4. Обновление одного заказа в БД, update
@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}

# 3.5. Удаление заказа из БД, delete
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}