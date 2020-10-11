import scrapy
from scrapy.selector import Selector
from movies.items import MoviesItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response, **kwargs):
        item = MoviesItem()
        content = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in content[:10]:
            file_name = movie.xpath('./div[1]/span/text()').get()
            file_types = movie.xpath('./div[2]/text()')[-1].get().strip()
            file_date = movie.xpath('./div[4]/text()')[-1].get().strip()
            item['file_name'] = file_name
            item['file_types'] = file_types
            item['file_date'] = file_date
            yield item
