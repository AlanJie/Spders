import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

MASK_IMG = 'wawa.jpg'
FONT_PATH = 'font/simsun.ttc'
FILE_PATH = 'comments.txt'

with open(FILE_PATH, encoding='utf8') as f:
    comments = f.read()
    word_list = jieba.cut(comments, cut_all=True)
    wl = " ".join(word_list)
    print(wl)

