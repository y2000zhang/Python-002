from selenium import webdriver
import time
import json

#第一次登陆，自动完成登录过程并将cookies存放到本地文件，以备第二次登录时，免输入用户名及密码
try:
    browser = webdriver.Chrome()
    browser.get('https://shimo.im/welcome')
    time.sleep(1)
    btm1 = browser.find_element_by_xpath('//*[@class="login-button btn_hover_style_8"]')
    btm1.click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@name="mobileOrEmail"]').send_keys('13983644971')
    browser.find_element_by_xpath('//*[@name="password"]').send_keys('123456')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@class="sm-button submit sc-1n784rm-0 bcuuIb"]').click()

    # 获取cookie并通过json模块将dict转化成str
    dictCookies = browser.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    # 登录完成后，将cookie保存到本地文件
    with open('cookies.json', 'w') as f:
        f.write(jsonCookies)
    time.sleep(3)
except Exception as e:
    print(e)
finally:
    # browser.close()
    pass

# 第二次登录网站时，通过读取存储到本地的cookie直接进入
browser = webdriver.Chrome()
browser.get('https://shimo.im/welcome')
# 删除第一次建立连接时的cookie
browser.delete_all_cookies()
with open('cookies.json', 'r', encoding='utf-8') as f:
    listCookies = json.loads(f.read())
for cookie in listCookies:
    # print(cookie['name'])
    browser.add_cookie({
        # 'domain':'.shimo.im',
        'name': cookie['name'],
        'value': cookie['value'],
        'path': cookie['path'],
        # 'expires': None
        'httpOnly':cookie['httpOnly'],
        'secure':cookie['secure']
    })
# 再次访问页面，便可实现免登陆访问
browser.get('https://shimo.im/welcome')
btm1=browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a/button')
btm1.click()
