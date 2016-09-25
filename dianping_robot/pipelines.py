# -*- coding: utf-8 -*-

import json
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DianpingRobotPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.has_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.has_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.has_seen.add(item['name'])
            return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), sort_keys=True, ensure_ascii=False) + "\n"
        # str = unicode.encode(line, 'utf-8')
        self.file.write(line)
        return item