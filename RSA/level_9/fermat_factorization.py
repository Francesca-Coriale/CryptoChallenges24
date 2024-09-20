from gmpy2 import isqrt
from Crypto.Util.number import getPrime, getRandomInteger
from gmpy2 import next_prime


def fermat(n):
    print("init")

    a = isqrt(n)
    b = a
    b2 = pow(a,2) - n

    print("a= "+str(a))
    print("b= " + str(b))

    print("b2=" + str(b2))
    print("delta-->" + str(pow(b, 2) - b2 % n)+"\n-----------")
    print("iterate")
    i = 0

    while True:
        if b2 == pow(b,2):
            print("found at iteration "+str(i))
            break;
        else:
            a +=1
            b2 = pow(a, 2) - n
            b = isqrt(b2)
        i+=1
        print("iteration="+str(i))
        print("a= " + str(a))
        print("b= " + str(b))
    print("b2 =" + str(b2))
    print("delta-->" + str(pow(b, 2) - b2 % n) + "\n-----------")

    p = a+b
    q = a-b

    return p,q

if __name__ == '__main__':

    # n = 400
    # p1 = getPrime(n)
    # delta = getRandomInteger(n//2+11)
    # # delta = getRandomInteger(100)
    # p2 = next_prime(p1+delta)
    # print(p1)
    # print(p2)
    # print(p2-p1)

    # n = p1*p2
    n = 138728501052719695830997827983870257879591108626209095010716818754108501959050430927220695106906763908822395818876460759364322997020222845247478635848425558793671347756842735011885094468024344931360037542098264527076663690119553302046205282212602106990248442514444587909723612295871002063257141634196430659767
    p,q = fermat(n)

    print("p = "+str(p))
    print("q = " + str(q))