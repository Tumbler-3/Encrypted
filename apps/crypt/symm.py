from cryptography.fernet import Fernet
from apps.crypt.mail import symm_enc_send, symm_dec_send


def symmetric_encryption(filename, receiver):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    with open(filename, 'rb') as f:
        inside = f.read()
        
    encrypted_file = cipher.encrypt(inside)
    
    with open(filename+'_key.pem', 'wb') as f:
        f.write(key)
        
    with open(filename+'_encrypted', 'wb') as f:
        f.write(encrypted_file)
    symm_enc_send(receiver=receiver, file=f'{filename}_encrypted', keyfile=f'{filename}_key.pem')



def symmetric_decryption(filename, file_type, keyfile, receiver):
    with open(keyfile, 'rb') as f:
        key = f.read()
    cipher = Fernet(key)
    
    with open(filename, 'rb') as f:
        inside = f.read()
        
    decrypted_file = cipher.decrypt(inside)
    
    with open(filename+f'_decrypted.{file_type}', 'wb') as f:
        f.write(decrypted_file)
    symm_dec_send(receiver=receiver, file=f'{filename}_decrypted.{file_type}')
