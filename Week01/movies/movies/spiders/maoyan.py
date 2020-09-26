import scrapy
from scrapy.selector import Selector
from movies.items import MoviesItem
from lxml import etree

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # selector 和 selectorList 都有 xpath 方法
        # 后者是对每个元素进行 xpath 方法
        # movies = Selector(response=response).xpath('//dl[@class="movie-list"]//dd/div[1]/a/@href')
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]/a/@href')  # 与上等同
        # print(movies.extract())

        # movie = movies.xpath('./dd[1]')
        # print(movie)
        #
        # movie = movies.xpath('.//dd/div[1]/a/@href')
        # print(movie)

        # 后面是 SelectorList 类型，直接使用 ‘,’解包
        # print(movies.extract_first())

        # print(movies.getall())
        # print(movies.extract())  # 相同，返回列表
        #
        # print(movies.get())  # 相同，返回单个元素
        # print(movies.extract_first())
        #
        # print(movies[0])
        # # print(movies[0].extract_first())  # 错误， sector 没有这个属性
        # print(movies[0].extract())
        # print(movies[0].get())
        # print(movies[0].getall())  # 列表


        # with open('test2.xml', 'w', encoding='utf-8') as f:
        #     f.write(movies.extract_first())

        # s = './dd[' + str(2) + ']/div[1]/a/@href'

        #
        # movie = movies.xpath('.//dd[2]')
        # print(movie)

        # links = []
        # for i in range(1, 11):
        #     print(i)
        #     # 错误，dd下面有两个div，每个 div 下面有两个 a
        #     # movie = movies.xpath('./dd[' + str(i) + ']/div/a/@href')
        #     s = './dd[' + str(2) + ']/div[1]/a/@href'
        #     print(s)
        #     movie = movies.xpath(s)
        #     print(movie)
            # link = movie.extract_first()
            # print(type(link))
            # print(link)
            # links.append(link)
            # print(link)
            # yield scrapy.Request(url=link, callback=self.parse2)
        # print(links)
        for i in range(10):
            link = 'https://maoyan.com' + movies[i].get()
            # print(link)
            yield scrapy.Request(url=link, callback=self.parse2)

    def parse2(self, response):
        item = MoviesItem()
        content = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        file_name = content.xpath('./h1/text()').get()
        file_types = '，'.join(x.get().strip() for x in content.xpath('./ul/li[1]/a/text()'))
        file_date = content.xpath('./ul/li[3]/text()').get()

        item['file_name'] = file_name
        item['file_types'] = file_types
        item['file_date'] = file_date
        yield item
        # print(file_name, file_types, file_date)
