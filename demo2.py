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

driver.get("https://www.gucci.cn/zh/ca/women/handbags?navigation.code=0-4-2-0")
# driver.get("https://www.gucci.cn/zh/ca/whats-new/horsebit-handbags-and-xiao-zhan-c-horsebit-handbags-xiao-zhan?navigation.code=0-2-1-0")


driver.implicitly_wait(100)


pos_a = {"x": 0, "y": 0}
pos_b = {"x": 0, "y": 1}


while pos_a["y"] != pos_b["y"]:
    iframe = driver.find_element(By.CLASS_NAME, "cta-text-item")
    print(iframe)
    pos_a["y"] = iframe.location["y"]
    ActionChains(driver).scroll_to_element(iframe).perform()
    pos_b["y"] = iframe.location["y"]
    print(iframe.text)
    print(iframe.location)
    time.sleep(2)

# with open("gucci.html", "w", encoding="utf-8") as f:
#     f.write(driver.page_source)

for i in range(1, 1000):
    str_xpath = "/html/body/div[@id='app']/div/div[@class='app-container']/div[@class='plp-container']/div/div[@class='goodsContainer']/div[@class='product-box']/div[@class='product-cont']/a["+str(i)+"]"
    locator = (By.XPATH, str_xpath)
    # WebDriverWait(driver,5).until(EC.)
    # ec_loc = WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
    # print(ec_loc)
    now = time.localtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", now))

    try:
        target_move = WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        target_move = None

    print(target_move)


    if target_move != None:
        ActionChains(driver).move_to_element(target_move).click(target_move).perform()
        action_bd = ActionBuilder(driver)
        action_bd.pointer_action.pointer_down(MouseButton.BACK)
        time.sleep(0.3)
        action_bd.pointer_action.pointer_up(MouseButton.BACK)
        action_bd.perform()

    elif target_move == None:
        now = time.localtime()
        print(time.strftime("%Y-%m-%d %H:%M:%S", now))
        break



# print(driver.page_source)

driver.quit()
