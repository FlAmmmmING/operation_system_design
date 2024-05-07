import requests
import csv


def get_page_text_size(url):
    try:
        # 发送GET请求获取网页内容
        response = requests.get(url)
        # 如果请求成功
        if response.status_code == 200:
            # 获取网页文本
            page_text = response.text
            # 计算文本大小（以KB为单位）
            text_size_kb = len(page_text) / 1024
            return text_size_kb
        else:
            print("Failed to retrieve page:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def save_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'URL', 'Text Size (KB)'])
            for row in data:
                writer.writerow(row)
        print("Data saved to", filename)
    except Exception as e:
        print("An error occurred while saving to CSV:", str(e))


if __name__ == "__main__":
    with open('cn_blogs.txt', 'r') as f:
        urls = f.read()
    urls = urls.split('\n')
    print(len(urls))
    data = []
    for i, url in enumerate(urls, start=1):
        text_size_kb = get_page_text_size(url)
        if text_size_kb:
            data.append([i, url, round(text_size_kb, 2)])
    save_to_csv(data, 'webpage_text_size.csv')
