import asyncio
import aiohttp
import time

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        ]

async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = 'Lesson_4/asyncio_' + url.replace('https://','').replace('.', '_').replace('/', '__') + '.html'
            with open(filename, "w", encoding='utf-8') as f:
                f.write(text)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")

async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':

    start_time = time.time()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек / Метод 3 - Асинхровнный")