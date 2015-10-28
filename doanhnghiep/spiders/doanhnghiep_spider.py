# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider , Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from bs4 import BeautifulSoup, Comment
from scrapy.conf import settings
#from selenium import webdriver
import time
import datetime
from ..items import TVVNItem
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from pymongo import MongoClient
class TrangVangVietNamSpider(CrawlSpider):
	name = "doanhnghiep"
	allowed_domains = [
		"cafef.vn",
		"http://cafef.vn"

	]

	start_urls = [	
		r'http://cafef.vn',
		r'http://cafef.vn/doanh-nghiep.chn',
	]

	__queue = [
		r'http://embed2.linkhay.com'
		# r'http://cafef.vn/thoi-su*',
		# r'http://cafef.vn/thi-truong-trung-khoan*',
		# r'http://cafef.vn/bat-dong-san*',
		# r'http://cafef.vn/tai-chinh-ngan-hang*',
		# r'http://cafef.vn/tai-chinh-quoc-te*',
		# r'http://cafef.vn/vi-mo-dau-tu*',
		# r'http://cafef.vn/hang-hoa-nguyen-lieu*',
		# r'http://cafef.vn/du-lieu*',
		# r'http://cafef.vn/videos*'
	]
	# client = MongoClient(settings.get('MONGODB_URI'))
	# db = client[settings.get('MONGODB_DATABASE')]

	# cursor = db[settings.get("CRAWLER_COLLECTION")].find({}, {"url": 1})
	# for i in cursor:
	# 	if 'url' in i:
	# 		__queue.append(i['url'])

	rules = [
	    Rule(
	    	LinkExtractor(allow=(
	    		r'doanh-nghiep.chn',
	    		r'doanh-nghiep\/[\d\w\/._%&-]+',
	    	), deny=__queue,
	    	restrict_xpaths=[
	    	]), 
	    	callback='parse_extract_data', follow=True
	    	)
	    ]

	def extract(self,sel,xpath,split = ''):
		try:
			data = sel.xpath(xpath).extract()
			text = filter(lambda element: element.strip(),map(lambda element: element.strip(), data))
			return split.join(text)
			# return re.sub(r"\s+", "", ''.join(text).strip(), flags=re.UNICODE)
		except Exception, e:
			raise Exception("Invalid XPath: %s" % e)


	def parse_extract_data(self, response):
		item = TVVNItem()
		sel = response

		if 'doanh-nghiep' in response.url:
			item['url'] = sel.url
			# import ipdb; ipdb.set_trace()
			item['title'] = self.extract(sel,'//div[@class="newscontent"]/div[1]/h1/text()')
			item['write_date'] = self.extract(sel,'//p[@class="date"]//text()')
			item['content'] = '\n'.join([self.extract(sel,'//div[@class="newscontent_right"]//h2[@class="sapo"]//text()'),
			self.extract(sel,'//div[@class="newscontent_right"]//div[@class="newsbody"]//text()')])
			item['author'] = self.extract(sel,'//p[@class="author"]//text()')
			item['source'] = self.extract(sel,'//p[@class="source"]//text()')
			item['crawl_date'] = datetime.datetime.strftime(datetime.datetime.now(),"%b %d %Y %H:%M:%S")
			return item