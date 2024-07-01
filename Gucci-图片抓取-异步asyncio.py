import asyncio
import time
import json
import aiohttp
import os

# 创建保存图片的目录
os.makedirs('images', exist_ok=True)


async def fetch_image(session, url, idx, pdt_p):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                file_path = "{path}\\{idx}.jpg".format(path=pdt_p, idx=idx)
                print(file_path)
                with open(file_path, 'wb') as f:
                    f.write(content)
                print(f'成功下载 {url} 到 {file_path}')
            else:
                print(f'下载 {url} 失败，状态码 {response.status}')
    except Exception as e:
        print(f'下载 {url} 时出错: {e}')


async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, url, idx, pdt_p) for pdt_p, idx, url in urls]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    s = time.time()

    # 获取当前工作目录
    url_dict = dict()  # json转换的字典
    urls = []  # 存放 SKU路径、图片编号、url地址

    # 获取当前py文件目录
    current_path = os.getcwd()
    dir_list = os.listdir(current_path)

    # 遍历当前目录的项目，判断是否为文件夹
    for d in dir_list:
        d_path = os.path.join(current_path, d)
        print(d_path)
        if os.path.isdir(d_path):
            json_path = os.path.join(d_path, "sku_url.json")
            # 检查文件夹内的json文件是否存在
            if os.path.isfile(json_path):
                with open(json_path, "r", encoding="utf-8") as f_sku_url:
                    url_dict = json.load(f_sku_url)

                # 路径./大类/SKU/图片名称
                for k_sku_url, v_pict_url in url_dict.items():
                    code_begin = k_sku_url.find("pr/")
                    code_end = k_sku_url.find("?url")
                    pdt_code = k_sku_url[code_begin + 3:code_end]

                    pdt_path = d_path + "\\" + pdt_code
                    for i in range(len(v_pict_url)):
                        urls.append([pdt_path, i, v_pict_url[i]])
        else:
            pass

    asyncio.run(main(urls))
    e = time.time()
    print(e-s)
