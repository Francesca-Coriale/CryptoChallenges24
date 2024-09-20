# How I've got the solution
RSA Encryption Basics:  
    - Public Key: Composed of the modulus n and the exponent e.  
    - Private Key: Derived from the modulus n and the private exponent d.

Modulus n: n is the product of two large prime numbers p and q.  
Given n = 180210299477107234107018310851575181787, p and q are obtained by using the command `factordb 180210299477107234107018310851575181787`  
$\rightarrow$ we obtain p = 12499036198482036913 and q = 14417935640429069899.  
Since p and q are coprime the Euler's Totient Function ϕ(n)ϕ(n):
        for n=p×q, ϕ(n)=(p−1)×(q−1).

Public Exponent e:chosen to be 65537.

Private Exponent d:
        d is the modular multiplicative inverse of e modulo ϕ(n)ϕ.

Decrypt the Ciphertext:
    Use the decrypt function, which performs modular exponentiation with the ciphertext, private exponent d, and modulus n