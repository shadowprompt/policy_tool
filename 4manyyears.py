import json

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


json_data = {}

# 对每个情景生成四个独立的图表
for scenario in scenarios:
    # 筛选出该情景的数据
    scenario_data = df[df['情景编号'] == scenario]
    # 提取单一的值用于文件名
    subsidy_value = scenario_data['subsidy'].iloc[0] if 'subsidy' in scenario_data.columns else 'N/A'
    range_value = scenario_data['range'].iloc[0] if 'range' in scenario_data.columns else 'N/A'
    who_value = scenario_data['who'].iloc[0] if 'who' in scenario_data.columns else 'N/A'
    gradient_value = scenario_data['gradient'].iloc[0] if 'gradient' in scenario_data.columns else 'N/A'
    #  下面的需要取list
    water_saving_value = scenario_data['逐年节水量（百万立方米）'].tolist() if '逐年节水量（百万立方米）' in scenario_data.columns else []
    acc_water_saving_value = scenario_data['累计节水量（百万立方米）'].tolist() if '累计节水量（百万立方米）' in scenario_data.columns else []
    new_adopt_radio = scenario_data['新增采纳比例'].tolist() if '新增采纳比例' in scenario_data.columns else []
    acc_new_adopt_radio = scenario_data['累计采纳比例'].tolist() if '累计采纳比例' in scenario_data.columns else []
    output_value = scenario_data['逐年产值（亿）'].tolist() if '逐年产值（亿）' in scenario_data.columns else []
    acc_output_value = scenario_data['累计产值（亿）'].tolist() if '累计产值（亿）' in scenario_data.columns else []
    water_saving_efficiency = scenario_data['逐年节水效率（立方米/元）'].tolist() if '逐年节水效率（立方米/元）' in scenario_data.columns else []
    acc_water_saving_efficiency = scenario_data['累计节水效率（立方米/元）'].tolist() if '累计节水效率（立方米/元）' in scenario_data.columns else []


    key = f"water-{folder_name}_subsidy-{subsidy_value}_range-{range_value}_who-{who_value}_gradient-{gradient_value}"

    x_ticks = [2022, 2024, 2026, 2028, 2030, 2032]

    json_data[key] = {
        "subsidy_value": subsidy_value,
        "range_value": range_value,
        "who_value": who_value,
        "gradient_value": int(gradient_value),
        "water_saving_value": water_saving_value,
        "acc_water_saving_value": acc_water_saving_value,
        "new_adopt_radio": new_adopt_radio,
        "acc_new_adopt_radio": acc_new_adopt_radio,
        "output_value": output_value,
        "acc_output_value": acc_output_value,
        "water_saving_efficiency": water_saving_efficiency,
        "acc_water_saving_efficiency": acc_water_saving_efficiency
    }


with open('../policy/src/assets/water_manyyearsData.json', 'w') as f:
    json.dump(json_data, f)

print('生成json数据完成')