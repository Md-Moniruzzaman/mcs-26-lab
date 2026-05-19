import string
import matplotlib.pyplot as plt
from caesar import encrypt, decrypt, brute_force, frequency_analysis, index_of_coincidence, find_key_frequency

def ex1_1():
    print("=== Ex 1.1 ===")
    pt = "cryptography is fun"
    ct_7 = encrypt(pt, 7)
    print(f"k=7: {ct_7}")
    pt_dec = decrypt(ct_7, 7)
    print(f"decrypted: {pt_dec}")
    ct_19 = encrypt(ct_7, 19)
    print(f"k=19 on ct_7: {ct_19}")
    for c in pt:
        if c.isalpha():
            num = ord(c.lower()) - ord('a')
            new_num = (num + 7) % 26
            print(f"{c} ({num}) + 7 = {num+7} % 26 = {new_num} ({chr(new_num + ord('a'))})")

def ex1_2():
    print("\n=== Ex 1.2 ===")
    ct = "MYXQVBKX ZKBDEOKX LOXGXXKVBOBK"
    print("Brute forcing:")
    for k in range(1, 26):
        print(f"k={k}: {decrypt(ct, k)}")

def ex1_3():
    print("\n=== Ex 1.3 ===")
    text = """Cryptography, or cryptology, is the practice and study of techniques for secure communication in the presence of adversarial behavior. More generally, cryptography is about constructing and analyzing protocols that prevent third parties or the public from reading private messages. Modern cryptography exists at the intersection of the disciplines of mathematics, computer science, electrical engineering, communication science, and physics. Applications of cryptography include electronic commerce, chip-based payment cards, digital currencies, computer passwords, and military communications. Cryptography prior to the modern age was effectively synonymous with encryption, the conversion of information from a readable state to apparent nonsense. The originator of an encrypted message shared the decoding technique needed to recover the original information only with intended recipients, thereby precluding unwanted persons from doing the same. The cryptography literature often uses the name Alice for the sender, Bob for the intended recipient, and Eve for the eavesdropper. Since the development of rotor cipher machines in World War I and the advent of computers in World War II, the methods used to carry out cryptology have become increasingly complex and its application more widespread."""
    print(f"Length of text: {len(text)}")
    ct = encrypt(text, 12)
    # create plot
    from caesar import plot_frequencies
    # plot_frequencies will save to caesar_freq.pdf and show() - we don't want it to block on show()
    # Let's monkeypatch plt.show
    plt.show = lambda: None
    k_recovered = find_key_frequency(ct)
    print(f"Recovered key: {k_recovered}")
    plot_frequencies(ct, k_recovered)

def ex1_4():
    print("\n=== Ex 1.4 ===")
    # IC of ct from ex 1.3
    ct = "MYXQVBKX ZKBDEOKX LOXGXXKVBOBK"
    ic = index_of_coincidence(ct)
    print(f"IC of ciphertext: {ic}")
    eng = "Cryptography, or cryptology, is the practice and study of techniques for secure communication in the presence of adversarial behavior."
    ic_eng = index_of_coincidence(eng)
    print(f"IC of English: {ic_eng}")

ex1_1()
ex1_2()
ex1_3()
ex1_4()
