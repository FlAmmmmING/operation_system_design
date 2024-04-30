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
    # links = soup.find_all('a', class_="post-item-title")
    links = soup.find('span', {'role': 'heading', 'aria-level': '2'})
    # return [(link["href"], link.get_text()) for link in links]
    return links.get_text()


def single_thread(file):
    # 获取文件内容
    cnt = 0
    with open(file, 'r') as f:
        data = f.read().split("\n")
    for url in data:
        html = craw(url)
        results = parse(html)
        # for result in results:
        #     print(result)
        #     # with open("url_data.txt", "a", encoding='utf-8') as f:
        #     #     f.write(str(result[0]) + "\n")
        #     print(cnt)
        #     cnt += 1
        cnt += 1
        print(results)
        print(cnt)
        with open('single_data.txt', 'a', encoding='utf-8') as f:
                f.write(str(results) + '\n')


if __name__ == '__main__':
    with open('single_data.txt', 'r+') as f:
        f.truncate(0)
    start = time.time()
    single_thread("url_data.txt")
    end = time.time()
    print(f"cost:{end - start}")
