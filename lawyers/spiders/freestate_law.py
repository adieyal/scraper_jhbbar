# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from datetime import datetime
from lawyers.items import FreeStateLawItem
from lawyers.scrapy_logger import get_logger

class FreeStateLawSpider(scrapy.Spider):
    name = 'freestatelawyers'
    item = FreeStateLawItem
    allowed_domains = ['fs-law.privyseal.com']

    def __init__(self, *args, **kwargs):
        self.logger.logger = get_logger(FreeStateLawSpider.name)
        return super(FreeStateLawSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.logger.info("Started Free State Law Society spider")
        urls = [
            'https://fs-law.privyseal.com/find-an-attorney?directory=%s',
            'https://fs-law.privyseal.com/find-a-conveyancer?directory=%s',
            'https://fs-law.privyseal.com/find-a-notary?directory=%s',
            'https://fs-law.privyseal.com/find-a-law-firm?directory=%s'
        ]

        for base_url in urls:
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                url = base_url % letter
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        freestatelawitem = FreeStateLawItem()
        anchor = response.xpath('//*[@id="FindAttorneyResults"]')[0]
        lawyers = zip(
            anchor.xpath('./label[text()="Attorney:"]/following-sibling::div/text()').extract(),
            anchor.xpath('./label[text()="Firm Name:"]/following-sibling::text()[1]').extract(),
            anchor.xpath('./label[text()="Physical Address:"]/following-sibling::text()[1]').extract(),
            anchor.xpath('./label[text()="Postal Address:"]/following-sibling::text()[1]').extract(),
            anchor.xpath('./label[text()="Phone:"]/following-sibling::text()[1]').extract(),
            anchor.xpath('./label[text()="Fax:"]/following-sibling::text()[1]').extract(),
            anchor.xpath('./label[text()="Email:"]/following-sibling::text()[1]').extract()
        )

        for lawyer in lawyers:
            url = response.url.split("/")[3].split("?")[0]
            if "find-an-" in url:
                lawyer_type = url.split("find-an-")[1]
            elif "find-a-" in url:
                lawyer_type = url.split("find-a-")[1]

            freestatelawitem = FreeStateLawItem(
                name=lawyer[0],
                firm=lawyer[1],
                physical_address=lawyer[2],
                postal_address=lawyer[3],
                phone=lawyer[4],
                fax=lawyer[5],
                email=lawyer[6],
                lawyer_type=lawyer_type,
                scraped_date=datetime.now()
            )
            yield freestatelawitem

        try:
            if len(lawyers) == 5:
                body = response.request.body
                parts = body.split("=")
                if len(parts) == 2:
                    offset = int(parts[1]) + 5
                else:
                    offset = 5
                yield FormRequest(url=response.url, callback=self.parse, formdata={'offset' : str(offset)})
        except Exception, e:
            import pdb; pdb.set_trace()
