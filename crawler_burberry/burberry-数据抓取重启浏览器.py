from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os
import json
import pandas as pd
import multiprocessing

crawler_urls = {
    "女士成衣": "https://www.burberry.cn/womens-clothing/",
    "女士包款": "https://www.burberry.cn/womens-bags/",
    "女士鞋履": "https://www.burberry.cn/womens-shoes/",
    "全部围巾": "https://www.burberry.cn/l/scarves/"
}

sku_picture_url = dict()  # 全局变量


def create_driver(*url):
    driver = webdriver.Chrome()

    # driver.get("https://www.burberry.cn/womens-clothing/")
    driver.get(url[1])

    time.sleep(8)

    accept_xpath = "//div/button[@id = 'onetrust-accept-btn-handler']"
    ele_accept = driver.find_element(By.XPATH, accept_xpath)

    ActionChains(driver).move_to_element(ele_accept).click(ele_accept).perform()

    time.sleep(1)

    print(url[0], url[1])

    # 创建大类文件夹
    class_path = "./" + url[0]
    make_class_dir(class_path)

    # 定义浏览更多按钮的xpath路径
    browse_more_xpath = "//button[@aria-label='浏览更多商品']//span[text()='浏览更多']"

    # 定义页面尾部文本的xpath路径
    trail_text_xpath = "//p[@class ='css-m9vibb eacud820']"

    browse_more_locator = (By.XPATH, browse_more_xpath)

    trail_text_locator = (By.XPATH, trail_text_xpath)

    pos_a = {"x": 0, "y": 0}
    pos_b = {"x": 0, "y": 1}

    # 当滚动前与滚动后的尾部文本y坐标不相同时，继续循环滚动
    while pos_b["y"] != pos_a["y"]:
        pos_a["x"] = pos_b["x"]
        pos_a["y"] = pos_b["y"]

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(trail_text_locator))

        trail_text_ele = driver.find_element(By.XPATH, trail_text_xpath)
        ActionChains(driver).scroll_to_element(trail_text_ele).perform()
        time.sleep(5)

        # 由于需要多次滚动到尾部文本，才能展示出浏览更多的按钮
        y1 = 0
        y2 = 1
        while y2 != y1:
            y1 = trail_text_ele.location["y"]
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(trail_text_locator))
            trail_text_ele = driver.find_element(By.XPATH, trail_text_xpath)
            ActionChains(driver).scroll_to_element(trail_text_ele).perform()
            print(trail_text_ele.location)
            time.sleep(5)
            y2 = trail_text_ele.location["y"]

        # 记录滚动后的尾部文本的y坐标值
        pos_b["x"] = trail_text_ele.location["x"]
        pos_b["y"] = trail_text_ele.location["y"]

        # 判断是否出现了浏览更多按钮，如果没有出现则说已经加载全部商品
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(browse_more_locator))
        except TimeoutException:
            break

        browse_more_ele = driver.find_element(By.XPATH, browse_more_xpath)

        ActionChains(driver).move_to_element(browse_more_ele).click(browse_more_ele).perform()

        time.sleep(1)

    return driver


# 创建大类名称文件夹
def make_class_dir(cls_path):
    if not os.path.exists(cls_path):
        os.mkdir(cls_path)

# 创建文件夹，以款号(SKU)为文件夹名称，并写入SKU商品介绍txt
def make_sku_dir(dir_path, js_context, gg_context):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(dir_path+"/introduce.txt", "w", encoding="utf-8") as f_introduce:
        f_introduce.write(js_context)
        f_introduce.write("\n")
        f_introduce.write(gg_context)


