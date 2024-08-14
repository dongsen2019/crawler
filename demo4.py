import requests as rts
import os
import xml.etree.ElementTree as ET
from io import StringIO

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

print(catalog_et)

if catalog_et.find("resultcode").text == "200":
    print("目录加载成功")
else:
    print("目录加载失败，程序退出")

# catalogs = catalog_et.find("result").findall("item")

catalogs = catalog_et.iter('item')
print(catalogs)

for cl in catalogs:
    cl_id = cl.find("id").text
    cl_text = cl.find("catalog").text
    print(cl_id, cl_text)


# 2.用户输入一个分类的ID, 发送一个网络请求，获取图书详情页
catalog_id = input("请输入需要查询的分类id: ")

catalog_url = "http://apis.juhe.cn/goodbook/query?key={}&catalog_id={}&pn=1&rn=15&dtype=xml"\
    .format(pams["key"], catalog_id)

print(catalog_url)

content_resp = rts.get(catalog_url)

book_detail_file = StringIO(content_resp.text)

book_detail_et = ET.ElementTree(file=book_detail_file)
items = book_detail_et.find("result").find("data").findall("item")

print(items)

book_catalog_temp = """
<a href="{}">
    <img src="{}" alt="xxx">
    <h4>{}</h4>
</a>

"""

book_catalog_str = ""

for item in items:

    keys = ["img", "title", "catalog", "tags", "sub1", "sub2", "bytime"]

    with open("book_detail.html", "r", encoding="utf-8") as file_template, \
         open("book_catalog_detail/{}.html".format(item.find("title").text), "w", encoding="utf-8") as file:
        str_ftp = file_template.read()
        for k in keys:

            str_ftp = str_ftp.replace("{{" + k + "}}", item.find(k).text)

        file.write(str_ftp)


    book_catalog_str += book_catalog_temp.format("{}.html".format(item.find("title").text), item.find("img").text, item.find("title").text)

with open("book_catalog.html", "r", encoding="utf-8") as f, \
     open("book_catalog_detail/book_catalog_html.html", "w", encoding="utf-8") as f_html:
    book_catalog_file = f.read()
    f_html.write(book_catalog_file.replace("{{catalog_content}}", book_catalog_str))















