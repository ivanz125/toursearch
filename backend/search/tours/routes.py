from tours import app
from tours import api_tui
from tours import api_tez
from scr.spiders import spider_selena
from flask import jsonify
from flask import request
from database import selena as selena_db


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

    results_tez = api_tez.get_results(code_country, start_date_from, start_date_to, adults, children, b_day_1, b_day_2,
                                      nights_min, nights_max, meals, price_max)
    results_tui = api_tui.get_results(code_country, start_date_from, start_date_to, adults, children,
                                      nights_min, nights_max, meals, price_max)

    results = dict()
    results['count_items'] = results_tui['count_items'] + results_tez['count_items']
    results['count_tui'] = results_tui['count_items']
    results['count_tez'] = results_tez['count_items']
    results['data'] = results_tui['data'] + results_tez['data']
    return jsonify(results)


@app.route('/bus')
def bus_tours():
    # selena = spider_selena.QuotesSpider()
    # return jsonify(spider_selena.run_spider())
    db = selena_db.Database()
    return jsonify(db.get_all_tours())
