# Read and understand the code. 
# You'll easily find a way to forge the target cookie.
# nc 130.192.5.212 6521 

# QUALCOSA NON FUNZIONA MA LA FLAG E' GIUSTA :)

from pwn import *

from Crypto.Cipher import ChaCha20 #output ChaCha20 = 64 bytes = 512 bits (?)
from Crypto.Random import get_random_bytes
import json, base64

import socket

HOST = '130.192.5.212'
PORT = 6521
DELTA_PORT = 101

def find_keystream(token_enc, username):
    # result = ""
    # for char1, char2 in zip(token_enc, user):
    #     result += chr(ord(char1) ^ ord(char2))
    # return result
    return bytes([d ^ o for d,o in zip(token_enc, username)])


def def_user(name):
    user = json.dumps({
        "username": name
    })
    return user


def create_token(admin, keystream):
    #result = ""
    # for char1, char2 in zip(admin, keystream):
    #     result += chr(ord(char1) ^ ord(char2))
    # result = result.encode()
    return bytes([d ^ o for d,o in zip(admin, keystream)])

conn = remote(HOST, PORT)
#conn = process(["python3","chall.py"])

print(conn.recvuntil(b'> '))

name = "A"*10
conn.sendline(name.encode())

user = def_user(name)
print(f"def_user: ", user)


conn.recvline() #{"username": "alice"}
token = conn.recvline().decode().strip().split()[-1]   #[-1] prende l'ultimo elemento
print("Token: ", token )
nonce, token_enc = token.split('.')

token_enc = base64.b64decode(token_enc)
print(f"Token decoded: ", token_enc.hex())

username = def_user(name).encode()
keystream = find_keystream(token_enc, username)
print(f"keystream used: ", keystream.hex())

print(conn.recvuntil(b'> ')) #what to do
conn.sendline(b'flag')

admin = f'{{"username": "{name}", "admin": true}}'
print(admin)
admin = admin.encode()
token_admin = create_token(admin, keystream)
send = nonce + '.' + base64.b64encode(token_admin).decode()
print(token)
print(send)  #for checking

print(conn.recvuntil(b'> '))  #'What is your token?\n'

conn.sendline(send.encode())

print(conn.recvline())  #voce della verità
print(conn.recvline())  #flag

conn.close()

##CRYPTO24{fdf00c66-1a1a-4b80-bccb-9cb689a8070e}