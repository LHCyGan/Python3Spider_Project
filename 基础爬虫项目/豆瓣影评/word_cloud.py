from wordcloud import WordCloud
import codecs
import jieba
from PIL import Image
import os
import re
import numpy as np
import matplotlib.pyplot as plt

def draw_wordcloud():
        f = open('./comments.txt', 'r', encoding='utf8')
        text = []
        for i in f.readlines():
            if len(i) <= 1:
                continue
            text.append(i.strip().strip('\n').replace(',', '').replace('，', '').replace('。', ''))
        print(len(text))

        string = "".join(text)
        data = jieba.lcut(string, cut_all=True)
        print(data)
        # 读取背景图片
        color_mask = Image.open('./1.png')
        color_mask = np.asanyarray(color_mask)
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

        word_cloud = cloud.generate(str(data))

        word_cloud.to_file("db_cloud.png") #保存图片
        #  显示词云图片
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
        draw_wordcloud()