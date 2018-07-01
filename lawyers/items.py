# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Member(scrapy.Item):
    name = scrapy.Field()
    group = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    cell = scrapy.Field()
    member_type = scrapy.Field()
    admitted = scrapy.Field(serializer=str)
    society = scrapy.Field(serializer=str)
    silk = scrapy.Field(serializer=str)
    seniority = scrapy.Field(serializer=str)
    scraped_date = scrapy.Field(serializer=str)

    def __repr__(self):
        x = "%s%s%s" % (self["name"], self["group"], self["member_type"])
        return x.encode("utf8")

class CourtRoll(scrapy.Item):
    name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    time = scrapy.Field()
    scraped_date = scrapy.Field(serializer=str)

    def __repr__(self):
        x = self["name"]
        return x.encode("utf8")

class CapeLawItem(scrapy.Item):
    first_name = scrapy.Field()
    surname = scrapy.Field()
    practising_at = scrapy.Field()
    specialisation = scrapy.Field()
    telno = scrapy.Field()
    location = scrapy.Field()
    scraped_date = scrapy.Field(serializer=str)

    def __repr__(self):
        x = self["first_name"] + " " + self["surname"] + self["practising_at"]
        return x.encode("utf8")
