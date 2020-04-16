from pyecharts.charts import Pie
from pyecharts import options as ops

f = open('PF.txt', 'r', encoding='utf8')
l = []
for i in f.readlines():
    l.append(i.strip('\n'))
print(l)

data = []
for s in l:
    data.append(s.replace("%", '').split('\t'))

data = [[d[0], float(d[1])] for d in data]
print(data)
c = (
    Pie()
    .add("", [z for z in data], radius=['30', '200'])
    .set_global_opts(title_opts=ops.TitleOpts(title='评分'))
    .set_series_opts(label_opts=ops.LabelOpts(formatter='{b}:{c}'))
    .render('./pf.html')
)
