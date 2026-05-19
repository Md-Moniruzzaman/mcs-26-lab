import string
import matplotlib.pyplot as plt
from caesar import encrypt, plot_frequencies

text = """Cryptography, or cryptology, is the practice and study of techniques for secure communication in the presence of adversarial behavior. More generally, cryptography is about constructing and analyzing protocols that prevent third parties or the public from reading private messages. Modern cryptography exists at the intersection of the disciplines of mathematics, computer science, electrical engineering, communication science, and physics. Applications of cryptography include electronic commerce, chip-based payment cards, digital currencies, computer passwords, and military communications. Cryptography prior to the modern age was effectively synonymous with encryption, the conversion of information from a readable state to apparent nonsense. The originator of an encrypted message shared the decoding technique needed to recover the original information only with intended recipients, thereby precluding unwanted persons from doing the same. The cryptography literature often uses the name Alice for the sender, Bob for the intended recipient, and Eve for the eavesdropper. Since the development of rotor cipher machines in World War I and the advent of computers in World War II, the methods used to carry out cryptology have become increasingly complex and its application more widespread."""
ct = encrypt(text, 12)

# Prevent show() from blocking
plt.show = lambda: None

plot_frequencies(ct, 12)
