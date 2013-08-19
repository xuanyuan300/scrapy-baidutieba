#!/usr/bin/env python
#conding utf-8
from BeautifulSoup import BeautifulSoup
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import urllib
from crawlpic.items import CrawlpicItem
class crawlpic(BaseSpider):
	name="tieba"
	start_urls=[
		"http://tieba.baidu.com/f/index/forumpark?cn=%CA%A7%C1%B5&ci=39&pcn=%D0%D4%C7%E9%D6%D0%C8%CB&pci=229&ct=0"
	]
	def parse(self,response):
		print response.url
		urlcontent=urllib.urlopen(response.url).read()
#		print urlcontent
		soup=BeautifulSoup(urlcontent)
		for i in range(16):
			url=soup.findAll('a',limit=43)[27+i]['href']
			relurl="http://tieba.baidu.com" + url
			yield Request(relurl, callback=self.parse_detail)
		
	def parse_detail(self,response):
		try:
			urllist=urllib.urlopen(response.url).read()
			soup=BeautifulSoup(urllist)
			next="http://tieba.baidu.com" + soup.findAll('a')[-7]['href']
			if next:
				yield Request(url=next,callback=self.parse_detail)
			num=len(soup.findAll('a',{"class":"ba_href clearfix"}))
			for i in range(num):
				url=soup.findAll('a',{"class":"ba_href clearfix"})[i]['href']
				relurl="http://tieba.baidu.com" + url
				yield Request(relurl, callback=self.parse_detailmore)
		except Exception,e:
			print e
	def parse_detailmore(self,response):
		hxs=HtmlXPathSelector(response)
#		items=[]
		next_link="http://tieba.baidu.com" + hxs.select('//*[@id="frs_list_pager"]/a[@class="next"]/@href').extract()[0]
		if next_link:
			yield Request(url=next_link,callback=self.parse_detailmore)
		relpicurl=hxs.select('//*/li/div/img/@bpic').extract()
#		for i in relpicurl:
#			yield Request(url=i,callback=self.picitem)
		title=hxs.select('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/a/text()').extract()[0]
		item=CrawlpicItem()
                item['image_urls']=relpicurl
		item['title']=title
		item['url']=response.url
#		print item['title']
		yield item
#	def picitem(self,response):
#		hxs=HtmlXPathSelector(response)
#		relpicurl=hxs.select('//*/li/div/img/@bpic').extract()
#		for i in relpicurl:
#			filename=i.split("/")[-1]
#			urllib.urlretrieve(i,'/mnt/%s' %filename)	
#		item=CrawlpicItem()
#		item['image_urls']=relpicurl
#		items.append(item)
#		return  item
