from wordcloud import WordCloud
import codecs
import jieba
import os
from scipy.misc import imread
# from PIL import Image
# Image.open()
import csv
import re
import matplotlib.pyplot as plt

def draw_wordcloud():
        f = open('./qiushi.csv', 'r', encoding='utf8')
        reader = csv.reader(f)
        text = [r for r in reader]
        text = [t[0].strip('(').strip(')').strip(',').replace('。', ' ').replace('？', ' ').strip(' ')
                for t in text if len(t) != 0]
        text = [re.sub(r'[\'\'\！\，\：\“\”]', ' ', t) for t in text]
        text = [t.strip(' ').replace(' ', '') for t in text]

        text = ''.join(text)
        # print(text)
        string = jieba.lcut(text, cut_all=True)
        print(string)
        # 读取背景图片
        color_mask = imread("./1.png")
        cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        font_path="data/simhei.ttf",
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='black',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=40
        )

        word_cloud = cloud.generate(str(string))

        word_cloud.to_file("qsbk_cloud.png") #保存图片
        #  显示词云图片
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
        draw_wordcloud()