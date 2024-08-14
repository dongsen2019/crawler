import json
import time
import requests
import threading
import multiprocessing
from tenacity import retry, stop_after_attempt, wait_fixed

s = ["218.95.37.11:25002","221.227.143.110:19700","122.232.66.153:15931","218.95.37.135:40394","221.229.212.173:25098","221.229.212.170:40137","218.95.37.135:40234","221.229.212.170:40617","218.95.37.135:40456","219.150.218.21:25002","221.131.165.73:27175","223.113.54.130:27214","125.105.224.181:16042","119.102.41.8:22312","218.95.37.135:40154","122.232.236.58:20892","218.95.37.135:40089","219.150.218.53:40190","221.131.165.73:27160","218.95.37.135:40194"]


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def picture_write(num, url, w_path, n):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    proxy = {
        "https": "http://d3392397682:ebxl5k5p@{ip}".format(ip=s[n])
    }
    resp = requests.get(url, headers=headers, proxies=proxy, timeout=(5, 14))

    if resp.status_code == 200:
        pic_path = w_path + "/" + str(num) + ".jpg"
        with open(pic_path, "wb") as f_pic:
            f_pic.write(resp.content)


def picture_requests(cls, url_json_path):
    time_s = time.time()
    # 加载sku_url.json
    url_dict = dict()
    with open(url_json_path, "r", encoding="utf-8") as f_sku_url:
        url_dict = json.load(f_sku_url)

    print(url_dict)

    # pool = multiprocessing.Pool(16)
    n = 0
    # 路径./大类/SKU/图片名称
    for k_sku_url, v_pict_url in url_dict.items():
        code_begin = k_sku_url.find("pr/")
        code_end = k_sku_url.find("?url")
        pdt_code = k_sku_url[code_begin + 3:code_end]

        pdt_path = "./"+cls+"/"+pdt_code
        print(pdt_path)

        for i in range(len(v_pict_url)):
            # 当并发一轮以后，睡眠3秒
            if n % 10 == 9:
                time.sleep(3)
            ix = n % 20

            # pool.apply_async(func=picture_write, args=(i, v_pict_url[i], pdt_path, ix))
            t = threading.Thread(target=picture_write, args=(i, v_pict_url[i], pdt_path, ix))
            t.daemon = False
            t.start()
            n = n + 1

    time_e = time.time()
    print(time_e - time_s)


if __name__ == '__main__':
    picture_requests("女士皮包小皮件", "./女士皮包小皮件/sku_url.json")


