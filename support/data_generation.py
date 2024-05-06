# 我需要爬取的是这个博客园的信息
urls = [
    f"https://www.zhihu.com/people/jerrywang_sap/posts?page={page}"
    for page in range(1, 201)
]

data = open("../data_url/zhihu_url.txt", "w")
for url in urls:
    data.write(url + "\n")
