import requests
from bs4 import BeautifulSoup


# 这个是爬虫方法
def craw(url):
    r = requests.get(url)
    # 返回文档内容
    return r.text.encode("utf-8")


# 这里是数据存储方法
def parse(html):
    # class = "post-item-title"
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a', class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]
