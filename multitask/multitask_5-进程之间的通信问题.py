import time
import multiprocessing
import os

# 在windows下，是通过多份存储空间，实现全局变量不共享，数据不互通
# 在linux下，通过fork机制，而不是多份存储空间（一份存储空间），实现进程间的数据不共享


def food(food_name, ts, ff):
    print("开始{fn}".format(fn=food_name).center(22, "*"))
    time.sleep(ts)
    print("结束{0}".format(food_name).center(22, "*"))

    ff.put(food_name)

def main():
    food_list = multiprocessing.Queue(6)
    p1 = multiprocessing.Process(target=food, args=["西红柿炒蛋", 5, food_list])
    p2 = multiprocessing.Process(target=food, args=("酸辣土豆丝", 3, food_list))

    p1.start()
    p2.start()

    time.sleep(6)
    while not food_list.empty():
        print(food_list.get())

if __name__ == '__main__':
    main()

