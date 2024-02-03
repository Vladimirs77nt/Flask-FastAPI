import requests
import threading
import time

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        ]

def download(url):
    response = requests.get(url)
    filename = 'Lesson_4/threading_' + url.replace('https://','').replace('.', '_').replace('/', '__') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)
        print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")

threads = []

start_time = time.time()

for url in urls:
    thread = threading.Thread(target=download, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Полное завершение работы: {time.time() - start_time:.2f} сек / Метод 1 - Многопоточный")