from tours import api_tui
from tours import api_tez


def get_tours_avia(code_country, start_date_from, start_date_to, adults, children,
                   b_day_1, b_day_2, nights_min, nights_max, meals, price_max):
    results_tez = api_tez.get_results(code_country, start_date_from, start_date_to, adults, children, b_day_1, b_day_2,
                                      nights_min, nights_max, meals, price_max)
    results_tui = api_tui.get_results(code_country, start_date_from, start_date_to, adults, children,
                                      nights_min, nights_max, meals, price_max)

    results = dict()
    results['count_items'] = results_tui['count_items'] + results_tez['count_items']
    results['count_tui'] = results_tui['count_items']
    results['count_tez'] = results_tez['count_items']
    results['data'] = results_tui['data'] + results_tez['data']
    return results
