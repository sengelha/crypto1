#!/usr/bin/python -tt
#
# Crypto1 MP5
#
# Use a meet in the middle attack to find x given p,g,h in Zp* such that
# h=g^x where 1 <= x <= 2^40.
#
# Basic equation:
# h/g^{x1} = (g^B)^{x0} in Zp

import gmpy2
import math

p = gmpy2.mpz(13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171)
g = gmpy2.mpz(11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568)
h = gmpy2.mpz(3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333)
B = gmpy2.mpz(2**20)

# 1. Build a hash table of all possible values of h/g^{x1} mod p for x1 = 0,1,...,2^20
print("Building hash table...")
values={}
for x1 in range(0, B):
	if (x1 % 1000 == 0): print('%d: %.1f%%' % (x1, 100*x1/B))
	try:
		v = gmpy2.divm(h, gmpy2.powmod(g, x1, p), p)
		values[v] = x1
	except ZeroDivisionError:
		pass

# 2. For each value x0 = 0,1,...,2^20 check if (g^B)^{x0} mod p is in the hash table.
#    If found, x = x0*B + x1.
print("Checking if value is in hash table...")
x = None
for x0 in range(0, B):
	if (x0 % 1000 == 0): print('%d: %.1f%%' % (x0, 100*x0/B))
	v = gmpy2.powmod(gmpy2.powmod(g, B, p), x0, p)
	if v in values:
		x1 = values[v]
		x = (x0*B + x1) % p
		break

# Verify the solution
h2 = gmpy2.powmod(g, x, p)
if (h != h2):
	raise Exception("INTERNAL ERROR")
print("x = %d" % (x))
