# 多次爬虫会封禁ip，测试的时候用这个
import time


def imitate_spider(url, headers=None):
    """
    模拟爬虫的过程
    :return:
    """
    st = time.time()
    time.sleep(1)
    ed = time.time()
    # print(ed - st)
    return "this is imitation for spider"


# if __name__ == '__main__':
#     for i in range(100):
#         imitate_spider("111")
