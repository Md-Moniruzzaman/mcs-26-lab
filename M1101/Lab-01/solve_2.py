import string
from caesar import decrypt, find_key_frequency

ct = "MYXQVBKX ZKBDEOKX LOXGXXKVBOBK"
k = find_key_frequency(ct)
print(f"Recovered key: {k}")
print(f"Plaintext: {decrypt(ct, k)}")
