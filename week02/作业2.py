from selenium import webdriver
import time

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

    # cookies = browser.get_cookies()  # 获取cookies
    # print(cookies)
    time.sleep(3)
except Exception as e:
    print(e)
finally:
    # browser.close()
    pass

