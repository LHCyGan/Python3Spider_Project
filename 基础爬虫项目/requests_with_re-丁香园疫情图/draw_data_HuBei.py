import json
import datetime
from pyecharts.charts import Map
from pyecharts import options as opts

# 读原始数据文件
today = datetime.date.today().strftime('%Y_%m_%d')   #20200315
datafile = today + '.json'
with open(datafile, 'r', encoding='UTF-8') as file:
    json_array = json.loads(file.read())

# 分析湖北省实时确诊数据
# 读入规范化的城市名称，用于规范化丁香园数据中的城市简称
with open('pycharts_city.txt', 'r', encoding='UTF-8') as f:
    defined_cities = [line.strip() for line in f.readlines()]


def format_city_name(name, defined_cities):
    for defined_city in defined_cities:
        if len((set(defined_city) & set(name))) == len(name):
            name = defined_city
            if name.endswith('市') or name.endswith('区') or name.endswith('县') or name.endswith('自治州'):
                return name
            return name + '市'
    return None


province_name = '湖北'
for province in json_array:
    if province['provinceName'] == province_name or province['provinceShortName'] == province_name:
        json_array_province = province['cities']
        hubei_data = [(format_city_name(city['cityName'], defined_cities), city['confirmedCount']) for city in
                      json_array_province]
        hubei_data = sorted(hubei_data, key=lambda x: x[1], reverse=True)

        print(hubei_data)

labels = [data[0] for data in hubei_data]
counts = [data[1] for data in hubei_data]
pieces = [
    {'min': 10000, 'color': '#540d0d'},
    {'max': 9999, 'min': 1000, 'color': '#9c1414'},
    {'max': 999, 'min': 500, 'color': '#d92727'},
    {'max': 499, 'min': 100, 'color': '#ed3232'},
    {'max': 99, 'min': 10, 'color': '#f27777'},
    {'max': 9, 'min': 1, 'color': '#f7adad'},
    {'max': 0, 'color': '#f7e4e4'},
]

m = Map()
m.add("累计确诊", [list(z) for z in zip(labels, counts)], '湖北')
m.set_series_opts(label_opts=opts.LabelOpts(font_size=12),
                  is_show=False)
m.set_global_opts(title_opts=opts.TitleOpts(title='湖北省实时确诊数据',
                                            subtitle='数据来源：丁香园'),
                  legend_opts=opts.LegendOpts(is_show=False),
                  visualmap_opts=opts.VisualMapOpts(pieces=pieces,
                                                    is_piecewise=True,
                                                    is_show=True))
m.render(path='湖北省实时确诊数据.html')
