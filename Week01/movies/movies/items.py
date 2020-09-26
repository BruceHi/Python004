# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_name = scrapy.Field()
    file_types = scrapy.Field()
    file_date = scrapy.Field()
