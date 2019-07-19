import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

MASK_IMG = 'apple.jpg'
FONT_PATH = 'font/simsun.ttc'
FILE_PATH = 'comments.txt'

def cut_word():
    with open(FILE_PATH, encoding='utf8') as f:
        comments = f.read()
        word_list = jieba.cut(comments, cut_all=True)
        wl = " ".join(word_list)
        print(wl)
        return wl

def create_word_cloud():
    img_mask = np.array(Image.open(MASK_IMG))
    wc = WordCloud(background_color='white', max_words=2000, mask=img_mask,
        scale=4, max_font_size=50, random_state=2019, font_path=FONT_PATH)

    wc.generate(cut_word())
    plt.axis('off')
    plt.imshow(wc, interpolation='bilinear')
    plt.savefig('apple_wc.jpg')
    plt.show()

if __name__ == '__main__':
    create_word_cloud()
