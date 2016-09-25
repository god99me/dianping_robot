# -*- coding: utf-8 -*-
# TODO doesnt work right in current dir
# import scrapy
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# from dianping_robot.items import DianpingRobotItem
#
# """
# Scrapy is built on top of the Twisted asynchronous networking library,
# so you need to run it inside the Twisted reactor.
# The first utility you can use to run your spiders is scrapy.crawler.CrawlerProcess.
# This class will start a Twisted reactor for you, configuring the logging and setting shutdown handlers.
# This class is the one used by all Scrapy commands.
# """
# class DianpingSpider(scrapy.Spider):
#     # Your spider definition
#     name = "dianping"
#     start_urls = [
#         'http://www.dianping.com/shop/2743444'
#     ]
#
#     def parse(self, response):
#
#         item = DianpingRobotItem()
#
#         # basic information
#         item['name'] = response.xpath('//h1[@class="shop-name"]/text()').extract_first().replace("\n", "").strip()
#         item['address'] = response.xpath(
#             '//div[@class="expand-info address"]/span[@class="item"]/text()').extract_first().replace("\n", "").strip()
#         item['phone_number'] = response.xpath('//p[@class="expand-info tel"]/span[@class="item"]/text()').extract()
#
#         # comments
#         brief_info_list = response.xpath('//div[@class="brief-info"]/span[@class="item"]/text()').extract()
#         item['comment_count'] = brief_info_list[0]
#         item['average_consumption'] = brief_info_list[1]
#         item['score_flavor'] = brief_info_list[2]
#         item['score_environment'] = brief_info_list[3]
#
#         if len(brief_info_list) > 4:
#             item['score_service'] = brief_info_list[4]
#
#         item['comment_star'] = response.xpath('//div[@class="brief-info"]/span/@title').extract_first()
#
#         # revelent information
#         # item['shop_branchs'] = response.xpath('//div[@id="shop-branchs"]/div/h3[@class="name"]/a/@href').extract()
#         # item['businessmen_nearby'] = response.xpath('//div[@id="around-info"]/div[@class="J-panel Hide"]/ul/li/a[@class="title"]/@href').extract()
#         yield item
#
#         shop_branchs = response.xpath('//div[@id="shop-branchs"]/div/h3[@class="name"]/a/@href').extract()
#         businessmen_nearby = response.xpath(
#             '//div[@id="around-info"]/div[@class="J-panel Hide"]/ul/li/a[@class="title"]/@href').extract()
#         for next_page in shop_branchs:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
#
#         for next_page in businessmen_nearby:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
#
# # Running multiple spiders in the same process
# class MySpider2(scrapy.Spider):
#     pass
#
# # use get_project_settings to get a Settings instance with your project settings
# process = CrawlerProcess(get_project_settings())
#
# # Crawler instance, Spider subclass or string
# # already created crawler, or a spider class or spider’s name inside the project to create it
# process.crawl(DianpingSpider)
# # There is some way you can run spiders sequentially by chaining the deferreds
# # process.crawl(MySpider2)
# process.start() # the script will block here until the crawling is finished