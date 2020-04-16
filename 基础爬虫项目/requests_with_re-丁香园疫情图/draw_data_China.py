import json
import datetime
from pyecharts.charts import Map
from pyecharts import options as opts

# 读原始数据文件
today = datetime.date.today().strftime('%Y_%m_%d')   #20200315
datafile = today + '.json'
with open(datafile, 'r', encoding='UTF-8') as file:
    json_array = json.loads(file.read())

# 分析全国实时确诊数据：'confirmedCount'字段
china_data = []
for province in json_array:
    china_data.append((province['provinceShortName'], province['confirmedCount']))
china_data = sorted(china_data, key=lambda x: x[1], reverse=True)                 #reverse=True,表示降序，反之升序

print(china_data)
# 全国疫情地图
# 自定义的每一段的范围，以及每一段的特别的样式。
pieces = [
    {'min': 10000, 'color': '#540d0d'},
    {'max': 9999, 'min': 1000, 'color': '#9c1414'},
    {'max': 999, 'min': 500, 'color': '#d92727'},
    {'max': 499, 'min': 100, 'color': '#ed3232'},
    {'max': 99, 'min': 10, 'color': '#f27777'},
    {'max': 9, 'min': 1, 'color': '#f7adad'},
    {'max': 0, 'color': '#f7e4e4'},
]
labels = [data[0] for data in china_data]
counts = [data[1] for data in china_data]

m = Map()
m.add("累计确诊", [list(z) for z in zip(labels, counts)], 'china')

#系列配置项,可配置图元样式、文字样式、标签样式、点线样式等
m.set_series_opts(label_opts=opts.LabelOpts(font_size=12),
                  is_show=False)
#全局配置项,可配置标题、动画、坐标轴、图例等
m.set_global_opts(title_opts=opts.TitleOpts(title='全国实时确诊数据',
                                            subtitle='数据来源：丁香园'),
                  legend_opts=opts.LegendOpts(is_show=False),
                  visualmap_opts=opts.VisualMapOpts(pieces=pieces,
                                                    is_piecewise=True,   #是否为分段型
                                                    is_show=True))       #是否显示视觉映射配置
#render（）会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件，也可以传入路径参数，如 m.render("mycharts.html")
m.render(path='./全国实时确诊数据.html')
