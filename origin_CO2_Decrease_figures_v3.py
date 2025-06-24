# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:36:40 2024

@author: PC
"""

import os
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib import patches
import geopandas as gpd
import matplotlib.font_manager as fm
import matplotlib.image as mpimg  # 导入处理图像的库

# 文件夹路径
folder_path = r"D:\组内资料\政策支持平台开发\任务分配\任务1-碳排放\碳排放\differ"
output_folder = r"D:\组内资料\政策支持平台开发\任务分配\任务1-碳排放\碳排放\differ_figure_normColor_v3"
os.makedirs(output_folder, exist_ok=True)

Jianghan_shp = r"D:\组内资料\政策支持平台开发\任务分配\任务1-碳排放\jianghan_couty\jianghan_UTM.shp"
gdf = gpd.read_file(Jianghan_shp)

# 获取文件夹中所有tif文件
tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

# sns.set()
plt.rc('font', family='SimHei')

# Step 1: 计算所有栅格的统一最大最小值
global_min, global_max = np.inf, -np.inf

for tif_file in tif_files:
    tifPath = os.path.join(folder_path, tif_file)
    with rasterio.open(tifPath) as src:
        data = src.read(1)
        # 获取NoData值并替换为NaN
        nodata_value = src.nodata
        if nodata_value is not None:
            data[data == nodata_value] = np.nan

        # 将小于0的值设置为0
        data[data < 0] = 0

        data = data / 1000000  #转化为千吨

        # 更新全局最大最小值
        global_min = min(global_min, np.nanmin(data))
        global_max = max(global_max, np.nanmax(data))

print(f"统一的颜色范围：最小值 = {global_min}, 最大值 = {global_max}")


# 绘图函数

def plot_raster_with_features(raster_path, output_path):
    with rasterio.open(raster_path) as src:
        # 读取栅格数据
        data = src.read(1)
        # 将像元值小于0的赋值为0
        data[data < 0] = 0
        data = data / 1000000  #转化为千吨

        # 获取投影和边界信息
        bounds = src.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        # 创建绘图
        fig, ax = plt.subplots(figsize=(8, 6))
        img = ax.imshow(data, extent=extent, cmap='viridis', vmin=global_min, vmax=global_max * 0.8)

        # 获取投影坐标范围
        x_min, x_max = bounds.left, bounds.right
        y_min, y_max = bounds.bottom, bounds.top

        # 去掉边框
        for spine in ax.spines.values():
            spine.set_visible(False)

            # 绘制shp面状边界数据
        gdf.plot(ax=ax, facecolor='none', edgecolor='darkgray', linewidth=0.8)

        # 设置宋体和新罗马字体
        font_path_heiti = 'C:/Windows/Fonts/simhei.ttf'  # 黑体
        font_path_simsun = 'C:/Windows/Fonts/simsun.ttc'  # 宋体
        font_path_times = 'C:/Windows/Fonts/times.ttf'  # Times New Roman
        font_heiti = fm.FontProperties(fname=font_path_heiti)
        font_simsun = fm.FontProperties(fname=font_path_simsun)
        font_times = fm.FontProperties(fname=font_path_times)

        # font_path = 'C:/Windows/Fonts/simsun.ttc'  # 修改为你的宋体字体路径
        prop = fm.FontProperties(fname=font_path_simsun)

        # 添加名称标签
        for _, row in gdf.iterrows():
            ax.text(row.geometry.centroid.x, row.geometry.centroid.y,
                    row['NAME'], fontsize=7, ha='center', color='white', fontproperties=prop)

        # # 添加比例尺
        # scalebar = ScaleBar(1, location='lower right', units="m", scale_loc='bottom',
        #                     length_fraction=0.2, font_properties={'size': 8})
        # ax.add_artist(scalebar)

        # 定义比例尺长度（单位：米）
        scalebar_length = 50000  # 设置比例尺长度为 50000 米
        scalebar_x_start = x_max - (x_max - x_min) * 0.24  # 距离右边 20%
        scalebar_y_start = y_min + (y_max - y_min) * 0.05  # 距离底部 5%

        # 绘制比例尺（两段黑白矩形）
        black_rect = patches.Rectangle((scalebar_x_start, scalebar_y_start),
                                       scalebar_length / 2, (y_max - y_min) * 0.01,
                                       facecolor='black', edgecolor='black')
        white_rect = patches.Rectangle((scalebar_x_start + scalebar_length / 2, scalebar_y_start),
                                       scalebar_length / 2, (y_max - y_min) * 0.01,
                                       facecolor='white', edgecolor='black')

        ax.add_patch(black_rect)
        ax.add_patch(white_rect)

        # 添加比例尺文字
        ax.text(scalebar_x_start, scalebar_y_start - (y_max - y_min) * 0.015,
                "0", fontsize=10, ha='center', va='top', color='black', fontfamily='Times New Roman')  # 最左端
        ax.text(scalebar_x_start + scalebar_length / 2, scalebar_y_start - (y_max - y_min) * 0.015,
                "25", fontsize=10, ha='center', va='top', color='black', fontfamily='Times New Roman')  # 中间
        ax.text(scalebar_x_start + scalebar_length, scalebar_y_start - (y_max - y_min) * 0.015,
                "50", fontsize=10, ha='center', va='top', color='black', fontfamily='Times New Roman')  # 最右端

        # 在比例尺右侧添加单位 "km"，并稍微向上调整
        ax.text(scalebar_x_start + scalebar_length + (x_max - x_min) * 0.01,
                scalebar_y_start + (y_max - y_min) * 0.005,  # 向上调整一点高度
                "km", fontsize=10, ha='left', va='center', color='black', fontfamily='Times New Roman')

        # # 添加指北针到左上角（箭头 + "N"）
        # arrow_x = 0.1  # 相对于轴的 x 位置
        # arrow_y = 0.85  # 相对于轴的 y 位置
        # ax.annotate(
        #     '', xy=(arrow_x, arrow_y + 0.05), xytext=(arrow_x, arrow_y),
        #     xycoords='axes fraction',
        #     arrowprops=dict(facecolor='black', width=2, headwidth=5, headlength=4)
        # )
        # ax.text(
        #     arrow_x, arrow_y - 0.04, 'N', ha='center', va='center',
        #     fontsize=10, fontweight='bold', color='black', transform=ax.transAxes
        # )
        # **修改部分：添加ESRI North 3风格的指北针**

        # 添加指北针（从图片文件加载）
        north_img = mpimg.imread(r"C:\Users\PC\Desktop\north.png")  # 加载指北针图片
        axin = fig.add_axes([0.24, 0.77, 0.072, 0.072], zorder=10)  # 设置指北针的位置和大小
        axin.imshow(north_img)
        axin.axis('off')  # 隐藏指北针的坐标轴

        # 添加颜色条并调整到图内右上角
        cbar = plt.colorbar(
            img, ax=ax, orientation='horizontal', fraction=0.046, pad=0.02
        )

        # 将颜色条移动到右上角
        cbar.ax.set_position([0.59, 0.79, 0.19, 0.025])  # [left, bottom, width, height]

        # 手动设置颜色条刻度为规整值（例如 0, 2.5, 5, ...）
        vmax_adjusted = np.ceil(global_max * 0.8 / 2.5) * 2.5  # 将最大值调整为最近的 2.5 的倍数
        cbar_ticks = np.arange(0, vmax_adjusted + 0.1, 2.5)  # 以 2.5 为间隔生成刻度
        cbar.set_ticks(cbar_ticks)
        cbar.ax.tick_params(labelsize=10, direction='in', length=3, width=1)  # 修改字体大小
        # 获取刻度线位置
        ticks = cbar.ax.get_xticks()

        # 隐藏第一个刻度线（刻度值为 0）
        for tick, line in zip(ticks, cbar.ax.xaxis.get_ticklines()):
            if tick == 0:  # 如果刻度值是 0
                line.set_visible(False)  # 隐藏刻度线                
        cbar.ax.set_xticklabels([f"{tick:.1f}" for tick in cbar_ticks], fontproperties=font_times)  # 格式化为 1 位小数 

        # 设置颜色条的文字到颜色条上方
        # cbar.ax.xaxis.set_ticks_position('top')
        cbar.ax.xaxis.set_label_position('top')
        # cbar.set_label('CO$_2$减排量（10$^3$ t）', fontsize=10)

        # 设置颜色条标题字体
        cbar_label_text = r"CO$_2$ 减排量（10$^3$ t）"

        # 清空默认标题
        cbar.ax.set_title('')

        # 绘制“CO₂”
        cbar.ax.text(
            0.23, 2.0,  # 调整位置
            "CO",
            fontsize=10,
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )
        cbar.ax.text(
            0.31, 1.9,  # 调整位置
            "₂",  # 下标数字2
            fontsize=12,  # 调小字号
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )

        # 绘制“减排量”
        cbar.ax.text(
            0.47, 2.2,  # 调整位置
            "减排量",
            fontsize=10,
            fontproperties=font_simsun,  # 宋体
            ha='center', va='center', transform=cbar.ax.transAxes
        )

        # 绘制“（10³ t）”
        cbar.ax.text(
            0.63, 2.2,  # 调整位置
            "(",
            fontsize=10,
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )
        cbar.ax.text(
            0.69, 2.0,  # 上调位置
            "10",
            fontsize=10,
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )
        cbar.ax.text(
            0.755, 2.1,  # 上标位置调整
            "³",  # 上标数字3
            fontsize=12,
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )
        cbar.ax.text(
            0.79, 2.0,  # 调整位置
            " t",
            fontsize=10,
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )
        cbar.ax.text(
            0.83, 2.2,  # 调整位置
            ")",
            fontsize=10,
            fontproperties=font_times,  # Times New Roman
            ha='center', va='center', transform=cbar.ax.transAxes
        )

        # 保留边框，隐藏坐标刻度和标签
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # 设置标题
        # 修改标题字体（中文用宋体，年份用 Times New Roman）
        # 设置标题
        title_text_chinese = "湖北省江汉平原水稻碳减排量："
        year = os.path.basename(raster_path).split("_")[0]  # 提取年份

        # 清空默认标题
        ax.set_title("")

        # 添加中文部分标题（黑体）
        ax.text(
            0.45, 1.043,  # 标题左侧中文的位置
            title_text_chinese,
            fontproperties=font_heiti,
            fontsize=14,
            fontweight='bold',
            ha='center', va='center', transform=ax.transAxes
        )

        # 年份数字（Times New Roman）
        ax.text(
            0.78, 1.039,  # 年份数字位置，稍微右移，避免与“量”字重叠
            f"{year}",
            fontproperties=font_times,
            fontsize=14,
            fontweight='bold',
            color='black',
            ha='center', va='center',  # 垂直居中对齐
            transform=ax.transAxes
        )

        # 添加“年”字（黑体）
        ax.text(
            0.85, 1.043,  # 将“年”紧随年份数字后显示
            "年",
            fontproperties=font_heiti,
            fontsize=14,
            fontweight='bold',
            ha='center', va='center', transform=ax.transAxes
        )
        # ax.set_title("湖北省江汉平原水稻碳减排量："+os.path.basename(raster_path).split("_")[0]+"年", fontsize=14,fontweight='bold', pad=8)  # 调整标题与图像的距离)
        # ax.set_xlabel('Longitude')
        # ax.set_ylabel('Latitude')

        # 保存图片
        plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.03)
        plt.close()


# 遍历栅格文件并绘图
for tif_file in tif_files:
    raster_path = os.path.join(folder_path, tif_file)
    output_path = os.path.join(output_folder, f"{os.path.splitext(tif_file)[0]}.png")
    plot_raster_with_features(raster_path, output_path)

print(f"绘图完成，结果保存在 {output_folder} 文件夹中。")
