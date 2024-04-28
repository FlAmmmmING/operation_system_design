# os 课设内容
import threading
import queue
import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures


# 这个是爬虫方法，解析网页内容
def craw(url):
    r = requests.get(url)
    # 返回文档内容
    return r.text.encode("utf-8")


# 这里是数据存储方法，解析需要的title
def parse(html):
    # class = "post-item-title"
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a', class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]


def single_thread(file):
    # 获取文件内容
    cnt = 0
    with open(file, 'r') as f:
        data = f.read().split("\n")
    for url in data:
        html = craw(url)
        results = parse(html)
        for result in results:
            print(result)
            print(cnt)
            cnt += 1
            with open('single_data.txt', 'a', encoding='utf-8') as f:
                for item in result:
                    f.write(str(item) + '\n')


if __name__ == '__main__':
    start = time.time()
    single_thread("data.txt")
    end = time.time()
    print(f"cost:{end - start}")
