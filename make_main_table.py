import pandas as pd
import matplotlib.pyplot as plt


def figure():
    # 读取 CSV 文件
    df = pd.read_csv("thread_times.csv")

    # 创建具有更大尺寸的表格绘图
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(111, frame_on=False)  # 添加没有框架的子图

    # 隐藏坐标轴
    ax.axis('off')

    # 绘制表格
    col_colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightsalmon', 'lightpink']
    cell_colors = [['white', 'lightgrey'] * (len(df.columns) // 2) for _ in range(len(df) + 1)]
    table_data = []
    for i, row in enumerate(df.values):
        table_data.append([f'{val:.2f}' if isinstance(val, float) else val for val in row])

    table = ax.table(cellText=table_data, colLabels=df.columns, loc='center')

    # 应用列颜色
    for key, cell in table._cells.items():
        row, col = key
        if row == 0:
            cell.set_facecolor(col_colors[col])

    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            table.get_celld()[(i, j)].set_facecolor(cell_colors[i][j])

    # 调整字体大小和行高
    table.auto_set_font_size(False)
    table.set_fontsize(14)  # 增加字体大小
    table.scale(1, 3)  # 增加行高

    # 文本居中对齐
    for _, cell in table._cells.items():
        cell.set_text_props(fontweight='normal', ha='center', va='center')

    # 保存图像
    plt.savefig("static/ret_img/table.png", bbox_inches='tight')


if __name__ == '__main__':
    figure()
