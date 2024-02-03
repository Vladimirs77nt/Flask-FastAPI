import threading
import time

# стартуем секундомер
time_start = time.perf_counter()

def worker(num):
    print(f"Начало работы потока {num}")
    time.sleep(5)
    print(f"Конец работы потока {num}")

threads = []

for i in range(5):
    t = threading.Thread(target=worker, args=(i, ))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# останавливаем секундомер
time_finish = time.perf_counter()
print(f"Вычисление заняло {time_finish-time_start:0.4f} секунд")

print("Все потоки завершили работу")