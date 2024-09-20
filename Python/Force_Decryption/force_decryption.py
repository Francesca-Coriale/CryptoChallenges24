# To get your flag, forge a payload that decrypts to a fixed value...
# nc 130.192.5.212 6523 

from pwn import *

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def xor(bytes1,bytes2):
    result = bytes([a ^ b for a, b in zip(bytes1, bytes2)])
    return result

def encryption(message):
    print(conn.recvuntil(b'> '))    #What do you want to do?
    conn.sendline(b'enc')
    print(conn.recvuntil(b'> '))    #What do you want to encrypt?
    
    msg_hex = message.hex()
    conn.sendline(msg_hex.encode())

    iv_received = conn.recvline().decode().strip()
    iv = iv_received.split()[-1]
    iv = bytes.fromhex(iv)

    ciphertext = conn.recvline().decode().strip()
    ciphertext = ciphertext.split()[-1]
    ciphertext = bytes.fromhex(ciphertext)

    return iv, ciphertext

def decryption(ciphertext, myIV):
    print(conn.recvuntil(b'> '))    #What do you want to do?
    conn.sendline(b'dec')
    print(conn.recvuntil(b'> '))    #What do you wnat to decrypt?
    ciphertext_hex = ciphertext.hex()
    conn.sendline(ciphertext_hex.encode())
    print(conn.recvuntil(b'> '))    #Give the IV
    myIV_hex = myIV.hex()
    conn.sendline(myIV_hex.encode())
    
    rec_line = conn.recvline().decode().strip()
    return rec_line
    

conn = remote('130.192.5.212', 6523)

message = b'1'*16
print(message)
iv, ciphertext = encryption(message)
print(f"IV: ", iv)
print(f"ciphertext: ", ciphertext)

######################
leak = b'mynamesuperadmin'
myIV = xor(xor(message, iv), leak)

################
# Decryption
flag = decryption(ciphertext, myIV)
print(flag)

conn.close()

##CRYPTO24{b468978c-869b-4748-affc-b2fc8f883ca9}