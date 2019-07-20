import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib.font_manager import FontProperties


font_song = FontProperties(fname=r"font\simsun.ttc", size=15)

plt.style.use('ggplot')
fig = plt.figure(figsize=(8, 6))
colors1 = '#6D6D6D'

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
# index_col='index'  将索引设置为 index
df = pd.read_csv('top100.csv', encoding='utf-8', header=None, names=columns, index_col='index')

df_score = df.sort_values('score', ascending=False)

name1 = df_score.name[:10]
score1 = df_score.score[:10]

# 用 range() 能够保持x轴的正确顺序
plt.bar(range(10), score1, tick_label=name1)

plt.ylim((9, 9.8))
plt.title('top 100', color=colors1)
plt.xlabel('moive name')
plt.ylabel('score')

# 为每个条形图添加数值标签
for x, y in enumerate(list(score1)):
    plt.text(x, y+0.01, f'{round(y, 1)}', ha='center', color=colors1)

plt.xticks(rotation=90, fontproperties=font_song)
# 自动控制空白边缘，以显示全部 x 轴名称
plt.tight_layout()
plt.savefig('top100.png')
plt.show()
