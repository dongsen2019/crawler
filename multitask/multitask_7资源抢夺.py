from multiprocessing import Manager, Pool
import multiprocessing
import time
import os


def task(a, l):
    for i in range(10):

        l.acquire()
        time.sleep(1)
        a[0] += 1
        print(a[0], os.getpid())
        # a.acquire()
        # print(i)
        # a.release()
        l.release()

    # print(n_list[0])


def main():
    manager = Manager()
    lock = manager.Lock()
    n = manager.list()
    n.append(0)

    print(n[0])

    # n = manager.dict()
    # n['m'] = 0
    # print(type(n['m']))
    # print(n['m'])
    pool = Pool(6)
    for i in range(3):
        # pool.apply(func=task, args=(n,lock))
        pool.apply_async(func=task, args=(n, lock))

    pool.close()
    pool.join()
    print("程序结束")


if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print(e-s)


