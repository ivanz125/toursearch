import scrapy
import re
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from database import selena as selena_db
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup
from scrapy import Selector


def currency_site_to_code(string):
    if string == '€' or string == '&#8364;':
        return 'EUR'
    elif string == 'грн':
        return 'UAH'
    return 'UNKNOWN'


class PtvSpider(scrapy.Spider):
    name = "ptv"
    start_urls = [
        'http://ptv.com.ua/type/bus-trip/'
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        resp = Selector(soup.prettify())
        a = 0
        for item in resp.css('li.article'):
            print(len(response.css('li.article')))
            tour = dict()
            a += 1
            tour['id'] = a
            tour['title'] = item.css('div.preview')[3].extract()
            yield tour
            continue
            tour['price'] = item.css('div')[5].xpath('text()')[1].extract().strip()
            # currency
            currency_site = item.css('div')[5].css('span::text')[1].extract().strip()
            tour['currency'] = currency_site_to_code(currency_site)
            route_str = tour['route_str'] = item.css('tr')[0].css('td::text')[1].extract().strip()
            tour['days'] = int(item.css('tr')[1].css('td::text')[1].extract().strip())

            # split route
            places = route_str.split(' - ')
            places = [p.strip() for p in places]
            tour['places'] = places

            # link to tour page
            link_attr = item.css("div::attr(onclick)").extract()[0]
            link = 'http://selena-tour.com.ua' + link_attr[link_attr.find("'") + 1: link_attr.rfind("'")]

            # print(tour)
            request = scrapy.Request(link, callback=self.parse_details)
            request.meta['tour'] = tour
            yield request

    def parse_details(self, response):
        tour = response.meta['tour']

        # start cities
        info_table = response.css('table.tbl_tour_info')
        cities_str = info_table.css('tr')[2].css('td::text')[1].strip()
        tour['start_places'] = [c.strip() for c in cities_str.split(',')]

        # description
        tour['description'] = list()
        route_table = response.css('table.tour_descr')
        descriptions = route_table.xpath('.//td[contains(@align, "left")]')
        i = 0
        for header in route_table.css('td.tour_descr_header::text').extract():
            item = dict()
            item['header'] = header
            if i < len(descriptions):
                d = descriptions[i]
                # d.extract().re(r'Name:\s*(.*)')
                content = d.extract()
                content = re.sub('<span[^>]*>', '', content)
                content = re.sub('<td[^>]*>', '', content)
                content = content.replace('</span>', '').replace('</td>', '')
                # text_list = d.xpath('.//*[self::span]/text()').extract()
                # text = ''
                # for t in text_list:
                #    text += t
                item['content'] = content
            i += 1
            tour['description'].append(item)

        yield tour


def run_spider_process(q):
    try:
        runner = CrawlerRunner(get_project_settings())
        deferred = runner.crawl(PtvSpider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


# the wrapper to make it run more times
def run_spider():
    # configure_logging({'LOG_LEVEL': 'INFO'})
    configure_logging()
    db = selena_db.Database()
    db.clear_data()

    q = Queue()
    p = Process(target=run_spider_process, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

    return db.get_all_tours()
