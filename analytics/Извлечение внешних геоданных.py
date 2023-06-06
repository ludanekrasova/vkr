#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Данные по уникальным точкам
uniq_point = pd.read_csv('data/df_points.csv', sep = ',')

# Точки
X_zone = uniq_point[['lat','lon']].values

# Функция для нахождения ближайших точек в радиусе
def r_neighbors(X_train, r=0.01): #0.01 - 1 км
    neigh = NearestNeighbors(n_neighbors=10, radius=r)
    neigh.fit(X_train)
    distances, indexes = neigh.radius_neighbors(X_zone, r)
    return np.array([len(x) for x in indexes])

def get_coord(col):
    # Выбор текста в []
    try:
        coord = col.split('[', 1)[1].split(']')[0]
        return coord
    except:
        return '0, 0'


### Косвенная оценка пешеходного траффика  

# Санитарные удобства
toilet = pd.read_csv('raw/геоданные/842_norm/842.csv', sep = ';', index_col=0)
toilet.columns = ['ADDRESS', 'REGIME', 'AVAILABIL', 'LON', 'LAT', 'GLOBALID']
toilet['LON'] = toilet['LON'].str.replace("'", "").str.replace(",", ".").astype(float)
toilet['LAT'] = toilet['LAT'].str.replace("'", "").str.replace(",", ".").astype(float)
uniq_point['toilet'] = r_neighbors(toilet[['LAT', 'LON']].values, r=0.01)

# Контейнеры для отходов
col_list=['Code', 'YardArea', 'Coordinates']
trash = pd.read_excel('raw/геоданные/data-54571-2020-08-17.xlsx', index_col=None, engine='openpyxl')[col_list]
# Разбиение кооординаты на широту и долготу
temp = trash['Coordinates'].str.split(',', 1 , expand=True)
trash['lat'] = temp[1].astype(float)
trash['lon'] = temp[0].astype(float)
trash.drop(columns = ['Coordinates'], axis=1, inplace=True)
trash.head()
uniq_point['trash'] = r_neighbors(trash[['lat', 'lon']].values, r=0.01)

# Станции метро
metro = pd.read_csv('raw/геоданные/624_norm/624.csv', sep = ';', index_col=0)
uniq_point['metro'] = r_neighbors(metro[['LAT', 'LON']].values, r=0.01)

# Парковки такси
col_list = ['Локальный идентификатор', 'Долгота в WGS-84', 'Широта в WGS-84', 'Количество парковочных мест']
df_taxi = pd.read_csv('raw/геоданные/data-621-2999-01-01.csv', sep = ';', skiprows=[0], index_col=None)[col_list]
uniq_point['taxi'] = r_neighbors(df_taxi[['Широта в WGS-84', 'Долгота в WGS-84']].values, r=0.01)

# Парковки авто платные
col_list = ['Локальный идентификатор', 'Долгота в WGS-84', 'Широта в WGS-84', 'Общее количество парковочных мест']
df_auto = pd.read_csv('raw/геоданные/data-623-2999-01-01.csv', sep = ';', skiprows=[0], index_col=None)[col_list]
uniq_point['auto'] = r_neighbors(df_auto[['Широта в WGS-84', 'Долгота в WGS-84']].values, r=0.01)

# Фонари
col_list = ['global_id', 'geoData', 'Количество светильников']
df_light = pd.read_csv('raw/геоданные/data-61762-2999-01-01.csv', sep = ';', skiprows=[0], index_col=None)[col_list]
# Разбиение кооординат на широту и долготу
df_light['Coordinates'] = df_light['geoData'].apply(get_coord)
temp = df_light['Coordinates'].str.split(',', 1 , expand=True)
df_light['lat'] = temp[1].astype(float)
df_light['lon'] = temp[0].astype(float)
df_light.drop(columns = ['Coordinates', 'geoData'], axis=1, inplace=True)
uniq_point['light'] = r_neighbors(df_light[['lat', 'lon']].values, r=0.01)

# Камеры наблюдения 
col_list = ['Код', 'geoData']
df_video = pd.read_csv('raw/геоданные/data-2386-2999-01-01.csv', sep = ';', skiprows=[0], index_col=None)[col_list]
# Разбиение кооординат на широту и долготу
df_video['Coordinates'] = df_video['geoData'].apply(get_coord)
temp = df_video['Coordinates'].str.split(',', 1 , expand=True)
df_video['lat'] = temp[1].astype(float)
df_video['lon'] = temp[0].astype(float)
df_video.drop(columns = ['Coordinates', 'geoData'], axis=1, inplace=True)
uniq_point['video'] = r_neighbors(df_video[['lat', 'lon']].values, r=0.01)

# Пункты охраны правопорядка
col_list = ['Локальный идентификатор', 'geoData']
df_keep = pd.read_csv('raw/геоданные/data-1661-2999-01-01.csv', encoding='windows-1251', sep = ';', 
                      skiprows=[0], index_col=None)[col_list]
# Разбиение кооординат на широту и долготу
df_keep['Coordinates'] = df_keep['geoData'].apply(get_coord)
temp = df_keep['Coordinates'].str.split(',', 1 , expand=True)
df_keep['lat'] = temp[1].astype(float)
df_keep['lon'] = temp[0].astype(float)
df_keep.drop(columns = ['Coordinates', 'geoData'], axis=1, inplace=True)
uniq_point['keep'] = r_neighbors(df_keep[['lat', 'lon']].values, r=0.01)


# Проверка наличия свободных нежилых помещений
# Объекты для аренды
arenda = pd.read_csv('raw/геоданные/1113_norm/1113.csv', sep = ';', index_col=0)
uniq_point['arenda'] = r_neighbors(arenda[['LAT', 'LON']].values, r=0.05)

