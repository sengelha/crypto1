#!/usr/bin/env python -tt
#
# Factoring composites N=pq where p and q are chosen poorly

import gmpy2
import math
import struct

def int_to_bytearray(n):
    hexstr = hex(n)[2:]
    if (len(hexstr) % 2 != 0):
        hexstr = '0' + hexstr
    return bytearray.fromhex(hexstr)

# 1. The following modulus N is a product of two primes p and q where |p-q| < 2N^{1/4}.
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

# 2. The following modulus N is a product of two primes p and q where |p-q| < 2^11 * N^{1/4}.
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

# Skip problem #3

# 4. Decrypt RSA ciphertext encoded using PKCS v1.5.
N=gmpy2.mpz(179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581)
e=65537
ct=22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

# Step 1: Calculate p,q such that p*q=N
A=gmpy2.isqrt(N)+1
x=gmpy2.isqrt(A*A-N)
p=A-x
q=A+x

# Step 2: Calculate phiN
phiN=(p-1)*(q-1)

# Step 3: Calculate e such that d*e = 1 mod \phiN
d=gmpy2.invert(e, phiN)

# Step 4: Use d to decrypt RSA ciphertext
pt=int_to_bytearray(gmpy2.powmod(ct, d, N))

# Step 5: Find the message -- its the text after the 0x00 delimiter
print("Challenge #4:")
print(pt[pt.index(0x00)+1:].decode('ascii'))
