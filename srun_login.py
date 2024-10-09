import requests
import time
import re
from urllib.parse import quote
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *

# 清除环境变量中的代理设置
import os
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}
init_url = "https://login.hdu.edu.cn"
get_challenge_api = "https://login.hdu.edu.cn/cgi-bin/get_challenge"
srun_portal_api = "https://login.hdu.edu.cn/cgi-bin/srun_portal"
n = '200'
type = '1'
ac_id = '0'
enc = "srun_bx1"

# 创建一个requests Session对象
session = requests.Session()

# 关闭代理
session.proxies = {
    'http': None,
    'https': None,
}

def get_chksum():
    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type
    chkstr += token + i
    return chkstr

def get_info():
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i

def init_getip():
    global ip
    init_res = session.get(init_url, headers=header)
    print("初始化获取ip")
    ip = re.search('ip     : "(.*?)"', init_res.text).group(1)
    print("ip:", ip)

def get_token():
    global token
    get_challenge_params = {
        "callback": "jQuery112406608265734960486_" + str(int(time.time() * 1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time() * 1000),
    }
    get_challenge_res = session.get(get_challenge_api, params=get_challenge_params, headers=header)
    token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)
    print(get_challenge_res.text)
    print("token为:" + token)

def do_complex_work():
    global i, hmd5, chksum
    i = get_info()
    i = "{SRBX1}" + get_base64(get_xencode(i, token))
    hmd5 = get_md5(password, token)
    chksum = get_sha1(get_chksum())
    print("所有加密工作已完成")

def login():
    srun_portal_params = {
        'callback': 'jQuery11240011249739290749128_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id,
        'ip': ip,
        'chksum': chksum,
        'info': i,
        'n': n,
        'type': type,
        'os': 'windows+10',
        'name': 'windows',
        'double_stack': 0,
        '_': int(time.time() * 1000)
    }
    print(srun_portal_params)
    srun_portal_res = session.get(srun_portal_api, params=srun_portal_params, headers=header)

    if 'ok' in srun_portal_res.text:
        print('登录成功')
    else:
        error_msg = eval(re.search('\((.*?)\)', srun_portal_res.text).group(1))
        print('error_type:' + error_msg['error'])
        print(error_msg['error_msg'])

if __name__ == '__main__':
    global username, password
    username = "XXXXX"  # 你的用户名和密码
    password = "XXXXX"
    while True:
        init_getip()
        get_token()
        do_complex_work()
        login()
        time.sleep(30)
