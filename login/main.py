#!/usr/bin/python3
import json
import base64
import requests
from urllib3 import encode_multipart_formdata
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

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
    'Origin': server,
    'Referer': server,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Access-Source': 'roc'
}


def save_json(file_name, file_content):
    with open(file_name.replace('/', '_') + '.json', 'wb') as f:
        f.write(file_content.encode(encoding='utf-8'))


def func_post_form(url, data={}):
    encode_data = encode_multipart_formdata(data)
    data = encode_data[0]
    _headers = headers.copy()
    _headers['Content-Type'] = encode_data[1]
    res = requests.post(url=server + url, data=data, headers=_headers)  # 发起请求
    res.encoding = 'utf-8'
    target = res.json()  # 将获取到的数据变成json类型
    return target


def func_post_json(url, data={}):
    res = requests.post(url=server + url, data=json.dumps(data), headers=headers)  # 发起请求
    res.encoding = 'utf-8'
    target = res.json()  # 将获取到的数据变成json类型
    return target


def func_get(url, params={}):
    res = requests.get(url=server + url, params=params, headers=headers)  # 发起请求
    res.encoding = 'utf-8'
    return res.json()


# def crack_pwd(password, key):
#     public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'  # 注意上述key的格式
#     risky = RSA.importKey(public_key)
#     cipher = Cipher_pkcs1_v1_5.new(risky)  # 生成对象
#     cipher_text = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
#     value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
#     return value

def crack_pwd(password):
    cipher_text = base64.b64encode(password.encode(encoding="utf-8"))  # 对传递进来的用户名或密码字符串加密
    value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return value


def login():
    # response = func_post_json('/workbench/admin/getPublicKey')
    # 全是中文只能加密17个
    print('-------------正在登录-------------')
    # encrypted = crack_pwd(pwd, response['data'])
    encrypted = crack_pwd(pwd)
    payload = {
        'username': username,
        'pwd': encrypted,
        'clientId': '8e8fe2f5582c326e7bb3e206f6936012'
    }
    res = func_post_json('/workbench/admin/appLogin', payload)
    if res['isSuccess']:
        print('-------------登录成功-------------')
        data = res['data']
        if 'orgList' in data:
            organ = get_organ(data['orgList'], org_name)
            token = get_user_oken(organ)
            headers['X-User-Token'] = token
        else:
            organ = data['orgInfo']
            headers['X-User-Token'] = data['tokenKey']
        get_apps(organ['orgId'])
    else:
        print(res)


def get_organ(data, name=''):
    if name == '':
        return data[0]
    else:
        for org in data:
            if org['orgName'] == name:
                return org
        return {}


def get_user_oken(data):
    payload = {
        'userName': username,
        'memberId': data['memberId'],
        'orgId': data['orgId']
    }
    res = func_post_form('/workbench/admin/multiOrganizationCallback', payload)
    if res['isSuccess']:
        return res['data']['tokenKey']


def get_apps(org_id):
    params = {'orgId': org_id, 'terminalType': 2}
    print('----------正在获取应用列表----------')
    res = func_get('/workbench/member/app/getAppGroupListNew', params)
    print(res)
    if res['isSuccess']:
        print('----------获取应用列表成功----------')
        get_app_by_name(res['data']['enterpriseAppGroup'], app_name)
        save_json(username+'-apps', json.dumps(res['data']).encode('utf-8').decode('unicode-escape'))


def get_app_by_name(app_groups, name):
    flag = False
    for app_group in app_groups:
        if name == '':
            print('-------------------------------')
        if 'appList' in app_group:
            for app in app_group['appList']:
                if name == '':
                    print(app['appName'] + ':' + app['code'])
                elif app['appName'] == name:
                    print(app['appName'] + ':' + app['code'])
                    get_app_token(app['code'])
                    flag = True
                    break
        if flag:
            break


def get_app_token(code):
    params = {'code': code}
    print('----------正在获取应用token----------')
    res = func_get('/open/oauth/getAccessToken', params)
    if res['isSuccess']:
        print('----------获取应用token成功----------')
        print(res['data']['accessToken'])


if __name__ == '__main__':
    login()
