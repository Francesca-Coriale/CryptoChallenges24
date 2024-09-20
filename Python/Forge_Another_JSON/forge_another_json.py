from pwn import *

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import json, base64

conn = remote('130.192.5.212', 6551)

def create_token(name):
    token = json.dumps({
        "username": name,
        "admin": False
    })
    return token

# {"username":           , "admin": false}
#{"username": "aa|true,           |aaaa", "admin": |false}
# 0                 1                   2               3               4               5               6                7                
#|               |                |                |                |                |                |                |                 |
#{"username": "aa|true,-----------|---------------"|old-------------|"---------------|:---------------|aaaa", "admin": |false}          |
#se metto '"' compare anche '\' quindi devo fare in modo che si dividano in due blocchi per non prenderlo
#{"username": "aa|true,-----------|---------------\|"---------------|old-------------|:---------------|aaaa", "admin": |false}          |


print(conn.recvuntil(b'> '))        #Hi, tell me your name!
admin = 'True'
admin_pad = pad(admin.encode(), AES.block_size)

double_dot = ":---------------".replace("-", " ")                   # 80:96
quotation = '---------------"---------------'.replace("-", " ")     # 32:64 così è staccato da '\'
old = "old-------------".replace("-", " ")                          # 64:80
true = "true,-----------".replace("-", " ")                         # 16:32


name = \
        "aa" + \
        true + \
        quotation + \
        old + \
        double_dot + \
        "aaaa"
conn.sendline(name)

token = create_token(name)
print(token)
print(conn.recvuntil(b': '))        #This is your token:
cookie = conn.recvuntil(b'\n').strip().decode()
cookie = base64.b64decode(cookie)
print(f"cookie: ", cookie)
print(f"length: ", len(cookie))

chuncks = [cookie[i:i+16] for i in range(0, len(cookie), AES.block_size)]
print(len(chuncks))
admin_cookie = chuncks[0]+chuncks[6]+chuncks[1]+chuncks[3]+chuncks[4]+chuncks[3]+chuncks[5]+chuncks[7]
admin_cookie = base64.b64encode(admin_cookie)

print(conn.recvuntil(b'> '))        #What do you want to do?
conn.sendline(b'flag')
print(conn.recvuntil(b'> '))        #What is your token?
conn.sendline(admin_cookie)
print(conn.recvline())              #You're admin!
print(conn.recvline())              #This is your flag:
print(conn.recvline())              #flag
       
conn.close()