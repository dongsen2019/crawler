from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time

ser = Service()
ser.path = r'D:\python project\pythonProject\chromedriver.exe'

# 初始化webdriver
driver = webdriver.Chrome(service=ser)

# 打开网页
driver.get("https://www.gucci.cn/zh/ca/whats-new/new-in/this-week-women?navigation.code=0-0-2")


# 定义一个函数来滚动页面到底部并等待加载
def scroll_and_wait(driver, wait_time=15):
    try:
        # 获取页面底部元素，这里假设是页面最后一个可见的元素
        last_element = driver.find_element(By.CLASS_NAME, 'select-view')

        # 计算页面底部元素的位置
        last_element_position = last_element.location_once_scrolled_into_view

        # 滚动到页面底部
        driver.execute_script(f"window.scrollTo(0, {last_element_position['y']});")

        # 等待加载新内容
        time.sleep(wait_time)  # 等待10秒

        # 检查是否有新内容加载，这里可以根据实际情况调整检查条件
        # 例如，检查某个新元素是否出现
        new_element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, 'new_element_id')))
        return new_element
    except:
        # 如果在等待过程中发生异常，可能是没有新内容加载
        return None


# 循环滚动页面直到没有新内容加载
while True:
    new_element = scroll_and_wait(driver)
    if new_element is None:
        # 如果没有新元素出现，说明没有更多内容加载
        break

# 在所有内容加载完毕后，你可以执行其他操作，比如获取页面内容
print(driver.page_source)

# 关闭浏览器
driver.quit()