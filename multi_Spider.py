# os 课设内容
import os
import threading
import queue
import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures
import dividing
import imitate_spider
import csv
from datetime import datetime

import csv
from datetime import datetime


def write_thread_times_to_csv(thread_times, URL_Number, Size, save_name="thread_times.csv"):
    """
    将 thread_times 中的数据按照 Thread ID 的阿拉伯数字排序后写入 CSV 文件
    """
    # 按照 Thread ID 的阿拉伯数字排序 thread_times
    sorted_thread_times = dict(sorted(thread_times.items(), key=lambda x: int(x[0])))

    with open(save_name, 'w', newline='') as csvfile:
        fieldnames = ['Thread ID', 'Start Time', 'End Time', 'Duration (s)', 'URL Number', 'URL Total Size (KB)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for filename, data in sorted_thread_times.items():
            start_time_local = datetime.fromtimestamp(data['Start Time']).strftime('%H:%M:%S.%f')[:-3]
            end_time_local = datetime.fromtimestamp(data['End Time']).strftime('%H:%M:%S.%f')[:-3]
            duration = "{:.3f}".format(data['End Time'] - data['Start Time'])
            idx = int(filename)
            writer.writerow({'Thread ID': "T" + filename, 'Start Time': start_time_local,
                             'End Time': end_time_local, 'Duration (s)': duration,
                             'URL Number': URL_Number[idx], 'URL Total Size (KB)': Size[idx]})


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
    try:
        r = requests.get(url)
        # 返回文档内容
        return r.text.encode("utf-8")
    except:
        return None


# 这里是数据存储方法，解析需要的title
# def parse(html):
#     # class = "post-item-title"
#     soup = BeautifulSoup(html, "html.parser")
#     links = soup.find_all('a', class_="post-item-title")
#     return [(link["href"], link.get_text()) for link in links]
def parse(html):
    if html == "this is imitation for spider":
        return html
    # class = "post-item-title"
    soup = BeautifulSoup(html, "html.parser")
    # links = soup.find_all('a', class_="post-item-title")
    links = soup.find('span', {'role': 'heading', 'aria-level': '2'})
    # return [(link["href"], link.get_text()) for link in links]
    return links.get_text()


class Crawler:
    fail_time = 0
    ret_text = []  # 返回的文本

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
        self.mutex4 = threading.Lock()
        self.terminate_signal = threading.Event()
        self.time = 0
        # 线程开始时间和结束时间的计算，最后将这个线程的时间放入csv中
        self.thread_start_times = {}
        self.thread_end_times = {}

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

            # 当需要测试的时候就用这个
            # html = imitate_spider.imitate_spider(url)

            self.data_queue.put(html)
            # print(self.data_queue.qsize())
            # print("data_queue size: ", self.data_queue.qsize())
            # print(threading.current_thread().name, f"craw {url}",
            #       "url_queue size: ", self.url_queue.qsize())
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
                    self.mutex2.acquire()  # 重新获取互斥锁，进入临界 区
                # 如果收到了终止信号并且队列为空，则退出循环
                if self.terminate_signal.is_set() and self.data_queue.empty():
                    break
                # 从队列中获取数据进行处理
                html = self.data_queue.get()
            if html is not None:
                results = parse(html)
                # for result in results:
                with self.mutex3:
                    Crawler.ret_text.append(str(results))
                    with open("result_data.txt", "a", encoding="utf-8") as f:
                        # for item in result:
                        f.write(str(results) + '\n')
                    print(results)
                # print(threading.current_thread().name, f"results size ", len(results),
                #       "data_queue size: ", self.data_queue.qsize())
            else:
                print("爬取失败")
                with self.mutex4:
                    # 互斥访问静态变量
                    Crawler.fail_time += 1

    def thread_start(self):
        """
            子线程中的内容并行开始
        """
        # 在这里记录时间
        self.thread_start_times = time.time()
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

        # 如果还有剩余
        while self.data_queue.qsize() > 0:
            html = self.data_queue.get()
            if html is None:
                Crawler.fail_time += 1
                print("爬取失败")
                continue
            results = parse(html)
            Crawler.ret_text.append(str(results))
            # for result in results:
            with open("result_data.txt", "a", encoding="utf-8") as f:
                # for item in result:
                f.write(str(results) + '\n')
                print(results)
            # print(threading.current_thread().name, f"results size ", len(results),
            #       "data_queue size: ", self.data_queue.qsize())
        # 这里是结束时间
        self.thread_end_times = time.time()

        # 返回开始时间与结束时间
        return self.thread_start_times, self.thread_end_times

    def print_url_queue(self):
        """
            查看当前变量状态: url_queue
        """
        print(self.url_queue.qsize())
        for url in QueueIterator(self.url_queue):
            print(url)


def multi_thread_start(folder, n1, n2, number=10, minimum=1, maximum=500):
    """
    对分割的文本进行多线程
    :param folder: 文件夹
    :param n1: 爬虫线程
    :param n2: 解析线程
    :param number: 文本分割大小
    :param dataset: 数据大小
    :param minimum: From
    :param maximum: To
    """
    # 用于存储每个 crawler.thread_start 的开始时间和结束时间，任务量以及任务大小
    thread_times = {}
    start = time.time()

    # dividing.dividing("data_url/temp_data.txt", number, dataset)
    URL_Number, Size = dividing.dividing_released(number, minimum, maximum)
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(number * 1.5)) as executor:
        for i in range(number):
            filename = f"{folder}/chunk_{i}.txt"
            crawler = Crawler(n1, n2, filename)
            crawler.read_urls_from_file()

            # 提交任务到线程池，返回 Future 对象
            future = executor.submit(crawler.thread_start)

            # 使用 add_done_callback() 方法在线程结束时记录结束时间和返回值
            def record_end_time_and_result(fut, fn=filename.split('/')[1].split('.')[0].split('_')[1]):
                nonlocal thread_times
                start_time, end_time = fut.result()  # 获取线程函数的返回值
                thread_times[fn] = {'Start Time': start_time, 'End Time': end_time}

            future.add_done_callback(record_end_time_and_result)

    print(thread_times)
    # 将数据写入 CSV 文件
    write_thread_times_to_csv(thread_times, URL_Number, Size)
    end = time.time()

    ret = Crawler.fail_time
    text = Crawler.ret_text
    Crawler.fail_time = 0
    Crawler.ret_text = []
    # 返回差错时间以及文本
    return text, round(end - start, 4)


