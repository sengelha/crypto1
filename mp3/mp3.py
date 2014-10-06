#!/usr/bin/python -tt
#
# This program implements a hashing function
# h0 -> block0 || h1 -> block1 || h2 -> block 2 ...
#
# Where h0 is the SHA256 hash of block0 || h1, h1 is the SHA256 hash of
# block1 || h2, etc.
#
# Block size is 1024 bytes (1KB)

from Crypto.Hash import SHA256
import binascii

def sha256(block):
	h = SHA256.new()
	h.update(block)
	return h.digest()

def hashFile(filename):
	"""Calculates and returns h0 for the file"""
	blocks = []
	with open(filename, 'rb') as f:
		block = f.read(1024)
		while block:
			blocks.append(block)
			block = f.read(1024)
	
	prevHash = b''
	for block in reversed(blocks):
		hash = sha256(block + prevHash)
		prevHash = hash
	return prevHash

h0 = hashFile('file2.mp4')
print(binascii.hexlify(h0))
