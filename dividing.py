import threading
import concurrent.futures
import csv


class FileSplitter:
    def __init__(self, num_threads, dataset=500, filename="data_url/temp_data.txt"):
        self.filename = filename
        self.num_threads = num_threads
        self.lock = threading.Lock()
        self.dataset = dataset

    def split_file(self):
        with open(self.filename, 'r') as f:
            content = f.read().split("\n")
            # print(content)

        file_length = min(self.dataset, len(content))
        chunk_size = file_length // self.num_threads
        chunks = [content[i:i + chunk_size] for i in range(0, file_length, chunk_size)]  # 分割内容

        threads = []
        # 并发分割文本
        for i, chunk in enumerate(chunks):
            thread = threading.Thread(target=self.write_chunk, args=(chunk, i))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def write_chunk(self, chunk, index):
        with self.lock:
            with open(f"divided_data/chunk_{index}.txt", 'w') as f:
                f.write('\n'.join(chunk))

    def dividing_self_made(self, minimum, maximum):
        # 基于线程数量以及数据内容，数据内容在mission里面，将mission里面的数据按照kb大小平均分给线程
        # 此外，将每一个线程的url数量也标记出来
        """
        :param minimum: from
        :param maximum: to
        :return:
        """
        # data 存放的就是数据
        data = []
        with open("webpage_text_size.csv", 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader, start=1):
                if minimum <= i <= maximum:
                    data.append(row)
                if i > maximum:
                    break

            # 分割数据——这里存放的是url
            partitions = [[] for _ in range(self.num_threads)]
            # 大小，这里存放的是每一个kb大小
            Size = [0 for _ in range(self.num_threads)]
            URL_Number = [0 for _ in range(self.num_threads)]

            for row in data:
                now_url = row["URL"]
                now_size = row["Text Size (KB)"]
                min_index = min(range(len(Size)), key=lambda i: (Size[i], i))
                Size[min_index] += float(now_size)
                URL_Number[min_index] += 1
                partitions[min_index].append(now_url)

            # 将分割后的数据写入txt文件并输出每个分割的URL数量和总KB值
            for i, partition in enumerate(partitions):
                with open(f'divided_data/chunk_{i}.txt', 'w', encoding='utf-8') as f:
                    for url in partition:
                        f.write(url + '\n')
        for idx in range(self.num_threads):
            Size[idx] = round(Size[idx], 3)
        return URL_Number, Size
        # print(Size)
        # print(URL_Number)


# 任务就是分割这个文本
def dividing(filename, num_threads, dataset):
    splitter = FileSplitter(num_threads, dataset, filename)
    splitter.dividing_self_made(1, 500)


def dividing_released(num_threads, minimum, maximum):
    splitter = FileSplitter(num_threads)
    URL_Number, Size = splitter.dividing_self_made(minimum, maximum)
    return URL_Number, Size


if __name__ == "__main__":
    dividing('data_cnblog_pro.txt', 10, 500)
