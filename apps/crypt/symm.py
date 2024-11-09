from cryptography.fernet import Fernet



def symmetric_encryption(filename):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    with open(filename, 'rb') as f:
        inside = f.read()
        
    encrypted_file = cipher.encrypt(inside)
    
    with open(filename+'_encrypted', 'wb') as f:
        f.write(encrypted_file)



def symmetric_decryption(filename, file_type, key):
    cipher = Fernet(key)
    
    with open(filename, 'rb') as f:
        inside = f.read()
        
    decrypted_file = cipher.decrypt(inside)
    
    with open(filename+f'_decrypted.{file_type}', 'wb') as f:
        f.write(decrypted_file)
