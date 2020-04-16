import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

def preprocess():
    df = pd.read_csv("./lagou.csv")
    # print(df.head())

    Salary = df['薪金'].values
    # print(Salary)
    Salary = [eval(s.replace('-', '+').replace('k', '000'))/2. for s in Salary]
    # print(Salary)
    df['SALARY'] = Salary
    # print(df.head(2))
    df['公司名称'] = df.drop_duplicates('公司名称', keep='first')
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    # print(df.head(2))
    company = df['公司名称'].values.tolist()
    zip_ = sorted(list(zip(company, Salary)), key=lambda x:x[1], reverse=True)
    return zip_

def draw():
    zip_ = preprocess()
    print(zip_[:20])
    c = (
        Pie()
            .add("", [list(z) for z in zip_[:20]],
                 radius=["10%", "100%"])
            .set_global_opts(title_opts=opts.TitleOpts(title="全国疫情统计"),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="100%", orient="vertical"), )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("lg_pythonSpider.html")
    )

if __name__ == '__main__':
    draw()