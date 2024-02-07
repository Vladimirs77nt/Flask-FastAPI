# Задание №1

# Создать API для управления списком задач. Приложение должно иметь
# возможность создавать, обновлять, удалять и получать список задач.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Task с полями id, title, description и status.
# Создайте список tasks для хранения задач.
# Создайте маршрут для получения списка задач (метод GET).
# Создайте маршрут для создания новой задачи (метод POST).
# Создайте маршрут для обновления задачи (метод PUT).
# Создайте маршрут для удаления задачи (метод DELETE).
# Реализуйте валидацию данных запроса и ответа.


import logging
from fastapi import FastAPI, HTTPException

from typing import Optional
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str

tasks = []
tasks_test = [Task(id=1, title="FastAPI", description="Просмотреть лекцию №5 и повторить задачи с семинара", status="active"),
              Task(id=2, title="Домашние заботы", description="Прикрутить полку в ванной", status="preparation"),
              Task(id=3, title="Новый год", description="Купить салют на празднование", status="delete")]

text_base_html = '<div>\
            <h1>API для управления списком задач</h1>\
            <a href="/">Главная</a><br>\
            <a href="/tasks/">Список задач</a><br>\
            <a href="/add3tasks/">Добавить 3 тестовые задачи</a><br>\
            <a href="/docs/">Интерактивная документация Swagger</a><br>\
            </div>'

# 1. Главная страница
@app.get("/", response_class=HTMLResponse)
async def main_page():
    logger.info('Отработал GET запрос на главной странице.')
    return f"{text_base_html}"

# 1.1. Страница 3 задачи
@app.get("/add3tasks/", response_class=HTMLResponse)
async def add_3_test_tasks():
    text_tasks = "\n"
    flag_break = False
    for task_test in tasks_test:
        for task in tasks:
            if task_test.id == task.id:
                flag_break = True
        if flag_break:
            break
        tasks.append(task_test)
        flag_break = False
        text_tasks += f"id={task_test.id}, "
    logger.info('Отработал GET запрос на странице добавления 3 задач.')
    return f"{text_base_html}<h3>--- добавлены тестовые задачи ---</h3>\n{text_tasks}"

# 2. Страница /tasks/ - вывести все таски из списка
@app.get("/tasks/", response_class=HTMLResponse)
async def read_all_tasks():
    logger.info('Отработал GET запрос. Запрос на ВСЕ таски (смотри в терминале)')
    text_tasks = "<h1>СПИСОК ЗАДАЧ</h1>\n"
    if tasks:
        for task in tasks:
            print (task)
            text_line = f"<h3>{task}</h3>\n"
            text_tasks += text_line
        return f"{text_base_html}{text_tasks}"
    else:
         return f"{text_base_html}{text_tasks}<h3>--- пусто ---</h3>\n"

# 3. Создание новой таски (задачи) путем передачи POST-запроса
@app.post("/task/", response_model=Task)
async def create_task(task: Task):
    logger.info('Отработал POST запрос. Создание новой таски')
    tasks.append(task)
    return f"{text_base_html}"

# 4. Поиск таски по ID-номеру
@app.get("/tasks/{task_id}", response_model=Task)
async def find_task(task_id: int):
    logger.info('Отработал GET запрос. Поиск таски по ID')
    for task in tasks:
        print(task)
        if task.id == task_id:
            return task
    print(f"Таска с ID={task_id} - не найдена")
    return f"{text_base_html}\nзадача с ID={task_id} - не найдена"

# 5. Изменение таски по ID-номеру
@app.put("/tasks/{task_id}", response_model=Task)
async def modify_task(task_id: int, task_new: Task):
    logger.info('Отработал PUT запрос. Редактирование таски по ID')
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = task_new
            print(f"задача с ID={task_id}изменена на задачу с ID]{task_new.id}!")
            raise HTTPException(status_code=200, detail=f"задача с ID={task_id} изменена на задачу с ID={task_new.id}!")
    print(f"Таска с ID={task_id} - не найдена")
    return f"{text_base_html}\nзадача с ID={task_id} - не найдена"

# 6. Удаление таски по ID-номеру
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    logger.info('Отработал PUT запрос. Удаление таски по ID')
    for task in tasks:
        if task.id == task_id:
            task.status = "delete"
            raise HTTPException(status_code=200, detail=f"задача ID={task_id} - удалена (помечена delete) !")
    print(f"Таска с ID={task_id} - не найдена")
    return f"{text_base_html}\nзадача с ID={task_id} - не найдена"