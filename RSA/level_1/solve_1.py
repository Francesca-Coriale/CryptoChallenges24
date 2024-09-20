from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from Crypto.Util.number import inverse
import math

def decrypt(cipher, d , n ):
    return pow(cipher, d, n)

e = 65537

#to get p,q use: factordb 180210299477107234107018310851575181787 (where this number is the modulus n = p*q)
n = 180210299477107234107018310851575181787
p = 12499036198482036913
q = 14417935640429069899
gcd = math.gcd(p,q)
print("gcd: ", gcd) # p and q are coprime
phi = (q-1)*(p-1)

d = inverse(e,phi)

c = 27280721977455203409121284566485400046
#decrypted = decrypt(c, key)
decrypted = decrypt(c, d, n)
print(long_to_bytes(decrypted))