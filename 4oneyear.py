import json
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

def convert_value(value):
    if np.isnan(value):
        return 0
    elif value == 1.0:
        return 1
    elif value == 0.0:
        return 0
    else:
        return value


json_data = {}

# 创建文件夹并保存图形
for index, row in df.iterrows():
    # 创建情景编号文件夹
    folder_name = f"{row['情景编号']}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # 提取subsidy, range, who, gradient的值
    subsidy_value = row['subsidy']
    subsidy_value = convert_value(subsidy_value)

    range_value = row['range']
    range_value = convert_value(range_value)

    who_value = row['who']
    gradient_value = row['gradient']
    water_value = row['用水量（亿立方米）'] if pd.notna(row['用水量（亿立方米）']) else 0
    base_water_value = row['基准用水量（亿立方米）'] if pd.notna(row['基准用水量（亿立方米）']) else 0

    key = f"water-{folder_name}_subsidy-{subsidy_value}_range-{range_value}_who-{who_value}_gradient-{gradient_value}"

    json_data[key] = {
        "subsidy_value": subsidy_value,
        "range_value": range_value,
        "who_value": who_value,
        "gradient_value": gradient_value,
        "water_value": water_value,
        "base_water_value": base_water_value
    }

with open('../policy_vue/src/assets/water_oneyearData.json', 'w') as f:
    json.dump(json_data, f)

print('生成json数据完成')
