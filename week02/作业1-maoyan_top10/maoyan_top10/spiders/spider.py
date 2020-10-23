# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from maoyan_top10.items import MaoyanTop10Item
import lxml.etree

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3/']
    mylist = []

    # def parse(self, response):
    #     pass

    def start_requests(self):
        # linkage = []
        # for i in range(0, 10):
        url = 'https://maoyan.com/films?showType=3'
        cookie = '__mta=188510743.1595690912462.1595691195672.1595691202506.4; uuid_n_v=v1; uuid=4279B570CE8B11EAB807BDA3D83E4DB4CA67D4B5A86B457D82575C73F1470534; _csrf=aaefc8f7e83102d4a3432576c7b75b516ee11fc030a409205c38f02feb2076ec; __guid=17099173.3222883424512248300.1595690909079.48; mojo-uuid=61aa3f55d618f7e6d1763119e3a3ad50; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595690912; _lxsdk_cuid=17386970a8dc8-0987116033d0a5-4e4c0f20-13c680-17386970a8dc8; _lxsdk=4279B570CE8B11EAB807BDA3D83E4DB4CA67D4B5A86B457D82575C73F1470534; mojo-session-id={"id":"1175d09fe22cd78d2df6a0f802c2f644","time":1595697040165}; monitor_count=7; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595697625; __mta=188510743.1595690912462.1595691202506.1595697625362.5; _lxsdk_s=17386d46e5a-afc-a34-750%7C%7C8'
        cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
        try:
            yield scrapy.Request(url=url, cookies=cookies,callback=self.parse) #这里的Request其实是调用downloader下载器
        except Exception as e:
            print(e)

        # url 请求访问的网址
            # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
            # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数


    # 解析函数
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(response.text)

        title_list = soup.find_all('dd')
            # for i in range(len(title_list)):
            # 在Python中应该这样写
        for i in title_list:
            # 在items.py定义
            item = MaoyanTop10Item()
            # title = i.find('a').find('span').text
            link = 'https://maoyan.com'+i.find('a').get('href')
            # item['title'] = title
            item['link'] = link
            try:
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)
            except Exception as d:
                print(d)

    def parse2(self, response):

        item = response.meta['item']
        # soup = BeautifulSoup(response.text, 'html.parser')
        # content = soup.find('div', attrs={'class': 'related-info'}).get_text().strip()
        # item['content'] = content

        selector = lxml.etree.HTML(response.text)

        # 电影名称
        film_name = selector.xpath('//*[@class="movie-brief-container"]/h1/text()')
        # print(f'电影名称: {film_name}')

        # 电影类型
        film_type_raw = selector.xpath('//*[@class="text-link"]/text()')
        film_type = "/".join(film_type_raw)
        # print(f'电影类型: {film_type}')

        # 上映时间
        film_time = selector.xpath('//*[@class="movie-brief-container"]/ul/li[3]/text()')
        time = film_time[0][:10]
        # print(f'上映时间：{time}')

        item['film_name'] = film_name[0]
        item['film_type'] = film_type
        item['time'] = time

        list = [item['film_name'], item['film_type'], item['time']]
        self.mylist.append(list)
        # print('************************')
        # for i in self.mylist:
        #     print(i)
        # print('************************')

        yield item

    #     import pandas as pd
    #
    #     maoyan_movie = pd.DataFrame(data=self.mylist)
    #
    #     # windows需要使用gbk字符集
    #     maoyan_movie.to_csv('./maoyan_movie2.csv', encoding='gbk', index=False, header=False)