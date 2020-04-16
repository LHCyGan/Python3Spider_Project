import numpy as np
import pandas as pd
import re
import jieba
import warnings
warnings.filterwarnings("ignore")

df = pd.read_excel(r"new_job_info1.xlsx",encoding="gbk")
df

def get_word_cloud(data=None, job_name=None):
    words = []
    describe = data['工作描述'][data['岗位名'] == job_name].str[1:-1]
    describe.dropna(inplace=True)
    [words.extend(i.split(',')) for i in describe]
    words = pd.Series(words)
    word_fre = words.value_counts()
    return word_fre

zz = ['数据分析', '算法', '大数据','开发工程师', '运营', '软件工程','运维', '数据库','java',"测试"]
for i in zz:
    word_fre = get_word_cloud(data=df, job_name='{}'.format(i))
    word_fre = word_fre[1:].reset_index()[:100]
    word_fre["岗位名"] = pd.Series("{}".format(i),index=range(len(word_fre)))
    #word_fre.to_excel(r"G:\8泰迪\python_project\51_job\词云图\{}.xlsx".format(i), encoding="gbk", index=None)
    word_fre.to_csv(r"词云图\bb.csv", mode='a',index=False, header=None,encoding="gbk")

# ====================================================================
def get_word_cloud(data=None):
    words = []
    describe = data['工作描述'].str[1:-1]
    describe.dropna(inplace=True)
    [words.extend(i.split(',')) for i in describe]
    words = pd.Series(words)
    word_fre = words.value_counts()
    return word_fre


word_fre = get_word_cloud(data=df)
word = word_fre.reset_index()[:5000]
word.to_excel(r"词云图.xlsx",encoding="gbk",index=None)



x  = pd.read_csv(r"词云图\bb.csv", encoding='GBK',engine="python")
x["热词"] = x["热词"].apply(lambda x:x[2:-1])
x.to_excel(r"词云图\bb.xlsx", encoding="gbk", index=None)





































