import matplotlib.pyplot as plt
import pandas as pd


def figure():
    # 读取 CSV 文件
    df = pd.read_csv("thread_times.csv")

    # 提取需要绘制的数据
    thread_ids = df["Thread ID"]
    durations = df["Duration (s)"]

    # 创建图形
    plt.figure(figsize=(12, 8))

    # 绘制柱状图
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink', 'lightyellow']  # 添加更多颜色
    plt.bar(thread_ids, durations, color=colors, label='Duration')
    plt.xlabel('Thread ID')
    plt.ylabel('Duration (seconds)')
    plt.title('Duration of Each Thread')
    plt.xticks(rotation=45, ha='right')  # 旋转刻度标签

    # 在每个柱状图上添加具体时间标记
    for idx, duration in enumerate(durations):
        plt.text(idx, duration, f'{duration:.3f}s', ha='center')  # 调整标记位置

    # 添加折线图
    plt.plot(thread_ids, durations, marker='o', color='skyblue', linestyle='-', linewidth=2, markersize=8, label='Duration Line')

    # 添加图例
    # plt.legend()

    # 保存图形为文件
    plt.savefig('static/ret_img/data.jpg')

    # 返回保存的文件路径
    return 'static/ret_img/data.jpg'


if __name__ == '__main__':
    figure()
