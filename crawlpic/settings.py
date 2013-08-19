# Scrapy settings for crawlpic project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawlpic'

SPIDER_MODULES = ['crawlpic.spiders']
NEWSPIDER_MODULE = 'crawlpic.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlpic (+http://www.yourdomain.com)'
ITEM_PIPELINES = [
#		'scrapy.contrib.pipeline.images.ImagesPipeline',
#		'crawlpic.pipelines.redispipeline.RedisPipeline',
		'crawlpic.pipelines.imagepipeline.MyImagesPipeline',
		'crawlpic.pipelines.mysqlpipeline.MyMysqlPipeline',
#		'crawlpic.pipelines.FSImagesStore',
		]

IMAGES_STORE ='/mnt/images'
IMAGES_EXPIRES = 1

DNSCACHE_ENABLED = True
#LOG_FILE = "logs/scrapy.log"

#enables scheduling storing requests queue in redis
SCHEDULER = "crawlpic.scrapy_redis.scheduler.Scheduler"
# don't cleanup redis queues, allows to pause/resume crawls
SCHEDULER_PERSIST = False 
# Schedule requests using a queue (FIFO)
SCHEDULER_QUEUE_CLASS = 'crawlpic.scrapy_redis.queue.SpiderPriorityQueue'

STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'
GRAPHITE_HOST = "localhost"
GRAPHITE_PORT = 2003 

RedirectMiddleware=False
