#!/usr/bin/env python3 -tt

import binascii
import urllib
from urllib.request import urlopen
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        url = TARGET + q    # Create query URL
        try:
            f = urlopen(url)          # Wait for response
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return True # good padding
            return False # bad padding

def main():
    ctstr = b'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
    ct = bytearray(binascii.unhexlify(ctstr))
    numblocks=int(len(ct)/16)-1
    msg = bytearray(16*numblocks)

    po = PaddingOracle()
    for blockidx in range(0, numblocks):
        for guess_num in range(0, 16):
            for g in range(0, 256):
                print("blockidx=%d guess_num=%d g=%d" % (blockidx, guess_num, g))
                guess_index = 15-guess_num
                pad_byte = guess_num+1

                ctprime = ct[0:16*(blockidx+2)]
                ctprime[16*blockidx+guess_index] = ctprime[16*blockidx+guess_index] ^ g ^ pad_byte
                for i in range(guess_index+1, 16):
                    ctprime[16*blockidx+i] = ctprime[16*blockidx+i] ^ msg[16*blockidx+i] ^ pad_byte

                if po.query(binascii.hexlify(ctprime).decode('ascii')):
                    print('msg[%d] = "%s" (%d)' % (16*blockidx+guess_index, chr(g), g))
                    msg[16*blockidx+guess_index] = g
                    break

    print(msg)

if __name__ == "__main__":
    main()
