
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
from mydata import HOST, PORT

# username=AAAAAAA|AAAAAAAAA&admin=|falsePPPPPP
# username=AAAAAAA|truePPPPPPPPPPPP|AAAAAAAAA&admin=|falsePPPPPP

def main():
    conn = remote(HOST, PORT)
    conn.recvuntil(b': ')
    true = pad(b'true', AES.block_size)
    name = 'A'*7 + true.decode() + 'A'*9
    conn.sendline(name)
    cookie_enc = int(conn.recvline().decode().strip())
    cookie_enc = long_to_bytes(cookie_enc)
    chunck1 = cookie_enc[:16]
    chunck2 = cookie_enc[16:32]
    chunck3 = cookie_enc[32:48]
    my_cookie = chunck1 + chunck3 + chunck2
    my_cookie = bytes_to_long(my_cookie)
    conn.recvuntil(b'> ')
    conn.sendline(b'flag')
    conn.recvuntil(b': ')
    conn.sendline(str(my_cookie).encode())
    
    print(conn.recvline().decode().strip())
    
    
    
if __name__ == "__main__":
    main()   