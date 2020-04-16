from pyecharts import options as opts
from pyecharts.charts import Pie
import json



with open('./statistics_data.json', 'r', encoding='utf-8') as f:
    json_data = json.loads(f.read())

# print(json_data.keys())
# print(json_data['湖北'][-1]['confirmedCount'])
names = json_data.keys()
values = [json_data[nm][-1]['confirmedCount'] for nm in names]
zip_ = sorted(list(zip(names, values)), key=lambda x:x[1], reverse=True)
print(zip_)
c = (
    Pie()
    .add("", [list(z) for z in zip_],
         radius=["5%", "100%"])
    .set_global_opts(title_opts=opts.TitleOpts(title="全国疫情统计"),
                     legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),)
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("pie_base.html")
)
