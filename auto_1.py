# -*- coding = UTF-8 -*-
# @Time : 2021/10/23 下午9:24
# @Author : XIADENGMA
# @File : auto_1.py
# @Software : PyCharm
# @achieve : 模拟网页登录(未测试,不可使用)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# 开启浏览器
def openChrome():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_argument("--headless")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)
    return driver

def find(driver,str):
    try:
        driver.find_element_by_xpath(str)
    except:
        return False
    else:
        return True

# 流程
def operate_dk(driver):
    exit_code = os.system('ping www.baidu.com -n 2')#检测网络
    if exit_code:
        url = "http://10.200.0.2/"
        account = "yimiao"
        password = "111111"

        driver.get(url)
        driver.find_element_by_xpath("//input[@placeholder='学号']").send_keys(account)
        driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys(password)
        driver.find_element_by_xpath("//form[@name='f1']//input[@name='0MKKey']").send_keys(Keys.ENTER)
        time.sleep(3)
        print("即将退出程序...")
        driver.quit()
    else:
        driver.quit()

if __name__ == '__main__':
    driver = openChrome()
    operate_dk(driver)
