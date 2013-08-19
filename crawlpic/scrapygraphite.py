from scrapy.statscol import StatsCollector
from galena import Galena

GRAPHITE_HOST = 'localhost'
GRAPHITE_PORT = 2003
GRAPHITE_IGNOREKEYS = ["envinfo/pid"]

class GraphiteStatsCollector(StatsCollector):
    def __init__(self, crawler):
        super(GraphiteStatsCollector, self).__init__(crawler)

        host = crawler.settings.get("GRAPHITE_HOST", GRAPHITE_HOST)
        port = crawler.settings.get("GRAPHITE_PORT", GRAPHITE_PORT)

        self.ignore_keys = crawler.settings.get("GRAPHITE_IGNOREKEYS", 
                                                GRAPHITE_IGNOREKEYS)
        self.crawler = crawler
        self._galena = Galena(host=host, port=port)

    def _get_stats_key(self, spider, key):
        if spider is not None:
            return "scrapy/spider/%s/%s" % (spider.name, key)
        return "scrapy/%s" % (key)

    def set_value(self, key, value, spider=None):
        super(GraphiteStatsCollector, self).set_value(key, value, spider)
        self._set_value(key, value, spider)

    def _set_value(self, key, value, spider):
        if isinstance(value, (int, float)) and key not in self.ignore_keys:
            k = self._get_stats_key(spider, key)
            self._galena.send(k, value)

    def inc_value(self, key, count=1, start=0, spider=None):
        super(GraphiteStatsCollector, self).inc_value(key, count, start, spider)
        self._galena.send(self._get_stats_key(spider, key), 
                            self.crawler.stats.get_value(key))

    def max_value(self, key, value, spider=None):
        super(GraphiteStatsCollector, self).max_value(key, value, spider)
        self._galena.send(self._get_stats_key(spider, key), 
                            self.crawler.stats.get_value(key))

    def min_value(self, key, value, spider=None):
        super(GraphiteStatsCollector, self).min_value(key, value, spider)
        self._galena.send(self._get_stats_key(spider, key), 
                            self.crawler.stats.get_value(key))

    def set_stats(self, stats, spider=None):
        super(GraphiteStatsCollector, self).set_stats(stats, spider)
        for key in stats:
            self._set_value(key, stats[key], spider)
