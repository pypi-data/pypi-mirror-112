# -*- coding: utf-8 -*-

import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
def draw_word_cloud(word,sw=''):
    words = jieba.cut(word)
    wordstr = " ".join(words)
    sw = set(STOPWORDS)
    sw.add(sw)
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
   # 保存词云图
    wc.to_file('result_1.jpg')
 
if __name__ == "__main__":
    with open("E://Download//7.txt", "rb") as f:#文本内容
        word = f.read()
    draw_word_cloud(word)