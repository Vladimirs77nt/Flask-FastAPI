import threading
import time

# стартуем секундомер
time_start = time.perf_counter()

counter = 0

def increment():
    global counter
    for _ in range(100_000_000):
        counter += 1
    print(f"Значение счетчика: {counter:_}")

threads = []

for i in range(5):
    increment()

# останавливаем секундомер
time_finish = time.perf_counter()
print(f"Вычисление заняло {time_finish-time_start:0.4f} секунд")

print(f"Значение счетчика в финале: {counter:_}")