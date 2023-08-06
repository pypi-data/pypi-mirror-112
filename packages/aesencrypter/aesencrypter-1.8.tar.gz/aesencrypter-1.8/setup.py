from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='aesencrypter',  
  version='1.8',
  author="Soluciones Andinas",
  author_email="info@sandinas.com.ar",
  description="AES-256 CBC Encrypt/Decrypt utility package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="http://www.solucionesandinas.com.ar",
  py_modules=["aesencrypter"],
  package_dir={'': 'src'},
  packages=find_packages(),
  install_requires=['pycryptodome','pycryptodomex',],
  classifiers=["Programming Language :: Python :: 3.7","Operating System :: OS Independent",],
)