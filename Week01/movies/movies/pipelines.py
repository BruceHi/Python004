# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import numpy as np
import os


class MoviesPipeline:
    def process_item(self, item, spider):
        # 一行一行往里面写
        file_name = item['file_name']
        file_types = item['file_types']
        file_date = item['file_date']

        # # 数据形状：(3,) --> (1,3)
        # df = pd.DataFrame(np.array([file_name, file_types, file_date]).reshape(1, 3))

        df = pd.DataFrame([[file_name, file_types, file_date]])

        # 第一次存数据将 header 也写入文件
        if not os.path.isfile('movie2.csv'):
            df.to_csv('movie2.csv', mode='a', index=False, header=['name', 'types', 'date'], encoding='utf-8')
        else:
            df.to_csv('movie2.csv', mode='a', index=False, header=False, encoding='utf-8')
        return item

