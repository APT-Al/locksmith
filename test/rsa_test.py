import os
import sys
import base64

sys.path.append(os.path.abspath('../../hasp'))
from RSACipher import RSACipher


pub = open("../victimNumber_rsa_public_key.pub","rb").read()
pri = open("../victimNumber_rsa_private_key","rb").read()

enc_cipher = RSACipher(pub)
dec_cipher = RSACipher(pri)

message = b"okan"
enc_mes = enc_cipher.encrypt(message)
print("ENC::",enc_mes)
print("base64(ENC)::",base64.b64encode(enc_mes))
dec_mes = dec_cipher.decrypt(enc_mes)
print(dec_mes)



