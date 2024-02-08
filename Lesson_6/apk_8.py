from fastapi import FastAPI, Path, Query

app = FastAPI()

# Проверка параметра пути через Path

# 1
# Параметр "item_id" имеет тип int и должен быть больше или равен 1.
# Мы используем многоточие (...) в качестве значения по умолчанию для параметра "item_id",
# что означает, что параметр обязателен для передачи в URL.
# Если параметр не передан bли его значение меньше 1, то будет сгенерировано исключение.
@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(..., ge=1), q: str = None):
    return {"item_id": item_id, "q": q}

# 2
# В этом примере мы создаем маршрут "/items/{item_id}" с параметром пути "item_id".
# Кроме ограничений на тип данных и значения, мы также задаем для параметра "item_id" заголовок "The ID of the item".
# Этоn заголовок будет использоваться при uенерации документации API: http://127.0.0.1:8000/redoc
@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(..., title="The ID of the item"), q: str = None):
    return {"item_id": item_id, "q": q}

# Проверка параметра запроса через Query

# 3
# В этом примере мы создаем маршрут "/items/" с параметром запроса "q".
# Параметр "q" имеет тип str и может быть длиной от 3 до 50 символов.
# Если параметр "q" не передан в запросе, то ему будет присвоено значение None.
# Если же параметр "q" передан, то его значение будет добавлено к результатам запроса.
@app.get("/items/")
async def read_items(q: str = Query(None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Spam"}, {"item_id": "Eggs"}]}
    if q:
        results.update({"q": q})
    return results

# 4
# В этом примере мы создаем маршрут "/items/" с параметром запроса "q".
# Параметр "q" имеет тип str и должен быть длиной не менее 3 символов.
# В отличие от первого примера, здесь мы используем многоточие (...) в качестве значения по умолчанию
# для параметра "q". Это означает, что параметр "q" обязателен для передачи в запросе.
# Если параметр не передан, то будет сгенерировано исключение.
@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Spam"}, {"item_id": "Eggs"}]}
    if q:
        results.update({"q": q})
    return results
