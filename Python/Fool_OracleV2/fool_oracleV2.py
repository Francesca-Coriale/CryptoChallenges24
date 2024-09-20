# fool this new one...
# nc 130.192.5.212 6542 

from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import string

conn = remote('130.192.5.212', 6542)

def encrypt(data: str):
    conn.recvuntil(b'> ')           #What do you want to do? ....
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data.encode())
    enc_data = conn.recvline().strip().decode()

    return enc_data

#len(flag) = 'CRYPTO24{}' + 36 = 46 bytes
#padding = 5 bytes
#encrypted = 
# PPPPPaaaaaaaaaaa|aaaaaaaaaaaaaaaa|CRYPTO24{............}
# padding_blocks = 1
# postfix_blocks = 46//16 = 3
# data_blocks = = postfix_blocks = 3


flag = 'CRYPTO24{'.encode().hex()

block_size = AES.block_size
block_size_hex = block_size * 2

padding_size = 5
padding_blocks = 1

padding_len_to_generate = 11
padding_len_to_generate_hex = padding_len_to_generate*2

flag_size = 46
flag_blocks = 3

tot_bloks = padding_blocks + flag_blocks * 2

known = flag 
blank_char = '0'
for i in range(len(flag)//2, block_size_hex//2 * flag_blocks):
    for guess in string.printable:
        guess = guess.encode().hex()
        if len(guess) != 2: 
            exit("guess len must be 2")

        prefix = blank_char * padding_len_to_generate_hex                            # toglie il padding dalla finestra
        payload = blank_char * (block_size_hex * flag_blocks - i*2 - 2) + known + guess
        postfix = blank_char * (block_size_hex * flag_blocks - i*2 - 2)
        
        encrypted = encrypt(prefix+payload+postfix)
        encrypted = encrypted[padding_blocks * block_size_hex:]

        if encrypted[:block_size_hex * flag_blocks] == encrypted[block_size_hex * flag_blocks:block_size_hex * 2 * flag_blocks]:
            known+= guess
            printable_flag = bytes.fromhex(known).decode('utf-8')
            print(printable_flag)
            if(len(printable_flag) == flag_size):
                exit('end of flag')
            break
    else:
        exit('Something went wrong')

conn.close()

#CRYPTO24{74feb336-e18f-4cf5-a9ec-10ed1b45c557}