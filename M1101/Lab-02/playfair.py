
import string
from collections import Counter
import matplotlib.pyplot as plt
import urllib.request

def build_matrix(key: str) -> list[list[str]]:
    key = key.upper().replace("J", "I")
    matrix = []
    for char in key:
        if char.isalpha() and char not in matrix:
            matrix.append(char)
    for char in string.ascii_uppercase.replace('J', ''):
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix: list[list[str]], char: str) -> tuple[int, int]:
    char = char.replace('J', 'I').upper()
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    raise ValueError(f"Character {char} not found in matrix")

def print_matrix(matrix: list[list[str]]):
    print("+------"*5+"+")
    for row in matrix:
        print ("| " + " | ". join ( f"{ cell :3} " for cell in row ) + " |")
        print("+------"*5+"+")

def prepare_plaintext(plaintext: str) -> str:
    plaintext = "".join(ch for ch in plaintext.upper() if ch.isalpha()).replace("J", "I")
    digraphs = []
    i = 0
    while i < len(plaintext):
        if i + 1 == len(plaintext):
            digraphs.append((plaintext[i], 'X'))
            break
        if plaintext[i] == plaintext[i+1]:
            digraphs.append((plaintext[i], 'X'))
            i += 1
        else:
            digraphs.append((plaintext[i], plaintext[i+1]))
            i += 2
    return digraphs

def encrypt_digraphs(digraphs: list[tuple[str, str]], key: str) -> str:
    matrix = build_matrix(key)
    print_matrix(matrix)
    ciphertext = ""
    for a, b in digraphs:
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]
    return ciphertext

def encrypt(plaintext: str, key: str) -> str:
    digraphs = prepare_plaintext(plaintext)
    return encrypt_digraphs(digraphs, key)

def decrypt_digraphs(digraphs: list[tuple[str, str]], key: str) -> str:
    matrix = build_matrix(key)
    plaintext = ""
    for a, b in digraphs:
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]
    return plaintext

def decrypt(ciphertext: str, key: str) -> str:
    ciphertext = "".join(ch for ch in ciphertext.upper() if ch.isalpha()).replace("J", "I")
    digraphs = [(ciphertext[i], ciphertext[i+1]) for i in range(0, len(ciphertext), 2)]
    return decrypt_digraphs(digraphs, key)

def digram_frequencies ( text : str , n =20) :
    text = ''.join(ch for ch in text.upper() if ch.isalpha())
    digrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    counts = Counter(digrams)
    total = sum(counts.values())
    top = counts.most_common(n)
    labels = [d[0] for d in top]
    freqs = [d[1]/total*100 for d in top]
    return labels , freqs

# Compare plaintext vs ciphertext digram distributions
import os

if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/2701/2701-0.txt" # Moby Dick
    filename = "english_sample.txt"

    if not os.path.exists(filename):
        print("english_sample.txt not found. Attempting to download Moby Dick...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.read().decode('utf-8'))
            print("Successfully downloaded english_sample.txt")
        except Exception as e:
            print(f"Could not download sample from Gutenberg ({e}). Creating a fallback sample...")
            fallback_text = (
                "The Project Gutenberg eBook of Moby-Dick; or The Whale, by Herman Melville. "
                "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, "
                "and nothing particular to interest me on shore, I thought I would sail about a little and see the watery "
                "part of the world. It is a way I have of driving off the spleen and regulating the circulation. "
                "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; "
                "whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every "
                "funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong "
                "moral principle to prevent me from deliberately stepping into the street, and methodically knocking "
                "people's hats off—then, I account it high time to get to sea as soon as I can. This is my substitute for pistol "
                "and ball. With a philosophical flourish Cato throws himself upon his sword; I quietly take to the ship. "
                "There is nothing surprising in this. If they but knew it, almost all men in their degree, some time or other, "
                "cherish very nearly the same feelings towards the ocean with me."
            ) * 50  # Repeat to make it long enough for frequency analysis
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(fallback_text)

    with open(filename, 'r', encoding='utf-8') as f:
        english = f.read()

    ct_full = encrypt(english, "MONARCHY")
    lp, fp = digram_frequencies(english)
    lc, fc = digram_frequencies(ct_full)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.bar(lp, fp, color='navy')
    ax1.set_title('Top-20 digrams - English plaintext')
    ax2.bar(lc, fc, color='firebrick')
    ax2.set_title('Top-20 digrams - Playfair ciphertext')
    for ax in (ax1, ax2):
        ax.set_xlabel('Digram')
        ax.set_ylabel('Frequency (%)')
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('playfair_digrams.pdf', dpi=150)
    plt.show()

    # key = "monarchy"
    # plaintext = "instrument"
    # print("Plaintext: ", plaintext)
    # print("Key: ", key)
    # print("Ciphertext: ", encrypt(plaintext, key))
    # print("Decrypted: ", decrypt(encrypt(plaintext, key), key))

    PT109_CT = (
        " KXJEYUREBE ZWEHEWRYTU HEYFS "
        " KREHE GOYFI WTTTU OLKSY CAJPO "
        " BOTEI ZONTX BYBNT GONEY CUZWR "
        " GDSON SXBOU YWRHE BAAHY USEDQ "
    )
    ct = PT109_CT.replace(' ', '')
    key = " ROYAL NEW ZEALAND NAVY "
    print("Ciphertext: ", ct)
    print("Key: ", key)
    pt = decrypt(ct, key)
    print("Decrypted (TT): ", pt)
    print("Expected Telegraphic Text (TT): ", "PTBOATONEONINELOSTINACTIONINBLACKETTSTRAIT")
    # TWOMILESSWMERESUCOVEXCREWOFTWELVEX
    # REQUESTANYINFORMATIONX