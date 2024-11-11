from django.core.mail import EmailMessage, send_mail


def symm_enc_send(receiver, file, keyfile):
    subject = f'Encrypted file and key for {receiver}'
    message = 'Do not delete your key. It is needed for decrypting'
    email = EmailMessage(subject, message, to=(receiver,))
    email.attach_file(file)
    email.attach_file(keyfile)
    email.send()


def symm_dec_send(receiver, file):
    subject = f'Decrypted file for {receiver}'
    message = 'Decrypted file'
    email = EmailMessage(subject, message, to=(receiver,))
    email.attach_file(file)
    email.send()
   
    

def asym_enc_send(receiver, file, pubkey, privkey):
    subject = f'Encrypted file and key for {receiver}'
    message = 'Do not delete your keys. Private key is needed for decrypting.'
    email = EmailMessage(subject, message, to=(receiver,))
    email.attach_file(file)
    email.attach_file(pubkey)
    email.attach_file(privkey)
    email.send()


def asym_dec_send(receiver, file):
    subject = f'Decrypted file for {receiver}'
    message = 'Decrypted file'
    email = EmailMessage(subject, message, to=(receiver,))
    email.attach_file(file)
    email.send()