# Проверка наличия рядом конкурентов. Много конкурентов - ранг точки ниже
# Объекты с лицензией на продажу алкоголя
col_list=['ID', 'geoData']
alco = pd.read_excel('raw/геоданные/data-586-2999-01-01.xlsx', index_col=None, skiprows=[1], engine='openpyxl')[col_list]
# Разбиение кооординат на широту и долготу
alco['Coordinates'] = alco['geoData'].progress_apply(get_coord)
temp = alco['Coordinates'].str.split(',', 1 , expand=True)
alco['lat'] = temp[1].astype(float)
alco['lon'] = temp[0].astype(float)
alco.drop(columns = ['geoData', 'Coordinates'], axis=1, inplace=True)
uniq_point['alco'] = r_neighbors(alco[['lat', 'lon']].values, r=0.01)

# Все торговые точки
col_list=['ID', 'TypeService', 'TypeObject', 'geoData']
shop = pd.read_csv('raw/геоданные/data-3304-2022-10-04.csv', encoding='windows-1251', sep = ';', index_col=None, 
                   skiprows=[1])[col_list]
# Только продовольственные
shop=shop[shop['TypeService']=='реализация продовольственных товаров']
# Разбиение кооординат на широту и долготу
shop['Coordinates'] = shop['geoData'].progress_apply(get_coord)
temp = shop['Coordinates'].str.split(',', 1 , expand=True)
shop['lat'] = temp[1].astype(float)
shop['lon'] = temp[0].astype(float)
shop.drop(columns = ['geoData', 'Coordinates'], axis=1, inplace=True)
uniq_point['shop'] = r_neighbors(shop[['lat', 'lon']].values, r=0.01)

# Все бытовые услуги
col_list = ['ID', 'TypeObject', 'Latitude_WGS84', 'Longitude_WGS84']
service = pd.read_excel('raw/геоданные/data-4272-2023-04-18.xlsx', sheet_name='0', header=0, skiprows=[1])[col_list]

# Список для парикмахерских
barbers_list=['парикмахерские и косметические услуги', 'парикмахерская']
temp = service[service['TypeObject'].isin(barbers_list)]
uniq_point['barbers'] = r_neighbors(temp[['Latitude_WGS84', 'Longitude_WGS84']].values, r=0.01)

# Список для бань и саун
spa_list=['услуги саун', 'услуги бань']
temp = service[service['TypeObject'].isin(spa_list)]
uniq_point['spa'] = r_neighbors(temp[['Latitude_WGS84', 'Longitude_WGS84']].values, r=0.01)

# Список для ремонта обуви
shoes_list=['ремонт, окраска и пошив обуви']
temp = service[service['TypeObject'].isin(shoes_list)]
uniq_point['shoes'] = r_neighbors(temp[['Latitude_WGS84', 'Longitude_WGS84']].values, r=0.01)

# Список для ремонта ювелирных изделий
jewelry_list=['ремонт ювелирных изделий', 'ремонт и изготовление металлоизделий']
temp = service[service['TypeObject'].isin(jewelry_list)]
uniq_point['jewelry'] = r_neighbors(temp[['Latitude_WGS84', 'Longitude_WGS84']].values, r=0.01)

# Список для фото на документы
foto_list=['фотоателье, фотоуслуги', 'фото и копировальные услуги, малая полиграфия']
temp = service[service['TypeObject'].isin(foto_list)]
uniq_point['foto'] = r_neighbors(temp[['Latitude_WGS84', 'Longitude_WGS84']].values, r=0.01)

# Торговля и общепит стационарные
riteil = pd.read_csv('raw/геоданные/586_norm/586.csv', sep = ';', index_col=0)
riteil.columns = ['NAME', 'ADDRESS', 'lat', 'lon', 'NAME_OPF', 'LIC_SERNUM', 'LIC_START', 'LIC_STOP','LIC_STATUS']
uniq_point['riteil'] = r_neighbors(riteil[['lat', 'lon']].values, r=0.01)

# Клубы
club = pd.read_csv('raw/геоданные/493_norm/493.csv', sep = ';', index_col=0)
uniq_point['club'] = r_neighbors(club[['LAT', 'LON']].values, r=0.02)

# Больницы
med = pd.read_csv('raw/геоданные/502_norm/502.csv', sep = ';', index_col=0)
uniq_point['med'] = r_neighbors(med[['LAT', 'LON']].values, r=0.05)

# Ветбольницы
vet = pd.read_csv('raw/геоданные/1193_norm/1193.csv', sep = ';', index_col=0)
vet['LON'] = vet['LON'].str.replace("'", "").str.replace(",", ".").astype(float)
vet['LAT'] = vet['LAT'].str.replace("'", "").str.replace(",", ".").astype(float)
uniq_point['vet'] = r_neighbors(vet[['LAT', 'LON']].values, r=0.05)

# Стоматологи
stomat = pd.read_csv('raw/геоданные/518_norm/518.csv', sep = ';', index_col=0)
uniq_point['stomat'] = r_neighbors(stomat[['LAT', 'LON']].values, r=0.05)

col_list = ['ap_mac', 'lat', 'lon', 'Субъект', 'traffic', 'toilet', 'trash', 'metro', 'taxi', 'auto', 'light', 
            'video', 'keep', 'alco', 'shop', 'arenda', 'barbers', 'spa', 'shoes', 'jewelry', 'foto', 'riteil', 
            'club', 'med', 'vet', 'stomat', 'Адрес']

uniq_point[col_list].to_csv('data/df_geo.csv', index=False)