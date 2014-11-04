#!/usr/bin/python -tt
#
# Factoring composites N=pq where p and q are chosen poorly

import gmpy2
import math

# The following modulus N is a product of two primes p and q where |p-q| < 2N^{1/4}.
# Find the smaller of the two factors and enter it as a decimal integer. 
#
# A=(p+q)/2
# We know that A - \sqrt(N) < 1, so if we round up sqrt(N) to the closest integer we get A
N=gmpy2.mpz(179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581)
A=gmpy2.isqrt(N)+1
x=gmpy2.isqrt(A*A-N)
p=A-x
q=A+x
if (p*q != N):
    raise Exception("Internal error: factoring failed")
print("Factoring challenge #1:")
#print("N=%d" % (N))
#print("A=%d" % (A))
#print("A*A=%d" % (A*A))
#print("A*A-N=%d" % (A*A-N))
#print("x=%d" % (x))
print("%d" % (p))
#print("q=%d" % (q))
#print("p*q=%d" % (p*q))

# The following modulus N is a product of two primes p and q where |p-q| < 2^11 * N^{1/4}.
# Find the smaller of the two factors and enter it as a decimal integer. 
#
# In this case A - \sqrt(N) < 2^20 so we can scan A from \sqrt(N) upwards
N=gmpy2.mpz(648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877)
sqrtN=gmpy2.isqrt(N)+1
for A in range(sqrtN, sqrtN+100000,1):
    x=gmpy2.isqrt(A*A-N)
    p=A-x
    q=A+x
    if (p*q == N):
        print("Factoring challenge #2:")
        print("%d" % (p))
        break

# The following modulus N is a products of two primes p and q where |3p-2q|<N^{1/4}.
# Find the smaller of the two factors and enter it as a decimal integer. 
#
# \sqrt(6N) is close to (3p+2q)/2

N=gmpy2.mpz(720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929)
sqrt6N=gmpy2.isqrt(6*N)