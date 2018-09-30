import multiprocessing
import time
from multiprocessing.pool import ApplyResult

lock = multiprocessing.Lock()
def worker_1(interval, count, lock):
    print('worker_1')
    #time.sleep(interval)
    with lock:
        for i in range(1,1000):
            count.append(i)
    print('end worker_1')

def worker_2(interval, count, lock):
    print('worker_2')
    #time.sleep(interval)
    with lock:
        for i in range(2000,3000):
            count.append(i)
    print('end worker_2')

def worker_3(interval, count, lock):
    print('worker_3')
    #time.sleep(interval)
    with lock:
        for i in range(3000,4000):
            count.append(i)
    print('end worker_3')

def single_test():
    m = multiprocessing.Manager()
    count = m.list()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p1 = multiprocessing.Process(target=worker_1, args=(2, count, lock,))
    p2 = multiprocessing.Process(target=worker_2, args=(3, count, lock,))
    p3 = multiprocessing.Process(target=worker_3, args=(4, count, lock,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    print('The number of CPU is:' + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print('child   p.name:' + p.name + '\tp.id' + str(p.pid))
    print(count)
    print('END!!!!!!!!!!!!!!!!!')

def f(x):
    for i in range(10):
        print('%s --- %s ' % (i, x))
        #time.sleep(1)
def pool_test():
    global result
    pool = multiprocessing.Pool(processes=2)  # set the processes max number 3
    for i in range(11, 20):
        result = pool.apply_async(f, (i,))
    pool.close()
    pool.join()
    if result.successful():
        print('successful')

if __name__ == '__main__':
    # test_single()
    pool_test()