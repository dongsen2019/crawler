import time
import multiprocessing
import os

def food(food_name, ts):
    print("开始{fn}".format(fn=food_name).center(22, "*"))
    time.sleep(ts)
    print("结束{0}".format(food_name).center(22, "*"))

def main():
    p1 = multiprocessing.Process(target=food, args=["西红柿炒蛋", 5])
    p2 = multiprocessing.Process(target=food, args=("酸辣土豆丝", 3))
    p1.daemon = True

    p1.start()
    p2.start()

    time.sleep(2)


if __name__ == '__main__':
    main()