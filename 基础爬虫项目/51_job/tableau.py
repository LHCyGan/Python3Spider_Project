import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv(r"./new_job_info1.csv", engine="python")
df.sample(10)
df1 = df.groupby("工作地点").agg({"岗位名": "count"}).reset_index()
df1.sort_values(by="岗位名", axis=0,inplace=True,ascending=False)
df1[:10].to_excel(r"./不同工作地点的岗位数量.xlsx",encoding="gbk",index=None)


df = pd.read_excel(r"./new_job_info2.xlsx")
df["工作地点"] = df["工作地点"].apply(lambda x:x+"市")
df.to_excel(r"./new_job_info2.xlsx",encoding="gbk",index=None)


df = pd.read_excel(r"./热门岗位城市薪资水平的折线图.xlsx")
df.sample(10)
"""
df["工作地点"] == "深圳" | 
df["工作地点"] == "苏州" | 
df["工作地点"] == "广州" | 
df["工作地点"] == "北京" | 
df["工作地点"] == "上海" | 
df["工作地点"] == "成都" | 
df["工作地点"] == "长沙" | 
df["工作地点"] == "杭州" | 
df["工作地点"] == "南京" | 
df["工作地点"] == "武汉"
"""
df = df[df["工作地点"].isin(["深圳","苏州","广州","北京","上海","成都","长沙","杭州","南京","武汉"])]
df.to_excel(r"./热门岗位城市薪资水平的折线图.xlsx")