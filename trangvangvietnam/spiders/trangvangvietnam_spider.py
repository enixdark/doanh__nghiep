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
from ..items import TVVNItem
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from pymongo import MongoClient
class TrangVangVietNamSpider(CrawlSpider):
	name = "trangvangvietnam"
	allowed_domains = [
		"trangvangvietnam.com"
	]

	start_urls = [
		'http://trangvangvietnam.com'
	]

	__queue = [
	r'trangvangvietnam.com\/dangky\/*',
	r'trangvangvietnam.com\/subpages\/*',
	r'pic.trangvangvietnam.com\/\d+\/[._\w\d]+',
	r'online.gov.vn',
	r'en.trangvangvietnam.com',
	r'http://trangvangvietnam.com\/findex\/',
	r'http://trangvangvietnam.com\/findex.asp',
	r'products\/[\d\w\/._-]+'
	]
	client = MongoClient(settings.get('MONGODB_URI'))
	db = client[settings.get('MONGODB_DATABASE')]

	cursor = db[settings.get("CRAWLER_COLLECTION")].find({}, {"url": 1})
	for i in cursor:
		if 'url' in i:
			__queue.append(i['url'])

	rules = [
	    Rule(
	    	LinkExtractor(allow=(
	    		# r'[-\w]+\/',
	    		r'listings\/[\d\w\/._%&-]+',
	    		r'categories\/[\d\w\/._%&-]+'
	    	), deny=__queue,
	    	restrict_xpaths=[
	    		# r'//div[6]/section[1]/div/div/div/div[2]/div/div[3]',
	    		# r'//div[6]/section[1]/div/div/div/div[2]/div',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[1]/div/div/div[1]',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[3]/div/div/div/div[3]/div/div/div[3]/div',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[3]/div/div/div/div[3]/div/div/div[4]',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[4]/div/div'
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
		item['url'] = sel.url
		if 'listings' in response.url:
			# import ipdb; ipdb.set_trace()
			item['company_name'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[1]//text()')
			item['rating'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[2]/div[1]//@src')
			item['address'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[1]/div[2]/text()')
			item['email'] =  self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[4]/div[2]//text()')
			item['website'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[5]/div[2]//text()')
			item['phone'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[2]/div[2]//text()')
			item['fax'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[3]/div[2]//text()')
			item['category_market'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[7]/div[2]//text()')
			item['category_product'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[3]/div[@class="detail_dc"]/div[6]/div[2]//text()')
			item['summary'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]/div[5]//text()')
			item['bussiness'] = self.extract(sel,'//div[2]/div[@id="main_businessdetail"]/div[1]//div[@style="margin-bottom:12px"]//text()',';')
			item['products'] = []

			for product in sel.xpath('//div[2]/div[@id="main_businessdetail"]/div[1]//div[@class="nhomsanphambox"]'):
				pd_name = self.extract(product,'div[@class="nhomsanpham_txtbold"]//text()')
				pd_products = self.extract(product,'div[@class="nhomsanpham_li2"]//text()')
				item['products'].append({pd_name:pd_products})
			#data = sel.xpath('//div[2]/div[@id="main_businessdetail"]/div[1]//div[@class="texthoso"]/text()').extract()
			try:
				item['tax_code'] = sel.xpath('//div[2]/div[@id="main_businessdetail"]/div[1]//div[@class="texthoso"]/text()').extract()[2].strip()
			except Exception,e:
				item['tax_code'] = ''
			try:
				item['established'] = sel.xpath('//div[2]/div[@id="main_businessdetail"]/div[1]//div[@class="texthoso"]/text()').extract()[3].strip()
			except Exception,e:
				item['established'] = ''
			try:
				item['num_employees'] = sel.xpath('//div[2]/div[@id="main_businessdetail"]/div[1]//div[@class="texthoso"]/text()').extract()[5].strip()
			except Exception,e:
				item['num_employees']  = ''


		return item


