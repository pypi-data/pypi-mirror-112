# AES-256 CBC Encrypter/Decrypter module

AESEncrypter is a utility package that allows you to encrypt with AES-256 CBC mode, a characters string with an encryption phrase passed as an argument. It also includes the decryption function.

## Requirements
Have pycryptodome and pycryptodomex installed

## Installation
Run the following to install:

pip install aesencrypter

## Usage
from aesencrypter import EncryptString, DecryptString

plain_string = "Hello, World!"  
secret_key = "9ka87c30-9889-77a4-24-7ce56a47-6718-41a4-8677-52fe438d4f7b"  
e = EncryptString(plain_string, secret_key)  
d = DecryptString(e, secret_key)  
print("Plain String.......: " + plain_string)  
print("Encrypted String...: " + e)  
print("Decrypted String...: " + d)  


