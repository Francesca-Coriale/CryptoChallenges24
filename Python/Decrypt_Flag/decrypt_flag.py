#As I don't have enough fantasy, I'm just reusing the same text as other challenges... 
# ...read the challenge code and find the flag!
# nc 130.192.5.212 6561


# Hint: Chacha20 calcola il keystream con key e nonce a modo suo, poi fa solo lo XOR tra keystream e plaintext
# Se so il plaintext e il ciphertext mi posso ricavare il keystream e decriptare tutto il resto

from pwn import *

import random
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Util.number import long_to_bytes

HOST = '130.192.5.212' 
PORT = 6561

def do_xor(bytes1, bytes2):
    result = bytes([a ^ b for a, b in zip(bytes1, bytes2)])
    # Convert the result back to a hexadecimal string
    return result


conn = remote(HOST, PORT)
#conn = process(["python3","chall.py"])

print(conn.recvuntil(b'> '))
seed = b'0'
conn.sendline(seed)

print(conn.recvline())
flag_enc_str = conn.recvline().decode().strip()
flag_enc_bytes = bytes.fromhex(flag_enc_str)
print(f"Flag encrypted: ", flag_enc_str)

print(conn.recvuntil(b'(y/n)'))
conn.sendline(b'y')
print(conn.recvuntil(b'? '))
msg_bytes = b'0'*46
print(f"msg: ", msg_bytes)
conn.sendline(msg_bytes)

msg_enc_str = conn.recvline().decode().strip()
msg_enc_bytes = bytes.fromhex(msg_enc_str)
print(f"Message encrypted: ", msg_enc_str)

keystream = do_xor(msg_bytes, msg_enc_bytes)
keystream_str = keystream.hex()
print(f"Keystream: ", keystream)

flag = do_xor(keystream, flag_enc_bytes)
print(f"Flag: ", flag)

conn.close()

##CRYPTO24{f4cc8ad5-98fb-4239-8c8d-306e437f85ef}