# deterministic-rsa-keygen

Use pycryptodome to generate a deterministic RSA key pair and perform encrypt and decrypt operations

## Install

`pip install deterministic-rsa-keygen`

## Ussage

```
from rsa import generate_key, encrypt, decrypt

# as alternatives you can use a bit39 phrase or another key as seed
secret_key = generate_key("the derived key cannot be stronger than this seed")

private_key = secret_key.exportKey("PEM")
public_key = secret_key.publickey().exportKey("PEM")

secret = encrypt("secret", public_key)
assert decrypt(secret, private_key) == bytes("secret", 'utf-8')
```
