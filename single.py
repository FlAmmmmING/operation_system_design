# os 课设内容
import threading
import queue
import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures
import json
import base64


# 代理 ip 生成
def get_ip_list():
    url = "https://api.wandouapp.com/?app_key=5c05a58cba892ce4e276c163a673dc11&num=1&xy=1&type=2&lb=\r\n&nr=0&area_id=&isp=0&"
    resp = requests.get(url)
    # 提取数据
    resp_json = resp.text
    # json 转变为字典
    resp_dict = json.loads(resp_json)
    ip_dict_list = resp_dict.get("data")
    return ip_dict_list


# 验证账户信息
def base_code(username, password):
    str = '%s:%s' % (username, password)
    encodestr = base64.b64encode(str.encode('utf-8'))
    return '%s' % encodestr.decode()


# 用代理ip访问目标网站
def spider_ip(ip_port, url):
    username = "13917734176"
    password = "Jwj823725"
    # 请求头
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'Proxy-Authorization': 'Basic %s' % (base_code(username, password))
    }
    # 代理ip地址放在proxy参数中
    proxy = {
        'http': f'http://{ip_port}'
    }
    # 发送网络请求
    # 发送成功就获取数据
    try:
        resp = requests.get(url, proxies=proxy, headers=headers)
        # 解析访问数据
        return resp.text.encode('utf-8')
    # 发送失败,则代理失效
    except:
        result = '代理失效'
        print(result)
        return None


# 这个是爬虫方法，解析网页内容
def craw(url):
    try:
        r = requests.get(url)
        print(url)
        # 返回文档内容
        return r.text.encode('utf-8')
    except:
        return None


# 这里是数据存储方法，解析需要的title
def parse(html):
    # class = "post-item-title"
    soup = BeautifulSoup(html, "html.parser")
    # links = soup.find_all('a', class_="post-item-title")
    links = soup.find("title")
    # return [(link["href"], link.get_text()) for link in links]
    return links.get_text()


def single_thread(file, dataset):
    # 代理ip的一些参数
    ip_dict_list = get_ip_list()

    # 获取文件内容
    cnt = 0
    with open(file, 'r') as f:
        data = f.read().split("\n")
    for url in data:
        if cnt >= dataset:
            return
        # 代理 ip
        html = craw(url)
        ip_port = '{ip}:{port}'.format(ip=ip_dict_list[0].get('ip'), port=str(ip_dict_list[0].get('port')))
        # html = spider_ip(ip_port, url)
        if html is None:
            print("爬取丢失")
            continue
        results = parse(html)
        # for result in results:
        #     print(result)
        #     # with open("data_cnblog_pro.txt", "a", encoding='utf-8') as f:
        #     #     f.write(str(result[0]) + "\n")
        #     print(cnt)
        #     cnt += 1
        cnt += 1
        print(results)
        print(cnt)
        with open('single_data.txt', 'a', encoding='utf-8') as f:
            f.write(str(results) + '\n')


def single_thread_setting(dataset, loop_time):
    """

    :param dataset: 爬取的数据大小
    :param loop_time: 爬取几次
    :return:
    """
    for i in range(loop_time):
        start = time.time()
        single_thread("data_url/data_cnblog_pro.txt", dataset)
        end = time.time()
        print(f"cost:{end - start}")
        with open(f'experiment_result/single/single_data_time_consumption_{dataset}.csv', 'a') as f:
            f.write(str(end - start) + ',\n')


if __name__ == '__main__':
    single_thread_setting(1000, 1)
