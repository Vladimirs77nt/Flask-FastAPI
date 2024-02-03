import multiprocessing
import time

counter = multiprocessing.Value('i', 0)

def increment(cnt, ii):
    print (f"Запуск {ii}-го процесса")
    for _ in range(1_000_000):
        with cnt.get_lock():
            cnt.value += 1
    print(f"Значение счетчика {ii}: {cnt.value:_}")

if __name__ == '__main__':
    # стартуем секундомер
    time_start = time.perf_counter()

    processes = []
    
    for i in range(5):
        p = multiprocessing.Process(target=increment, args=(counter, i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    # останавливаем секундомер
    time_finish = time.perf_counter()
    print(f"Вычисление заняло {time_finish-time_start:0.4f} секунд")

    print(f"Значение счетчика в финале: {counter.value:_}")