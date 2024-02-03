import requests
import time

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        ]

start_time = time.time()

for url in urls:
    response = requests.get(url)
    filename = 'Lesson_4/sync_' + url.replace('https://', '').replace('.','_').replace('/', '__') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")

print(f"Полное завершение работы: {time.time() - start_time:.2f} сек / Метод 0 - Синхронный")