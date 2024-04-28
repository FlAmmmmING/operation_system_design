# 我需要爬取的是这个博客园的信息
urls = [
    f"https://www.cnblogs.com/sitehome/p/{page}"
    for page in range(1, 101)
]

data = open("../data.txt", "w")
for url in urls:
    data.write(url + "\n")
