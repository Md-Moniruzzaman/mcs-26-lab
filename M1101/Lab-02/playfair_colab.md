# Google Colab Step-by-Step Blueprint: Playfair Cipher Lab-02
**Bangladesh University of Professionals (BUP)**  
**MCS-26 - M1101 - Lab 02: Playfair Cipher**  
**Group 2 Members**: Lt Col Mamun (007), Lt Col Hasnat (005), Shaon Mir (026), Moniruzzaman (012)

This document provides the exact code and markdown cells you need to copy and paste into Google Colab. Create a new notebook in Google Colab, and add the cells sequentially as described below.

---

### [Cell 1] - Markdown (Notebook Header)
Copy and paste this into a **Markdown Cell** at the very top:
```markdown
# Bangladesh University of Professionals (BUP)
## MCS-26 - M1101: Cryptography Lab-02
### Topic: Complete Implementation & Analysis of the Playfair Cipher

**Group Members (Group 2):**
1. Lt Col Mamun (ID-007)
2. Lt Col Hasnat (ID-005)
3. Shaon Mir (ID-026)
4. Moniruzzaman (ID-012)
```

---

### [Cell 2] - Code (Setup & Imports)
Copy and paste this into a **Code Cell**:
```python
# Cell 2: Imports & Environment Setup
import string
import os
import urllib.request
from collections import Counter
import matplotlib.pyplot as plt

print("Libraries imported successfully!")
```

---

### [Cell 3] - Code (Core Playfair Functions)
Copy and paste this into a **Code Cell**:
```python
# Cell 3: Core Matrix Construction & Utility Functions

def build_matrix(key: str) -> list[list[str]]:
    """Builds a 5x5 Playfair matrix from a keyword (replacing J with I)."""
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
    """Finds row and column coordinates of a character in the 5x5 matrix."""
    char = char.replace('J', 'I').upper()
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    raise ValueError(f"Character {char} not found in matrix")

def print_matrix(matrix: list[list[str]]):
    """Utility to print the 5x5 matrix beautifully."""
    print("+------"*5+"+")
    for row in matrix:
        print("| " + " | ".join(f"{cell:3}" for cell in row) + " |")
        print("+------"*5+"+")
```

---

### [Cell 4] - Code (Plaintext Pre-processing & Digraph Logic)
Copy and paste this into a **Code Cell**:
```python
# Cell 4: Plaintext Pre-processing

def prepare_plaintext(plaintext: str) -> list[tuple[str, str]]:
    """Filters out non-alphabetic characters, replaces J with I, 
    inserts X between identical consecutive letters, and pads odd length with X."""
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
```

---

### [Cell 5] - Code (Encryption and Decryption Logic)
Copy and paste this into a **Code Cell**:
```python
# Cell 5: Encryption & Decryption Core Logic

def encrypt_digraphs(digraphs: list[tuple[str, str]], key: str) -> str:
    matrix = build_matrix(key)
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
```

---

### [Cell 6] - Markdown (Exercise 2.1 Title)
Copy and paste this into a **Markdown Cell**:
```markdown
## Exercise 2.1 – Matrix Construction
**Task**: Build the Playfair matrix for the keyword **CRYPTOGRAPHY** and verify with `build_matrix()`.
```

---

### [Cell 7] - Code (Exercise 2.1 Execution)
Copy and paste this into a **Code Cell**:
```python
# Cell 7: Verify Exercise 2.1
matrix_crypto = build_matrix("CRYPTOGRAPHY")
print("Verified Matrix for Keyword 'CRYPTOGRAPHY':")
print_matrix(matrix_crypto)
```

---

### [Cell 8] - Markdown (Exercise 2.2 Title)
Copy and paste this into a **Markdown Cell**:
```markdown
## Exercise 2.2 – Encryption Verification
**Task**: Encrypt "HIDE THE GOLD IN THE TREE STUMP" using keyword **PLAYFAIR EXAMPLE** and show each digram step.
```

---

### [Cell 9] - Code (Exercise 2.2 Step-by-Step)
Copy and paste this into a **Code Cell**:
```python
# Cell 9: Verify Exercise 2.2 step-by-step
key_ex2 = "PLAYFAIR EXAMPLE"
plaintext_ex2 = "HIDE THE GOLD IN THE TREE STUMP"

print("Keyword Matrix for 'PLAYFAIR EXAMPLE':")
matrix_ex2 = build_matrix(key_ex2)
print_matrix(matrix_ex2)

prepared = prepare_plaintext(plaintext_ex2)
print(f"\nPrepared Digraphs: {prepared}")

print("\nStep-by-step Digram Encryption:")
print("-" * 75)
print(f"{'Digram':<8} | {'Coordinates':<22} | {'Applied Rule':<25} | {'Encrypted':<10}")
print("-" * 75)

ciphertext_ex2 = ""
for a, b in prepared:
    row_a, col_a = find_position(matrix_ex2, a)
    row_b, col_b = find_position(matrix_ex2, b)
    pos_str = f"{a}:({row_a},{col_a}), {b}:({row_b},{col_b})"
    
    if row_a == row_b:
        enc_a = matrix_ex2[row_a][(col_a + 1) % 5]
        enc_b = matrix_ex2[row_b][(col_b + 1) % 5]
        rule = "Same Row (shift right)"
    elif col_a == col_b:
        enc_a = matrix_ex2[(row_a + 1) % 5][col_a]
        enc_b = matrix_ex2[(row_b + 1) % 5][col_b]
        rule = "Same Column (shift down)"
    else:
        enc_a = matrix_ex2[row_a][col_b]
        enc_b = matrix_ex2[row_b][col_a]
        rule = "Rectangle (swap columns)"
    
    enc_digram = enc_a + enc_b
    ciphertext_ex2 += enc_digram
    print(f"  {a}{b:<4} | {pos_str:<22} | {rule:<25} |   {enc_digram}")

print("-" * 75)
print(f"Final Ciphertext: {ciphertext_ex2}")
```