def multi_thread_setting(number, n1, n2, dataset=1000):
    """

    :param dataset: 数据集大小
    :param n1: 爬虫线程通道
    :param n2: 数据获取线程通道
    :param number: 文本分割大小
    :return: 返回花费的时间、爬取失败的次数
    """
    with open('result_data.txt', 'r+') as f:
        f.truncate(0)
    for item in os.listdir("divided_data"):
        os.remove(os.path.join("divided_data", item))
    start = time.time()
    text, total_time = multi_thread_start("divided_data", n1, n2, number, dataset)
    end = time.time()
    print(f"cost: {end - start:.2f}")
    return text, round(end - start, 4)


def multi_Spider(inputed_url, text_number, n1, n2):
    with open("data_url/temp_data.txt", 'w') as f:
        f.write(inputed_url)
    # 打开文件并读取内容
    with open("data_url/temp_data.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 去除空行并重写文件
    with open("data_url/temp_data.txt", 'w', encoding='utf-8') as file:
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        file.write('\n'.join(non_empty_lines))
    text, total_time = multi_thread_setting(text_number, n1, n2, len(non_empty_lines))
    return text, total_time


def data_1000_n1_10_n2_10_number(looptime):
    """
    这里规定数据量是 1000， n1 是 10，n2 是 10
    :param looptime: 实验次数
    """
    # 这里设置通道大小
    n1 = 5
    n2 = 5
    # 这里设置数据量大小
    dataset = 100
    # 这里设置几个分割参量
    # split_reference = [10, 20, 50, 100]
    split_reference = [10]
    # 测试几次
    cnt = 1
    while cnt <= looptime:
        for splits in split_reference:
            text, time_consumption = multi_thread_setting(dataset, n1, n2, splits)
            # with open(f"experiment_result/text_number/data_{dataset}_n1_{n1}_n2_{n2}_number/time_consumption.csv",
            #           'a') as f:
            #     if splits == 100:
            #         f.write(str(time_consumption) + "\n")
            #     else:
            #         f.write(str(time_consumption) + ",")
            # f.close()
            # with open(f"experiment_result/text_number/data_{dataset}_n1_{n1}_n2_{n2}_number/fail_rate.csv", 'a') as f:
            #     if splits == 100:
            #         f.write(str(fail_cnt / dataset) + "\n")
            #     else:
            #         f.write(str(fail_cnt / dataset) + ",")
            # f.close()
        cnt += 1


if __name__ == '__main__':
    """
    数据量
    测试次数
    爬虫通道
    获取通道
    文本分割数量（建议是数据量的整数倍）
    """

    # 实验分割对于爬虫时间以及爬取成功率的影响
    data_1000_n1_10_n2_10_number(1)
