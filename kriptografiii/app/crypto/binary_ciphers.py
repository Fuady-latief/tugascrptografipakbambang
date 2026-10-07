import hashlib
import math
import secrets
from typing import Dict, Any, List, Tuple, Union

# ----------------- Helper Math & Hashing -----------------

def sha256_hash(data: bytes) -> str:
    """Compute SHA-256 hex digest of byte data."""
    return hashlib.sha256(data).hexdigest()

def egcd_mod(a: int, m: int = 256) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm."""
    if a == 0:
        return m, 0, 1
    gcd, x1, y1 = egcd_mod(m % a, a)
    x = y1 - (m // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse_256(a: int, m: int = 256) -> int:
    """Modular multiplicative inverse modulo m (default 256)."""
    a = a % m
    gcd, x, _ = egcd_mod(a, m)
    if gcd != 1:
        raise ValueError(f"Nilai a = {a} tidak memiliki invers modulo {m} (karena gcd({a}, {m}) = {gcd} != 1. Untuk modulo 256, a harus ganjil).")
    return (x % m + m) % m

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    """Pad bytes data to multiple of block_size using PKCS#7."""
    padding_len = block_size - (len(data) % block_size)
    if padding_len == 0:
        padding_len = block_size
    return data + bytes([padding_len] * padding_len)

def pkcs7_unpad(data: bytes, block_size: int) -> bytes:
    """Unpad bytes data padded with PKCS#7."""
    if not data or len(data) % block_size != 0:
        return data
    padding_len = data[-1]
    if padding_len < 1 or padding_len > block_size:
        return data
    if data[-padding_len:] == bytes([padding_len] * padding_len):
        return data[:-padding_len]
    return data

# ----------------- 1. Binary Shift Cipher -----------------

def encrypt_shift_bytes(data: bytes, key: int) -> bytes:
    k = key % 256
    return bytes((b + k) % 256 for b in data)

def decrypt_shift_bytes(data: bytes, key: int) -> bytes:
    k = key % 256
    return bytes((b - k) % 256 for b in data)

# ----------------- 2. Binary Substitution Cipher -----------------

def build_sbox_from_key(key: Union[str, bytes]) -> Tuple[List[int], List[int]]:
    """Deterministically derive a 256-byte S-box permutation and its inverse from a key string/bytes."""
    if isinstance(key, str):
        key_bytes = key.encode('utf-8')
    else:
        key_bytes = key

    if not key_bytes:
        key_bytes = b"CRYPTODEX_DEFAULT_SUBSTITUTION_KEY"

    # RC4-style KSA to create permutation of 0..255
    sbox = list(range(256))
    j = 0
    key_len = len(key_bytes)
    for i in range(256):
        j = (j + sbox[i] + key_bytes[i % key_len]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]

    # Invert S-box
    inv_sbox = [0] * 256
    for i in range(256):
        inv_sbox[sbox[i]] = i

    return sbox, inv_sbox

def encrypt_substitution_bytes(data: bytes, key: Union[str, bytes]) -> bytes:
    sbox, _ = build_sbox_from_key(key)
    return bytes(sbox[b] for b in data)

def decrypt_substitution_bytes(data: bytes, key: Union[str, bytes]) -> bytes:
    _, inv_sbox = build_sbox_from_key(key)
    return bytes(inv_sbox[b] for b in data)

# ----------------- 3. Binary Affine Cipher -----------------

def validate_affine_key_256(a: int, b: int) -> Tuple[int, int, int]:
    a_mod = a % 256
    b_mod = b % 256
    if math.gcd(a_mod, 256) != 1:
        raise ValueError(f"Nilai a = {a} tidak relatif prima dengan 256 (gcd({a_mod}, 256) = {math.gcd(a_mod, 256)} != 1). Untuk modulo 256, a harus berupa bilangan GANJIL.")
    a_inv = mod_inverse_256(a_mod, 256)
    return a_mod, b_mod, a_inv

def encrypt_affine_bytes(data: bytes, a: int, b: int) -> bytes:
    a_val, b_val, _ = validate_affine_key_256(a, b)
    return bytes((a_val * byte_val + b_val) % 256 for byte_val in data)

def decrypt_affine_bytes(data: bytes, a: int, b: int) -> bytes:
    _, b_val, a_inv = validate_affine_key_256(a, b)
    return bytes((a_inv * (byte_val - b_val)) % 256 for byte_val in data)

