import MySQLdb  
import MySQLdb.cursors
from twisted.enterprise import adbapi
class MyMysqlPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',  
                db = 'tieba',  
                user = 'root',  
                passwd = '',  
                cursorclass = MySQLdb.cursors.DictCursor,  
                charset = 'utf8',  
                use_unicode = False  
        )  

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self._conditional_insert, item)  
		return item
	def _conditional_insert(self, tx, item):
		tx.execute(\
                	"insert into info (title,count,url) "
                	"values (%s, %s,%s)",
                	(item['title'],
                 	len(item['image_urls']),
			item['url'])
            	)

