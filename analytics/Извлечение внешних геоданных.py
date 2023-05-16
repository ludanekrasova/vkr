#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Данные по уникальным точкам
uniq_point = pd.read_csv('data/uniq_point.csv', sep = ',')

# Наши точки
X_zone = uniq_point[['lat','lon']].values

# Функция для нахождения блюжайших точек в радиусе
def r_neighbors(X_train, r=0.01):
    #0.01 - 1 км
    neigh = NearestNeighbors(n_neighbors=10, radius=r)
    neigh.fit(X_train)
    distances, indexes = neigh.radius_neighbors(X_zone, r)
    return np.array([len(x) for x in indexes])

# Туалеты
toilet = pd.read_csv('геоданные/842_norm/842.csv', sep = ';', index_col=0)
toilet.columns = ['ADDRESS', 'REGIME', 'AVAILABIL', 'LON', 'LAT', 'GLOBALID']
toilet['LON'] = toilet['LON'].str.replace("'", "").str.replace(",", ".").astype(float)
toilet['LAT'] = toilet['LAT'].str.replace("'", "").str.replace(",", ".").astype(float)
# Количество туалетов в километровом радуиусе
X_train = toilet[['LAT', 'LON']].values
uniq_point['toilet'] = r_neighbors(X_train, r=0.01)

# Торговля и общепит стационарные
riteil = pd.read_csv('геоданные/586_norm/586.csv', sep = ';', index_col=0)
riteil.columns = ['NAME', 'ADDRESS', 'lat', 'lon', 'NAME_OPF', 'LIC_SERNUM', 'LIC_START', 'LIC_STOP','LIC_STATUS']
# Количество торговых точек и общепита в радиусе 1 км
X_train = riteil[['lat', 'lon']].values
uniq_point['riteil'] = r_neighbors(X_train, r=0.01)

# Бытовые услуги
service = pd.read_excel('геоданные/быт_усл-4272-2021-06-09.xlsx')
# Количество точек бытовых в радиусе 1 км
X_train = service[['Latitude_WGS84', 'Longitude_WGS84']].values
uniq_point['service'] = r_neighbors(X_train, r=0.01)

# Станции метро
metro = pd.read_csv('геоданные/624_norm/624.csv', sep = ';', index_col=0)
# Количество станций метро в радиусе 1 км
X_train = metro[['LAT', 'LON']].values
uniq_point['metro'] = r_neighbors(X_train, r=0.01)

# Объекты для аренды
arenda = pd.read_csv('геоданные/1113_norm/1113.csv', sep = ';', index_col=0)
# Количество свободных помещений в радиусе 5 км
X_train = arenda[['LAT', 'LON']].values
uniq_point['arenda'] = r_neighbors(X_train, r=0.05)

# Клубы
club = pd.read_csv('геоданные/493_norm/493.csv', sep = ';', index_col=0)
# Количество клубов в радиусе 2 км
X_train = club[['LAT', 'LON']].values
uniq_point['club'] = r_neighbors(X_train, r=0.02)

# Больницы
med = pd.read_csv('геоданные/502_norm/502.csv', sep = ';', index_col=0)
# Количество больниц в радиусе 5 км
X_train = med[['LAT', 'LON']].values
uniq_point['med'] = r_neighbors(X_train, r=0.05)

# Ветбольницы
vet = pd.read_csv('геоданные/1193_norm/1193.csv', sep = ';', index_col=0)
vet['LON'] = vet['LON'].str.replace("'", "").str.replace(",", ".").astype(float)
vet['LAT'] = vet['LAT'].str.replace("'", "").str.replace(",", ".").astype(float)
# Количество ветлечебниц в радиусе 5 км
X_train = vet[['LAT', 'LON']].values
uniq_point['vet'] = r_neighbors(X_train, r=0.05)

# Стоматологи
stomat = pd.read_csv('геоданные/518_norm/518.csv', sep = ';', index_col=0)
# Количество стоматологий в радиусе 5 км
X_train = stomat[['LAT', 'LON']].values
uniq_point['stomat'] = r_neighbors(X_train, r=0.05)

uniq_point[['ap_mac', 'toilet', 'metro', 'arenda', 'riteil', 'service', 'club', 'med', 'vet', 'stomat']].to_csv('data/df_geo.csv', index=False)
