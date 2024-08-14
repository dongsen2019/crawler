from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

import time

ser = Service()
ser.path = r'D:\python project\pythonProject\chromedriver.exe'



# 初始化driver
driver = webdriver.Chrome(service=ser)

# 打开网页
driver.get("https://www.gucci.cn/zh/ca/whats-new/new-in/this-week-women?navigation.code=0-0-2")

# 创建一个ActionChains对象
actions = ActionChains(driver)

# 定位到页面底部的元素（可以是一个按钮、链接等，或者只是页面上的一个点）
# 这里我们假设页面底部有一个ID为'bottom-element'的元素
bottom_element = driver.find_element(By.CLASS_NAME, 'return-top-text')

# 使用ActionChains的move_to_element方法来模拟鼠标移动到该元素上
actions.move_to_element(bottom_element)

# 执行ActionChains中的操作
actions.perform()

# 在鼠标移动到元素上之后，可以使用JavaScript来滚动页面到底部
driver.execute_script("arguments[0].scrollIntoView();", bottom_element)

# 等待一段时间，让页面加载完成
time.sleep(5)

# 关闭driver
driver.quit()
