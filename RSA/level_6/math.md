The equation $( n = \gcd(2^e - c1, 3^e - c2) )$ where $( c1 = \text{pow}(m1, e, n) )$ and $( c2 = \text{pow}(m2, e, n) )$ leverages the mathematical property of modular arithmetic and the fact that the gcd (greatest common divisor) operation can be used to deduce properties about common factors.

Here’s a detailed breakdown of the property and the logic behind it:

### Modular Arithmetic and RSA Encryption

In RSA encryption, ciphertexts $( c1 )$ and $( c2 )$ are calculated using the public key $( (e, n) )$ as:  
$[
c1 = m1^e \mod n
]$  
$[
c2 = m2^e \mod n
]$

### Chosen Messages \( m1 \) and \( m2 \)

The key idea is to choose $( m1 )$ and $( m2 )$ in such a way that the results $( c1 )$ and $(c2)$ expose some information about $(n)$ when manipulated. In this context, $( m1)$ and $(m2)$ are chosen as small coprime integers (like 2 and 3).

### Polynomial Expressions

Given that c1 and c2 are results of RSA encryption:  
$[
c1 = 2^e \mod n
]$  
$[
c2 = 3^e \mod n
]$

We know from number theory that $( 2^e )$ and $( 3^e)$ are polynomial expressions in $e$. When these values are reduced modulo $n$ they produce residues $c1$ and $c2$ respectively.

### Greatest Common Divisor (GCD) Property

The equation $n = \gcd(2^e - c1, 3^e - c2)$ makes use of the fact that:  
$[
2^e \equiv c1 \mod n
]$  
$[
3^e \equiv c2 \mod n
]$

This implies:  
$[
2^e - c1 = k_1 n \quad \text{for some integer } k_1
]$  
$[
3^e - c2 = k_2 n \quad \text{for some integer } k_2
]$

Therefore, both $2^e - c1$ and $3^e - c2$ are multiples of $n$ This implies that $n$ is a common divisor of $2^e - c1$ and $3^e - c2$:  
$[
n \mid (2^e - c1)
]$  
$[
n \mid (3^e - c2)
]$

### Conclusion

The mathematical property used here is that the greatest common divisor of two numbers that are both multiples of $n$ will include $n$ itself. By calculating $\gcd(2^e - c1, 3^e - c2)$, we can potentially recover $n$ or a factor of $n$ Given the way $c1$ and $c2$ are defined, the gcd operation will reveal $n$ directly, assuming $m1$ and $m2$ are coprime with $n$.

This technique is a clever use of properties of gcd and modular arithmetic to extract the modulus $n$ from given RSA-encrypted values $c1$ and $c2$.