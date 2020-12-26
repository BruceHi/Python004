# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ProductsPipeline:
    # 打开连接，建表
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456',
                                   database='work', charset='utf8mb4')
        self.cur = self.conn.cursor()
        sql = """
        CREATE TABLE shorts(
        id INT auto_increment PRIMARY KEY,
		phone_name varchar(100),
        short varchar(400),
        storage_time TIMESTAMP
        );
        """
        try:
            self.cur.execute(sql)
            print('建表成功。')
            self.conn.commit()
        except:
            print('建表失败，可能已经存在表了。')
            self.conn.rollback()

    def process_item(self, item, spider):
        phone_name = item['phone_name']
        short = item['short']
        # 存入 utc_time
        sql = 'insert into shorts(phone_name, short, storage_time) values (%s, %s, UTC_TIMESTAMP())'
        try:
            self.cur.execute(sql, [phone_name, short])
            self.conn.commit()
        except:
            print('插入失败')
            self.conn.rollback()
        return item

    # 关闭游标，关闭连接
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
