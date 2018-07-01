import scrapy
from datetime import datetime
from lawyers.items import CourtRoll
from lawyers.scrapy_logger import get_logger

class CourtRollSpider(scrapy.Spider):
    name = "courtroll"
    item = CourtRoll

    def __init__(self, *args, **kwargs):
        self.logger.logger = get_logger(CourtRollSpider.name)
        return super(CourtRollSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.logger.info("Started Johannesburg Court Roll spider")
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

