import hashlib, sys
import binascii
import struct
	

def token(key):
 keystr = struct.pack("!Q", key)
 
 hashd = hashlib.sha1(keystr.rjust(8,'\00')).digest()
 token , dsn = hashd[0:4] , hashd[-8:]

 d1, d2 = struct.unpack("!II",dsn)

 token, dsn = (struct.unpack("!I",token)[0], (long(d1)<<32)+d2 + 1)
 return token, dsn


def token2(key):
 keystr = struct.pack("!Q", key)
 
 hashd = hashlib.sha1(keystr.rjust(8,'\00')).digest()
 token , dsn = hashd[0:4] , hashd[-8:]

 d1, d2 = struct.unpack("!II",dsn)

 token, dsn = (struct.unpack("!I",token)[0], (long(d1)>>64)+d2 + 1)
 return dsn


