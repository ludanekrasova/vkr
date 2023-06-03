#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response
import pandas as pd
import folium
import os
import random
import shutil

retail_list = ['Супермаркет', 'Магазин у дома', 'Магазин спиртных напитков', 'Кондитерский магазин', 'Магазин здоровой пищи','Бытовая химия', 'Магазин косметики', 'Магазин одежды', 'Газетный киоск']
service_list = ['Парикмахерская', 'Салон красоты', 'Спа салон', 'Ремонт обуви', 'Ремонт ювелирных изделий', 'Автомойка', 'Фото на документы']
catering_list = ['Ресторан', 'Кафе', 'Бар', 'Кофе на вынос', 'Киоск мороженного']
culture_list = ['Ночной клуб']
medical_list = ['Клиника', 'Стоматологическая клиника', 'Ветеринарная клиника', 'Женская консультация']

reatail_col = ['Количество_торговля_rank', 'Выручка_торговля_rank', 'Прибыль_торговля_rank', 'riteil_rank']
service_col = ['Количество_бытовые_rank', 'Выручка_бытовые_rank', 'Прибыль_бытовые_rank', 'service_rank']
catering_col = ['Количество_общепит_rank', 'Выручка_общепит_rank', 'Прибыль_общепит_rank', 'riteil_rank']
culture_col = ['Количество_клубы_rank', 'Выручка_клубы_rank', 'Прибыль_клубы_rank', 'club_rank']
medical_col = ['Количество_медицина_rank', 'Выручка_медицина_rank', 'Прибыль_медицина_rank', 'med_rank', 'vet_rank', 'stomat_rank']

weekdays = ['day_1_rank', 'day_2_rank', 'day_3_rank', 'day_4_rank', 'day_5_rank',]
weekend = ['day_6_rank', 'day_7_rank']

work_time = ['hour_6_rank', 'hour_7_rank', 'hour_8_rank', 'hour_9_rank', 'hour_10_rank', 'hour_11_rank', 'hour_12_rank', 'hour_13_rank', 'hour_14_rank', 'hour_15_rank', 'hour_16_rank', 'hour_17_rank', 'hour_18_rank']
rest_time = ['hour_19_rank', 'hour_20_rank', 'hour_21_rank', 'hour_22_rank', 'hour_23_rank','hour_0_rank', 'hour_1_rank', 'hour_2_rank', 'hour_3_rank', 'hour_4_rank', 'hour_5_rank', ]

default_col = weekdays + work_time + ['crime_rank', 'money_rank', 'device_count_rank', 'device_nunique_rank', 'device_frec_rank', 'user_nunique_rank', 'duration_rank', 'duration_min_rank', 'duration_max_rank', 'toilet_rank', 'metro_rank']

app = Flask(__name__, static_url_path='/static')

@app.after_request
def after_request(response):
   response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
   response.headers["Expires"] = 0
   response.headers["Pragma"] = "no-cache"
   return response

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
root = root_dir() + '/'

data = pd.read_csv(root + 'df_rank.csv')

def get_result(data, request):
    # Предсказание рангов по выбранным параметрам
    if request.args.get('branch'):

        headers =  {
            'branch': 'Вид деятельности',
            'week': 'Режим неделя',
            'day':'Режим сутки',
            'hour':'Режим обед',
            'money':'Доходы клиентов',
            'place':'Мест',
            'people':'Специалистов',
            'room':'Наличие помещений'
            }

        #request_data = [title:request.args.get(key) for key,title in headers.items()]

        branch = request.args.get('branch')
        day = request.args.get('day')
        hour = request.args.get('hour')
        money = request.args.get('money')
        room = request.args.get('room')

        if branch in retail_list:
            branch_cols = reatail_col
        elif branch in service_list:
            branch_cols = service_col
        elif branch in catering_list:
            branch_cols = catering_col
        elif branch in culture_list:
            branch_cols = culture_col
        elif branch in medical_list:
            branch_cols = medical_col

        if day == 'будни':
            #day_col = weekdays по умолчанию
            day_col = []
        else:
            #day_col = weekdays + weekend
            day_col = weekend

        if hour == '6-18':
            #hour_col = work_time по умолчанию
            pass
        else:
            #hour_col = work_time + rest_time
            hour_col = rest_time

        if room == 'yes':
            room_col = ['arenda']
        else:
            room_col = []

        cols = default_col + branch_cols + day_col + hour_col + room_col

        data['rank'] = data[cols].mean(axis=1)

        #точки для визуализации
        result = data.sort_values(by='rank', ascending=True).reset_index(drop=True)

    else:
        result = data

    return(result[0:50])

def color_change(elev):
    # Цвета маркеров
    if(elev >= 40):
        return('beige')
    elif(elev >=30) & (elev <40):
        return('orange')
    elif(elev >=20) & (elev <30):
        return('lightred')
    elif(elev >=10) & (elev <20):
        return('red')
    else:
        return('darkred')


@app.route('/', methods=['GET', 'POST'])
def index():

    # Предсказание
    result = get_result(data, request)
    rank = result.index
    lat, lon = result['lat'], result['lon']
    elevation = result['ap_mac']
    address = result['address']

    # Карта
    folium_map = folium.Map(location=[55.73702, 37.62256], zoom_start = 13, tiles = "OpenStreetMap")

    # Маркеры
    for lat, lon, elevation, rank, address in zip(lat, lon, elevation, rank, address):
        folium.Marker(location=[lat, lon], popup="Ранг " + str(rank) + "<br>Адрес: "+ address, icon=folium.Icon(color = color_change(rank))).add_to(folium_map)
        #return folium_map._repr_html_()

    folium_map.save(root + '/tmp/map.html')

    return render_template('index.html')

@app.route('/map')
def map():

    r = int(random.triangular(0,100))
    t = root+"tmp/map_{i}.html"
    for i in range(0,100):
        f = t.format(i=i)
        if os.path.exists(f):
            os.remove(f)
    f = t.format(i=r)
    shutil.copy(root+"tmp/map.html", f)

    r = make_response(render_template(os.path.split(f)[1]))
    r.cache_control.max_age = 0
    r.cache_control.no_cache = True
    r.cache_control.no_store = True
    r.cache_control.must_revalidate = True
    r.cache_control.proxy_revalidate = True
    return r

if __name__ == '__main__':
    app.run(debug=True, port = 5005)
