import rsa
from apps.crypt.mail import asym_dec_send, asym_enc_send


def asymmetric_encryption(filename, receiver, pubkey_file):

    if pubkey_file == None:
        key, priv_key = rsa.newkeys(2048)

        keyfile = open(f'media/{filename} public key.pem', 'wb')
        keyfile.write(key.save_pkcs1("PEM"))

        with open(f'media/{filename} private key.pem', 'wb') as priv:
            priv.write(priv_key.save_pkcs1("PEM"))

    else:
        keyfile = open(f'media/{pubkey_file}', 'rb')
        key = rsa.PublicKey.load_pkcs1(keyfile.read())

    with open(f'media/{filename}', 'rb') as file:
        inside = file.read()
        
            
    try:
        encrypted_file = rsa.encrypt(inside, key)
    except:
        return 1


    with open(f'media/{filename}_encrypted', 'wb') as f:
        f.write(encrypted_file)

    if pubkey_file == None:
        asym_enc_send(receiver=receiver, file=f'media/{filename}_encrypted',pubkey=f'{keyfile.name}', privkey=f'media/{filename} private key.pem')

    else:
        asym_enc_send(
            receiver=receiver, file=f'media/{filename}_encrypted', pubkey=None, privkey=None)


def asymmetric_decryption(filename, file_type, privkey_file, receiver):
    with open(f'{filename}', 'rb') as f:
        inside = f.read()

    with open(privkey_file, 'rb') as priv:
        privkey = rsa.PrivateKey.load_pkcs1(priv.read())

    decrypted_file = rsa.decrypt(inside, privkey)

    with open(f'{filename.replace("encrypted", "decrypted")}.{file_type}', 'wb') as f:
        f.write(decrypted_file)

    asym_dec_send(receiver=receiver,
                  file=f'{filename.replace("encrypted", "decrypted")}.{file_type}',)
