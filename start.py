# os 课设内容
import threading
import queue
import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures
import dividing

class QueueIterator:
    def __init__(self, q):
        self.queue = q

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue.empty():
            raise StopIteration
        else:
            return self.queue.get()


# 这个是爬虫方法，解析网页内容
def craw(url):
    r = requests.get(url)
    # 返回文档内容
    return r.text.encode("utf-8")


# 这里是数据存储方法，解析需要的title
# def parse(html):
#     # class = "post-item-title"
#     soup = BeautifulSoup(html, "html.parser")
#     links = soup.find_all('a', class_="post-item-title")
#     return [(link["href"], link.get_text()) for link in links]
def parse(html):
    # class = "post-item-title"
    soup = BeautifulSoup(html, "html.parser")
    # links = soup.find_all('a', class_="post-item-title")
    links = soup.find('span', {'role': 'heading', 'aria-level': '2'})
    # return [(link["href"], link.get_text()) for link in links]
    return links.get_text()


class Crawler:

    def __init__(self, number1, number2, txt):
        """
        一个子线程
        :param number1: 线程数量1
        :param number2: 线程数量2
        :param txt: 文本
        """
        # 一个是存储网页链接的
        # 一个是存储网页内容的
        self.url_queue = queue.Queue()
        self.data_queue = queue.Queue()
        self.n1 = number1
        self.n2 = number2
        self.filename = txt
        # 互斥锁保护线程
        self.mutex1 = threading.Lock()
        self.mutex2 = threading.Lock()
        self.mutex3 = threading.Lock()
        self.terminate_signal = threading.Event()
        self.time = 0

    def read_urls_from_file(self):
        """
            读取分割完毕的文本数据
        """
        with open(self.filename, "r") as f:
            for line in f:
                url = line.strip()
                self.url_queue.put(url)

    def do_craw(self):
        """
            基于url_queue爬取网页内容，这里多线程并发，大小是n1
        """
        while True:
            has_url = False
            url = None
            with self.mutex1:
                if not self.url_queue.empty():
                    url = self.url_queue.get()
                    has_url = True
            if not has_url or url is None:
                break
            html = craw(url)
            self.data_queue.put(html)
            print(self.data_queue.qsize())
            # print("data_queue size: ", self.data_queue.qsize())
            print(threading.current_thread().name, f"craw {url}",
                  "url_queue size: ", self.url_queue.qsize())
        # 发送终止信号
        self.terminate_signal.set()

    def do_parse(self):
        # while True:
        #     # 终止信号
        #     if self.terminate_signal.is_set():
        #         break
        #     has_data = False
        #     html = None
        #     # 互斥保证线程安全
        #     with self.mutex2:
        #         if not self.data_queue.empty():
        #             html = self.data_queue.get()
        #             print(html)
        #             has_data = True
        #     if not has_data and self.url_queue.empty() or html is None:
        #         break
        #     results = parse(html)
        #     for result in results:
        #         print(result)
        #     print(threading.current_thread().name, f"results size ", len(results),
        #           "data_queue size: ", self.data_queue.qsize())
        while True:
            # 互斥保证线程安全
            with self.mutex2:
                while self.data_queue.empty() and not self.terminate_signal.is_set():
                    # 等待数据的到来或者收到终止信号
                    self.mutex2.release()  # 释放互斥锁，允许其他线程进入临界区
                    self.terminate_signal.wait(timeout=1)  # 等待1秒，期间可以被终止信号唤醒
                    self.mutex2.acquire()  # 重新获取互斥锁，进入临界区
                # 如果收到了终止信号并且队列为空，则退出循环
                if self.terminate_signal.is_set() and self.data_queue.empty():
                    break
                # 从队列中获取数据进行处理
                html = self.data_queue.get()
            if html is not None:
                results = parse(html)
                # for result in results:
                with self.mutex3:
                    with open("result.txt", "a", encoding="utf-8") as f:
                        # for item in result:
                            f.write(str(results) + '\n')
                    print(results)
                print(threading.current_thread().name, f"results size ", len(results),
                      "data_queue size: ", self.data_queue.qsize())

    def thread_start(self):
        """
            子线程中的内容并行开始
        """
        threading_queue1 = []
        threading_queue2 = []
        for idx in range(self.n1):
            thread = threading.Thread(target=self.do_craw,
                                      name=f"craw{idx}_{self.filename}", args=())
            threading_queue1.append(thread)
            thread.start()

        for idx in range(self.n2):
            thread = threading.Thread(target=self.do_parse,
                                      name=f"parse{idx}_{self.filename}", args=())
            threading_queue2.append(thread)
            thread.start()

        for thread in threading_queue1:
            thread.join()

        for thread in threading_queue2:
            thread.join()

        while self.data_queue.qsize() > 0:
            html = self.data_queue.get()
            results = parse(html)
            # for result in results:
            with open("result.txt", "a", encoding="utf-8") as f:
                # for item in result:
                f.write(str(results) + '\n')
                print(results)
            # print(threading.current_thread().name, f"results size ", len(results),
            #       "data_queue size: ", self.data_queue.qsize())

    def print_url_queue(self):
        """
            查看当前变量状态: url_queue
        """
        print(self.url_queue.qsize())
        for url in QueueIterator(self.url_queue):
            print(url)


def multi_thread_start(number, folder, n1, n2, dividing_number=10):
    """
        对分割的文本进行多线程
        :param number: 有多少分割文本
        :param folder: 文件夹
        :param n1: 爬虫线程
        :param n2: 解析线程
        :param dividing_number: 文本分割大小
    """
    dividing.dividing("url_data.txt", dividing_number)
    with concurrent.futures.ThreadPoolExecutor(max_workers=number * 1.2) as executor:
        for i in range(number):
            filename = f"{folder}/chunk_{i}.txt"
            crawler = Crawler(n1, n2, filename)
            crawler.read_urls_from_file()
            executor.submit(crawler.thread_start)


if __name__ == '__main__':
    with open('result.txt', 'r+') as f:
        f.truncate(0)
    start = time.time()
    multi_thread_start(10, "divided_data", 10, 10, 40)
    end = time.time()
    print(f"cost: {end - start}")
