import  Crypto.Util.Counter
from Crypto.Cipher import AES
from Crypto import Random
import binascii
from itertools import chain, islice

def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i+n]

def xor(bytestr1, bytestr2):
	return bytes(bytearray([a^b for a,b in zip(bytestr1,bytestr2)]))

def padPKCS5(bytestr):
	padValue = 16 - len(bytestr) % 16
	return bytestr + bytearray([padValue]*padValue)

def unpadPKCS5(bytestr):
	lastByte = bytestr[-1]
	return bytestr[0:len(bytestr)-lastByte]

def decryptAESBlock(key, ct):
	"""Decrypts a 16 or 32-byte AES block"""
	if len(ct) != 16 and len(ct) != 32:
		raise Exception("Ciphertext is not length 16 or 32")
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(ct)

def encryptAESBlock(key, pt):
	"""Decrypts a 16 or 32-byte AES block"""
	if len(pt) != 16 and len(pt) != 32:
		raise Exception("Plaintext is not length 16 or 32")
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(pt)

def decryptAESCBCPKCS5(key, iv, ct):
	"""Decrypts AES-CBC with our own implementation of CBC mode"""
	pt = b''
	xorSource = iv
	for ctBlock in chunks(ct, 16):
		dt = decryptAESBlock(key, ctBlock)
		pt += xor(dt, xorSource)
		xorSource = ctBlock
	return unpadPKCS5(pt)

def encryptAESCBCPKCS5(key, iv, pt):
	"""Encrypts AES-CBC with our own implementation of CBC mode and PKCS5 padding"""
	pt = padPKCS5(pt)
	ct = b''
	xorSource = iv
	for ptBlock in chunks(pt, 16):
		b = xor(ptBlock, xorSource)
		ctBlock = encryptAESBlock(key, b)
		ct += ctBlock
		xorSource = ctBlock
	return ct

def decryptAESCTR(key, nonce, ct):
	"""Decrypts AES-CTR with our own implementation of CTR mode"""
	pt = b''
	counter = 0
	for ctBlock in chunks(ct, 16):
		block = (int.from_bytes(nonce, byteorder='big') + counter).to_bytes(16, byteorder='big')
		encBlock = encryptAESBlock(key, block)
		pt += xor(ctBlock, encBlock)		
		counter += 1
	return pt

def encryptAESCTR(key, nonce, pt):
	"""Encrypts AES-CTR with our own implementation of CTR mode"""
	ct = b''
	counter = 0
	for ptBlock in chunks(pt, 16):
		block = (int.from_bytes(nonce, byteorder='big') + counter).to_bytes(16, byteorder='big')
		encBlock = encryptAESBlock(key, block)
		ct += xor(ptBlock, encBlock)		
		counter += 1
	return ct

def main():
	keystr = '140b41b22a29beb4061bda66b6747e14'
	ctstr = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
	key = binascii.a2b_hex(keystr)
	iv = binascii.a2b_hex(ctstr)[0:16]
	ct = binascii.a2b_hex(ctstr)[16:]
	pt = decryptAESCBCPKCS5(key,iv,ct)
	print(pt)
	ct2 = encryptAESCBCPKCS5(key,iv,pt)
	if ct==ct2:
		print('REENCRYPT MATCH')
	else:
		print('REENCRYPT FAIL.  Expected = %s, actual=%s' % (ct, ct2))

	keystr = '140b41b22a29beb4061bda66b6747e14'
	ctstr = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
	key = binascii.a2b_hex(keystr)
	iv = binascii.a2b_hex(ctstr)[0:16]
	ct = binascii.a2b_hex(ctstr)[16:]
	pt = decryptAESCBCPKCS5(key,iv,ct)
	print(pt)
	ct2 = encryptAESCBCPKCS5(key,iv,pt)
	if ct==ct2:
		print('REENCRYPT MATCH')
	else:
		print('REENCRYPT FAIL.  Expected = %s, actual=%s' % (ct, ct2))

	keystr = '36f18357be4dbd77f050515c73fcf9f2'
	ctstr = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
	key = binascii.a2b_hex(keystr)
	nonce = binascii.a2b_hex(ctstr)[0:16]
	ct = binascii.a2b_hex(ctstr)[16:]
	pt = decryptAESCTR(key,nonce,ct)
	print(pt)
	ct2 = encryptAESCTR(key,nonce,pt)
	if ct==ct2:
		print('REENCRYPT MATCH')
	else:
		print('REENCRYPT FAIL.  Expected = %s, actual=%s' % (ct, ct2))

	keystr = '36f18357be4dbd77f050515c73fcf9f2'
	ctstr = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'
	key = binascii.a2b_hex(keystr)
	nonce = binascii.a2b_hex(ctstr)[0:16]
	ct = binascii.a2b_hex(ctstr)[16:]
	pt = decryptAESCTR(key,nonce,ct)
	print(pt)
	ct2 = encryptAESCTR(key,nonce,pt)
	if ct==ct2:
		print('REENCRYPT MATCH')
	else:
		print('REENCRYPT FAIL.  Expected = %s, actual=%s' % (ct, ct2))

if __name__ == '__main__':
	main()