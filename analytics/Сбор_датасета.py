#!/usr/bin/env python
# coding: utf-8

# In[91]:


import pandas as pd
import numpy as np
import folium


# In[92]:


# Данные по уникальным точкам
uniq_point = pd.read_csv('data/uniq_point.csv', sep = ',')
uniq_point.head(2)


# In[93]:


# Данные по регионам
df_region = pd.read_csv('data/df_region.csv', sep = ',')
df_region.head(2)


# In[94]:


# Статистика по точкам
df_points = pd.read_csv('data/df_points.csv', sep = ',')
df_points.head(2)


# In[95]:


# Внешеяя статистика по точкам
df_geo = pd.read_csv('data/df_geo.csv', sep = ',')
df_geo.head(2)


# Объединение в общий датасет

# In[96]:


df = pd.merge(uniq_point, df_region, how='left', on=['Субъект']) 
df = pd.merge(df, df_points, how='left', on=['ap_mac']) 
df = pd.merge(df, df_geo, how='left', on=['ap_mac']) 
df.head(2)


# Ранги

# In[97]:


count_branch = ['Количество_торговля', 'Количество_бытовые', 'Количество_общепит', 'Количество_клубы',
                'Количество_медицина']
for col in count_branch:
    df[col+'_rank'] = df[col].rank(ascending=True)


# In[98]:


money_branch = ['Выручка_торговля', 'Прибыль_торговля', 'Выручка_бытовые', 'Прибыль_бытовые', 'Выручка_общепит', 
                'Прибыль_общепит', 'Выручка_клубы', 'Прибыль_клубы', 'Выручка_медицина', 'Прибыль_медицина',
               'Население']
for col in money_branch:
    df[col+'_rank'] = df[col].rank(ascending=False)


# In[99]:


df['crime_rank'] = df['На 100 тыс. жителей Всего преступлений'].rank(ascending=True)
df['money_rank'] = df['Доходы от НДФл, млн.р.'].rank(ascending=False)


# In[100]:


count_point = ['hour_0', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 
               'hour_9', 'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 
               'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 'day_1', 'day_2',
               'day_3', 'day_4', 'day_5', 'day_6', 'day_7', 'device_count', 'device_nunique', 'device_frec', 
               'user_nunique', 'duration', 'duration_min', 'duration_max']
for col in count_point:
    df[col+'_rank'] = df[col].rank(ascending=False)


# In[101]:


count_infrastr = ['toilet', 'metro', 'arenda']
for col in count_infrastr:
    df[col+'_rank'] = df[col].rank(ascending=True)


# In[102]:


count_konkurent = ['riteil', 'service', 'club', 'med', 'vet', 'stomat']
for col in count_konkurent:
    df[col+'_rank'] = df[col].rank(ascending=False)


# In[106]:


#['ap_mac', 'lat', 'lon']
cols = ['ap_mac', 'lat', 'lon'] + list(df.columns[69:])
df[cols].to_csv('data/df_rank.csv', index=False)


# Проверка работы на рангах по умолчанию

# In[104]:


default_col = ['Выручка_торговля_rank','day_1_rank', 'day_2_rank', 'day_3_rank', 'day_4_rank', 'day_5_rank', 
               'day_6_rank', 'day_7_rank', 'device_count_rank', 'device_nunique_rank', 'device_frec_rank',
               'user_nunique_rank', 'duration_rank', 'duration_min_rank', 'duration_max_rank', 'toilet_rank', 
               'metro_rank']
df['rank'] = df[default_col].mean(axis=1)


# In[105]:


df[['ap_mac', 'lat', 'lon', 'rank']].sort_values(by='rank', ascending=True)


# In[ ]:





# In[16]:




# Создание карты
m = folium.Map(location=[55.753215, 37.622504], zoom_start=10)

# Фильтрация по отрасли кафе
df_cafe = df[df['Количество_общепит'] > 0]

# Выбор 10 случайных точек
df_random = df_cafe.sample(n=10, random_state=42)

# Ограничение количества строк до 10
df_top10 = df_cafe.head(10)


# Добавление маркеров на карту
for i, row in df_top10.iterrows():
    lat, lon = row['lat'], row['lon']
    rank = row['Выручка_общепит_rank']
    color = 'red' if rank <= 10 else 'orange' if rank <= 50 else 'green' if rank <= 100 else 'blue'
    folium.Marker([lat, lon], icon=folium.Icon(color=color), tooltip=row['ap_mac']).add_to(m)

# Вывод карты
m


# In[ ]:




