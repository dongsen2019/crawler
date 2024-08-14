url = "https://assets.burberry.cn/is/image/Burberryltd/37602101-FFE9-4BE0-99AD-AEC017DA9D4E?$BBY_V3_SL_1$&wid=400&hei=400, https://assets.burberry.cn/is/image/Burberryltd/37602101-FFE9-4BE0-99AD-AEC017DA9D4E?$BBY_V3_SL_1$&wid=800&hei=800 2x"

print(url[url.rfind("http"):url.rfind(" ")])

url = "https://www.burberry.cn/small-check-shoulder-bag-p80946781"

print(url[url.rfind("p"):])

url = ["女士包款", "sdadk"]
if url[0] != "女士包款" and url[0] != "全部围巾":
    print("1")
else:
    print("2")

print(100 % 100)