# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import items
import os
import json

class MemberDuplicatesPipeline(object):

    def __init__(self):
        self.cache = set()

    def open_spider(self, spider):
        filename = spider.settings["FEED_URI"] % {"name" : spider.name}

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
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.cache.add(repr(item))
            return item
