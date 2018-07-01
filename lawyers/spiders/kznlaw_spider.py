# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from datetime import datetime
from lawyers.items import KZNLawItem
from lawyers.scrapy_logger import get_logger
import itertools

class KZNLawSpider(scrapy.Spider):
    name = 'kznlawyers'
    item = KZNLawItem
    allowed_domains = ['www.lawsoc.co.za']

    def __init__(self, *args, **kwargs):
        self.logger.logger = get_logger(KZNLawSpider.name)
        self.base_url = 'https://www.lawsoc.co.za/default.asp?id=1418'
        return super(KZNLawSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.logger.info("Started KZN Law Society spider")
        yield FormRequest(url=self.base_url, callback=self.parse, formdata={'search' : '1', 'paging' : '1'})

    def parse(self, response):
        last_idx = int(response.xpath('//span[@class="paging_normal"]')[-1].re("\[([^]]*)\]")[0].split("-")[1].strip())
        for idx in itertools.count(start=1, step=50):
            print last_idx
            if idx > last_idx:
                break
            yield FormRequest(url=self.base_url, formdata={'search' : '1', 'paging' : str(idx)}, callback=self.parse_body)
    def parse_body(self, response):
        print response.request.body
        def u(x):
            return x.strip()

        for chunk in response.xpath('//form[@name="searchform3"]/table/tr'):
            kznlawitem = KZNLawItem(
                title=u(chunk.xpath("normalize-space(./td[1]/text())").extract_first()),
                initials=u(chunk.xpath("normalize-space(./td[2]/text())").extract_first()),
                surname=u(chunk.xpath("normalize-space(./td[3]/text())").extract_first()),
                firm_name=u(chunk.xpath("normalize-space(./td[4]/text())").extract_first()),
                location=u(chunk.xpath("normalize-space(./td[5]/text())").extract_first()),
                telno=u(chunk.xpath("normalize-space(./td[6]/text())").extract_first()),
                practice_number=u(chunk.xpath("normalize-space(./td[7]/text())").extract_first()),
                admission=u(chunk.xpath("normalize-space(./td[8]/text())").extract_first()),
                speciality_description=u(chunk.xpath("normalize-space(./td[9]/text())").extract_first()),
                scraped_date=datetime.now()
            )

            if kznlawitem["initials"] and kznlawitem["surname"]:
                yield kznlawitem
