import cufflinks as cf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

plt.style.use('ggplot')
fig = plt.figure(figsize=(8, 6))

font_song = FontProperties(fname=r"font\simsun.ttc", size=8)
colors1 = '#6D6D6D'

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
# index_col='index'  将索引设置为 index
df = pd.read_csv('top100.csv', encoding='utf-8', header=None, names=columns, index_col='index')

area_count = df.groupby(by='area').area.count().sort_values(ascending=False)
area_count.plot.bar(color='#4652B1')

for x,y in enumerate(list(area_count.values)):
    plt.text(x, y+0.5, '%s' % (round(y, 1)), ha='center', color=colors1)

# plt.bar(np.arange(len(area_count.index)), area_count.values, tick_label=area_count.index)
plt.xticks(rotation=0, fontproperties=font_song)
plt.xlabel('国家/地区', fontproperties=font_song)
plt.ylabel('数量(部)', fontproperties=font_song)
plt.title('各国家/地区电影数量分布', fontproperties=font_song)
plt.tight_layout()
plt.savefig('各国(地区)电影数量分布.png')
plt.show()
