#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, render_template_string
import pandas as pd
import folium
from folium import plugins
import os

retail_list = ['Супермаркет', 'Магазин спиртных напитков', 'Кондитерский магазин', 'Магазин здоровой пищи']
service_list = ['Парикмахерская', 'Спа салон', 'Ремонт обуви', 'Ремонт ювелирных изделий', 'Фото на документы']
culture_list = ['Ресторан', 'Кафе', 'Бар', 'Ночной клуб']
medical_list = ['Клиника', 'Стоматологическая клиника', 'Ветеринарная клиника']

reatail_col = ['Количество_торговля_rank', 'Выручка_торговля_rank', 'Прибыль_торговля_rank', 'Магазины_ранг']
service_col = ['Количество_бытовые_rank', 'Выручка_бытовые_rank', 'Прибыль_бытовые_rank']
culture_col = ['Количество_общепит_rank', 'Количество_клубы_rank', ]
medical_col = ['Количество_медицина_rank', 'Выручка_медицина_rank', 'Прибыль_медицина_rank']

top_n=30 # Вывод точек на карту

app = Flask(__name__, static_url_path='/static')
app.secret_key = "super secret key"

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
        branch = request.args.get('branch')
        money = request.args.get('money')
        keep = request.args.get('keep')
        eco = request.args.get('eco')
        cost = request.args.get('cost')
        room = request.args.get('room')
        people = request.args.get('people')

        default_col = ['traffic_rank', 'toilet_rank']
        branch_cols = []

        if branch in retail_list:
            branch_cols = reatail_col
            if branch=='Супермаркет':
                branch_cols+=['people_rank', 'auto_rank', 'riteil_rank', 'shop_rank']
            if branch=='Магазин спиртных напитков':
                branch_cols+=['taxi_rank', 'club_rank', 'alco_rank']
            if branch=='Кондитерский магазин':
                branch_cols+=['Условия для детей_ранг']
            if branch=='Магазин здоровой пищи':
                branch_cols+=['Спорт и отдых_ранг', 'auto_rank', 'Стоимость жизни_ранг']

        elif branch in service_list:
            branch_cols = service_col
            if branch=='Парикмахерская':
                branch_cols+=['taxi_rank', 'barbers_rank', 'houseparenda_rank']
            if branch=='Спа салон':
                branch_cols+=['people_rank', 'taxi_rank', 'auto_rank', 'spa_rank']
            if branch=='Ремонт обуви':
                branch_cols+=['shoes_rank']
            if branch=='Ремонт ювелирных изделий':
                branch_cols+=['money_rank', 'Стоимость жизни_ранг', 'jewelry_rank']
            if branch=='Фото на документы':
                branch_cols+=['people_rank', 'foto_rank']

        elif branch in culture_list:
            branch_cols = culture_col
            if branch=='Ресторан':
                branch_cols+=['taxi_rank', 'auto_rank', 'alco_rank', 'video_rank', 'Прибыль_общепит_rank', 'houseprise_rank']
            if branch=='Кафе':
                branch_cols+=['metro_rank', 'auto_rank', 'riteil_rank', 'Выручка_общепит_rank', ]
            if branch=='Бар':
                branch_cols+=['club_rank', 'video_rank', 'Выручка_клубы_rank', 'alco_rank']
            if branch=='Ночной клуб':
                branch_cols+=['club_rank', 'Стоимость жизни_ранг', 'light_rank', 'Прибыль_клубы_rank', 'alco_rank', 'houseprise_rank']

        elif branch in medical_list:
            branch_cols = medical_col
            if branch=='Клиника':
                branch_cols+=['metro_rank', 'people_rank', 'med_rank', 'trash_rank']
            if branch=='Стоматологическая клиника':
                branch_cols+=['stomat_rank', 'trash_rank']
            if branch=='Ветеринарная клиника':
                branch_cols+=['taxi_rank', 'auto_rank', 'vet_rank', 'trash_rank']

        if money== 'low':
            money_col = []
        else:
            money_col = ['money_rank', 'Стоимость жизни_ранг']

        if keep == 'yes':
            keep_col = ['crime_rank', 'light_rank', 'video_rank', 'keep_rank', 'Безопасность_ранг', 'Соседи_ранг']           
        else:
            keep_col = []

        if eco == 'yes':
            eco_col = ['danger_rank', 'Чистота_ранг',  'Экология_ранг', 'ЖКХ_ранг']
        else:
            eco_col = []

        if cost == 'yes':
            cost_col = ['houseprise_rank']
        else:
            cost_col = []

        if room == 'yes':
            room_col = ['arenda_rank', 'houseparenda_rank']
        else:
            room_col = []

        cols = default_col + branch_cols + money_col + keep_col + eco_col + cost_col + room_col

        data['rank'] = data[cols].mean(axis=1)

        # Точки для визуализации
        result = data.sort_values(by='rank', ascending=True)
        result['new_rank']=result['rank'].rank(ascending=True, method='first').astype(int)

    else:
        result = data.reset_index(drop=False, names=['new_rank'])

    return result[0:top_n]

def color_change(elev):
    # Цвета маркеров
    if(elev >= 20):
        return('beige')
    elif(elev >=15) & (elev <20):
        return('orange')
    elif(elev >=10) & (elev <15):
        return('lightred')
    elif(elev >=5) & (elev <10):
        return('red')
    else:
        return('darkred')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Получение параметров из формы
    department = request.args.get('department')
    branch = request.args.get('branch')
    # Предсказание по введенным значениям
    result = get_result(data, request)
    session['data'] = result[['lat', 'lon', 'Адрес', 'new_rank']].to_dict('list')
    return render_template('index.html', department=department, branch=branch)

@app.route('/map', methods=['GET', 'POST'])
def map():
    # Рендеринг карты по введенным данным
    try:
        result = session.get('data', None)
        rank = result['new_rank']
        lat, lon = result['lat'], result['lon']
        elevation = result['Адрес']  # адрес точки
    except:
        # Заглушка, если данные не пришли
        lat = (55.7211, 55.7371)
        lon = (37.6061, 37.6237)
        elevation = (12, 14)
        rank = (1, 2)
    
    # Карта
    folium_map = folium.Map(location=[55.73702, 37.62256], zoom_start=11, min_zoom = 11, max_zoom = 15, tiles = "OpenStreetMap")

    # Маркеры
    for lat, lon, elevation, rank in zip(lat, lon, elevation, rank):
        icon_number = plugins.BeautifyIcon(number= rank, border_color=color_change(rank), text_color='darkred', \
                      inner_icon_style='margin-top:0;')
        folium.Marker(location=[lat, lon], icon=icon_number, tooltip=elevation).add_to(folium_map) #, popup=elevation

    html_string = folium_map.get_root().render()

    return render_template_string(html_string)

if __name__ == '__main__':
    app.run(debug=True)
