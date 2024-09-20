import requests

import json

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Util.number import long_to_bytes, bytes_to_long
import time
from random import randint

BASE_URL = 'http://130.192.5.212:6522'
LOGIN_URL = f'{BASE_URL}/login'
FLAG_URL = f'{BASE_URL}/flag'


def get_cookie(username, admin, expire_date):
    return f"username={username}&expires={expire_date}&admin={admin}"

with requests.Session() as sess:
    username = 'admin'
    admin = 1
    r = sess.get(LOGIN_URL, params={
        'username': username,
        'admin': admin
    })
    expire_date = int(time.time()) + 30 * 24 * 60 * 60
    cookie = get_cookie(username, admin, expire_date)
    print(f"cookie: ", cookie)

    res = json.loads(r.text)
    print(res)
    res['cookie'] = long_to_bytes(res['cookie'])
    
    key = bytes([a^b for a,b in zip(res['cookie'], cookie.encode())])

    n1 = 290 * 24 * 60 * 60
    n2 = 300 * 24 * 60 * 60

    for i in range(10, 300):

        forged_time = int(time.time()) + i * 24 * 60 * 60
        print('forged_time: ', forged_time)
        forged_cookie = get_cookie('admin', 1, forged_time)
        encoded = bytes_to_long(bytes([a^b for a,b in zip(key, forged_cookie.encode())]))

        res['cookie'] = encoded

        r = sess.get(FLAG_URL, params=res)
        if 'OK' in r.text:
            print('flag: ', r.text)
            break
    else: 
        print('flag not found')

pass
