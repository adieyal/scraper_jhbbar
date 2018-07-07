# -*- coding: utf-8 -*-
import scrapy
from lawyers.items import PretoriaBarItem
from datetime import datetime

class PretoriaBarSpider(scrapy.Spider):
    name = 'pretoria_bar'
    item = PretoriaBarItem
    allowed_domains = ['www.pretoriabar.co.za']
    start_urls = ['https://www.pretoriabar.co.za/index.php/list-of-all-members']

    def parse_profile(self, response):
        pretoria_bar = PretoriaBarItem(scraped_date=datetime.now())
        pretoria_bar["name"] = response.css(".title")[0].xpath("text()").extract_first().strip()
        parts = pretoria_bar["name"].split()
        if parts[-1] == "SC":
            parts = parts[0:-1]
        pretoria_bar["name"] = " ".join(parts)

        dates = response.xpath("//div[@class='people']//div[@class='box']//div[@class='span6']")[1].xpath("text()").extract()
        pretoria_bar["date_admission"] = dates[1].strip()
        dates = dates[3:]
        pretoria_bar["date_membership"] = dates[0].strip()
        dates = dates[2:]

        if "Date of Senior Status" in response.body:
            pretoria_bar["date_senior_status"] = dates[0].strip()
            dates = dates[2:]

        if "Tel:" in response.body:
            pretoria_bar["phone"] = dates[0].strip()
            dates = dates[2:]

        if "Fax:" in response.body:
            pretoria_bar["fax"] = dates[0].strip()
            dates = dates[2:]

        if "Mobile:" in response.body:
            pretoria_bar["mobile"] = dates[0].strip()
            dates = dates[2:]

        pretoria_bar["interests"] = []
        for foi in response.xpath("//div[@class='box']//ul/li/text()"):
            pretoria_bar["interests"].append(foi.extract())

        yield pretoria_bar

    def parse(self, response):
        for profile in response.css(".profile-person"):
            url = profile.xpath("./a/@href").extract_first()
            yield response.follow(url, self.parse_profile)
