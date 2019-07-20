import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
colors1 = '#6D6D6D'
font_song = FontProperties(fname=r'font\simsun.ttc', size=10)

plt.style.use('ggplot')
fig = plt.figure(figsize=(8, 6))

df = pd.read_csv('top100.csv', encoding='utf-8', header=None, names=columns, index_col='index')

starlist = []
star_total = df.star
for i in df.star.str.replace(' ', '').str.split(','):
    starlist.extend(i)

# print(starlist)
# print(len(starlist))

# 去重
starall = set(starlist)
# print(starall)
# print(len(starall))

starall2 = {}
for i in starall:
    if starlist.count(i) > 1:
        starall2[i] = starlist.count(i)

starall2 = sorted(starall2.items(), key=lambda starlist:starlist[1], reverse=True)

starall2 = dict(starall2[:10])

x_star = list(starall2.keys())
y_star = list(starall2.values())

plt.bar(range(10), y_star, tick_label=x_star)
plt.xticks(rotation=90)
for x,y in enumerate(y_star):
    plt.text(x, y+0.1, '%s'%round(y, 1), ha='center', color=colors1)

plt.title('演员电影作品数量排名', fontproperties=font_song)
plt.xlabel('演员', fontproperties=font_song)
plt.ylabel('数量(部)', fontproperties=font_song)
plt.xticks(fontproperties=font_song)
plt.tight_layout()
plt.savefig('演员作品数量排名.png')
plt.show()
