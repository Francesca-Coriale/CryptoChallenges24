# Needless to say, you the proper authorization cookie to get the flag
# nc 130.192.5.212 6552 

# key = 32 bytes
from pwn import *

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Util.number import long_to_bytes, bytes_to_long


def sanitize_field(field: str):
    return field \
        .replace("/", "_") \
        .replace("&", "") \
        .replace(":", "") \
        .replace(";", "") \
        .replace("<", "") \
        .replace(">", "") \
        .replace('"', "") \
        .replace("'", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("{", "") \
        .replace("}", "") \
        .replace("=", "")
        
def create_user(username, admin):
    return f"username={sanitize_field(username)}&admin={admin}"
    
conn = remote('130.192.5.212', 6552)

# if admin == false: length 21 + username 
# username=xxxxxxx | xxxx&admin=false | 
# username=xxxxxxx | xxxx&admin=trueP | &admin=falsePPPP |   NON VA BENE
# username=xxxxxxx | truePPPPPPPPPPPP | xxxxxxxxx&admin= | falsePPPPPPPPPPP
admin = 'true'
admin = pad(admin.encode(), AES.block_size)

print(conn.recvuntil(b': ').decode())       #Username:
#'username=' == 9 bytes     '&admin=' == 7 bytes
username = 'a'*7 + admin.decode() + 'a'*9
print(username)
conn.sendline(username.encode())

cookie = int(conn.recvline().decode().strip())
cookie = long_to_bytes(cookie)
print("Cookie")
print(cookie.hex())

chuncks = [cookie[i:i+16] for i in range(0, len(cookie), AES.block_size)]
print(f"number of chunks:", len(chuncks))

conn.recvuntil(b'> ')   #What do you want to do?
conn.sendline(b'flag')

conn.recvuntil(b': ')   #Cookie:
admin_cookie = chuncks[0]+chuncks[2]+chuncks[1]
admin_cookie = bytes_to_long(admin_cookie)
conn.sendline(str(admin_cookie).encode())

print(conn.recvline().decode())

conn.close()


