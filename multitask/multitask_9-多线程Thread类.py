import multiprocessing
from threading import Thread
import time

class Make_Food(Thread):
    def __init__(self, q_order, q_serve):
        super().__init__()
        self.q_order = q_order
        self.q_serve = q_serve

    def run(self):
        while True:
            food_order = self.q_order.get()
            print("开始制作{0}".format(food_order).center(22, "*"))
            time.sleep(2)
            print("结束制作{0}".format(food_order).center(22, "*"))
            self.q_serve.put(food_order)


class Serve_Food(Thread):
    def __init__(self, q_serve):
        super().__init__()
        self.q_serve = q_serve

    def run(self):
        while True:
            food_serve = self.q_serve.get()
            print("上菜:{0}".format(food_serve).center(44, "*"))


def main():
    qo = multiprocessing.Queue(6)
    qs = multiprocessing.Queue(6)
    mf = Make_Food(qo, qs)
    sf = Serve_Food(qs)
    mf.start()
    sf.start()

    while True:
        food_name = input("请输入您的点菜名:")
        qo.put(food_name)


if __name__ == '__main__':
    main()
