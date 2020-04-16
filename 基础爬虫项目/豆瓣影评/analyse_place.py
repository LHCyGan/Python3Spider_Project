from collections import Counter
from pyecharts.charts import Map
from pyecharts import options as opts

f = open('./place.csv', 'r', encoding='utf8')
l = list()
for i in f.readlines():
    if len(i) >= 4:
        i = i[:2]
    l.append(i.strip('\n'))
print(l)
data = Counter(l)
print(list(data.items()))
data_ = list(data.items())
c = (
    Map()
    .add("", [list(z) for z in data_], 'china')
    .set_global_opts(opts.TitleOpts(title="评论分布图"),
                     visualmap_opts=opts.VisualMapOpts(max_=200))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .render("./map.html")
)

