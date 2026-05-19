
import matplotlib.pyplot as plt

ENGLISH_FREQ = [
    8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, # a-g
    6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, # h-n
    7.51, 1.93, 0.10, 5.99, 6.33, 9.06, 2.76, # o-u
    0.98, 2.36, 0.15, 1.97, 0.07 # v-z
]

def encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - start + key) % 26 + start)
        else:
            result += char
    return result

def decrypt(encrypted_text, key):
    return encrypt(encrypted_text, -key)

def brute_force(encrypted_text):
    print ( f"{'KEY' : >3} {'DECRYPTED TEXT'}")
    print ("-" * 60)
    for k in range (1 , 26) :
        candidate = decrypt ( encrypted_text , k )
        print ( f"{k: >3} { candidate }")

def frequency_analysis(text):
    """ Return relative frequencies (%) of each letter a-z."""
    freq = {}
    total = 0
    for char in text:
        if char.isalpha():
            char = char.lower()
            freq[char] = freq.get(char, 0) + 1
            total += 1
    if total > 0:
        for char in freq:
            freq[char] = freq[char] / total * 100
            
    return freq



def chi_squared(observed_text, expected_freq):
    """Compute the Chi-squared statistic."""
    observed_freq = frequency_analysis(observed_text)
    chi2 = sum((observed_freq.get(char, 0) - expected_freq[char]) ** 2 / expected_freq[char] for char in expected_freq)
    return chi2

def find_key_frequency(ciphertext):
    """ Find best key by minimising chi - squared score ."""
    obs_dict = frequency_analysis(ciphertext)
    obs = [obs_dict.get(chr(i + ord('a')), 0) for i in range(26)]
    scores = {}
    for k in range(26):
        # Shift observed frequencies back by k to compare against English
        shifted = obs[k:] + obs[:k]
        scores[k] = sum((o - e) ** 2 / e for o, e in zip(shifted, ENGLISH_FREQ))
        
    best_k = min(scores, key=scores.get)
    # Print scores table
    print(f"{'Key':>4} {'Chi-squared':>12}")
    print("-" * 20)
    for k, score in sorted(scores.items()):
        marker = " <-- best " if k == best_k else ""
        print(f"{k:>4} {score:>12.4f}{marker}")
    return best_k

def plot_frequencies(ciphertext, k):
    
    letters = list('abcdefghijklmnopqrstuvwxyz')
    obs_dict = frequency_analysis(ciphertext)
    obs = [obs_dict.get(char, 0) for char in letters]
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    # Ciphertext frequencies
    axes[0].bar(letters, obs, color='steelblue')
    axes[0].set_title('Ciphertext letter frequencies')
    axes[0].set_xlabel('Letter'); axes[0].set_ylabel('Frequency (%)')
    # English reference
    axes[1].bar(letters, ENGLISH_FREQ, color='darkorange')
    axes[1].set_title('Expected English frequencies')
    axes[1].set_xlabel('Letter'); axes[1].set_ylabel('Frequency (%)')
    plt.suptitle(f'Frequency analysis -- recovered key k = {k}')
    plt.tight_layout()
    plt.savefig('caesar_freq.pdf', dpi=150)
    plt.show()

def index_of_coincidence(text):
    """Compute the Index of Coincidence (IC)."""
    freq = frequency_analysis(text)
    total = sum(freq.values())
    ic = sum(freq[char] * (freq[char] - 1) for char in freq) / (total * (total - 1))
    return ic

def ex1_1():
    print("=== Exercise 1.1 ===")
    pt = "cryptography is fun"
    ct_7 = encrypt(pt, 7)
    ct_19 = encrypt(pt, 19)
    pt_dec = decrypt(ct_7, 7)
    print("Plain Text: ", pt)
    print("Cipher Text (k=7): ", ct_7)
    print("Decrypted Text (k=7): ", pt_dec)
    print("Cipher Text (k=19): ", ct_19)
    print("Decrypted Text (k=19): ", decrypt(ct_19, 19))
    print("\nNumeric calculations for each letter (k=7):")
    for c in pt:
        if c.isalpha():
            num = ord(c.lower()) - ord('a')
            new_num = (num + 7) % 26
            print(f"{c} ({num}) + 7 = {num+7} % 26 = {new_num} ({chr(new_num + ord('a'))})")

def ex1_2():
    print("\n=== Exercise 1.2 ===")
    ct = "MYXQVBKX ZKBDEOKX LOXGXXKVBOBK"
    print("Cipher Text: ", ct)
    print("Brute forcing:")
    brute_force(ct)

