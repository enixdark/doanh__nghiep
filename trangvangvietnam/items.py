# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TVVNItem(scrapy.Item):
    company_name = scrapy.Field()
    email = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    category_market = scrapy.Field()
    category_product = scrapy.Field()
    summary = scrapy.Field()
    bussiness = scrapy.Field()
    products = scrapy.Field()
    tax_code = scrapy.Field()
    rating = scrapy.Field()
    established = scrapy.Field()
    num_employees =scrapy.Field()
