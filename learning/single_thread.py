# 这个是单线程爬虫程序
# 用来与多线程爬虫做对比的
import requests
import time

# 要爬取的网页集合
urls = [
    f"https://www.cnblogs.com/sitehome/p/{page}"
    for page in range(1, 101)
]


def craw(url):
    r = requests.get(url)
    print(url, len(r.text))


# 单线程爬取
def single_thread():
    for url in urls:
        craw(url)

# craw(urls[10])


if __name__ == '__main__':
    start = time.time()
    single_thread()
    end = time.time()
    # print(end - start)
    print(f"single thread is {end - start}")
