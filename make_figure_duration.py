import matplotlib.pyplot as plt
import pandas as pd


def figure():
    # 读取 CSV 文件
    df = pd.read_csv("thread_times.csv")

    # 提取需要绘制的数据
    thread_ids = df["Thread ID"]
    durations = df["Duration"]

    # 绘制柱状图
    plt.figure(figsize=(15, 9))
    plt.bar(thread_ids, durations, color='skyblue')
    plt.xlabel('Thread ID')
    plt.ylabel('Duration (seconds)')
    plt.title('Duration of Each Thread')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    bars = plt.bar(thread_ids, durations, color='skyblue')
    # 在每个柱状图上添加具体时间标记
    for bar, duration in zip(bars, durations):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{duration:.2f}s',
                 ha='center', va='bottom')
    # 保存图形为文件
    plt.savefig('static/ret_img/data.jpg')

    # 显示图形
    plt.show()


if __name__ == '__main__':
    figure()
