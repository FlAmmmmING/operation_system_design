# 线程池并发执行
import concurrent.futures
from bs4 import BeautifulSoup
import queue
import random
import requests
import time
import threading

# 要爬取的网页集合
urls = [
    f"https://www.cnblogs.com/sitehome/p/{page}"
    for page in range(1, 101)
]


# 爬虫
def craw(url):
    r = requests.get(url)
    return r.text


# 解析
# 获取网页的每一个文章标题
def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="post-item-title")
    return [(link['href'], link.get_text()) for link in links]


# 线程池 craw
with concurrent.futures.ThreadPoolExecutor() as pool:
    htmls = pool.map(craw, urls)
    htmls = list(zip(urls, htmls))
    for url, html in htmls:
        print(url, len(html))

print("craw finished")

# 线程池 parse
with concurrent.futures.ThreadPoolExecutor() as pool:
    futures = {}
    for url, html in htmls:
        future = pool.submit(parse, html)
        futures[future] = url

    for future, url in futures.items():
        print(url, "\n", future.result())
