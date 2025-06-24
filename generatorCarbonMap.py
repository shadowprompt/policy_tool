import os
import geopandas as gpd
import rasterio
import json
import numpy as np
from rasterio._err import CPLE_OpenFailedError
from rasterio.errors import RasterioIOError
from shapely.geometry import Point, MultiPolygon, box
import random

# 文件夹路径
folder_path = "./files"
output_folder = "../../../policy/src/assets/carbon_output"
os.makedirs(output_folder, exist_ok=True)

# 读取.shp文件
# 已知SHP的坐标系EPSG:32649，TIFF的坐标系EPSG:4326
Jianghan_shp = 'jianghan_UTM.shp'
gdf = gpd.read_file(Jianghan_shp)
print("SHP 的坐标系:", gdf.crs)
gdf = gdf.to_crs('EPSG:4326')
print("SHP 的坐标系2:", gdf.crs)

# 准备地图数据
mapdata = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": row.NAME},  # 添加名称属性
            "geometry": geom.__geo_interface__
        }
        for geom, row in zip(gdf.geometry, gdf.itertuples(index=False))
    ]
}
# 保存geoJSON数据
with open('../../../policy/src/assets/carbon_MapData.json', 'w') as f:
    json.dump(mapdata, f)

# 获取文件夹中所有tif文件
tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

# Step 1: 计算所有栅格的统一最大最小值
global_min, global_max = np.inf, -np.inf

for tif_file in tif_files:
    tifPath = os.path.join(folder_path, tif_file)
    try:
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
    except FileNotFoundError:
        print(f"Error: File not found - {tifPath}")
        continue
    except CPLE_OpenFailedError as e:
        # 捕获特定于 rasterio 的 IO 错误
        print(f"无法识别文件格式或文件损坏: {tifPath}. 错误: {str(e)}")
        # 记录错误后，跳过当前文件，继续下一个
        continue
    except RasterioIOError as e:
        # 捕获特定于 rasterio 的 IO 错误
        print(f"无法识别文件格式或文件损坏: {tifPath}. 错误: {str(e)}")
        # 记录错误后，跳过当前文件，继续下一个
        continue
    except Exception as e:
        print('error', {str(e)})
        continue

print(f"统一的颜色范围：最小值 = {global_min}, 最大值 = {global_max}")


def get_tif_value(point, src):
    try:
        # 确保点在TIFF范围内
        # 获取TIFF边界并创建边界框
        bounds = src.bounds
        bbox = box(bounds.left, bounds.bottom, bounds.right, bounds.top)
        if not bbox.contains(point):
            return None

        # 计算窗口时添加边界缓冲
        row, col = src.index(point.x, point.y)
        window = rasterio.windows.Window(col_off=col - 1, row_off=row - 1, width=3, height=3)
        # window = rasterio.windows.from_bounds(
        #     *point.bounds, transform=src.transform)

        # 读取数据并处理NoData值
        data = src.read(1, window=window)
        # 获取NoData值并替换为NaN
        # 将像元值小于0的赋值为0
        # data[data < 0] = 0
        data = data / 1000000  #转化为千吨
        if data.size == 0:
            return 0
        # 处理NoData值
        if src.nodatavals and data[1][1] == src.nodatavals[0]:
            return 0

        if np.isnan(data[1][1]):
            return 0

        result_value = data[1][1]

        return result_value
    except Exception as e:
        print(f"Error reading point {point}: {str(e)}")
        return None


# 在写入JSON之前，将float32转换为Python float
def convert_float32(obj):
    if isinstance(obj, np.float32):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_float32(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_float32(v) for v in obj]
    return obj


def plot_raster_with_features(raster_path, output_path):
    # 读取.tif文件
    valid_data = []
    with rasterio.open(raster_path) as src:  # 提取每个多边形内的多个采样点
        for idx, row in gdf.iterrows():
            polygon = row['geometry']
            minx, miny, maxx, maxy = polygon.bounds
            print('gdf polygon:', idx, row.NAME, row.geometry.geom_type, minx, maxx, miny, maxy)
            # 在多边形内生成采样点
            points = []
            while len(points) < 10:  # 每个多边形生成10个采样点
                x = random.uniform(minx, maxx)
                y = random.uniform(miny, maxy)
                point = Point(x, y)
                if polygon.contains(point):
                    points.append(point)

            width = src.width
            height = src.height
            # 计算每个采样点的值
            for idx, point in enumerate(points):
                result = get_tif_value(point, src)
                if result:
                    valid_data.append({
                        "value": [point.x, point.y, result],
                        "name": f"Point_{row.NAME}_{idx}_{len(points)}"
                    })

    # 保存热力图数据
    with open(output_path, 'w') as f:
        valid_data = convert_float32(valid_data)
        json.dump(valid_data, f)


# 遍历栅格文件并绘图
for tif_file in tif_files:
    raster_path = os.path.join(folder_path, tif_file)
    output_path = os.path.join(output_folder, f"{os.path.splitext(tif_file)[0]}.json")
    try:
        plot_raster_with_features(raster_path, output_path)
    except Exception as e:
        print('error', {str(e)})

print(f"绘图完成，结果保存在 {output_folder} 文件夹中。")
