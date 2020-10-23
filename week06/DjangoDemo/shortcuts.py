import pymysql as pymysql
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import lxml.etree
import re

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
cookie = '__mta=221532455.1595692043743.1595733379928.1595733443727.5; _lxsdk_s=173894d2686-69c-6f1-f98%7C%7C4; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595737713; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595692044,1595733201,1595733208; __mta=221532455.1595692043743.1595733443727.1595737713392.6; mojo-session-id={"id":"b2a94373440e77bbc2d86f1cda40c5f8","time":1595737713156}; mojo-trace-id=1; _csrf=2c10075ac79860250137c4b640705c3b63d697b6cf78ffb6b7631c0cc3b92539; mojo-uuid=d1258ebf1c78e9c6a25df48e2782cb74; _lxsdk=214AA780CE8E11EA9BFE43BA456BAEDE4D04A84BC03A4AD7895C4A5FAD2326C0; _lxsdk_cuid=17386a84dbec8-0d9afd3c7fac4f8-481d3201-13c680-17386a84dbec8; uuid=214AA780CE8E11EA9BFE43BA456BAEDE4D04A84BC03A4AD7895C4A5FAD2326C0; uuid_n_v=v1'

# header
header = {'user-agent': user_agent, 'cookie': cookie}
# 请求地址
myurl = 'https://movie.douban.com/subject/1292052/comments?start=0&limit=20&sort=new_score&status=P'
response = requests.get(myurl, headers=header)

bs_info = bs(response.text, 'html.parser')

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='rootroot',
                       database='demo',
                       charset='utf8mb4'
                       )
cur = conn.cursor()

MovieListAll = bs_info.find_all('div', attrs={'class': 'comment-item'})
for piece in MovieListAll:
    # 1条，找到movie-hover-title,1条4个。
    OnePiece = piece.find('div', attrs={'class': 'comment'})
    comment = OnePiece.find('span', attrs={'class': 'short'}).text
    rate = OnePiece.find('span', attrs={'class': re.compile('.*rating')})['title']
    comment_time = OnePiece.find('span', attrs={'class': 'comment-time'})['title']
    if rate == "力荐":
        n_star = 5
    elif rate == "推荐":
        n_star = 4
    elif rate == "还行":
        n_star = 3
    elif rate == "较差":
        n_star = 2
    else:
        n_star = 1

    short = [n_star, comment, comment_time]

    sql = u"INSERT INTO shortcuts(n_star, short, sentiment) VALUES(%s,%s,%s)"
    cur.execute(sql, short)
    conn.commit()
