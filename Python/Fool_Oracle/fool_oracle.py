# you have the code, guess the flag
# nc 130.192.5.212 6541 


## len(flag) = 46 == 3 blocks (2,8 più padding)

from pwn import *

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import string

conn = remote('130.192.5.212', 6541)
#conn = process(["python3","chall.py"])

def encrypt(data: str):
    conn.recvuntil(b'> ')
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data.encode())
    enc_data = conn.recvline().strip().decode()

    return enc_data


flag = 'CRYPTO24{'.encode().hex()
blank_char = '0'

block_size = AES.block_size
block_sizeHex = block_size*2    #each byte represented by 2 hexadecimal
N = 3                           #number of DATA blocks
# data | data | data | CRYPTO24{XXXXXXX | XXXXXXXXXXXXXXXX | XXXXXXXXXXXXX}PP |
# 0...0 | 0...0 | 000000CRYPTO24{? | 0...0 | 0...0 | 000000CRYPTO24{X | ....

known = flag
for i in range(len(known)//2, block_sizeHex//2 * N):
    for guess in string.printable:
        guess = guess.encode().hex()
        if len(guess) != 2:
            exit("guess len must be 2")
        payload = blank_char * (block_sizeHex * N - i*2 - 2) + known + guess
        padding = blank_char * (block_sizeHex * N - i*2 - 2)
        # 0...0 | 0...0 | 000000CRYPTO24{? | 0...0 | 0...0 | 000000CRYPTO24{X |... 
        encrypted = encrypt(payload + padding)
        if encrypted[:block_sizeHex * N] == encrypted[block_sizeHex * N:block_sizeHex * N + 3 * block_sizeHex]:
            known+= guess
            print(bytes.fromhex(known).decode())
            if(len(known) == 46*2):
                exit('end of flag')
            break
    else:
        exit('something went wrong')

conn.close()