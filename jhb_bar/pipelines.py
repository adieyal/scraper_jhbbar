# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import items
import os
import json
from jhb_bar.scrapy_logger import get_logger


class MemberDuplicatesPipeline(object):

    def __init__(self):
        self.cache = set()

    def open_spider(self, spider):
        filename = spider.settings["FEED_URI"] % {"name" : spider.name}
        spider.crawler.stats.set_value("records_collected", 0)
        spider.crawler.stats.set_value("records_dropped", 0)

        if hasattr(spider, "item"):
            SpiderItem = spider.item

            if filename and os.path.exists(filename):
                for row in open(filename):
                    try:
                        js = json.loads(row)
                        item = SpiderItem(**js)
                        self.cache.add(repr(item))
                    except ValueError:
                        pass

    def process_item(self, item, spider):
        if repr(item) in self.cache:
            spider.crawler.stats.inc_value("records_dropped")
            raise DropItem("Duplicate item found: %s" % item)
        else:
            spider.crawler.stats.inc_value("records_collected")
            self.cache.add(repr(item))
            return item

    def close_spider(self, spider):
        spider.logger.info("{name} spider collected: {count} new records".format(
            name=spider.name, count=spider.crawler.stats.get_value("records_collected"))
        )
        spider.logger.info("{name} spider dropped: {count} records as duplicates".format(
            name=spider.name, count=spider.crawler.stats.get_value("records_dropped"))
        )
        
