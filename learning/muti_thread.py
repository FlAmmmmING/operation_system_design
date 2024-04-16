# 这个是多线程爬虫程序

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
    print(url, len(url))


# 多线程爬虫开始
def mutli_thread():
    start = time.time()
    print("mutli thread started")
    threads = []
    for url in urls:
        threads.append(
            threading.Thread(target=craw, args=(url,))
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("mutli thread end")
    end = time.time()
    print(f"mutli thread time is {end - start}")


if __name__ == '__main__':
    mutli_thread()
