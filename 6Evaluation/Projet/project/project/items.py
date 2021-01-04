# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    votes = scrapy.Field()
    answers = scrapy.Field()
    date = scrapy.Field()
    views = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    
