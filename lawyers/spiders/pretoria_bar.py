# -*- coding: utf-8 -*-
import scrapy


class PretoriaBarSpider(scrapy.Spider):
    name = 'pretoria_bar'
    allowed_domains = ['www.pretoriabar.co.za']
    start_urls = ['http://www.pretoriabar.co.za/']

    def parse(self, response):
        pass
