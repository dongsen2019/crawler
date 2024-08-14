import multiprocessing

import datetime
from gevent import monkey
import time

import os

import json

import pandas as pd

from selenium import webdriver

# 获取当前工作目录
current_path = os.getcwd()
dir_list = os.listdir(current_path)

for d in dir_list:
    d_path = os.path.join(current_path, d)
    print(d_path)
    if os.path.isdir(d_path):
        print("打开json文件")
    else:
        pass

c = 1

c += 1


