# -*- coding: utf-8 -*-

import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp import SnowNLP

def draw_word_cloud(word):
    words = jieba.cut(word)
    wordstr = " ".join(words)
    sw = set(STOPWORDS)
    wc = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
        max_words=300,
        max_font_size=70,
        stopwords=sw,
        background_color='white',
        scale=20,
    ).generate(wordstr)
    # 显示词云图 
    plt.imshow(wc.recolor())
    plt.axis("off")
    plt.show()

def analysis_text_expression(text):
    s = SnowNLP(text)
    print(text,'的情感倾向得分为' ,s.sentiments) 