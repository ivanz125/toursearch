from tours import app
from scr.spiders import spider_selena
from flask import jsonify
from flask import request
from database import selena as selena_db
from urllib.parse import unquote
from tours import tours_general
from monitoring import monitoring


@app.route('/')
@app.route('/tours')
def tours():
    code_country = request.args.get('code_country', default='', type=str)
    start_date_from = request.args.get('start_date_from', default=20180920, type=int)
    start_date_to = request.args.get('start_date_to', default=20180923, type=int)
    adults = request.args.get('adults', default=2, type=int)
    children = request.args.get('children', default=0, type=int)
    b_day_1 = request.args.get('b_day_1', default=20050801)
    b_day_2 = request.args.get('b_day_2', default=20070801)
    nights_min = request.args.get('nights_min', default=6, type=int)
    nights_max = request.args.get('nights_max', default=7, type=int)
    meals = request.args.get('meals', default='bb', type=str)
    price_max = request.args.get('price_max', default=0, type=int)

    results = tours_general.get_tours_avia(code_country, start_date_from, start_date_to, adults, children,
                                        b_day_1, b_day_2, nights_min, nights_max, meals, price_max)
    return jsonify(results)


@app.route('/bus')
def bus_tours():
    start_date_from = request.args.get('start_date_from', default=0, type=int)
    start_date_to = request.args.get('start_date_to', default=0, type=int)
    days_min = request.args.get('days_min', default=4, type=int)
    days_max = request.args.get('days_max', default=10, type=int)
    price_max = request.args.get('price_max', default=0, type=int)
    places = request.args.get('places_str', default='', type=str)
    places_mode = request.args.get('places_mode', default='one', type=str)
    update = request.args.get('update', default=False, type=bool)

    places = unquote(places)
    if update:
        spider_selena.run_spider()
    db = selena_db.Database()
    t = db.get_tours(days_min, days_max, price_max, places, places_mode, start_date_from, start_date_to)
    return jsonify(t)


@app.route('/bus/all')
def bus_tours_all():
    update = request.args.get('update', default=False, type=bool)
    if update:
        return jsonify(spider_selena.run_spider())
    db = selena_db.Database()
    return jsonify(db.get_all_tours())


@app.route('/monitoring/execute')
def execute_monitoring():
    monitoring_id = request.args.get('id', default=0, type=int)
    if monitoring_id == 0:
        return jsonify({'error': 'No correct monitoring id provided (param "id")'})
    return jsonify(monitoring.execute(monitoring_id))


@app.route('/monitoring/create')
def create_monitoring():
    result = monitoring.create(request.args)
    return jsonify({'result': result})


@app.route('/monitoring/get')
def get_monitorings():
    user_id = request.args.get('user_id', default=0, type=int)
    if user_id == 0:
        return jsonify({'error': 'no user_id passed'})
    monitoring_list = monitoring.get(user_id)
    return jsonify({'count': len(monitoring_list), 'data': monitoring_list})
