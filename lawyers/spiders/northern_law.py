# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from datetime import datetime
from lawyers.items import NorthernLawItem
from lawyers.scrapy_logger import get_logger


class NorthernLawSpider(scrapy.Spider):
    name = 'northern_law'
    item = NorthernLawItem

    allowed_domains = ['northernlaw.privyseal.com']
    start_urls = ['http://northernlaw.privyseal.com/']

    def __init__(self, *args, **kwargs):
        self.logger.logger = get_logger(NorthernLawSpider.name)
        return super(NorthernLawSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.logger.info("Started Northern Law Society spider")
        urls = [
            'https://northernlaw.privyseal.com/find-an-attorney?directory=%s',
            'https://northernlaw.privyseal.com/find-a-conveyancer?directory=%s',
            'https://northernlaw.privyseal.com/find-a-notary?directory=%s',
            'https://northernlaw.privyseal.com/find-a-law-firm?directory=%s'
        ]

        for base_url in urls:
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                url = base_url % letter
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        northernlawitem = NorthernLawItem()
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

            northernlawitem = NorthernLawItem(
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
            yield northernlawitem

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
