# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class MoviesPipeline:
    def process_item(self, item, spider):
        file_name = item['file_name']
        file_types = item['file_types']
        file_date = item['file_date']

        # 建立连接，打开游标
        conn = pymysql.connect(host='localhost', user='root', password='123456',
                               database='test', charset='utf8mb4')
        cur = conn.cursor()

        # 插入数据
        sql = 'insert into movies values (%s, %s, %s);'
        try:
            cur.execute(sql, [file_name, file_types, file_date])
            conn.commit()
        except:
            conn.rollback()

        # 关闭游标，关闭连接
        cur.close()
        conn.close()

        # 莫忘返回，能够在 console 里打印出来
        return item