# ----------------- 4. Binary Vigenere Cipher -----------------

def encrypt_vigenere_bytes(data: bytes, key: Union[str, bytes]) -> bytes:
    k_bytes = key.encode('utf-8') if isinstance(key, str) else key
    if not k_bytes:
        raise ValueError("Key untuk Vigenere Cipher tidak boleh kosong.")
    k_len = len(k_bytes)
    return bytes((data[i] + k_bytes[i % k_len]) % 256 for i in range(len(data)))

def decrypt_vigenere_bytes(data: bytes, key: Union[str, bytes]) -> bytes:
    k_bytes = key.encode('utf-8') if isinstance(key, str) else key
    if not k_bytes:
        raise ValueError("Key untuk Vigenere Cipher tidak boleh kosong.")
    k_len = len(k_bytes)
    return bytes((data[i] - k_bytes[i % k_len]) % 256 for i in range(len(data)))

# ----------------- 5. Binary Hill Cipher -----------------

def validate_hill_matrix_256(matrix: List[List[int]]) -> Dict[str, Any]:
    n = len(matrix)
    if n not in (2, 3):
        raise ValueError("Hill Cipher untuk file biner mendukung matriks 2x2 atau 3x3.")
    for row in matrix:
        if len(row) != n:
            raise ValueError(f"Setiap baris matriks harus berukuran {n} kolom.")

    if n == 2:
        raw_det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        adj = [
            [matrix[1][1] % 256, (-matrix[0][1]) % 256],
            [(-matrix[1][0]) % 256, matrix[0][0] % 256]
        ]
    else:
        a, b, c = matrix[0][0], matrix[0][1], matrix[0][2]
        d, e, f = matrix[1][0], matrix[1][1], matrix[1][2]
        g, h, i = matrix[2][0], matrix[2][1], matrix[2][2]
        raw_det = (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g))

        c00 = (e * i - f * h)
        c01 = -(d * i - f * g)
        c02 = (d * h - e * g)
        c10 = -(b * i - c * h)
        c11 = (a * i - c * g)
        c12 = -(a * h - b * g)
        c20 = (b * f - c * e)
        c21 = -(a * f - c * d)
        c22 = (a * e - b * d)

        adj = [
            [c00 % 256, c10 % 256, c20 % 256],
            [c01 % 256, c11 % 256, c21 % 256],
            [c02 % 256, c12 % 256, c22 % 256]
        ]

    det_mod = raw_det % 256
    gcd_val = math.gcd(det_mod, 256)
    if gcd_val != 1:
        raise ValueError(f"Matriks tidak dapat diinvers pada modulo 256! det(K) = {det_mod} (mod 256) bukan ganjil (gcd({det_mod}, 256) = {gcd_val} != 1).")

    det_inv = mod_inverse_256(det_mod, 256)
    inv_matrix = [
        [(det_inv * adj[r][c]) % 256 for c in range(n)]
        for r in range(n)
    ]

    return {
        "size": n,
        "det": raw_det,
        "det_mod": det_mod,
        "det_inv": det_inv,
        "adjugate": adj,
        "inverse_matrix": inv_matrix
    }

def encrypt_hill_bytes(data: bytes, matrix: List[List[int]]) -> bytes:
    analysis = validate_hill_matrix_256(matrix)
    n = analysis["size"]
    padded_data = pkcs7_pad(data, n)

    out = bytearray(len(padded_data))
    for i in range(0, len(padded_data), n):
        block = padded_data[i:i + n]
        for c in range(n):
            val = sum(block[r] * matrix[r][c] for r in range(n)) % 256
            out[i + c] = val
    return bytes(out)

def decrypt_hill_bytes(data: bytes, matrix: List[List[int]]) -> bytes:
    analysis = validate_hill_matrix_256(matrix)
    n = analysis["size"]
    inv_k = analysis["inverse_matrix"]

    if len(data) % n != 0:
        raise ValueError(f"Ukuran ciphertext ({len(data)} bytes) harus kelipatan ukuran matriks ({n}).")

    out = bytearray(len(data))
    for i in range(0, len(data), n):
        block = data[i:i + n]
        for c in range(n):
            val = sum(block[r] * inv_k[r][c] for r in range(n)) % 256
            out[i + c] = val

    return pkcs7_unpad(bytes(out), n)

