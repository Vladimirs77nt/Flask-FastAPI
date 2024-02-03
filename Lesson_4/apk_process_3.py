import multiprocessing
import time

counter = 0
abs = 0

def increment(abs, ii):
    print (f"Запуск {ii}-го процесса")
    global counter
    for _ in range(100_000_000):
        counter += 1
    print(f"Значение счетчика {ii}: {counter:_}")

if __name__ == '__main__':
    # стартуем секундомер
    time_start = time.perf_counter()

    processes = []
    
    for i in range(5):
        p = multiprocessing.Process(target=increment, args=(abs, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    # останавливаем секундомер
    time_finish = time.perf_counter()
    print(f"Вычисление заняло {time_finish-time_start:0.4f} секунд")

    print(f"Значение счетчика в финале: {counter:_}")