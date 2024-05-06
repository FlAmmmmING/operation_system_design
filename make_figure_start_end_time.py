import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def figure():
    # 读取 CSV 文件
    df = pd.read_csv("thread_times.csv")

    # 将开始时间和结束时间转换为 datetime 对象
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # 提取需要绘制的数据
    thread_ids = df["Thread ID"]
    start_times = df["Start Time"]
    end_times = df["End Time"]

    # 绘制时间图
    plt.figure(figsize=(15, 9))

    # 绘制每个线程的开始时间和结束时间
    for thread_id, start_time, end_time in zip(thread_ids, start_times, end_times):
        plt.plot([start_time, end_time], [thread_id, thread_id], marker='o', label=f'Thread {thread_id}', linewidth=10)  # 加粗线条

        # 在每个线程的开始时间上标出具体时间（秒和毫秒）
        plt.text(start_time, thread_id, f'{start_time.strftime("%S.%f")[:-3]}s', ha='right', va='bottom')

        # 在每个线程的结束时间上标出具体时间（秒和毫秒）
        plt.text(end_time, thread_id, f'{end_time.strftime("%S.%f")[:-3]}s', ha='left', va='bottom')

    plt.xlabel('Time')
    plt.ylabel('Thread ID')
    plt.title('Start and End Time of Each Thread')
    # plt.legend()
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.yticks(thread_ids)  # 设置 y 轴刻度为线程 ID
    plt.grid(True)
    plt.tight_layout()

    # 保存图形为文件
    plt.savefig('static/ret_img/thread_start_end_time_plot.jpg')

    # 显示图形
    plt.show()


if __name__ == '__main__':
    figure()
