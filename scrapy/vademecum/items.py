# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VademecumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tittle = scrapy.Field()
    identifier = scrapy.Field()
    concept = scrapy.Field()
