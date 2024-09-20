from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
import decimal

e = 65537


def print_bounds(low, up):
    print("[" + str(low) + "," + str(up) + "]")


conn = remote('130.192.5.212', 6647)
n = int(conn.recvline().decode())
c = int(conn.recvline().decode())

decimal.getcontext().prec = n.bit_length()
lower_bound = decimal.Decimal(0)
upper_bound = decimal.Decimal(n)

length = n.bit_length()
for i in range(length):
    print(f"Status: {(i+1)/length*100:.2f}%", end="\r")
    c = (pow(2, e, n) * c) % n

    conn.sendline(str(c).encode())
    bit = int(conn.recvline().decode().strip())
    # print(f"Received bit: {bit}", bit==0)
    if  bit == 1:
        lower_bound = (upper_bound + lower_bound) / 2
    else:
        upper_bound = (upper_bound + lower_bound) / 2

print(length)
print(int(upper_bound))
print(long_to_bytes(int(upper_bound),length))


