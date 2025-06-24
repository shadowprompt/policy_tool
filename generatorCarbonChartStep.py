import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pylab import mpl

chinese_font = font_manager.FontProperties(fname = 'C:\\Windows\\Fonts\\simsun.ttc')
english_font = font_manager.FontProperties(fname = 'C:\\Windows\\Fonts\\times.ttf')

policy_reduction = pd.read_csv('./files/policy_reduction.csv', index_col = 0)
pattern_reduction = pd.read_csv('./files/pattern_reduction.csv', index_col = 0)
policy_carbon = pd.read_csv('./files/policy_carbon.csv', index_col = 0)
dpnf = pd.read_csv('./files/DPNF.csv', index_col = 0)
srnf = pd.read_csv('./files/SRNF.csv', index_col = 0)
production = pd.read_csv('./files/production.csv', index_col = 0)

policy_scenarios = ['BASE', 'C_2', 'C_3', 'C_4', 'D_20%', 'D_30%', 'D_40%', 'S_40%', 'S_50%', 'S_60%']
pattern_scenarios = ['BASE', 'DX', 'DY', 'DM']
xticks = range(2020, 2026)

for scenario in policy_scenarios:
    for pattern in pattern_scenarios:
        plt.figure(figsize = (5, 3))
        plt.plot(xticks, policy_reduction[scenario], linewidth = 2, color = '#4682B4', marker = 'o', label = '补贴政策')
        plt.plot(xticks, pattern_reduction[pattern], linewidth = 2, color = '#A0C1D1', marker = 's', label = '种植模式')
        plt.xlabel('年份', fontsize = 12, fontproperties = chinese_font)
        # plt.ylabel('碳减排量（万吨）', fontsize = 12, fontproperties = chinese_font)
        plt.xticks(xticks, fontproperties = english_font)
        plt.yticks(fontproperties = english_font)
        plt.ylim(-20, 270)
        plt.title('碳减排量（万吨）', fontsize = 14, fontproperties = 'SimHei')
        plt.legend(loc = 'upper left', fontsize = 12, prop={'family': 'SimSun'}, frameon = False)
        plt.gca().tick_params(axis = 'x', direction = 'in')
        plt.gca().tick_params(axis = 'y', direction = 'in')
        plt.tight_layout()
        plt.savefig(f'./tongji/reduction_{pattern}_{scenario}.png', dpi = 500, transparent = True)
        plt.show()