# Guess the mode. Now you need to reason about how modes work. 
# Ask a second encryption to confirm your hypothesis...
# nc 130.192.5.212 6532 


from pwn import *

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import random

modes_mapping = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC
}

conn = remote('130.192.5.212', 6532)

data = '00'*32
data = data.encode()
outputs = []
for i in range(128):
    conn.recvuntil(b": ") #Input:
    conn.sendline(data)
    conn.recvuntil(b": ") #Output:
    line1 = conn.recvline().decode().strip().split()[-1]
    conn.recvuntil(b": ") #Input:
    conn.sendline(data)
    conn.recvuntil(b": ") #Output:
    line2 = conn.recvline().decode().strip().split()[-1]
    # è come se mandassi 64 bytes tutti uguali
    # se ECB: primi 32 bytes == ultimi 32 bytes
    # se CBC: ultimi 32 bytes dipendono anche dai primi 32
    # non posso confrontare dentro ai 32 bytes perchè fa XOR con un otp random
    if line1 == line2:
        mode = "ECB"
    else:
        mode = "CBC"
    print(conn.recvuntil(b')\n'))
    conn.sendline(mode)
    print(conn.recvline().strip())
print(conn.recvline())
        
    