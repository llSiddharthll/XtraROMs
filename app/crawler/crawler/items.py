import scrapy

class MyItem(scrapy.Item):
    article_id = scrapy.Field()
    article_title = scrapy.Field()
    article_content = scrapy.Field()
    article_url = scrapy.Field()
    article_image = scrapy.Field()
