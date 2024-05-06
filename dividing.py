import threading
import concurrent.futures


class FileSplitter:
    def __init__(self, filename, num_threads, dataset):
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


# 任务就是分割这个文本
def dividing(filename, num_threads, dataset):
    splitter = FileSplitter(filename, num_threads, dataset)
    splitter.split_file()


# if __name__ == "__main__":
#     dividing('data_cnblog_pro.txt', 10)
