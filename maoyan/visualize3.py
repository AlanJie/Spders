import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
colors1 = '#6D6D6D'
font_song = FontProperties(fname=r'font\simsun.ttc', size=8)

plt.style.use('ggplot')
fig = plt.figure(figsize=(8, 6))

df = pd.read_csv('top100.csv', encoding='utf-8', header=None, names=columns, index_col='index')

df['year'] = df['time'].map(lambda x: x.split('-')[0])
grouped_year = df.groupby('year')
grouped_year_amount = grouped_year.year.count()
top_year = grouped_year_amount.sort_values(ascending=False)

# print(top_year.index)
# print('#' * 30)
# print(top_year.values)
top_year.plot(kind='bar', color='orangered')
for x, y in enumerate(top_year.values):
    plt.text(x, y+0.1, '%s'%round(y,1), ha='center', color=colors1)
plt.xticks(rotation=90)
plt.xlabel('年份(年)', fontproperties=font_song)
plt.ylabel('数量(部)', fontproperties=font_song)
plt.title('电影数量年份排名', fontproperties=font_song)

plt.tight_layout()
plt.savefig('电影数量排名(年份).png')
plt.show()
