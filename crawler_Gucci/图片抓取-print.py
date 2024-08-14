from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time
import os
import json
import pandas as pd
import multiprocessing
import threading
import requests

crawler_urls = {
    "女士手袋": "https://www.gucci.cn/zh/ca/women/handbags?navigation.code=0-4-2-0",
    "女士成衣": "https://www.gucci.cn/zh/ca/women/readytowear?navigation.code=0-2-3-0"
}

sku_picture_url = dict()  # 全局变量


# 创建大类名称文件夹
def make_class_dir(cls_path):
    if not os.path.exists(cls_path):
        os.mkdir(cls_path)


# 创建文件夹，以款号(SKU)为文件夹名称，并写入SKU商品介绍txt
def make_sku_dir(dir_path, js_context, gg_context):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(dir_path+"/introduce.txt", "a", encoding="utf-8") as f_introduce:
        f_introduce.write(js_context)
        f_introduce.write("\n")
        f_introduce.write(gg_context)


def write_excel():
    pass


def picture_write(num, url, w_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        pic_path = w_path + "/" + str(num) + ".jpg"
        with open(pic_path, "wb") as f_pic:
            f_pic.write(resp.content)


# 多进程下载图片写入图片文件
def picture_requests(cls, url_json_path):
    # 加载sku_url.json
    url_dict = dict()
    with open(url_json_path, "r", encoding="utf-8") as f_sku_url:
        url_dict = json.load(f_sku_url)

    # 路径./大类/SKU/图片名称
    for k_sku_url, v_pict_url in url_dict.items():
        code_begin = k_sku_url.find("pr/")
        code_end = k_sku_url.find("?url")
        pdt_code = k_sku_url[code_begin + 3:code_end]

        pdt_path = "./"+cls+"/"+pdt_code

        for i in range(len(v_pict_url)):
            t = threading.Thread(target=picture_write, args=(i, v_pict_url[i], pdt_path))
            t.start()


def main(*url):
    product_code = ""
    product_name = ""
    product_introduce = ""
    product_price = 0
    product_color = ""
    product_size = ""
    product_all = []

    driver = webdriver.Chrome()

    # driver.get("https://www.gucci.cn/zh/ca/women/handbags?navigation.code=0-4-2-0")
    driver.get(url[1])

    # 创建大类文件夹
    class_path = "./" + url[0]
    make_class_dir(class_path)

    # 1.滚动页面至底部 将JavaScript动态渲染的内容全部展示出
    pos_a = {"x": 0, "y": 0}
    pos_b = {"x": 0, "y": 1}
    # while pos_a["y"] != pos_b["y"]:
    #     to_top = driver.find_element(By.CLASS_NAME, "cta-text-item")
    #     pos_a["x"] = to_top.location["x"]
    #     pos_a["y"] = to_top.location["y"]
    #     ActionChains(driver).scroll_to_element(to_top).perform()
    #     time.sleep(2)
    #     pos_b["x"] = to_top.location["x"]
    #     pos_b["y"] = to_top.location["y"]
    #     print(to_top.rect)

    # 1.1利用xpath表达式计算出所有页面商品的数量
    list_xpath = "/html/body/div[@id='app']/div/div[@class='app-container']/div[@class='plp-container']/" \
                 "div/div[@class='goodsContainer']/div[@class='product-box']/div[@class='product-cont']/a"

    list_elements = driver.find_elements(By.XPATH, list_xpath)

    list_elements_counts = len(list_elements)

    print("{0}:{1}".format(driver.title, list_elements_counts))

    # 2.循环点击每一个商品链接，进入商品详情页面
    begin_time = time.time()

    for i in range(1, list_elements_counts + 1):
        list_xpath_i = ("/html/body/div[@id='app']/div/div[@class='app-container']/div[@class='plp-container']/"
                        "div/div[@class='goodsContainer']/div[@class='product-box']/div[@class='product-cont']/a["
                        + str(i) + "]")

        list_ele = driver.find_element(By.XPATH, list_xpath_i)

        ActionChains(driver).move_to_element(list_ele).click(list_ele).perform()
        print(i)
        time.sleep(1)

        # 进入商品详情页面
        cta_locator = (By.XPATH, "//span[text()='商品详情']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(cta_locator))

        # 2.1 商品详情按钮、商品名称、商品价格、商品详情信息-介绍 的web标签的xpath路径、商品详情信息-规格 的web标签的xpath路径、详情页关闭按钮的路径
        product_detail_xpath = "//span[text()='商品详情']"

        size_detail_xpath = "//div[@class='spice-product-style']/div[@class='left-style']/" \
                            "span[contains(text(),'尺码')]/../following-sibling::div[1]/i"

        product_detail_name_xpath = "//h1[@class = 'spice-product-name']"

        product_detail_price_xpath = "//span[@class = 'goods-price']"

        product_detail_color_xpath = "//span[text()='颜色']/following-sibling::*[1]"

        product_detail_size_xpath = "//div[@class='style-list-content']/div[@class = 'style-content']/" \
                                    "div[@class = 'size-list']/div[@class = 'item']//div[@class = 'left']"

        product_detail_js_xpath = "/html/body/div[@class='product-dialog-container']/" \
                                  "div[@class='base-box header-dialog-base-box main-dialog main-dialog-in']/" \
                                  "div[@class='product-detail']/div[@class='product-content']/" \
                                  "div[contains(@class,'detail-info')]"

        product_detail_gg_xpath = "/html/body/div[@class='product-dialog-container']/" \
                                  "div[@class='base-box header-dialog-base-box main-dialog main-dialog-in']/" \
                                  "div[@class='product-detail']/div[@class='product-content']/" \
                                  "div[@class='detail-list']/ul/li"

        product_detail_close_xpath = "/html/body/div[@class='product-dialog-container']/" \
                                     "div[@class='base-box header-dialog-base-box main-dialog main-dialog-in']/" \
                                     "div[@class='close-warp']/div[@class='close-btn']/i[@class='icon-font icon-close1']"

        size_detail_close_xpath = "/html/body/div[@class='product-dialog-container']/" \
                                  "div[@class='base-box header-dialog-base-box main-dialog main-dialog-in']/" \
                                  "div[@class='close-warp']/div[@class='close-btn']/i[@class='icon-font icon-close1']"

        # 获取详情页的商品名称
        product_detail_name = driver.find_element(By.XPATH, product_detail_name_xpath)
        product_name = product_detail_name.text
        print(product_name)

        # 获取详情页商品价格
        product_detail_price = driver.find_element(By.XPATH, product_detail_price_xpath)
        print("操作2")
        print(product_detail_price.text)
        sku_price = int(product_detail_price.text[1:len(product_detail_price.text) + 1].replace(",", ""))
        product_price = sku_price
        print(product_price)

        # 获取详情页颜色span标签的文本
        product_detail_color = None
        try:
            product_detail_color = driver.find_element(By.XPATH, product_detail_color_xpath)
        except NoSuchElementException:
            pass

        if product_detail_color is not None:
            product_color = product_detail_color.text
            print(product_color)
        else:
            product_color = ""

        # 模拟鼠标点击商品详情按钮的操作
        product_detail_element = driver.find_element(By.XPATH, product_detail_xpath)
        print("操作:1")
        ActionChains(driver).click(product_detail_element).perform()

        # 获取详情页-介绍
        product_detail_js_ele = driver.find_element(By.XPATH, product_detail_js_xpath)
        str_js = product_detail_js_ele.get_attribute("innerHTML").strip()
        print(str_js)

        # 获取详情页 <li>标签文本内容
        str_gg = ""
        product_detail_gg_ele = driver.find_elements(By.XPATH, product_detail_gg_xpath)
        for s in product_detail_gg_ele:
            str_gg += (s.get_attribute("innerHTML").strip() + ";")
            print(s.get_attribute("innerHTML").strip())
        print(str_gg)

        product_introduce = str_js + str_gg

        # 等待关闭按钮的出现
        cta_locator = (By.XPATH, product_detail_close_xpath)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(cta_locator))
        time.sleep(1)

        # 模拟鼠标关闭商品详情按钮的操作
        product_detail_close = driver.find_element(By.XPATH, product_detail_close_xpath)
        print("操作:3")
        ActionChains(driver).click(product_detail_close).perform()
        time.sleep(1)

        # 2.2 利用当前商品的URL地址提取SKU，并创建该类别 路径下的每个SKU的文件夹
        product_url = driver.current_url
        print(product_url)

        # 获取URL地址中的SKU
        sku_begin = product_url.find("pr/")
        sku_end = product_url.find("?url")
        sku_code = product_url[sku_begin + 3:sku_end]
        product_code = sku_code
        print(product_code)
        sku_path = "./" + url[0] + "/" + product_code

        # 调用创建文件夹、写入介绍文本函数
        make_sku_dir(sku_path, str_js, str_gg)

        # 2.3 获取尺码详情页的文本，根据不同尺码的情况，创建相应的商品资料列表
        size_detail_button = None
        try:
            size_detail_button = driver.find_element(By.XPATH, size_detail_xpath)
        except NoSuchElementException:
            pass

        if size_detail_button is not None:
            # 如果找到该元素执行以下操作
            ActionChains(driver).click(size_detail_button).perform()

            product_detail_size = driver.find_elements(By.XPATH, product_detail_size_xpath)
            for s_ele in product_detail_size:
                print(s_ele.text)
                product_all.append([product_code, product_name, product_introduce, product_price,
                                    product_color, s_ele.text])

            # 等待尺码详情页的关闭按钮出现
            size_locator = (By.XPATH, size_detail_close_xpath)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(size_locator))
            time.sleep(1)

            # 模拟鼠标关闭商品详情按钮的操作
            size_close = driver.find_element(By.XPATH, size_detail_close_xpath)
            print("操作:size详情页关闭")
            ActionChains(driver).click(size_close).perform()
            time.sleep(1)
        else:
            product_all.append([product_code, product_name, product_introduce, product_price, product_color, ""])

        # 2.4存储图片URL的web标签xpath路径
        detail_img_xpath = "//div/div/div/div/div/div/div/div/div/div/img[contains(@src,'800x800')]"
        detail_elements = driver.find_elements(By.XPATH, detail_img_xpath)

        list_url = []
        # 获取图片URL地址
        for ele in detail_elements:
            list_url.append(ele.get_attribute("src"))

        sku_picture_url[product_url] = list_url

        # 2.5鼠标键4返回操作
        action_back = ActionBuilder(driver)
        action_back.pointer_action.pointer_down(MouseButton.BACK)
        action_back.pointer_action.pointer_up(MouseButton.BACK)
        action_back.perform()
        time.sleep(1)

    end_time = time.time()
    print(end_time - begin_time)

    for k_sku, v_url in sku_picture_url.items():
        print(k_sku, v_url)

    sku_json_path = "./" + url[0] + "/sku_url.json"
    with open(sku_json_path, "w", encoding="utf-8") as f_url:
        json.dump(sku_picture_url, f_url)

    counts_list = len(product_all)

    for i in product_all:
        print(i)

    df = pd.DataFrame({
        "品牌": ["GUCCI" for _ in range(counts_list)],
        "国际码": [i[0] for i in product_all],
        "名称": [i[1] for i in product_all],
        "介绍": [i[2] for i in product_all],
        "价格": [i[3] for i in product_all],
        "颜色": [i[4] for i in product_all],
        "尺寸": [i[5] for i in product_all]
    })

    excel_path = "./" + url[0] + "/sku_data.xlsx"
    with pd.ExcelWriter(excel_path) as writer:
        df.to_excel(writer, sheet_name="data1")
        df.to_excel(writer, sheet_name="data2")

    # url_json_path = "./" + url[0] + "/sku_url.json"
    # picture_requests(url[0], url_json_path)

    driver.quit()


if __name__ == '__main__':
    pool = multiprocessing.Pool(2)
    for k, v in crawler_urls.items():
        pool.apply_async(func=main, args=(k, v))
        time.sleep(3)

    pool.close()
    pool.join()
