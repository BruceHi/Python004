# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class MoviesPipeline:

    def open_spider(self, spider):
        # 建立连接，打开游标
        self.conn = pymysql.connect(host='localhost', user='root', password='123456',
                                    database='test', charset='utf8mb4')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        file_name = item['file_name']
        file_types = item['file_types']
        file_date = item['file_date']
        # 插入数据
        sql = 'insert into movies values (%s, %s, %s);'
        try:
            self.cur.execute(sql, [file_name, file_types, file_date])
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        # 关闭游标，关闭连接
        self.cur.close()
        self.conn.close()
