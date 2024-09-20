from pwn import *
from Crypto.Util.number import bytes_to_long, getPrime, inverse, long_to_bytes
from math import gcd
#nc 130.192.5.212 6646
conn = remote('130.192.5.212', 6646)

e = 65537
cipher = int(conn.recvline().decode())
print("cipher: ", cipher)

##How can I found the modulus?
# RSA: c = m^e mod n
# for modular arithmetic: c-m^e = kn mod n for some integer k
# try with 2
m1 = b'e2'
conn.sendline(m1)
c1 = int(conn.recvline().decode())

# if I try with another integer (prime with 2 ex.3) I can have c' - 3^e = k'n mod n for some integer k'
m2 = b'e3'
conn.sendline(m2)
c2 = int(conn.recvline().decode())

# but now their both a multiple of n so if I do the GCD(kn,k'n) I should get n
n = gcd(2**e -c1, 3**e -c2) #vedi math.md per la spiegazione
print("n: ", n)

print("modular arithmetic 2: ", c1-pow(2,e,n)%n)
print("modular arithmetic 3: ", c2-pow(3,e,n)%n)

#as level_5
c = 2**e * cipher %n

req = f"d{c}"
conn.sendline(req.encode())

response = int(conn.recvline().decode())

#flag = response//2
# or more correct for Di Scala:
mult_inverse = pow(2, -1, n)
flag = response * mult_inverse %n
print(long_to_bytes(flag))