---

### [Cell 10] - Markdown (Exercise 2.3 Title)
Copy and paste this into a **Markdown Cell**:
```markdown
## Exercise 2.3 – Statistical Digram & Index of Coincidence (IC) Analysis
**Task**: Analyze English plaintext digrams vs Playfair ciphertext and compute Index of Coincidence.
```

---

### [Cell 11] - Code (Exercise 2.3 Computations & Plotting)
Copy and paste this into a **Code Cell**:
```python
# Cell 11: Statistical Frequency & IC Calculations

def digram_frequencies(text: str, n=20):
    text = ''.join(ch for ch in text.upper() if ch.isalpha())
    digrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    counts = Counter(digrams)
    total = sum(counts.values())
    top = counts.most_common(n)
    labels = [d[0] for d in top]
    freqs = [d[1]/total*100 for d in top]
    return labels, freqs

def compute_ic(text: str) -> float:
    text = "".join(ch for ch in text.upper() if ch.isalpha())
    N = len(text)
    if N <= 1:
        return 0.0
    counts = Counter(text)
    numerator = sum(count * (count - 1) for count in counts.values())
    return numerator / (N * (N - 1))

# Retrieve/Generate English corpus text
url = "https://www.gutenberg.org/files/2701/2701-0.txt" # Moby Dick
filename = "english_sample.txt"

if not os.path.exists(filename):
    print("Attempting to download English sample corpus (Moby Dick)...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.read().decode('utf-8'))
        print("Corpus downloaded successfully!")
    except Exception as e:
        print(f"Connection failed ({e}). Generating fallback text...")
        fallback_text = (
            "The Project Gutenberg eBook of Moby-Dick; or The Whale, by Herman Melville. "
            "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, "
            "and nothing particular to interest me on shore, I thought I would sail about a little and see the watery "
            "part of the world. It is a way I have of driving off the spleen and regulating the circulation."
        ) * 100
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(fallback_text)

with open(filename, 'r', encoding='utf-8') as f:
    english_text = f.read()

# Filter and encrypt the corpus
pt_clean = "".join(ch for ch in english_text.upper() if ch.isalpha()).replace("J", "I")
ct_clean = encrypt(pt_clean, "MONARCHY")

# Computations
ic_pt = compute_ic(pt_clean)
ic_ct = compute_ic(ct_clean)
labels_p, freqs_p = digram_frequencies(pt_clean)
labels_c, freqs_c = digram_frequencies(ct_clean)

print(f"Index of Coincidence (Plaintext): {ic_pt:.5f}")
print(f"Index of Coincidence (Ciphertext): {ic_ct:.5f}\n")

print(f"Most common plaintext digram: '{labels_p[0]}' ({freqs_p[0]:.2f}%)")
print(f"Most common ciphertext digram: '{labels_c[0]}' ({freqs_c[0]:.2f}%)")

# Plot the frequencies side-by-side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.bar(labels_p, freqs_p, color='navy')
ax1.set_title('Top-20 Digrams - English Plaintext')
ax1.set_xlabel('Digram')
ax1.set_ylabel('Frequency (%)')
ax1.tick_params(axis='x', rotation=45)

ax2.bar(labels_c, freqs_c, color='firebrick')
ax2.set_title('Top-20 Digrams - Playfair Ciphertext')
ax2.set_xlabel('Digram')
ax2.set_ylabel('Frequency (%)')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```

---

### [Cell 12] - Markdown (PT-109 Section)
Copy and paste this into a **Markdown Cell**:
```markdown
## Historic PT-109 Message Decryption
**Task**: Decrypt the historical World War II message from John F. Kennedy's boat using the key **ROYAL NEW ZEALAND NAVY** and examine field-encryption anomalies.
```

---

### [Cell 13] - Code (PT-109 Decryption)
Copy and paste this into a **Code Cell**:
```python
# Cell 13: Decrypt PT-109 message
PT109_CT = (
    " KXJEYUREBE ZWEHEWRYTU HEYFS "
    " KREHE GOYFI WTTTU OLKSY CAJPO "
    " BOTEI ZONTX BYBNT GONEY CUZWR "
    " GDSON SXBOU YWRHE BAAHY USEDQ "
)
ct = PT109_CT.replace(' ', '')
key_pt109 = " ROYAL NEW ZEALAND NAVY "

print("Decryption Key Matrix:")
print_matrix(build_matrix(key_pt109))

decrypted_text = decrypt(ct, key_pt109)
print(f"\nDecrypted Plaintext message:\n{decrypted_text}")
print("\nExpected Telegraphic Text:\nPTBOATONEONINELOSTINACTIONINBLACKETTSTRAIT")
```
