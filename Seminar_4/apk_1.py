# Задание №1

# � Написать программу, которая считывает список из 10 URL-адресов и одновременно
#    загружает данные с каждого адреса. 
# � После загрузки данных нужно записать их в отдельные файлы.
# � Используйте потоки.
# -----------------------

import requests
from threading import Thread
import time

urls = ['https://gb.ru/',
        'https://google.com',
        'https://yandex.ru',
        'https://python.org',
        'https://mail.ru',
        'https://stepik.org',
        'https://vk.com',
        'https://yahoo.com',
        'https://pikabu.ru',
        'https://codelessons.ru',
        ]

def download(url):
    response = requests.get(url)
    filename = 'Seminar_4/task_1_potok_' + url.replace('https://','').split('/')[0] + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)

# -----------------------
if __name__ == '__main__':

    print("Задание 1 / Многопоточный")
    threads = []
    start_time = time.time()

    for url in urls:
        thread = Thread(target=download, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек (задание 1)")