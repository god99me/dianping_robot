# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingRobotItem(scrapy.Item):
    # basic
    type = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()

    # comment
    comment_star = scrapy.Field()
    comment_count = scrapy.Field()
    average_consumption = scrapy.Field()
    score_flavor = scrapy.Field()
    score_environment = scrapy.Field()
    score_service = scrapy.Field()

    # location
    lng = scrapy.Field()
    lat = scrapy.Field()

    # revelent
    # shop_branchs = scrapy.Field()
    # businessmen_nearby = scrapy.Field()
