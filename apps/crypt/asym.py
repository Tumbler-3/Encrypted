import rsa
from apps.crypt.mail import asym_dec_send, asym_enc_send


def asymmetric_encryption(filename, receiver):
    public_key, private_key = rsa.newkeys(2048)
    
    with open(f'media/{filename}', 'rb') as file:
            inside = file.read()
    
    try:
        encrypted_file = rsa.encrypt(inside, public_key)
    except:
        return 1
    
    with open(f'media/{filename} public key.pem', 'wb') as pub:
        pub.write(public_key.save_pkcs1("PEM"))
        
    with open(f'media/{filename} private key.pem', 'wb') as priv:
        priv.write(private_key.save_pkcs1("PEM"))
  
    
    with open(f'media/{filename}_encrypted', 'wb') as f:
        f.write(encrypted_file)
    asym_enc_send(receiver=receiver, file=f'media/{filename}_encrypted', pubkey=f'media/{filename} public key.pem', privkey=f'media/{filename} private key.pem')


def asymmetric_decryption(filename, file_type, privkey_file, receiver):
    with open(f'{filename}', 'rb') as f:
        inside = f.read()
        
    with open(privkey_file, 'rb') as priv:
        privkey = rsa.PrivateKey.load_pkcs1(priv.read())
        
    decrypted_file = rsa.decrypt(inside, privkey)
    
    with open(f'{filename.replace("encrypted", "decrypted")}.{file_type}', 'wb') as f:
        f.write(decrypted_file)
    asym_dec_send(receiver=receiver, file=f'{filename.replace("encrypted", "decrypted")}.{file_type}',)

# asymmetric_encryption('Адабият.pdf', 'topkek164@gmail.com')