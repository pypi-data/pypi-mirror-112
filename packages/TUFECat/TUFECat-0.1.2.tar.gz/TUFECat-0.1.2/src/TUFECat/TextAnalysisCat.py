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
    if s.sentiments <= 0.4:
        commment = '表现为消极情绪倾向'
    elif s.sentiments > 0.4 and s.sentiments <= 0.6:
        commment = '表现为中立情绪倾向'
    else:
        commment = '表现为积极情绪倾向'
    print('该文本的情感倾向得分为：' ,s.sentiments,commment) 