import threading
import time

abs = 0

# стартуем секундомер
time_start = time.perf_counter()

counter = 0

def increment(abs, ii):
    print (f"Запуск {ii}-го Потока")
    global counter
    for _ in range(100_000_000):
        counter += 1
    print(f"Значение счетчика (в потоке {ii}): {counter:_}")

threads = []

for i in range(5):
    t = threading.Thread(target=increment, args=(abs, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# останавливаем секундомер
time_finish = time.perf_counter()
print(f"Вычисление заняло {time_finish-time_start:0.4f} секунд")

print(f"Значение счетчика в финале: {counter:_}")