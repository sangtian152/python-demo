# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/python3

import time
import numpy as np
from numpy import ndarray
import xlwt
import xlrd
import requests

username = ''
pwd = ""
server = ''
org_name = ''
app_name = ''

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'cookie': 'Hm_lvt_6b7b8615af4a1f51df2500d655268be1=1665651018; auth.token=JT5xWCtJz0LIN8be; Hm_lvt_0b726272e9aed3b1c5ea0a02b3c7a45c=1665651344; Hm_lpvt_0b726272e9aed3b1c5ea0a02b3c7a45c=1665651344; auth.token=JT5xWCtJz0LIN8be; Hm_lpvt_6b7b8615af4a1f51df2500d655268be1=1665651371',
    'authorization': 'Bearer JT5xWCtJz0LIN8be',
    'Origin': server,
    'Referer': server,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Access-Source': 'roc'
}


# xlwt,xlrd是python将数据导入excel表格使用的库

wb = xlwt.Workbook()
# 添加一个表
ws = wb.add_sheet('test')

wb.save('test.xls')


def save_xls():
    # 将数据导出，保存格式为xxx.xls。其中xxx与上文表名同步
    # 注意此处一定要保存为.xls形式，如果是xlsx会打不开
    wb.save('test.xls')


def write_xls(row, data):
    # 添加数据使用.write函数（横坐标，纵坐标，内容）注意横纵坐标从0开始，横纵坐标即对于excel而言
    ws.write(row, 3, data['company'])
    ws.write(row, 2, data['cityname'])
    ws.write(row, 4, data['position'])
    ws.write(row, 0, data['realname'])
    ws.write(row, 1, data['phone'])


def save_json(file_name, file_content):
    with open(file_name.replace('/', '_') + '.json', 'wb') as f:
        f.write(file_content.encode('utf-8', 'replace'))


def func_get(url, params={}):
    res = requests.get(url=server + url, params=params, headers=headers)  # 发起请求
    res.encoding = 'utf-8'
    return res.json()


def get_apps(page):
    params = {'keyword': '', 'id': '8abbaf3595cb', 'page': page, 'size': 50}
    print('----------正在获取列表----------')
    res = func_get('/url', params)
    print(res)
    if -1 < res['next']:
        print(str(page) + '----------获取列表成功----------')
        r = (page - 1) * 50
        for ele in res['list']:
            write_xls(r, ele['card'])
            r += 1
        save_xls()
        time.sleep(5)
        get_apps(res['next'])
    else:
        print(res)


def print_hi():
    a1 = [1]
    a2 = [2, 3]
    a = np.concatenate((a1, a2))
    print(a)  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_apps(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
