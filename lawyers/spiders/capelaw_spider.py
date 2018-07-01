# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from lawyers.items import CapeLawItem
from lawyers.scrapy_logger import get_logger

class CapeLawSpider(scrapy.Spider):
    name = 'capelawyers'
    item = CapeLawItem
    allowed_domains = ['capelawsoc.law.za']

    def __init__(self, *args, **kwargs):
        self.logger.logger = get_logger(CapeLawSpider.name)
        return super(CapeLawSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.logger.info("Started Cape Law Society spider")
        urls = ['http://capelawsoc.law.za/find-an-attorney/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        capelawitem = CapeLawItem()
        for chunk in response.xpath('//*[@id="tablepress-13"]/tbody/tr'):
            capelawitem = CapeLawItem(
                first_name=chunk.xpath("./td[1]").extract_first(),
                surname=chunk.xpath("./td[2]").extract_first(),
                practising_at=chunk.xpath("./td[3]").extract_first(),
                specialisation=chunk.xpath("./td[4]").extract_first(),
                telno=chunk.xpath("./td[5]").extract_first(),
                location=chunk.xpath("./td[6]").extract_first(),
                scraped_date=datetime.now()
            )
            yield capelawitem

