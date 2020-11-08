import scrapy
from scrapy.selector import Selector
from movie.items import MovieItem
from selenium import webdriver
import time


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/1292064/']  # 楚门的世界

    def parse(self, response, **kwargs):
        # 爬取 3 页
        for i in range(3):
            link = 'comments?start=' + str(i * 20) + '&limit=20&status=P&sort=new_score'
            # 路径拼接：response.urljoin(link)
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse2)

    def parse2(self, response):
        star_to_num = {
            '力荐': 5,
            '推荐': 4,
            '还行': 3,
            '较差': 2,
            '很差': 1,
        }
        item = MovieItem()
        # 最后 class 空格不能省略 /div[@class="comment-item "]
        comments = Selector(response=response).xpath('//*[@id="comments"]/div[@class="comment-item "]')
        for comment in comments:
            star = comment.xpath('./div[2]/h3/span[2]/span[2]/@title').get()
            if star not in star_to_num:  # 处理没有评分的情况，那上面得到的是完整时间，比如 2020-05-17 17:27:09
                continue
            star = star_to_num[star]
            record_time = comment.xpath('./div[2]/h3/span[2]/span[3]/text()').get().strip()
            short = comment.xpath('./div[2]/p/span/text()').get()

            item['short'] = short
            item['star'] = star
            item['record_time'] = record_time

            yield item
