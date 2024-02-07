# Домашняя работа.

# Задание №2

# Создать API для получения списка фильмов по жанру.
# Приложение должно иметь возможность получать список фильмов по заданному жанру.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Movie с полями id, title, description и genre.
# Создайте список movies для хранения фильмов.
# Создайте маршрут для получения списка фильмов по жанру (метод GET).
# Реализуйте валидацию данных запроса и ответа.


import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

app = FastAPI()

class Movie(BaseModel):
    id: int             # ID-номер
    name: str           # название фильма
    description: str    # описание
    genre: str          # жанр
    status: str         # статус

films = []
films_test = [Movie(id=1, name="Терминатор", description="История противостояния солдата Кайла Риза и киборга-терминатора,\
                    прибывших в 1984 год из пост-апокалиптического будущего, где миром правят машины-убийцы,\
                    а человечество находится на грани вымирания", genre="фантастика", status="active"),
               Movie(id=2, name="Чужие", description="Команда рудодобывающего коробля сталкивается с инопланетной формой\
                     жизни", genre="фантастика", status="active"),
               Movie(id=3, name="Маска", description="Волшебная маска помогает банковскому клерку выпустить демона\
                     и поверить в себя.", genre="Комедия", status="active")]

text_base_html = '<div>\
            <h1>API для фильмов</h1>\
            <a href="/">Главная</a><br>\
            <a href="/films/">Список фильмов</a><br>\
            <a href="/add3films/">Добавить 3 тестовых фильма</a><br>\
            <a href="/genre/">Поиск фильма по жанру</a><br>\
            <a href="/docs/">Интерактивная документация Swagger</a><br>\
            </div>'

# 1. Главная страница
@app.get("/", response_class=HTMLResponse)
async def main_page():
    logger.info('Отработал GET запрос на главной странице.')
    return f"{text_base_html}"

# 2. Страница - добавить 3 тестовых фильма
@app.get("/add3films/", response_class=HTMLResponse)
async def add_3_test_films():
    text_films = "\n"
    flag_break = False
    for film_test in films_test:
        for film in films:
            if film_test.id == film.id:
                flag_break = True
        if flag_break:
            break
        films.append(film_test)
        flag_break = False
        text_films += f"id={film_test.id}, "
    logger.info('Отработал GET запрос на странице добавления 3 тестовых фильма.')
    return f"{text_base_html}<h3>--- добавлены тестовые фильмы ---</h3>\n{text_films}"

# 3. Страница /films/ - вывести все фильмы из списка
@app.get("/films/", response_class=HTMLResponse)
async def read_all_films():
    logger.info('Отработал GET запрос. Запрос на ВСЕ фильмы (смотри в терминале)')
    text_films = "<h1>СПИСОК ФИЛЬМОВ</h1>\n"
    if films:
        for film in films:
            text_line = f"<h3>{film}</h3>\n"
            text_films += text_line
        return f"{text_base_html}{text_films}"
    else:
         return f"{text_base_html}{text_films}<h3>--- пусто ---</h3>\n"

# 4. Создание записи о новом фильме путем передачи POST-запроса
@app.post("/films/", response_model=Movie)
async def create_movie(film: Movie):
    logger.info('Отработал POST запрос. Создание записи о фильме')
    films.append(film)
    return f"{text_base_html}"

# 5. Поиск фильма по ID-номеру
@app.get("/films/{film_id}", response_model=Movie)
async def find_movie_id(film_id: int):
    logger.info('Отработал GET запрос. Поиск фильма по ID')
    for film in films:
        if film.id == film_id:
            return film
    logger.info(f" >>> Фильм с ID={film_id} - не найден")
    return f"{text_base_html}\nфильм с ID={film_id} - не найдена"

# 6. Поиск фильма по жанру
@app.get("/genre/{film_genre}", response_class=HTMLResponse)
async def find_movie_ganre(film_genre: str):
    logger.info('Отработал GET запрос. Поиск фильма по жанру')

    films_genre = []    # СПИСОК ФИЛЬМОВ ПО ЗАДАННОМУ ЖАНРУ

    for film in films:
        if film.genre.lower() == film_genre.lower():
            films_genre.append(film)

    text_films = f"<h1>Список фильмов с жанром: {film_genre}</h1>\n"
    if len(films_genre)>0:
        for film in films_genre:
            text_line = f"<h3>{film}</h3>\n"
            text_films += text_line
        return f"{text_base_html}{text_films}"
    
    logger.info(f" >>> Фильмы с жанром {film_genre} - не найдены")
    return f"Фильмы с жанром {film_genre} - не найдены"

# 7. Изменение фильма по ID-номеру
@app.put("/films/{film_id}", response_model=Movie)
async def modify_movie(film_id: int, film_new: Movie):
    logger.info('Отработал PUT запрос. Редактирование фильма по ID')
    for i, film in enumerate(films):
        if film.id == film_id:
            films[i] = film_new
            print(f"фильм с ID={film_id}изменен на новый фильм с ID]{film_new.id}!")
            return f"фильм с ID={film_id}изменен на новый фильм с ID]{film_new.id}!"
    logger.info(f" >>> Фильм с ID={film_id} - не найден")
    return f"{text_base_html}\nФильм с ID={film_id} - не найден"

# 8. Удаление таски по ID-номеру
@app.delete("/films/{film_id}", response_model=Movie)
async def delete_movie(film_id: int):
    logger.info('Отработал PUT запрос. Удаление таски по ID')
    for film in films:
        if film.id == film_id:
            film.status = "delete"
            return f"фильм ID={film_id} - удален (помечен delete) !"
    logger.info(f" >>> Фильм с ID={film_id} - не найден")
    return f"{text_base_html}\nФильм с ID={film_id} - не найден"