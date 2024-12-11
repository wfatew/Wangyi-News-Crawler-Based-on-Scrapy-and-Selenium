import scrapy

class WangyiproItem(scrapy.Item):
    path = scrapy.Field() #存储新闻的路径
    title = scrapy.Field() #新闻标题
    content = scrapy.Field() #新闻内容