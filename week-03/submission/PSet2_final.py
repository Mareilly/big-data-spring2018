import pandas as pd
import numpy as np
import matplotlib.pylab as plt

%matplotlib inline


df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

# read in for PH
df = pd.read_csv('/Users/phoebe/Dropbox (MIT)/big-data/data/skyhook_2017-07.csv', sep=',')

df.head()
# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.head()
# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
    ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
    )
    ].index, inplace = True)
  else:
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)
df.head()

#PROBLEM 1 - Need I say this graph is gorgeous?!
## Agree! Love the color choice! - PH
by_date = df['count'].groupby(df['date_new']).sum()
by_date
by_date .plot.bar(title= 'GPS pings', color='#FFC222')


#PROBLEM #2

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
    df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
  else:
    df['hour'].replace(range(j, j + 24, 1), range(-5, 19, 1), inplace=True)
df.head()

#PROBLEM 3
df['time_date']=df['date_new']+pd.to_timedelta(df['hour'],unit='h')
df.head()

#PROBLEM 4
#Line Chart
df['count'].groupby(df['time_date']).sum().plot()

#Bar Chart
by_date = df['count'].groupby(df['hour']).sum()
by_date
by_date .plot.bar(title= 'GPS pings per hour', color='#FFC555')

#PROBLEM 5

by_date=df[df['time_date']=='2017-07-002T09:00:00.000000000']
by_date.plot.scatter(x='lat',y='lon',s=df['count']*0.5,alpha=0.3,title ="Scatterplot of latitude and longitude on July 2nd 2017 at 9:00")

by_date=df[df['time_date']=='2017-07-004T20:00:00.000000000']
by_date.plot.scatter(x='lat',y='lon',s=df['count']*0.5,alpha=0.3,title ="Scatterplot of latitude and longitude on July 4th 2017 at 20:00")


by_date=df[df['time_date']=='2017-07-0029T12:00:00.000000000']
by_date.plot.scatter(x='lat',y='lon',s=df['count']*0.5,alpha=0.3,title ="Scatterplot of latitude and longitude on July 29th 2017 at 12:00")

## Marissa, your 'maps' are lovely, but you have switched your lat and lon. x is lon and y is lat, so this will make interpreting your map difficult!


#PROBLEM 6 WOOOHOOO I MADE IT!
Scatterplot of latitude and longitude on Sunday, July 2st at 7am
This scatterplot reveals that the humans represented in this dataset live
in both in the suburbs and in the city of Boston. This is confirmed when
comparing the 9am weekend timestamp to the 12pm weekday timestamp.
A shortcoming of the data is that people are often on vacation in
July and are thus are not captured in this data set.
The visualization reveals that most people in the Boston area live
near the water. Coastal areas will be hit the hardest in the wake of
major storms and continued sea level rise and thus are vulnerable to climate change.

Scatterplot of latitude and longitude on July 4st at 8pm
This scatterplot reveals that people are gathering in specific locations
to watch the July 4th fireworks! A shortcoming of this data is that children
most likely do not have devices with GPS and are not accounted for in this dataset.
If children were accounted for, the GPS ping concentration at firework viewing
locations would be greater. This scatterplot reveals that some of the BostonArea’s
 most beloved firework viewing locations are near the water and thus
at risk of coastal flooding and storm surges.

Scatterplot of latitude and longitude on July 29st at 8pm

This scatterplot reveals that many people in the Boston Area travel
to the CBD to work during the weekday. This phenomenon becomes apparent
when comparing this scatterplot to the scatterplot from the weekend on July 2nd.
A shortcoming of the data is that people are often on vacation in July and are
are not captured in this data set. With climate change causing summers to be even
hotter, the heat island effect in urban areas is becoming more and more dangerous.
With thousands of people traveling to work in the CBD urban temperatures may
become a threat in the future.
