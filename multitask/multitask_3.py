import time
import multiprocessing
import os

def food(food_name):
    print("开始{fn}".format(fn=food_name).center(22, "*"))
    time.sleep(3)
    print("结束{0}".format(food_name).center(22, "*"))

def main():
    p1 = multiprocessing.Process(target=food, args=("西红柿炒蛋",))
    p2 = multiprocessing.Process(target=food, args=("酸辣土豆丝",))
    print(os.getpid())
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()



