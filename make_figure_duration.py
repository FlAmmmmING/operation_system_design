# import matplotlib.pyplot as plt
# import pandas as pd
#
#
# def figure():
#     # 读取 CSV 文件
#     df = pd.read_csv("thread_times.csv")
#
#     # 提取需要绘制的数据
#     thread_ids = df["Thread ID"]
#     durations = df["Duration (s)"]
#
#     # 计算平均耗时
#     average_duration = sum(durations) / len(durations)
#
#     # 创建图形
#     plt.figure(figsize=(12, 8))
#
#     # 绘制柱状图
#     colors = ['skyblue', 'lightgreen', 'coral', 'salmon', 'pink', 'yellow']  # 添加更多颜色
#     plt.bar(thread_ids, durations, color=colors, label='_nolegend_')  # 去掉 Duration 的图例
#     plt.xlabel('Thread ID')
#     plt.ylabel('Duration (seconds)')
#     plt.title('Duration of Each Thread')
#     plt.xticks(rotation=45, ha='right')
#
#     # 在每个柱状图上添加具体时间标记
#     for idx, duration in enumerate(durations):
#         plt.text(idx, duration - 0.2, f'{duration:.3f}s', ha='center')  # 调整标记位置
#
#     # 添加折线图
#     plt.plot(thread_ids, durations, marker='o', color='purple', linestyle='-', linewidth=2, markersize=8, label='_nolegend_')  # 去掉 Duration 的图例
#
#     # 添加平均耗时的红色虚线
#     plt.axhline(y=average_duration, color='red', linestyle='--', label=f'Average Cost: {average_duration:.3f}s')
#
#     # 动态调整纵坐标轴范围
#     plt.ylim(min(durations) - 0.5, max(durations) + 0.5)
#
#     # 添加图例
#     plt.legend()
#
#     # 保存图形为文件
#     plt.savefig('static/ret_img/data.jpg')
#
#     # 返回保存的文件路径
#     return 'static/ret_img/data.jpg'
#
#
# if __name__ == '__main__':
#     figure()
import matplotlib.pyplot as plt
import pandas as pd


def figure():
    # 读取 CSV 文件
    df = pd.read_csv("thread_times.csv")

    # 提取需要绘制的数据
    thread_ids = df["Thread ID"]
    durations = df["Duration (s)"]

    # 计算平均耗时
    average_duration = sum(durations) / len(durations)

    # 创建图形
    plt.figure(figsize=(12, 8))

    # 添加折线图
    plt.plot(thread_ids, durations, marker='o', color='navy', linestyle='-', linewidth=2, markersize=8, label='Thread Duration')

    # 在每个数据点上添加连接横坐标轴的虚线
    for idx, duration in enumerate(durations):
        plt.plot([thread_ids[idx], thread_ids[idx]], [0, duration], color='gray', linestyle='--', linewidth=1)

    # 添加平均耗时的红色虚线
    plt.axhline(y=average_duration, color='red', linestyle='--', label=f'Average Cost: {average_duration:.3f}s')

    # 动态调整纵坐标轴范围
    plt.ylim(min(durations) - 0.5, max(durations) + 0.5)

    # 添加图例
    plt.legend()

    # 添加标签
    plt.xlabel('Thread ID')
    plt.ylabel('Duration (seconds)')
    plt.title('Thread Duration Trend')

    # 保存图形为文件
    plt.savefig('static/ret_img/data.jpg')

    # 返回保存的文件路径
    return 'static/ret_img/data.jpg'


if __name__ == '__main__':
    figure()
