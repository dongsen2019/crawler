import time
import multiprocessing
import os

def food1():
    print("开始西红柿炒蛋".center(22, "*"))
    time.sleep(3)
    print("结束西红柿炒蛋".center(22, "*"))

def food2():
    print("开始酸辣土豆丝".center(22, "*"))
    time.sleep(4)
    print("结束酸辣土豆丝".center(22, "*"))

def main():
    p1 = multiprocessing.Process(target=food1)
    p2 = multiprocessing.Process(target=food2)
    print(os.getpid())
    p1.start()
    p2.start()
    print(p1.pid)
    print(p2.pid)
    os.kill(p2.pid, 9)

if __name__ == '__main__':
    main()
