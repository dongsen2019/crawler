import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--healthcheck-interval=3")

driver = webdriver.Chrome()

driver.get("http://localhost:8000/view_study/")
# driver.get("https://www.gucci.cn/zh/ca/whats-new/horsebit-handbags-and-xiao-zhan-c-horsebit-handbags-xiao-zhan?navigation.code=0-2-1-0")


driver.implicitly_wait(100)


str_xpath = "//div/div/div/div/div/div/div/div/div/div/img[contains(@src,'800x800')]"
locator = (By.XPATH, str_xpath)

url_elements = driver.find_elements(*locator)
print(url_elements)

# selenium.webdriver.remote.webelement.WebElement

for ele in url_elements:
    print(ele.get_attribute("src"))


now = time.localtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", now))




    # if target_move != None:
    #     ActionChains(driver).move_to_element(target_move).click(target_move).perform()
    #     action_bd = ActionBuilder(driver)
    #     action_bd.pointer_action.pointer_down(MouseButton.BACK)
    #     time.sleep(0.3)
    #     action_bd.pointer_action.pointer_up(MouseButton.BACK)
    #     action_bd.perform()
    #
    # elif target_move == None:
    #     now = time.localtime()
    #     print(time.strftime("%Y-%m-%d %H:%M:%S", now))
    #     break



# print(driver.page_source)

driver.quit()