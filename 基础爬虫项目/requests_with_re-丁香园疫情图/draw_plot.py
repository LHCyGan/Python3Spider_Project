import numpy as np
import json
from pyecharts.charts import Line
from pyecharts import options as opts

# 读原始数据文件
datafile = 'statistics_data.json'
with open(datafile, 'r', encoding='UTF-8') as file:
    json_dict = json.loads(file.read())

# 分析各省份2月1日至今的新增确诊数据：'confirmedIncr'
statistics__data = {}
for province in json_dict:
    statistics__data[province] = []
    for da in json_dict[province]:
        if da['dateId'] >= 20200201:
            statistics__data[province].append(da['confirmedIncr'])

# 获取日期列表
dateId = [str(da['dateId'])[4:6] + '-' + str(da['dateId'])[6:8] for da in json_dict['湖北'] if
          da['dateId'] >= 20200201]

# 全国新增趋势
all_statis = np.array([0] * len(dateId))
for province in statistics__data:
    all_statis = all_statis + np.array(statistics__data[province])

all_statis = all_statis.tolist()
# 湖北新增趋势
hubei_statis = statistics__data['湖北']
# 湖北以外的新增趋势
other_statis = [all_statis[i] - hubei_statis[i] for i in range(len(dateId))]

line = Line()
line.add_xaxis(dateId)
line.add_yaxis("全国新增确诊病例",   #图例
                all_statis,       #数据
                is_smooth=True,   #是否平滑曲线
               linestyle_opts=opts.LineStyleOpts(width=4, color='#B44038'),#线样式配置项
               itemstyle_opts=opts.ItemStyleOpts(color='#B44038',          #图元样式配置项
                                                 border_color="#B44038",   #颜色
                                                 border_width=10))         #图元的大小
line.add_yaxis("湖北新增确诊病例", hubei_statis, is_smooth=True,
               linestyle_opts=opts.LineStyleOpts(width=2, color='#4E87ED'),
               label_opts=opts.LabelOpts(position='bottom'),              #标签在折线的底部
               itemstyle_opts=opts.ItemStyleOpts(color='#4E87ED',
                                                 border_color="#4E87ED",
                                                 border_width=3))
line.add_yaxis("其他省份新增病例", other_statis, is_smooth=True,
               linestyle_opts=opts.LineStyleOpts(width=2, color='#F1A846'),
               label_opts=opts.LabelOpts(position='bottom'),              #标签在折线的底部
               itemstyle_opts=opts.ItemStyleOpts(color='#F1A846',
                                                 border_color="#F1A846",
                                                 border_width=3))
line.set_global_opts(title_opts=opts.TitleOpts(title="新增确诊病例", subtitle='数据来源：丁香园'),
                     yaxis_opts=opts.AxisOpts(max_=16000, min_=1, type_="log",    #坐标轴配置项
                                              splitline_opts=opts.SplitLineOpts(is_show=True),#分割线配置项
                                              axisline_opts=opts.AxisLineOpts(is_show=True)))#坐标轴刻度线配置项
line.render(path='新增确诊趋势图.html')
