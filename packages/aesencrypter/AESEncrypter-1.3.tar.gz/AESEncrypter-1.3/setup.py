import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name='AESEncrypter',  
  version='1.3',
  scripts=['AESEncrypter'] ,
  author="Soluciones Andinas",
  author_email="info@sandinas.com.ar",
  description="AES-256 CBC Encrypt/Decrypt utility package",
  long_description="AESEncrypter is a utility package that allows you to encrypt with AES-256 CBC mode, a character string with an encryption phrase passed as an argument. It also includes the decryption function.",
  long_description_content_type="text/markdown",
  url="http://www.solucionesandinas.com.ar",
  packages=setuptools.find_packages(),
  install_requires=['pycryptodome','pycryptodomex'],
  classifiers=[
      "Programming Language :: Python :: 3.7",
      "Operating System :: OS Independent",
  ],
)