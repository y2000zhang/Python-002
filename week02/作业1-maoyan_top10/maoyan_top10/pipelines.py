# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
import pymysql.cursors

        # windows需要使用gbk字符集

class MaoyanTop10Pipeline(object):
    def process_item(self, item, spider):
        # film_name = item['film_name']
        # film_type = item['film_type']
        # time = item['time']
        movie_info = (
            item['film_name'],
            item['film_type'],
            item['time']
        )
        maoyan_movie = pd.DataFrame(data=[movie_info])
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='121',
                               db='test',
                               charset='utf8')

        maoyan_movie.to_csv('./maoyan_movie3.csv', encoding='gbk', index=False, mode='a',header=False)

        # output = f'|{film_name}|\t|{film_type}|\t|{time}|\n\n'
        # with open('./doubanmovie2.csv', 'a+', encoding='gbk') as article:
        #     article.write(output)

        return item
