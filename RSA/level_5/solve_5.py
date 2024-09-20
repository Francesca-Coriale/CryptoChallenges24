from Crypto.Util.number import bytes_to_long, getPrime, inverse, long_to_bytes
from pwn import *

#nc 130.192.5.212 6645
conn = remote('130.192.5.212', 6645)

e = 65537
n = int(conn.recvline().decode())
cipher = int(conn.recvline().decode())
print("n: ", n)
print("cipher: ", cipher)

# SEE RSHack code for CHOSEN_PLAINTEXT:
c_bis = (cipher * pow(2,e,n)) %n

req = f"d{c_bis}"
conn.sendline(req.encode())

response = int(conn.recvline().decode())

#flag = response // 2
# or more correct for Di Scala:
mult_inverse = pow(2, -1, n)
flag = response * mult_inverse %n
print(long_to_bytes(flag))


