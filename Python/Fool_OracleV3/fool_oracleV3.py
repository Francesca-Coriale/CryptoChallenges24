#nc 130.192.5.212 6543

from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import string

def encrypt(data: str):
    conn.recvuntil(b'> ')           #What do you want to do? ....
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data.encode())
    enc_data = conn.recvline().strip().decode()

    return enc_data

def find_size_prefix(empty_enc):
    prefix_size = 0
    max_prefix = 15
    min_prefix = 1
    block_size = AES.block_size
    
    empty_size = len(bytes.fromhex(empty_enc))
    print(f"empty size: ", empty_size)
    full = ''
    full_size = empty_size
    for i in range(min_prefix, max_prefix+1):
        full += 'a'*2       #in hexadecimal
        full_enc = encrypt(full)
        full_size = len(bytes.fromhex(full_enc))
        print(i, full_size)
        if full_size != empty_size:
            break
    prefix_size = block_size - (i-2)    #last round I added 2 bytes more (need to be removed)
    return prefix_size 
    

conn = remote('130.192.5.212', 6543)

#This time I do not know the length of the padding -> I need to discover it
# padding_blocks = 1
# postfix_blocks = 46//16 = 3
# data_blocks = = postfix_blocks = 3

flag = 'CRYPTO24{'.encode().hex()

block_size = AES.block_size
block_size_hex = block_size * 2

flag_size = 46
flag_blocks = 3

#first I send an empty line to get how many bytes is the prefix 
empty = ''
empty_enc = encrypt(empty)
print(f"empty encrypted: ", empty_enc)
#Now I add one byte each time to substitute the padding in the first block: when the total length of the encrypted is > original one then I've got the size of the prefix 
prefix_size = find_size_prefix(empty_enc)
    
print(f"prefix size: ", prefix_size)

prefix_blocks = 1

prefix_len_to_generate = prefix_blocks*block_size - prefix_size
print(f"prefix to generate: ", prefix_len_to_generate)
prefix_len_to_generate_hex = prefix_len_to_generate*2

tot_bloks = prefix_blocks + flag_blocks * 2
print(f"total blocks: ", tot_bloks)

known = flag
blank_char = 'a'
for i in range(len(flag)//2, block_size_hex//2 * flag_blocks):
    for guess in string.printable:
        guess = guess.encode().hex()
        if len(guess) != 2: 
            exit("guess len must be 2")

        prefix = blank_char * prefix_len_to_generate_hex                            # toglie il padding dalla finestra
        payload = blank_char * (block_size_hex * flag_blocks - i*2 - 2) + known + guess
        postfix = blank_char * (block_size_hex * flag_blocks - i*2 - 2)
        
        encrypted = encrypt(prefix+payload+postfix)
        encrypted = encrypted[prefix_blocks * block_size_hex:]

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

#CRYPTO24{5408a811-867e-49bc-86b3-b28090ba89d0}