# ----------------- 6. Binary Permutation Cipher -----------------

def parse_perm_key_bytes(key: Union[str, List[int]]) -> List[int]:
    if isinstance(key, list):
        nums = [int(x) for x in key]
    elif isinstance(key, str):
        cleaned = key.strip()
        parts = cleaned.replace(",", " ").split()
        if parts and all(p.isdigit() for p in parts):
            nums = [int(p) for p in parts]
        elif cleaned.isdigit():
            nums = [int(ch) for ch in cleaned]
        elif cleaned.isalpha():
            word = cleaned.upper()
            sorted_chars = sorted(list(enumerate(word)), key=lambda x: (x[1], x[0]))
            ranks = [0] * len(word)
            for rank, (orig_idx, _) in enumerate(sorted_chars):
                ranks[orig_idx] = rank
            return ranks
        else:
            raise ValueError("Format key permutasi tidak valid.")
    else:
        raise ValueError("Key harus berupa list integer atau string.")

    m = len(nums)
    if m < 2:
        raise ValueError("Panjang blok permutasi minimal 2.")
    if set(nums) == set(range(1, m + 1)):
        return [x - 1 for x in nums]
    elif set(nums) == set(range(0, m)):
        return nums
    else:
        raise ValueError(f"Key permutasi harus berisi angka 1 hingga {m} tanpa duplikasi.")

def encrypt_permutation_bytes(data: bytes, key: Union[str, List[int]]) -> bytes:
    perm = parse_perm_key_bytes(key)
    m = len(perm)
    padded_data = pkcs7_pad(data, m)

    out = bytearray(len(padded_data))
    for i in range(0, len(padded_data), m):
        block = padded_data[i:i + m]
        for j in range(m):
            out[i + j] = block[perm[j]]
    return bytes(out)

def decrypt_permutation_bytes(data: bytes, key: Union[str, List[int]]) -> bytes:
    perm = parse_perm_key_bytes(key)
    m = len(perm)
    # Inverse permutation
    inv_perm = [0] * m
    for i, p in enumerate(perm):
        inv_perm[p] = i

    if len(data) % m != 0:
        raise ValueError(f"Ukuran ciphertext ({len(data)} bytes) harus kelipatan ukuran blok ({m}).")

    out = bytearray(len(data))
    for i in range(0, len(data), m):
        block = data[i:i + m]
        for j in range(m):
            out[i + j] = block[inv_perm[j]]

    return pkcs7_unpad(bytes(out), m)

# ----------------- 7. Binary One-Time Pad -----------------

def generate_random_bytes(length: int) -> bytes:
    """Generate cryptographically secure random bytes for binary OTP."""
    return secrets.token_bytes(length)

def encrypt_otp_bytes(data: bytes, key_bytes: bytes, mode: str = "xor") -> Tuple[bytes, int]:
    """Encrypt binary OTP using either XOR or Byte-addition modulo 256.
    Returns (ciphertext_bytes, unused_key_bytes_count).
    """
    if len(key_bytes) < len(data):
        raise ValueError(
            f"Panjang file key OTP ({len(key_bytes)} bytes) kurang dari panjang file data ({len(data)} bytes). "
            f"Sesuai prinsip One-Time Pad, key harus minimal sama panjang dengan data."
        )

    used_key = key_bytes[:len(data)]
    unused_count = len(key_bytes) - len(data)

    if mode == "add":
        cipher = bytes((data[i] + used_key[i]) % 256 for i in range(len(data)))
    else:  # standard XOR
        cipher = bytes(data[i] ^ used_key[i] for i in range(len(data)))

    return cipher, unused_count

def decrypt_otp_bytes(data: bytes, key_bytes: bytes, mode: str = "xor") -> Tuple[bytes, int]:
    if len(key_bytes) < len(data):
        raise ValueError(
            f"Panjang file key OTP ({len(key_bytes)} bytes) kurang dari panjang ciphertext ({len(data)} bytes)."
        )

    used_key = key_bytes[:len(data)]
    unused_count = len(key_bytes) - len(data)

    if mode == "add":
        plain = bytes((data[i] - used_key[i]) % 256 for i in range(len(data)))
    else:  # standard XOR
        plain = bytes(data[i] ^ used_key[i] for i in range(len(data)))

    return plain, unused_count
