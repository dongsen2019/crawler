import time

def food1():
    print("开始西红柿炒蛋".center(22, "*"))
    time.sleep(3)
    print("结束西红柿炒蛋".center(22, "*"))

def food2():
    print("开始酸辣土豆丝".center(22, "*"))
    time.sleep(4)
    print("结束酸辣土豆丝".center(22, "*"))

def main():
    s = time.time()
    food1()
    food2()
    e = time.time()
    print(e-s)

if __name__ == '__main__':
    main()