def ex1_3():
    print("\n=== Exercise 1.3 ===")
    text = """
    Cryptography, or cryptology, is the practice and study of techniques for secure communication in the presence of adversarial behavior. More generally, cryptography is about constructing and analyzing protocols that prevent third parties or the public from reading private messages. Modern cryptography exists at the intersection of the disciplines of mathematics, computer science, electrical engineering, communication science, and physics. Applications of cryptography include electronic commerce, chip-based payment cards, digital currencies, computer passwords, and military communications. Cryptography prior to the modern age was effectively synonymous with encryption, the conversion of information from a readable state to apparent nonsense. The originator of an encrypted message shared the decoding technique needed to recover the original information only with intended recipients, thereby precluding unwanted persons from doing the same. The cryptography literature often uses the name Alice for the sender, Bob for the intended recipient, and Eve for the eavesdropper. Since the development of rotor cipher machines in World War I and the advent of computers in World War II, the methods used to carry out cryptology have become increasingly complex and its application more widespread.
    """
    print("Original Text: ", text)
    print("Length of text: ", len(text))
    print("Encrypting with Key: ", 12)
    ct = encrypt(text, 12)
    print("Cipher Text: ", ct)
    print("Length of Cipher Text: ", len(ct))

    print("\nFrequency analysis:")

    k_recovered = find_key_frequency(ct)
    print(f"Recovered key: {k_recovered}")

    print("\nDecrypting with recovered key...")
    pt_dec = decrypt(ct, k_recovered)
    print("Decrypted Text: ", pt_dec)
    
    print("\nPlotting frequencies...")
    plot_frequencies(ct, k_recovered)

def ex1_4():
    print("\n=== Exercise 1.4 ===")
    # IC of ct from ex 1.3
    ct = "MYXQVBKX ZKBDEOKX LOXGXXKVBOBK"
    ic = index_of_coincidence(ct)
    print(f"IC of ciphertext: {ic}")
    eng = "Cryptography, or cryptology, is the practice and study of techniques for secure communication in the presence of adversarial behavior."
    ic_eng = index_of_coincidence(eng)
    print(f"IC of English: {ic_eng}")
    ic_mono = ic_eng
    ic_vigenere = 0.0385 # Polyalphabetic IC approaches 1/26 ≈ 0.0385

    print("IC of Monoalphabetic (Caesar):", ic_mono)
    print("IC of Polyalphabetic (Vigenere):", ic_vigenere)
    print("IC of English:", ic_eng)
    
    if abs(ic - ic_mono) < 0.05:
        print("The ciphertext is likely encrypted with a monoalphabetic cipher.")
        print("Attack: Frequency Analysis")
        print("Time: ~0.001s")
    elif abs(ic - ic_vigenere) < 0.05:
        print("The ciphertext is likely encrypted with a polyalphabetic cipher.")
        print("Attack: Kasiski Examination / Index of Coincidence")
        print("Time: ~1s to find key, depends on text length")
    else:
        print("Cannot determine cipher type.")
    print("\nSecurity Table:")
    print("=" * 60)
    print("{:<50} {:<25}".format("Property", "Caesar Cipher"))
    print("-" * 75)
    print("{:<50} {:<25}".format("1. Key space size", "26"))
    print("{:<50} {:<25}".format("2. Time to brute-force (at 10^9 keys/sec)", "~26ns"))
    print("{:<50} {:<25}".format("3. Vulnerable to frequency analysis?", "Yes"))
    print("{:<50} {:<25}".format("4. Index of Coincidence", ic_mono))
    print("{:<50} {:<25}".format("5. Attack type that breaks it", "Frequency Analysis / Brute-Force"))
    print("=" * 75)

if __name__ == "__main__":
    print("="*60)
    print("{:^60}".format("MCS-26 - M1101 - LAB 01 - CAESAR CIPHER"))
    print("="*60)
    print("{:^60}".format("Group Members:"))
    print("="*60)
    print(" {:<30} {:<25}".format("1. Lt Col Mamun", "(ID-007)"))
    print(" {:<30} {:<25}".format("2. Lt Col Hasnat", "(ID-005)"))
    print(" {:<30} {:<25}".format("3. Shaon Mir", "(ID-026)"))
    print(" {:<30} {:<25}".format("4. Moniruzzaman", "(ID-012)"))
    print("="*60)
    
    while True:
        print("\nPlease Select an option:")
        option = int(input("1. Exercise 1.1\n2. Exercise 1.2\n3. Exercise 1.3\n4. Exercise 1.4\n5. Exit\n"))
        if option == 1:
            ex1_1()
        elif option == 2:
            ex1_2()
        elif option == 3:
            ex1_3()
        elif option == 4:
            ex1_4()
        elif option == 5:
            break
        else:
            print("Invalid option. Please try again.")



