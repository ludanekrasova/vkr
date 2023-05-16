#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Май - координаты и проходимость
df_05 = pd.read_csv('data/2021-05-01_low.csv.zip', parse_dates=['ts'])

# Районы Москвы
region = gpd.read_file('data/mo-shape/mo.shp')
region.rename(columns={'NAME': "Субъект"}, inplace = True)

# Продолжительность
df_05_1 = pd.read_csv('data/duraion_2021-05-01_low.csv.zip', parse_dates=['ts'])


# ### Список точек с координатами и регионом

ap_uniq = df_05.drop_duplicates(subset=['ap_mac'])
ap_uniq['location'] = ap_uniq['gps'].map(lambda x: [x for x in str(x).strip('(').strip(')').split(",")])
ap_uniq['lat'] = (ap_uniq['location'].str[0]).astype(float)
ap_uniq['lon'] = (ap_uniq['location'].str[1]).astype(float)
ap_uniq['geometry'] = ap_uniq.location.apply(lambda x: Point(float(x[1]), float(x[0])))
ap_uniq.drop(['ts', 'device_id', 'user_id', 'gps', 'location'], axis=1, inplace = True)


ap_point = gpd.GeoDataFrame({"ap_mac" : ap_uniq.ap_mac, "lat" : ap_uniq.lat, "lon" : ap_uniq.lon,
                             "geometry": ap_uniq.geometry})


# left_join "within" 
merging = gpd.sjoin(ap_point, region, how="left", op="within")


# Сохранение для анализа
merging[['ap_mac', 'lat', 'lon', 'Субъект']].to_csv('data/uniq_point.csv', index=False)


# ### Статистики по точкам

# Группировка по часовым инервалам
df_05['day'] = df_05['ts'].dt.day  #Понедельник 0
df_05['day_week'] = df_05['ts'].dt.dayofweek
df_05['hour'] = df_05['ts'].dt.hour
df_05['count']=1
df_05.head(2)


df_05_hour = df_05[['ap_mac', 'day', 'day_week', 'hour', 'count']].groupby(['ap_mac', 'day', 'day_week','hour']).agg('count').reset_index()
df_05_hour.head(2)


# Среднее в час
hour_count = pd.pivot_table(df_05_hour, values='count', index=['ap_mac'], columns=['hour'], aggfunc='mean')#
hour_count.columns = ['hour_' + str(i) for i in range(0, 24)] 
hour_count.reset_index(inplace=True)
hour_count.head(2)


# Группировка по дням
df_05_day = df_05[['ap_mac', 'day', 'day_week', 'count']].groupby(['ap_mac', 'day', 'day_week',]).agg('count').reset_index()

# Среднее в день недели 1 - понедельник, 7 -воскресенье
week_count = pd.pivot_table(df_05_day, values='count', index=['ap_mac'], columns=['day_week'], aggfunc='mean')
week_count.columns = ['day_' + str(i) for i in range(1, 8)] 
week_count.reset_index(inplace=True)

# Группировка по пользователям
df_05_user = df_05.groupby(['ap_mac']).agg(device_count=('device_id', 'count'),
                                           device_nunique = ('device_id', 'nunique'),
                                           ).reset_index()
df_05_user['device_frec']=df_05_user['device_count']/df_05_user['device_nunique']

# Группировка по продолжительности
def q1(x):
    return x.quantile(0.05)

def q2(x):
    return x.quantile(0.95)

df_05_dur = df_05_1.groupby(['ap_mac']).agg(user_nunique=('user_id', 'nunique'),
                                            duration = ('duration', 'median'),
                                            duration_min = ('duration', q1),
                                            duration_max = ('duration', q2),
                                           ).reset_index()



# Объединение статистики по трафику
df_points = pd.merge(hour_count, week_count, how='left', on=['ap_mac']) 
df_points = pd.merge(df_points, df_05_user, how='left', on=['ap_mac']) 
df_points = pd.merge(df_points, df_05_dur, how='left', on=['ap_mac']) 
df_points.head(2)

df_points.to_csv('data/df_points.csv', index=False)

