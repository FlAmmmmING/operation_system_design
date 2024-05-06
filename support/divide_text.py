# # 分割文本，按照每10个网页分割
#
# def divided_data(start, end, data):
#     """
#     :param start: 开始idx
#     :param end: 结束idx
#     :param data: 目标文本
#     :param id: 线程号
#     :return: 返回分割文本，是数组
#     """
#     ret_data = []
#     max_length = len(data)
#     for i in range(start, min(end, max_length)):
#         ret_data.append(data[i])
#     return ret_data
#
#
# def divide_text():
#     # 这里的data存储的就是全部的文本内容
#     with open("data_cnblog.txt", "r") as f:
#         data = f.read().split(",\n")
#     f.close()
#     print(len(data))
#     for i in range(0, 10):
#         now_data = divided_data(i * 10, (i + 1) * 10, data)
#         print(now_data)
#     # 开始多线程分割
#     # 为了防止重复读，这里需要互斥
#
# if __name__ == '__main__':
#     divide_text()


import threading


class FileSplitter:
    def __init__(self, filename, num_threads):
        self.filename = filename
        self.num_threads = num_threads
        self.lock = threading.Lock()

    def split_file(self):
        with open(self.filename, 'r') as f:
            content = f.read().split('\n')

        file_length = len(content)
        chunk_size = file_length // self.num_threads
        threads = []

        for i in range(self.num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < self.num_threads - 1 else file_length
            thread = threading.Thread(target=self.write_chunk, args=(content[start:end],))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def write_chunk(self, chunk):
        with self.lock:
            with open(f"divided_data/{threading.current_thread().name}_chunk.txt", 'w') as f:
                f.write(chunk)


def main():
    filename = '../data_url/data_cnblog.txt'  # 要分割的文件名
    num_threads = 10  # 线程数量
    splitter = FileSplitter(filename, num_threads)
    splitter.split_file()


if __name__ == "__main__":
    main()
