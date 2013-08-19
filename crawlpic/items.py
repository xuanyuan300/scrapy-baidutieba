# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.conf import settings
import os 
#print settings.images_store 
class CrawlpicItem(Item):
    # define the fields for your item here like:
    # name = Field()
	image_urls=Field()
	images=Field()
	title=Field()
	image_paths=Field()
	url=Field()