def main(*url):
    product_code = ""
    product_name = ""
    product_introduce = ""
    product_price = 0
    product_color = ""
    product_size = ""
    product_all = []

    driver = create_driver(url[0], url[1])

    # 获取所有商品的xpath路径，以备后续依次进入
    list_xpath = "//div[@class = 'product-listing-shelf__product-card-container']/div[@data-test='shelf-row']//a"

    list_elements = driver.find_elements(By.XPATH, list_xpath)

    print(list_elements)

    list_elements_counts = len(list_elements)

    print("{0}:{1}".format(driver.title, list_elements_counts))

    error_num = 0
    # 2.循环点击每一个商品链接，进入商品详情页面
    begin_time = time.time()

    for ele_i in range(1, len(list_elements)+1):
        print(ele_i)

        if ele_i % 100 == 0:
            driver.quit()

            driver = create_driver(url[0], url[1])

        list_xpath_i = "(//div[@class = 'product-listing-shelf__product-card-container']/div[@data-test='shelf-row']//a)[" + str(ele_i) + "]"

        nvcy_xpath = "//h1[text()='" + url[0] + "']"

        ele_nvcy = driver.find_element(By.XPATH, nvcy_xpath)

        ActionChains(driver).move_to_element(ele_nvcy).perform()

        time.sleep(1)

        # 获取当前循环的商品元素并点击进入详情页
        ele = driver.find_element(By.XPATH, list_xpath_i)
        print(list_xpath_i)

        ActionChains(driver).move_to_element(ele).click(ele).perform()

        # 定义各元素的xpath路径
        size_detail_xpath = "//div[@class = 'add-to-bag__text-wrapper'][text()='加入购物袋']"

        product_detail_name_xpath = "//div/div/h1[@class = 'product-info-panel__title css-183zbdt e19cbv3t0']/span[1]"

        product_detail_price_xpath = "//div/div/h1[@class = 'product-info-panel__title css-183zbdt e19cbv3t0']/following-sibling::*[1]"

        product_detail_color_xpath = "//div[@class='product-swatches-panel__description']/span"

        product_detail_size_xpath = "//div[@class = 'size-picker__radio-type-selector size-picker__radio-type-selector-column']/label"

        product_detail_jsgg_xpath = "//li[@data-test = 'productdetails']//div[@class = 'product-details-accordion__content']/ul/li"

        # 等待加入购物袋的button出现
        try:
            product_name_locator = (By.XPATH, product_detail_name_xpath)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located(product_name_locator))
            time.sleep(2)

            print("操作1")

            # 获取商品名称
            product_detail_name = driver.find_element(By.XPATH, product_detail_name_xpath)
            product_name = product_detail_name.text
            print(product_name)
        except NoSuchElementException:
            print("NoSuchElementException", driver.current_url)
            error_num += 1

            action_back = ActionBuilder(driver)
            action_back.pointer_action.pointer_down(MouseButton.BACK)
            action_back.pointer_action.pointer_up(MouseButton.BACK)
            action_back.perform()

            continue
        except TimeoutException:
            print("TimeoutException", driver.current_url)
            error_num += 1

            action_back = ActionBuilder(driver)
            action_back.pointer_action.pointer_down(MouseButton.BACK)
            action_back.pointer_action.pointer_up(MouseButton.BACK)
            action_back.perform()

            continue

        # 获取详情页的价格
        product_detail_price = driver.find_element(By.XPATH, product_detail_price_xpath)
        product_price = float(product_detail_price.text[1:len(product_detail_price.text)+1].replace(",", ""))
        print(product_price)

        # 获取颜色
        product_detail_color = driver.find_element(By.XPATH, product_detail_color_xpath)
        product_color = product_detail_color.text
        print(product_color)

        print("操作2")

        # 获取商品介绍和规格
        product_detail_jsgg = driver.find_elements(By.XPATH, product_detail_jsgg_xpath)

        str_js = product_detail_jsgg[0].get_attribute("innerHTML")
        str_gg = ""
        for i in range(1, len(product_detail_jsgg)):
            str_gg += product_detail_jsgg[i].get_attribute("innerHTML")

        product_introduce = str_js + str_gg

        # 将商品介绍和商品规格写入txt文件中
        product_code = driver.current_url[driver.current_url.rfind("p")+1:]

        sku_path = "./" + url[0] + "/" + product_code
        print(sku_path)

        make_sku_dir(sku_path, str_js, str_gg)

        print("操作3")

        size_list = []
        # 获取商品尺寸信息，当遇到预订的链接是，则捕捉NoSuchElementException异常
        if url[0] != "女士包款" and url[0] != "全部围巾":
            try:
                # 点击购物袋按钮
                ele_size_button = driver.find_element(By.XPATH, size_detail_xpath)

                ActionChains(driver).move_to_element(ele_size_button).click(ele_size_button).perform()

                # 获取尺寸信息
                product_detail_size = driver.find_elements(By.XPATH, product_detail_size_xpath)
                for s_ele in product_detail_size:
                    size_list.append(s_ele.text)
                    print(s_ele.text)

            except NoSuchElementException:
                # 预订按钮的Xpath路径
                predetermine_xpath = "//div[@class = 'pre-order-button__button-title']/div"

                # 点击预定按钮
                ele_pre_button = driver.find_element(By.XPATH, predetermine_xpath)

                ActionChains(driver).move_to_element(ele_pre_button).click(ele_pre_button).perform()

                # 获取预订按钮的尺寸信息
                product_detail_size = driver.find_elements(By.XPATH, product_detail_size_xpath)
                for s_ele in product_detail_size:
                    size_list.append(s_ele.text)
                    print(s_ele.text)

        else:
            size_list.append("")

        print(size_list)

        for size_ele in size_list:
            product_all.append([product_code, product_name, product_introduce, product_price, product_color, size_ele])

        print("操作4")

        # 获取商品详情页的图片URL
        detail_img_xpath = "//picture[@class = 'desktop-product-gallery__image__picture']/source[@media = '(min-width:300px)']| " \
                           "//picture[@class = 'desktop-product-gallery__image__picture']/source[@media = '(min-width:300px)']"
        img_elements = driver.find_elements(By.XPATH, detail_img_xpath)
        print(img_elements)

        img_url_list = []
        for ele_img in img_elements:
            if ele_img.get_attribute("srcset") != "":
                src = ele_img.get_attribute("srcset")
                img_url_list.append(src[src.rfind("http"):src.rfind(" ")])
            else:
                src = ele_img.get_attribute("data-srcset")
                img_url_list.append(src[src.rfind("http"):src.rfind(" ")])

        product_url = driver.current_url
        sku_picture_url[product_url] = img_url_list

        # 准备页面后退
        time.sleep(1)

        # 一个商品采集数据完毕，页面后退操作
        action_back = ActionBuilder(driver)
        action_back.pointer_action.pointer_down(MouseButton.BACK)
        action_back.pointer_action.pointer_up(MouseButton.BACK)
        action_back.perform()

        time.sleep(1)

    end_time = time.time()
    print(end_time - begin_time)

    print(error_num)
    error_txt_path = "./" + url[0] + "/error.txt"
    with open(error_txt_path, "w", encoding="utf-8") as f_error:
        f_error.write(url[0])
        f_error.write(":")
        f_error.write(str(error_num))

    # 将sku_picture_url字典类型数据写入json文件
    sku_json_path = "./" + url[0] + "/sku_url.json"
    with open(sku_json_path, "w", encoding="utf-8") as f_url:
        json.dump(sku_picture_url, f_url)

    # 将商品属性数据写入Excel
    counts_list = len(product_all)
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

    driver.quit()

if __name__ == '__main__':
    pool = multiprocessing.Pool(16)
    for k, v in crawler_urls.items():
        pool.apply_async(func=main, args=(k, v))
        time.sleep(5)

    pool.close()
    pool.join()



