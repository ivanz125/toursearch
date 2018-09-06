import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
import re
import json
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


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
            d = descriptions[i]
            i += 1
            #d.extract().re(r'Name:\s*(.*)')
            content = d.extract()
            content = re.sub('<span[^>]*>', '', content)
            content = re.sub('<td[^>]*>', '', content)
            content = content.replace('</span>', '').replace('</td>', '')
            #text_list = d.xpath('.//*[self::span]/text()').extract()
            #text = ''
            #for t in text_list:
            #    text += t
            item['content'] = content
            tour['route'].append(item)

        yield tour


def get_data():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data.json'
    })

    process.crawl(QuotesSpider)
    process.start()  # the script will block here until the crawling is finished

    with open('data.json') as f:
        data = json.load(f)

    return data


def get_data2():
    configure_logging()

    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result.json')

    runner = CrawlerRunner(settings)

    d = runner.crawl(QuotesSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished

    with open('result.json') as f:
        data = json.load(f)

    return data
