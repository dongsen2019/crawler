import multiprocessing
import threading
import time

def make_food(q_order, q_serve):
    while True:
        food_order = q_order.get()
        print("开始制作{0}".format(food_order).center(22, "*"))
        time.sleep(2)
        print("结束制作{0}".format(food_order).center(22, "*"))
        q_serve.put(food_order)

def serve_food(q_serve):
    while True:
        food_serve = q_serve.get()
        print("上菜:{0}".format(food_serve).center(44, "*"))

def main():
    qo = multiprocessing.Queue(6)
    qs = multiprocessing.Queue(6)
    p1 = multiprocessing.Process(target=make_food, args=(qo, qs))
    p2 = multiprocessing.Process(target=serve_food, args=(qs,))
    p1.start()
    p2.start()

    while True:
        food_name = input("请输入您的点菜名:")
        qo.put(food_name)


if __name__ == '__main__':
    main()



