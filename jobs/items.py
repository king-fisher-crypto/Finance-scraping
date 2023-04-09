import scrapy

class JobItem(scrapy.Item):
    _id = scrapy.Field()
    task_id = scrapy.Field()
    url = scrapy.Field()
    raw_html = scrapy.Field()