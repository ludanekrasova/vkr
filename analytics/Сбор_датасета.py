#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import folium

# Данные по уникальным точкам
uniq_point = pd.read_csv('data/uniq_point.csv', sep = ',')

# Данные по регионам
df_region = pd.read_csv('data/df_region.csv', sep = ',')

# Статистика по точкам
df_points = pd.read_csv('data/df_points.csv', sep = ',')

# Внешеяя статистика по точкам
df_geo = pd.read_csv('data/df_geo.csv', sep = ',')


# Объединение в общий датасет
df = pd.merge(uniq_point, df_region, how='left', on=['Субъект']) 
df = pd.merge(df, df_points, how='left', on=['ap_mac']) 
df = pd.merge(df, df_geo, how='left', on=['ap_mac']) 


# Ранги
count_branch = ['Количество_торговля', 'Количество_бытовые', 'Количество_общепит', 'Количество_клубы',
                'Количество_медицина']
for col in count_branch:
    df[col+'_rank'] = df[col].rank(ascending=True)


money_branch = ['Выручка_торговля', 'Прибыль_торговля', 'Выручка_бытовые', 'Прибыль_бытовые', 'Выручка_общепит', 
                'Прибыль_общепит', 'Выручка_клубы', 'Прибыль_клубы', 'Выручка_медицина', 'Прибыль_медицина',
               'Население']
for col in money_branch:
    df[col+'_rank'] = df[col].rank(ascending=False)


df['crime_rank'] = df['На 100 тыс. жителей Всего преступлений'].rank(ascending=True)
df['money_rank'] = df['Доходы от НДФл, млн.р.'].rank(ascending=False)


count_point = ['hour_0', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 
               'hour_9', 'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 
               'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 'day_1', 'day_2',
               'day_3', 'day_4', 'day_5', 'day_6', 'day_7', 'device_count', 'device_nunique', 'device_frec', 
               'user_nunique', 'duration', 'duration_min', 'duration_max']
for col in count_point:
    df[col+'_rank'] = df[col].rank(ascending=False)


count_infrastr = ['toilet', 'metro', 'arenda']
for col in count_infrastr:
    df[col+'_rank'] = df[col].rank(ascending=True)

count_konkurent = ['riteil', 'service', 'club', 'med', 'vet', 'stomat']
for col in count_konkurent:
    df[col+'_rank'] = df[col].rank(ascending=False)


#['ap_mac', 'lat', 'lon']
cols = ['ap_mac', 'lat', 'lon'] + list(df.columns[69:])
df[cols].to_csv('data/df_rank.csv', index=False)
