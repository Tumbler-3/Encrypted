import rsa
import base64



def asymmetric_encryption(filename):
    public_key, private_key = rsa.newkeys(2048)

    with open(f'{filename} public key.pem', 'wb') as pub:
        pub.write(public_key.save_pkcs1("PEM"))
        
    with open(f'{filename} private key.pem', 'wb') as priv:
        priv.write(private_key.save_pkcs1("PEM"))
  
    
    with open(filename, 'rb') as file:
        inside = file.read()

    encrypted_file = rsa.encrypt(inside, public_key)
    
    with open(filename+'_encrypted', 'wb') as f:
        f.write(encrypted_file)



def asymmetric_decryption(filename:str, file_type, privkey_file):
    with open(filename, 'rb') as f:
        inside = f.read()
        
    with open(privkey_file, 'rb') as priv:
        privkey = rsa.PrivateKey.load_pkcs1(priv.read())
        
    decrypted_file = rsa.decrypt(inside, privkey)
    
    with open(filename.replace('encrypted', 'decrypted')+f'.{file_type}', 'wb') as f:
        f.write(decrypted_file)

