import requests as rts
import os
import xml.etree.ElementTree as ET

catalog_url = "http://apis.juhe.cn/goodbook/catalog"

pams = {
    "key": "04a5da146132d587bf50b9b2f7cdca88",
    "dtype": "xml"
}

catalog_path = "cache/catalog.xml"

# 建立缓存机制(若文件不存在，下载保存，若存在，直接加载)

if not (os.path.exists(catalog_path)):
    print("网络加载")
    resp = rts.request("post", catalog_url, data=pams)
    with open(catalog_path, "w", encoding="utf-8") as f:
        f.write(resp.text)

print("本地缓存加载")

catalog_et = ET.ElementTree(file=catalog_path)

catalog_root_ele = catalog_et.getroot()

print(catalog_root_ele)

if catalog_root_ele.find("resultcode").text == "200":
    print("目录加载成功")
else:
    print("目录加载失败，程序退出")

catalogs = catalog_root_ele.iter("item")

print(catalogs)

for cl in catalogs:
    cl_id = cl.find("id").text
    cl_text = cl.find("catalog").text
    print(cl_id, cl_text)


