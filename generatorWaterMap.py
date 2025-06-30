import os
import json

import shapefile


def data_map(data):
    str0 = str(data[0])
    str1 = str(data[1])
    return [str0, str1] + (data[2:])


current = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(current, './water.shp')
# 打开Shapefile
sf = shapefile.Reader(filepath)

# # 获取几何体和属性信息
shapes = sf.shapes()  # 几何体列表
records = sf.records()  # 属性记录列表（字典形式）
records = [data_map(record) for record in records]  # 将记录转换为字典列表
fields = sf.fields[1:]  # 字段描述，第一个字段是删除标记，通常忽略
json_data = json.dumps(records, indent=4)
json_file_path = os.path.join(current, '../policy_vue/src/assets/water_mapData.json')
with open(json_file_path, "w", encoding='utf-8') as fb:
    fb.write(json_data)
    print(f"water datamap json结果保存在 {json_file_path} 文件。")
    print(f"water map json通过在线生成geoJson。")
