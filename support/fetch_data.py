import threading
import queue
import requests
import time
from bs4 import BeautifulSoup


# 两个全局变量

class Crawler:
    def __init__(self, filename, data_queue):
        self.filename = filename
        self.urls_queue = queue.Queue()
        self.data_queue = data_queue

    def read_urls_from_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                url = line.strip()
                # print(url)
                self.data_queue.put(url)

    def crawl(self):
        while not self.urls_queue.empty():
            url = self.urls_queue.get()
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # 将爬取到的数据放入数据队列
                    self.data_queue.put(response.text)
                    print(f"Successfully crawled {url}")
                else:
                    print(f"Failed to crawl {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Failed to crawl {url}. Error: {str(e)}")


def parse_data(data_queue, crawler_threads):
    while True:
        print(data_queue.qsize())
        data = data_queue.get()
        # 检查数据是否为 None 并且所有爬虫线程是否已经完成
        if data is None and all(not thread.is_alive() for thread in crawler_threads):
            break
        # 在这里编写解析数据的代码
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('a', class_="post-item-title")
        print([(link["href"], link.get_text()) for link in links])
        print("Parsing data:", data)


def main():
    filenames = ['chunk_0.txt']  # 存储网页链接的txt文件列表
    data_queue = queue.Queue()

    # 创建爬虫线程
    crawler_threads = []
    for filename in filenames:
        crawler = Crawler(filename, data_queue)
        crawler_thread = threading.Thread(target=crawler.read_urls_from_file)
        crawler_threads.append(crawler_thread)
        crawler_thread.start()

    # 等待所有爬虫线程结束
    for thread in crawler_threads:
        thread.join()
    print(crawler.urls_queue)
    #
    # # 创建解析数据的线程并启动
    # parser_threads = []
    # for _ in range(5):  # 假设有5个解析数据的线程
    #     parser_thread = threading.Thread(target=parse_data, args=(data_queue, crawler_threads))
    #     parser_threads.append(parser_thread)
    #     parser_thread.start()
    #
    # # 等待所有解析数据的线程结束
    # for thread in parser_threads:
    #     thread.join()
    #
    # # 添加退出标志到队列，使解析数据的线程可以退出
    # for _ in range(len(parser_threads)):
    #     data_queue.put(None)


if __name__ == "__main__":
    main()
