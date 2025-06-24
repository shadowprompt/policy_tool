import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm as cm
from pylab import mpl
import os
simsun = 'SimSun'  # 宋体
times_new_roman = 'Times New Roman'  # Times New Roman

# 设置字体
mpl.rcParams['font.sans-serif'] = [simsun]  # 中文宋体
mpl.rcParams['font.serif'] = times_new_roman  # 英文新罗马
mpl.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rc('xtick', labelsize = 12)
plt.rc('ytick', labelsize = 12)

# 读取Excel文件，假设文件路径为 '多年的.xlsx'
file_path = './files/manyyears.xlsx'
df = pd.read_excel(file_path)

# 创建一个情景编号的列表（从1到21）
scenarios = range(1, 22)

# 获取蓝色系的调色板
blue_colors = cm.Blues([i/len(scenarios) for i in range(len(scenarios))])

# 对每个情景生成四个独立的图表
for scenario in scenarios:
    # 筛选出该情景的数据
    scenario_data = df[df['情景编号'] == scenario]
    # 为每个情景创建一个文件夹
    folder_name = f'{scenario}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

        # 提取单一的值用于文件名
    subsidy_value = scenario_data['subsidy'].iloc[0] if 'subsidy' in scenario_data.columns else 'N/A'
    range_value = scenario_data['range'].iloc[0] if 'range' in scenario_data.columns else 'N/A'
    who_value = scenario_data['who'].iloc[0] if 'who' in scenario_data.columns else 'N/A'
    gradient_value = scenario_data['gradient'].iloc[0] if 'gradient' in scenario_data.columns else 'N/A'
    x_ticks = [2022, 2024, 2026, 2028, 2030, 2032]

    # 绘制逐年节水量和累计节水量图
    plt.figure(figsize=(5, 3))
    plt.plot(scenario_data['年份'], scenario_data['逐年节水量（百万立方米）'], label='逐年节水量', linewidth = 2,color='#A0C1D1',marker='o', markersize=6)
    plt.plot(scenario_data['年份'], scenario_data['累计节水量（百万立方米）'], label='累计节水量', linewidth = 2,color='#4682B4', marker='s', markersize=6)
    #plt.title(f'情景 {scenario} - 节水量')
    plt.xticks(x_ticks)
    plt.xlabel('年份', fontsize = 12, family=simsun)
    if scenario == 1:
        plt.ylabel('用水量（百万立方米）', fontsize=12, family=simsun)
        plt.ylim(-200, 2300)
        plt.yticks([0, 400, 800, 1200, 1600, 2000], family=times_new_roman)
    else:
        plt.ylabel('节水量（百万立方米）', fontsize=12, family=simsun)
        plt.ylim(-10, 110)
        plt.yticks([0, 20, 40, 60, 80, 100], family=times_new_roman)
    #plt.ylabel('节水量（百万立方米）', fontsize = 15)
    plt.xticks(x_ticks, family=times_new_roman)
    plt.xlim(2021.5, 2032.5)
    plt.legend(loc = 'upper left', fontsize = 12)
    plt.gca().tick_params(axis = 'x', direction = 'in')
    plt.gca().tick_params(axis = 'y', direction = 'in')
    plt.tight_layout()
    plt.savefig(f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_water.png', dpi = 500)
    plt.close()

    # 绘制采纳比例h 和 累计采纳比例图
    plt.figure(figsize=(5, 3))
    plt.plot(scenario_data['年份'], scenario_data['新增采纳比例'], label='新增采纳比例', linewidth = 2,color='#A0C1D1',marker='o', markersize=6)
    plt.plot(scenario_data['年份'], scenario_data['累计采纳比例'], label='累计采纳比例',linewidth = 2, color='#4682B4', marker='s', markersize=6)
    #plt.title(f'情景 {scenario} - 采纳比例')
    plt.xlabel('年份', fontsize = 12, family=simsun)
    plt.ylabel('采纳比例(%)', fontsize = 12, family=simsun)
    plt.ylim(-10, 110)
    plt.xticks(x_ticks, family=times_new_roman)
    plt.xlim(2021.5, 2032.5)
    plt.yticks([0, 20, 40, 60, 80, 100], family=times_new_roman)
    plt.legend(loc = 'upper left', fontsize = 12)
    plt.gca().tick_params(axis = 'x', direction = 'in')
    plt.gca().tick_params(axis = 'y', direction = 'in')
    plt.tight_layout()
    plt.savefig(f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_adoption.png', dpi = 500)
    plt.close()

    # 绘制逐年产值和累计产值图
    plt.figure(figsize=(5, 3))
    plt.plot(scenario_data['年份'], scenario_data['逐年产值（亿）'], label='逐年产值',linewidth = 2, color='#A0C1D1',marker='o', markersize=6)
    plt.plot(scenario_data['年份'], scenario_data['累计产值（亿）'], label='累计产值', linewidth = 2,color='#4682B4', marker='s', markersize=6)
    #plt.title(f'情景 {scenario} - 产值')
    plt.xlabel('年份', fontsize = 12, family=simsun)
    plt.ylabel('产值（亿）', fontsize = 12)
    plt.ylim(0, 120)
    plt.yticks([10, 30, 50, 70, 90, 110], family=times_new_roman)
    plt.xlim(2021.5, 2032.5)
    plt.xticks(x_ticks, family=times_new_roman)
    plt.legend(loc = 'upper left', fontsize = 12)
    plt.gca().tick_params(axis = 'x', direction = 'in')
    plt.gca().tick_params(axis = 'y', direction = 'in')
    plt.tight_layout()
    plt.savefig(f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_production.png', dpi = 500)
    plt.close()

    # 绘制逐年节水效率和累计节水效率图
    plt.figure(figsize=(5, 3))
    plt.plot(scenario_data['年份'], scenario_data['逐年节水效率（立方米/元）'], label='逐年节水效率', linewidth = 2,color='#A0C1D1', marker='o', markersize=6)
    plt.plot(scenario_data['年份'], scenario_data['累计节水效率（立方米/元）'], label='累计节水效率', linewidth = 2, color='#4682B4',marker='s', markersize=6)
    #plt.title(f'情景 {scenario} - 节水效率')
    plt.xlabel('年份', fontsize = 12, family=simsun)
    plt.ylabel('节水效率（立方米/元）', fontsize = 12, family=simsun)
    plt.ylim(-2, 27)
    plt.yticks([0, 5, 10, 15, 20, 25], family=times_new_roman)
    plt.xticks(x_ticks, family=times_new_roman)
    plt.xlim(2021.5, 2032.5)
    plt.legend(loc = 'upper left', fontsize = 12)
    plt.gca().tick_params(axis = 'x', direction = 'in')
    plt.gca().tick_params(axis = 'y', direction = 'in')
    plt.tight_layout()
    plt.savefig(f'water_{folder_name}_subsidy{subsidy_value}_range{range_value}_{who_value}_gradient{gradient_value}_efficiency.png', dpi = 500)
    plt.close()