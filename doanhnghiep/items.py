# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TVVNItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    write_date = scrapy.Field()
    crawl_date = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
