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
    n = 84579385253850209980531118129485716360575269582423585759001305965013034395499445816183248675447710453177558996114910965695049824431833160231360553529286419317374940825879760576417322050461035628520331998356731488662783964882867470865445762024182798458285340930223702904421982112483822508094601373760076526513
    #n = 2061967200227682478892466800664375981780200323053931198705407209204250941958336129844795487423453613029326452196390948676768692154173488243846139936920256794251314998112316290908934913863837212956458092446009358741194058371369097581541094913
    p,q = fermat(n)

    print("p = "+str(p))
    print("q = " + str(q))