import os
import scrapy
from dateutil import parser
from datetime import datetime
from jhb_bar.items import CourtRoll

def eorz(x):
    return x[0].strip() if x else None

def dateorz(x):
    try:
        if type(x) == list:
            x = x[0]
        return parser.parse(x)
    except (ValueError, TypeError, IndexError):
        return None

class CourtRollSpider(scrapy.Spider):
    name = "courtroll"
    item = CourtRoll

    def start_requests(self):
        urls = [
            'https://johannesburgbar.co.za/court-rolls/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_courtroll(self, response):
        for chunk in response.xpath('//*[@id="main"]/div[2]/div/main/article/div/div/div/div/article/div[2]/header'):
            courtroll = CourtRoll(
                name=chunk.xpath('normalize-space(./h2/a/text())').extract_first(),
                file_urls=[chunk.xpath('./div/div/p/a/@href').extract_first()],
                time=chunk.xpath('./span[3]/time/text()').extract_first(),
                scraped_date=datetime.now()
            )

            yield courtroll

        for href in response.xpath("//ul[contains(@class, 'frm_pagination')]//a/@href").extract():
            yield response.follow(href, self.parse_lawyers)

    def parse(self, response):
        for href in response.xpath('//*[@id="main"]/div[2]/div/main/article/div/div/div/div/div/nav/a/@href').extract():
            yield response.follow(href, self.parse_courtroll)

