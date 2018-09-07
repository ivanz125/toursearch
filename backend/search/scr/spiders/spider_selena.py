import scrapy
import re
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from database import selena as selena_db
from multiprocessing import Process, Queue


def currency_site_to_code(string):
    if string == '€' or string == '&#8364;':
        return 'EUR'
    elif string == 'грн':
        return 'UAH'
    return 'UNKNOWN'


class QuotesSpider(scrapy.Spider):
    name = "selena"
    start_urls = [
        'http://selena-tour.com.ua/vse_tury/avtobusnie_tury'
    ]

    def parse(self, response):
        for item in response.css('div.block_item'):
            tour = dict()
            tour['title'] = item.css('div')[4].xpath('normalize-space()').extract_first()
            tour['price'] = item.css('div')[5].xpath('text()')[1].extract().strip()
            # currency
            currency_site = item.css('div')[5].css('span::text')[1].extract().strip()
            tour['currency'] = currency_site_to_code(currency_site)
            tour['route'] = item.css('tr')[0].css('td::text')[1].extract().strip()
            tour['days'] = int(item.css('tr')[1].css('td::text')[1].extract().strip())

            # link to tour page
            link_attr = item.css("div::attr(onclick)").extract()[0]
            link = 'http://selena-tour.com.ua' + link_attr[link_attr.find("'") + 1: link_attr.rfind("'")]

            # print(tour)
            request = scrapy.Request(link, callback=self.parse_details)
            request.meta['tour'] = tour
            yield request

    def parse_details(self, response):
        tour = response.meta['tour']
        tour['route'] = list()
        route_table = response.css('table.tour_descr')
        descriptions = route_table.xpath('.//td[contains(@align, "left")]')
        i = 0

        for header in route_table.css('td.tour_descr_header::text').extract():
            item = dict()
            item['header'] = header
            d = object()
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
            tour['route'].append(item)

        yield tour


def run_spider_process(q):
    try:
        runner = CrawlerRunner(get_project_settings())
        deferred = runner.crawl(QuotesSpider)
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
