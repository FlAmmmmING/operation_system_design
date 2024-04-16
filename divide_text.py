# 分割文本，按照每10个网页分割

def dividing(start, end, data, id):
    """
    :param start: 开始idx
    :param end: 结束idx
    :param data: 目标文本
    :param id: 分割ID
    :return: 返回分割文本，是数组
    """
    ret_data = []
    for i in range(start, end + 1):
        ret_data.append(data[i])
    return id, ret_data


def split_text_multithreaded():
    pass

def divide_text():
    data = []
    with open("data.txt", "r") as f:
        data = f.read().split(",\n")
    f.close()

    # 开始多线程分割
    # 为了防止重复读，这里需要互斥
