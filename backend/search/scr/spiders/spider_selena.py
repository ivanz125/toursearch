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
            tour['price'] = int(item.css('div')[5].xpath('text()')[1].extract().strip())
            # currency
            currency_site = item.css('div')[5].css('span::text')[1].extract().strip()
            tour['currency'] = currency_site_to_code(currency_site)
            route_str = tour['route_str'] = item.css('tr')[0].css('td::text')[1].extract().strip()

            # image
            style_str = item.css('div::attr(style)').extract_first()
            backgrounds = re.findall('background-image:[ ]*url\(.*\)', style_str)
            if len(backgrounds) > 0:
                bcg = backgrounds[0]
                bcg = bcg[bcg.find('url(') + 4: len(bcg)-1]
                tour['image'] = "http://selena-tour.com.ua" + bcg

            # days count
            tour['days'] = int(item.css('tr')[1].css('td::text')[1].extract().strip())

            # split route
            places = route_str.split(' - ')
            places = [p.strip() for p in places]
            tour['places'] = places

            # link to tour page
            link_attr = item.css('div::attr(onclick)').extract()[0]
            link = 'http://selena-tour.com.ua' + link_attr[link_attr.find("'") + 1: link_attr.rfind("'")]
            tour['url'] = link

            # print(tour)
            request = scrapy.Request(link, callback=self.parse_details)
            request.meta['tour'] = tour
            yield request

    def parse_details(self, response):
        tour = response.meta['tour']

        # start cities
        info_table = response.css('table.tbl_tour_info')
        cities_str = info_table.css('tr')[3].css('td::text').extract()[1].strip()
        tour['start_places'] = [c.strip() for c in cities_str.split(',')]

        # dates
        dates = info_table.css('tr')[0].css('select.inp_t')[0].css('option::text').extract()
        d = list()
        for s in dates:
            for ss in re.findall('([0-9]{2}[-|.][0-9]{2}[-|.][0-9]{4})', s):  # dd.mm.yyyy
                d.append(ss)
        tour['dates'] = d

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
