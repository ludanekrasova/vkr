#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
import folium
import re
from folium import plugins

df_region = pd.read_csv('data/df_region.csv', sep = ',')
df_geo = pd.read_csv('data/df_geo.csv', sep = ',')

# Объединение в общий датасет
df = pd.merge(df_geo, df_region, how='left', on=['Субъект'])

# Ранги  

# По возрастанию - меньше конкурентов - лучше место
count_branch = ['Количество_торговля', 'Количество_бытовые', 'Количество_общепит', 'Количество_клубы',
                'Количество_медицина', 'barbers', 'spa', 'shoes', 'jewelry', 'foto', 'riteil', 'club', 'med', 
                'vet', 'stomat', 'alco', 'shop']
for col in count_branch:
    df[col+'_rank'] = df[col].rank(ascending=True, na_option='bottom')

# По убыванию. Если прибыль предприятий этой отрасли выше - место лучше
money_branch = ['Выручка_торговля', 'Прибыль_торговля', 'Выручка_бытовые', 'Прибыль_бытовые', 'Выручка_общепит', 
                'Прибыль_общепит', 'Выручка_клубы', 'Прибыль_клубы', 'Выручка_медицина', 'Прибыль_медицина']
for col in money_branch:
    df[col+'_rank'] = df[col].rank(ascending=False, na_option='top')

# Много людей и доходов - хорошо (по возрастанию), преступность плохо - по убыванию, дешевле недвижимость - лучше
df['crime_rank'] = df['Преступлений, на 100 тыс.чел.'].rank(ascending=True)
df['danger_rank'] = df['Экологическая опасность'].rank(ascending=True)
df['houseprise_rank'] = df['Продажа руб/кв.м.'].rank(ascending=True)
df['houseparenda_rank'] = df['Аренда руб/кв.м.'].rank(ascending=True)
df['money_rank'] = df['Доходы от НДФл, млн.р.'].rank(ascending=False)
df['people_rank'] = df['Население'].rank(ascending=False)

social_rank =['ЖКХ_ранг', 'Соседи_ранг', 'Условия для детей_ранг', 'Спорт и отдых_ранг', 'Магазины_ранг', 
              'Транспорт_ранг', 'Безопасность_ранг', 'Стоимость жизни_ранг', 'Чистота_ранг', 'Экология_ранг']

# По убыванию. Если пешеходов больше, камер и стоянок - место лучше
count_point = ['traffic', 'toilet', 'trash', 'metro', 'taxi', 'auto', 'light', 'video', 'keep', 'arenda']
for col in count_point:
    df[col+'_rank'] = df[col].rank(ascending=False)

rank_list = ['ap_mac', 'lat', 'lon', 'Количество_торговля_rank', 'Количество_бытовые_rank', 
             'Количество_общепит_rank', 'Количество_клубы_rank', 'Количество_медицина_rank',
             'Выручка_торговля_rank', 'Прибыль_торговля_rank', 'Выручка_бытовые_rank', 'Прибыль_бытовые_rank', 
             'Выручка_общепит_rank', 'Прибыль_общепит_rank', 'Выручка_клубы_rank', 'Прибыль_клубы_rank',
             'Выручка_медицина_rank', 'Прибыль_медицина_rank', 'barbers_rank', 'spa_rank', 'shoes_rank', 
             'jewelry_rank', 'foto_rank', 'riteil_rank', 'club_rank', 'med_rank', 'vet_rank', 'stomat_rank', 
             'alco_rank','shop_rank',
             'crime_rank', 'danger_rank', 'houseprise_rank', 'houseparenda_rank','money_rank', 'people_rank', 
             'traffic_rank', 'toilet_rank', 'trash_rank', 'metro_rank', 'taxi_rank', 'auto_rank', 'light_rank', 
             'video_rank', 'keep_rank', 'arenda_rank', 'ЖКХ_ранг', 'Соседи_ранг', 'Условия для детей_ранг', 
             'Спорт и отдых_ранг', 'Магазины_ранг', 'Транспорт_ранг', 'Безопасность_ранг', 'Стоимость жизни_ранг',
             'Чистота_ранг', 'Экология_ранг', 'Адрес']

df[rank_list].to_csv('data/df_rank.csv', index=False)