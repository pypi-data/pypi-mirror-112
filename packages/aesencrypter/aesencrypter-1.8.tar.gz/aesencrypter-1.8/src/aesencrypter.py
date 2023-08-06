import base64
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
         
#Encryption function
def EncryptString(text, phrase):
    phrase_len = 32
    while len(phrase) < phrase_len:
        phrase += phrase
    phrase = phrase[0:phrase_len]
    key = phrase
    IV = get_random_bytes(AES.block_size)

    cryptor = AES.new(key.encode("utf8"), AES.MODE_CBC, IV)
    ciphertext = cryptor.encrypt(bytes(Padding.pad(text.encode('utf-8'), block_size=16)))
    return base64.b64encode(IV + ciphertext).decode()

#Decryption function
def DecryptString(text, phrase):
    phrase_len = 32
    while len(phrase) < phrase_len:
        phrase += phrase
    phrase = phrase[0:phrase_len]
    key = phrase
    unpad = lambda s: s[0:-ord(s[-1:])]
    plain_text = base64.b64decode(text)
    encoded_data = plain_text[AES.block_size:]
    IV = plain_text[0:AES.block_size]

    cryptor = AES.new(key.encode("utf8"), AES.MODE_CBC, IV)
    decrypted = cryptor.decrypt(encoded_data)
    return unpad(decrypted).decode()
