# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class MoviePipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456',
                                   database='db1', charset='utf8mb4')
        self.cur = self.conn.cursor()
        # 建表，加上自增主键
        sql = """
        CREATE TABLE shorts (
        id INT auto_increment PRIMARY KEY ,
        short varchar(400),
        star int,
        record_time date
        );
        """
        try:
            self.cur.execute(sql)
            print('建表成功。')
            # 建表好像不需要 commit
            self.conn.commit()
        except:
            print('建表失败，可能已经存在表了。')
            self.conn.rollback()

    def process_item(self, item, spider):
        short = item['short']
        star = item['star']
        record_time = item['record_time']

        # 换成 %d 就失败了，只能使用 %s，自动插入主键。
        sql = 'insert into shorts(short, star, record_time) values (%s, %s, %s)'
        try:
            self.cur.execute(sql, [short, star, record_time])
            self.conn.commit()
        except:
            print('插入失败')
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        # 关闭游标，关闭连接
        self.cur.close()
        self.conn.close()
