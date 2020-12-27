import scrapy
from scrapy.selector import Selector
from products.items import ProductsItem
from copy import deepcopy


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['smzdm.com']
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    # 解析商品链接，存储商品名称
    def parse(self, response, **kwargs):
        item = ProductsItem()
        contents = Selector(response).xpath('//*[@id="feed-main-list"]/li[@class="feed-row-wide"]')
        for content in contents[:10]:

            phone_name = content.xpath('div/div[2]/h5/a/text()').get().strip()
            item['phone_name'] = phone_name.split(': ')[-1]

            link = content.xpath('div/div[2]/h5/a/@href').get()
            # 深拷贝，不然总是显示最后一个
            yield scrapy.Request(url=link, meta={'item': deepcopy(item)}, callback=self.parse2)

    # 解析评论链接
    def parse2(self, response):
        item = response.meta['item']
        pages = 1
        comments_block = Selector(response).xpath('//*[@id="commentTabBlockNew"]/ul')
        # 判断是否有多页
        if len(comments_block) == 2:
            pages = int(comments_block[-1].xpath('li[last()-3]/a/text()').get())

        for i in range(1, pages+1):
            link = response.url + 'p' + str(i)
            # 重复的请求不过滤
            yield scrapy.Request(url=link, meta={'item': deepcopy(item)},
                                 callback=self.parse3, dont_filter=True)

    # 提取评论
    def parse3(self, response):
        print('hello')
        item = response.meta['item']
        comments = Selector(response).xpath('//*[@id="commentTabBlockNew"]/ul[1]/li[@class="comment_list"]')
        for comment in comments:
            short = comment.xpath('div[2]/div[@class="comment_conWrap"]/div[1]/p/span/text()').get().strip()
            item['short'] = short
            yield item
