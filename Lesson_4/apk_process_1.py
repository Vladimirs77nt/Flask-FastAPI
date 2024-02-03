import multiprocessing
import time

def worker(num):
    print(f"Запущен процесс {num}")
    time.sleep(3)
    print(f"Завершён процесс {num}")

if __name__ == '__main__':
    # стартуем секундомер
    time_start = time.perf_counter()

    processes = []
    
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    # останавливаем секундомер
    time_finish = time.perf_counter()
    print(f"Вычисление заняло {time_finish-time_start:0.4f} секунд")

    print("Все процессы завершили работу")