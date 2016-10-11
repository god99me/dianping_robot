# -*- coding: utf-8 -*-

import json
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import pymysql

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


class DBPipeline(object):
    def __init__(self):
        self.db_pool = adbapi.ConnectionPool('pymysql', db='wifi_union', user='root', passwd='819819',
                                             cursorclass=pymysql.cursors.DictCursor,
                                             use_unicode=True,
                                             charset='utf8')

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self._conditional_insert, item, spider)
        query.addErrback(self.handle_error, item, spider)
        query.addBoth(lambda _: item)
        return item


    def _conditional_insert(self, tx, item, spider):
        tx.execute("select name from dianping where name = %s", (item['name'][0],))
        result = tx.fetchone()
        if result:
            pass
        else:
            # 简写的 mysql 语句，保持插入数据属性名与列名一致
            values = (
                item['address'],
                item['average_consumption'],
                item['comment_count'],
                item['comment_star'],
                item['lat'][0],
                item['lng'][0],
                item['name'],
                ','.join(item['phone_number']),
                item['score_environment'],
                item['score_flavor'],
                item['score_service'],
                item['type'],
            )

            tx.execute("insert into dianping values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)

    def handle_error(self, failure, item, spider):
        print('Error: ', failure)
        print('Error Item: ', item)


