import queue
import random
import requests
import time
import threading
from bs4 import BeautifulSoup

# 要爬取的网页集合
urls = [
    f"https://www.cnblogs.com/sitehome/p/{page}"
    for page in range(1, 101)
]

# 特殊值，用于指示消费者线程停止运行
STOP_SIGNAL = object()

# 创建互斥锁
write_lock = threading.Lock()


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


# 生产者
def do_craw(url_queue: queue.Queue, html_queue: queue.Queue):
    while True:
        url = url_queue.get()
        if url is STOP_SIGNAL:  # 如果接收到停止信号，结束循环
            html_queue.put(STOP_SIGNAL)  # 发送停止信号给消费者线程
            break
        html = craw(url)
        html_queue.put(html)
        print(threading.current_thread().name, f"craw {url}",
              f"url_queue.size=", url_queue.qsize())
        # time.sleep(random.randint(1, 2))


# 消费者
def do_parse(html_queue: queue.Queue, fout):
    while True:
        html = html_queue.get()
        if html is STOP_SIGNAL:  # 如果接收到停止信号，结束循环
            break
        results = parse(html)
        # 使用互斥锁确保写入操作的原子性
        with write_lock:
            for result in results:
                fout.write(f"{result}\n")
        print(threading.current_thread().name, f"results.size={len(results)}",
              f"html_queue.size=", html_queue.qsize())
        # time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    for url in urls:
        url_queue.put(url)

    # 多线程-生产者
    craw_threads = []
    for idx in range(3):
        t = threading.Thread(target=do_craw, args=(url_queue, html_queue),
                             name=f"craw_idx = {idx}")
        t.start()
        craw_threads.append(t)

    # 消费者
    fout = open("data.txt", "w")
    parse_threads = []
    for idx in range(2):
        t = threading.Thread(target=do_parse, args=(html_queue, fout),
                             name=f"parse_idx = {idx}")
        t.start()
        parse_threads.append(t)

    # 等待所有生产者线程结束
    for t in craw_threads:
        t.join()

    # 等待所有消费者线程结束
    for t in parse_threads:
        t.join()

    fout.close()
