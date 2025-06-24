import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

excel_file_path = './files/oneyear.xlsx'

# 设置字体
# 定义字体变量
simsun = 'SimSun'  # 宋体
times_new_roman = 'Times New Roman'  # Times New Roman

# 设置字体
mpl.rcParams['font.sans-serif'] = [simsun]  # 中文宋体
mpl.rcParams['font.serif'] = times_new_roman  # 英文新罗马
mpl.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# # mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文宋体
# # mpl.rcParams['font.serif'] = 'Times New Roman'  # 英文新罗马
# plt.rcParams['font.family'] = 'Times New Roman'
# mpl.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# plt.rc('xtick', labelsize=12)
# plt.rc('ytick', labelsize=12)
#plt.rc('font', family='SimHei')
# mpl.rcParams['font.sans-serif'] = ['SimSun']  # 中文使用 SimSun
# mpl.rcParams['axes.unicode_minus'] = False
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
# plt.rc('font', family='Times New Roman')  # 英文使用 Times 

# 读取CSV文件
df = pd.read_excel(excel_file_path)

# 创建文件夹并保存图形
for index, row in df.iterrows():
    # 创建情景编号文件夹
    folder_name = f"{row['情景编号']}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 提取subsidy, range, who, gradient的值
    subsidy_value = row['subsidy']
    range_value = row['range']
    who_value = row['who']
    gradient_value = row['gradient']
    water_value = row['用水量（亿立方米）'] if pd.notna(row['用水量（亿立方米）']) else 0
    base_water_value = row['基准用水量（亿立方米）'] if pd.notna(row['基准用水量（亿立方米）']) else 0

    # 创建柱状图：用水量和基准用水量
    plt.figure(figsize=(5, 3))
    bar_width = 0.15  # 调整条形宽度
    #x = [0.3, 0.7]  # 设置条形的x位置为1/3和2/3，确保条形图间隔
    bars = plt.bar(['用水量', '基准用水量'], [row['用水量（亿立方米）'], row['基准用水量（亿立方米）']],
                   color=['#4682B4', '#A0C1D1'], width=0.4, align='center')
    plt.ylabel('用水量（亿立方米）', fontsize=12, family=simsun)
    plt.ylim(-0.2, 2.7)
    plt.yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5], family=times_new_roman)
    plt.gca().tick_params(axis='x', direction='in')
    plt.gca().tick_params(axis='y', direction='in')
    #plt.xticks([1/3, 2/3], ['用水量', '基准用水量'], fontsize=12)  # 设置x轴标签

    # 在条形图上添加数值标注
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom', fontsize=12,
                 family=times_new_roman)

    # 保存图表
    plt.tight_layout()
    plt.savefig(os.path.join(
        f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_water.png'),
        dpi=500)
    plt.close()

    # 创建饼状图：采纳比例
    plt.figure(figsize=(5, 3))

    # 计算采纳和未采纳的值
    adopted = row['采纳比例']
    not_adopted = 100 - adopted

    # 创建饼状图，只显示颜色，不显示标签
    wedges, texts = plt.pie([adopted, not_adopted],
                            labels=['', ''],  # 不显示默认标签
                            colors=['#4682B4', '#A0C1D1'],
                            autopct=None,  # 取消自动百分比标注
                            textprops={'fontsize': 12, 'fontweight': 'bold'},
                            labeldistance=0.4,  # 标签距离圆心的距离
                            pctdistance=0.6,  # 百分比距离圆心的距离
                            startangle=90,  # 让图从顶部开始绘制
                            radius=1.2)  # 增加radius，增大饼状图

    # 为每个扇区手动设置标签
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 + wedge.theta1) / 2  # 获取扇区的中间角度
        x = 0.5 * np.cos(np.radians(angle))  # 计算标签x位置
        y = 0.5 * np.sin(np.radians(angle))  # 计算标签y位置
        label = f"{['采纳', '未采纳'][i]}\n{[adopted, not_adopted][i]}%"  # 使用换行符
        plt.text(x, y + 0.1, f"{['采纳', '未采纳'][i]}", ha='center', va='center', fontsize=12, family=simsun)
        plt.text(x, y - 0.1, f"{[adopted, not_adopted][i]}%", ha='center', va='center', fontsize=12,
                 family=times_new_roman)
        #plt.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')

    # 调整图像布局
    plt.tight_layout()

    # 保存图片
    plt.savefig(os.path.join(
        f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_adoption.png'),
        dpi=500)
    plt.close()

    # 创建柱状图：产值和基准产值
    plt.figure(figsize=(5, 3))
    bar_width = 0.15  # 调整条形宽度
    #x = [0.3, 0.7]  # 设置条形的x位置为1/3和2/3
    bars = plt.bar(['产值', '基准产值'], [row['产值（亿元）'], row['基准产值（亿元）']], color=['#4682B4', '#A0C1D1'],
                   width=0.4, align='center')
    plt.ylabel('产值（亿元）', fontsize=12, family=simsun)
    plt.ylim(-1, 16)
    plt.yticks([0, 3, 6, 9, 12, 15], family=times_new_roman)
    plt.gca().tick_params(axis='x', direction='in')
    plt.gca().tick_params(axis='y', direction='in')
    #plt.xticks([1/3, 2/3], ['产值', '基准产值'], fontsize=15)  # 设置x轴标签

    # 在条形图上添加数值标注
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom', fontsize=12,
                 family=times_new_roman)

    # 保存图表
    plt.tight_layout()
    plt.savefig(os.path.join(
        f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_production.png'),
        dpi=500)
    plt.close()

    # 创建柱状图：节水效率
    if pd.notna(row['节水效率（立方米/元）']):
        plt.figure(figsize=(5, 3))
        #bar_width = 0.15
        #x = [0.5]  # 将节水效率放置在横向最中间
        bars = plt.bar(['节水效率'], [row['节水效率（立方米/元）']], color=['#4682B4', '#4682B4', '#4682B4'], width=0.3,
                       align='center')
        plt.ylabel('节水效率（立方米/元）', fontsize=12, family=simsun)
        plt.ylim(-2, 22)
        plt.xlim(-0.5, 0.5)
        plt.yticks([0, 4, 8, 12, 16, 20], family=times_new_roman)
        plt.gca().tick_params(axis='x', direction='in')
        plt.gca().tick_params(axis='y', direction='in')

        # 在条形图上添加数值标注
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom',
                     fontsize=12, family=times_new_roman)

        # 保存图表
        plt.tight_layout()
        plt.savefig(os.path.join(
            f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_efficiency.png'),
            dpi=500)
        plt.close()
