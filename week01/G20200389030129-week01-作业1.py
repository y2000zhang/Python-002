import requests
from bs4 import BeautifulSoup as bs
import lxml.etree

# 爬取页面详细信息

# 电影详细页面
url = 'https://maoyan.com/films?showType=3'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
cookie = '__mta=188510743.1595690912462.1595691195672.1595691202506.4; uuid_n_v=v1; uuid=4279B570CE8B11EAB807BDA3D83E4DB4CA67D4B5A86B457D82575C73F1470534; _csrf=aaefc8f7e83102d4a3432576c7b75b516ee11fc030a409205c38f02feb2076ec; __guid=17099173.3222883424512248300.1595690909079.48; mojo-uuid=61aa3f55d618f7e6d1763119e3a3ad50; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595690912; _lxsdk_cuid=17386970a8dc8-0987116033d0a5-4e4c0f20-13c680-17386970a8dc8; _lxsdk=4279B570CE8B11EAB807BDA3D83E4DB4CA67D4B5A86B457D82575C73F1470534; mojo-session-id={"id":"1175d09fe22cd78d2df6a0f802c2f644","time":1595697040165}; monitor_count=7; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595697625; __mta=188510743.1595690912462.1595691202506.1595697625362.5; _lxsdk_s=17386d46e5a-afc-a34-750%7C%7C8'
# 声明为字典使用字典的语法赋值
header = {}
header['user-agent'] = user_agent
header['Cookie'] = cookie
response = requests.get(url, headers=header)
# print(response.text)

bs_info = bs(response.text, 'html.parser')

#以下代码为抓取前10个电影的url
linkage=[]
i=0
for tags in bs_info.find_all('dd'):
    if i>=10:
        break
    else:
        linkage.append('https://maoyan.com'+tags.find('a').get('href'))
        i=i+1
# for lin in linkage:
#     print(lin)
mylist=[]
for kd in linkage:
    response = requests.get(kd, headers=header)
    # print(response.text)
    # xml化处理
    selector = lxml.etree.HTML(response.text)

    # 电影名称
    film_name = selector.xpath('//*[@class="movie-brief-container"]/h1/text()')
    print(f'电影名称: {film_name}')

    # 电影类型
    film_type_raw = selector.xpath('//*[@class="text-link"]/text()')
    film_type="/".join(film_type_raw)
    print(f'电影类型: {film_type}')

    # 上映时间
    film_time = selector.xpath('//*[@class="movie-brief-container"]/ul/li[3]/text()')
    time=film_time[0][:10]
    print(f'上映时间：{time}')

    list = [film_name[0], film_type, str(time)]
    mylist.append(list)

import pandas as pd

maoyan_movie = pd.DataFrame(data = mylist)

# windows需要使用gbk字符集
maoyan_movie.to_csv('./maoyan_movie.csv', encoding='gbk', index=False, header=False)