import pandas as pd
import numpy as np
import matplotlib.pylab as plt
%matplotlib inline
df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')
df.head()
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.head()
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)
df.head()

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
    df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
  else:
    df['hour'].replace(range(j, j + 24, 1), range(-5, 19, 1), inplace=True)


df.head()
x = [datetime.datetime(2017, 12, 1, 10, 0),
    datetime.datetime(2017, 1, 4, 9, 0),
    datetime.datetime(2017, 5, 5, 9, 0)]
y = [boston, massachusetts]

ax = plt.subplot(111)
ax.bar(x, y, width=10)
ax.xaxis_date()

plt.show()
# Probelm 2 Notes
.replace (val1, val2, inplace) #replace all instances of this range of values with this other range of values
3 USE SIMILAR CODE STRUCTURE FOR WHATS GIVEN above
