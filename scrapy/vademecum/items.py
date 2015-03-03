# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VademecumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    alternative = scrapy.Field()
    concept = scrapy.Field()
    url = scrapy.Field()
    
    # First sentence
    definition = scrapy.Field()
    
    # Full text
    description = scrapy.Field()
    
    # List of all the links in the page
    links = scrapy.Field()
    
    # Related topics
    broader = scrapy.Field()
    narrower = scrapy.Field()
    
    # List with examples.
    examples = scrapy.Field()