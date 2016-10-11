# -*- coding: utf-8 -*-

import scrapy
import re
import logging

from scrapy.utils.log import configure_logging
from dianping_robot.items import DianpingRobotItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class DianpingSpider(scrapy.Spider):
    name = "dianping"
    start_urls = [
        'http://www.dianping.com/search/category/2/10/g101',
        'http://www.dianping.com/search/category/2/10/g102',
        'http://www.dianping.com/search/category/2/10/g103',
        'http://www.dianping.com/search/category/2/10/g104',
        'http://www.dianping.com/search/category/2/10/g105',
        'http://www.dianping.com/search/category/2/10/g106',
        'http://www.dianping.com/search/category/2/10/g108',
        'http://www.dianping.com/search/category/2/10/g109',
        'http://www.dianping.com/search/category/2/10/g110',
        'http://www.dianping.com/search/category/2/10/g111',
        'http://www.dianping.com/search/category/2/10/g112',
        'http://www.dianping.com/search/category/2/10/g113',
        'http://www.dianping.com/search/category/2/10/g114',
        'http://www.dianping.com/search/category/2/10/g115',
        'http://www.dianping.com/search/category/2/10/g116',
        'http://www.dianping.com/search/category/2/10/g117',
        'http://www.dianping.com/search/category/2/10/g118',
        'http://www.dianping.com/search/category/2/10/g132',
        'http://www.dianping.com/search/category/2/10/g246',
        'http://www.dianping.com/search/category/2/10/g248',
        'http://www.dianping.com/search/category/2/10/g251',
        'http://www.dianping.com/search/category/2/10/g311',
        'http://www.dianping.com/search/category/2/10/g508',
        'http://www.dianping.com/search/category/2/10/g1783',
        'http://www.dianping.com/search/category/2/10/g3243',
        'http://www.dianping.com/search/category/2/10/g26481',
        'http://www.dianping.com/search/category/2/10/g26483'
    ]
    # url_seen = set()
    # start_url = 'http://www.dianping.com/search/category/2/10/g110'

    def __init__(self, name=None, **kwargs):
        # configure_logging is automatically called when using Scrapy commands
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename='log_info.txt',
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )
        logging.basicConfig(
            filename='log_warning.txt',
            format='%(levelname)s: %(message)s',
            level=logging.WARNING
        )
        super(DianpingSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_index)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    # def parse_indexs(self, response):
    #     index_pages = response.xpath('//div[contains(@id,"main-nav")]//div[contains(@class,"secondary-category")]//a/@href').re(r'.*\d+')
    #     for index_page in index_pages:
    #         pass

    def parse_index(self, response):
        # debug cmd: scrapy shell "http://www.dianping.com/beijing"
        # response.xpath('//div[contains(@class,"page-home")]//div[contains(@class,"popular-nav")]
        # //li[contains(@class,"term-list-item")]//a/@href').extract()

        # index_pages = response.xpath('//div[contains(@id,"main-nav")]
        #   //div[contains(@class,"secondary-category")]//a/@href').re(r'.*\d+')
        start_urls = response.xpath('//div[@id="shop-all-list"]//div[contains(@class,"pic")]/a/@href').extract()

        for u in start_urls:
            u = response.urljoin(u)
            yield scrapy.Request(u, callback=self.parse)

    def parse(self, response):

        item = DianpingRobotItem()

        # basic information
        type_text = response.xpath('//div[contains(@class,"breadcrumb")]//a/text()').extract_first()
        item['type'] = type_text.replace("\n", "").strip()

        item['name'] = response.xpath('//h1[@class="shop-name"]/text()').extract_first().replace("\n", "").strip()
        item['address'] = response.xpath('//div[@class="expand-info address"]/span[@class="item"]/text()').extract_first().replace("\n", "").strip()
        item['phone_number'] = response.xpath('//p[@class="expand-info tel"]/span[@class="item"]/text()').extract()

        # location
        lng_lat = response.xpath('//script/text()')
        item['lng'] = lng_lat.re(r'lng:([\d\.]+)') if lng_lat else ' '
        item['lat'] = lng_lat.re(r'lat:([\d\.]+)') if lng_lat else ' '

        # comments
        brief_info_list = response.xpath('//div[@class="brief-info"]/span[@class="item"]/text()').extract()
        # switch len(brief_info_list)
        re_count = re.search(r'[\d\.]+', brief_info_list[0])
        re_consumption = re.search(r'[\d\.]+', brief_info_list[1])

        item['comment_count'] = re_count.group() if re_count else 0
        item['average_consumption'] = re_consumption.group() if re_consumption else ' '
        item['score_flavor'] = brief_info_list[2] if len(brief_info_list) > 2 else ' '
        item['score_environment'] = brief_info_list[3] if len(brief_info_list) > 3 else ' '
        item['score_service'] = brief_info_list[4] if len(brief_info_list) > 4 else ' '
        item['comment_star'] = response.xpath('//div[@class="brief-info"]/span/@title').extract_first()

        # revelent information
        # item['shop_branchs'] = response.xpath('//div[@id="shop-branchs"]/div/h3[@class="name"]/a/@href').extract()
        # item['businessmen_nearby'] = response.xpath('//div[@id="around-info"]/div[@class="J-panel Hide"]/ul/li/a[@class="title"]/@href').extract()
        yield item

        shop_branchs = response.xpath('//div[@id="shop-branchs"]/div/h3[@class="name"]/a/@href').extract()
        businessmen_nearby = response.xpath('//div[@id="around-info"]/div[@class="J-panel Hide"]/ul/li/a[@class="title"]/@href').extract()
        for next_page in shop_branchs:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            # if next_page not in self.url_seen:
            #     self.url_seen.add(next_page)

        for next_page in businessmen_nearby:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            # if next_page not in self.url_seen:
            #     self.url_seen.add(next_page)

            # with open(filename, 'wb') as f:
            #     f.write(response.body)
