#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import time
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim

# Точки - координаты и траффик
df_points = pd.read_csv('data/df_uniq.csv')

# Районы Москвы
region = gpd.read_file('raw/mo-shape/mo.shp')
region.rename(columns={'NAME': "Субъект"}, inplace = True)
region.drop(columns = ['OKATO', 'OKTMO', 'NAME_AO', 'OKATO_AO', 'ABBREV_AO', 'TYPE_MO'], axis = 1, inplace=True)
region.replace({'Субъект': {'"Мосрентген"': 'Мосрентген'}}, inplace=True)

### Список точек с координатами и регионом

# Проверка точек на дубликаты
if len(df_points['ap_mac'].unique()) > df_points.shape[0]:
    df_points = df_points.drop_duplicates(subset=['ap_mac'])
else:
    print('Нет дубликатов')

# Сопостовление координат с полигонами и геоточек с георайонами в геопандас
df_points['geometry'] = df_points.apply(lambda x: Point(x['lon'], x['lat']), axis=1)
ap_point = gpd.GeoDataFrame({"ap_mac" : df_points.ap_mac, "lat" : df_points.lat, "lon" : df_points.lon,
                             "geometry": df_points.geometry, "traffic": df_points.traffic})
merging = gpd.sjoin(ap_point, region, how="left", op="within")
# Удаление точек, не входящих в г. Москва
merging.dropna(subset=['Субъект'], inplace=True)

# Получение адреса
geolocator = Nominatim(user_agent="my-app")
def get_address(lat, lon):
    time.sleep(1) #запросы не чаще 1 раза в секунду
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location is not None:
        addr = ""
        if 'road' in location.raw['address'] is not None:
            addr += location.raw['address']['road']+ ", "
        if 'house_number' in location.raw['address'] is not None:
            addr += location.raw['address']['house_number']+ ", "
        if 'city' in location.raw['address'] is not None:
            addr += location.raw['address']['city']+ ", "
        if 'country' in location.raw['address'] is not None:
            addr += location.raw['address']['country']
        return addr
    else:
        return "Адрес не найден"
    
merging['Адрес'] = merging.progress_apply(lambda row: get_address(row['lat'], row['lon']), axis=1)

merging[['ap_mac', 'lat', 'lon', 'Субъект', 'traffic']].to_csv('data/df_points.csv', index=False)