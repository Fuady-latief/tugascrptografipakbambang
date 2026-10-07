import math
from typing import Dict, Any, List, Tuple
from .utils import letter_to_num, num_to_letter, sanitize_text, mod_inverse

# Valid values of 'a' coprime to 26
COPRIME_26 = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

def validate_key(a_val: Any, b_val: Any) -> Tuple[int, int, int]:
    try:
        a = int(a_val)
        b = int(b_val)
    except (ValueError, TypeError):
        raise ValueError("Key 'a' dan 'b' pada Affine Cipher harus berupa bilangan bulat.")

    a_mod = a % 26
    b_mod = b % 26

    if math.gcd(a_mod, 26) != 1:
        raise ValueError(f"Nilai a = {a} tidak relatif prima dengan 26 (gcd({a_mod}, 26) = {math.gcd(a_mod, 26)} != 1). Pilihan valid untuk 'a' mod 26 adalah: {COPRIME_26}")

    a_inv = mod_inverse(a_mod, 26)
    if a_inv is None:
        raise ValueError(f"Invers modulo untuk a = {a} tidak ditemukan pada modulo 26.")

    return a_mod, b_mod, a_inv

def encrypt(plaintext: str, a_val: Any, b_val: Any) -> Dict[str, Any]:
    a, b, a_inv = validate_key(a_val, b_val)
    clean_p = sanitize_text(plaintext)
    ciphertext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, char in enumerate(clean_p):
        p_val = letter_to_num(char)
        c_val = (a * p_val + b) % 26
        c_char = num_to_letter(c_val)
        ciphertext_chars.append(c_char)
        if i < 20:
            steps.append({
                "index": i,
                "plain_char": char,
                "p": p_val,
                "calculation": f"({a} * {p_val} + {b}) mod 26 = {c_val}",
                "cipher_char": c_char
            })

    return {
        "ciphertext": "".join(ciphertext_chars),
        "a": a,
        "b": b,
        "a_inv": a_inv,
        "input_length": len(clean_p),
        "steps": steps
    }

def decrypt(ciphertext: str, a_val: Any, b_val: Any) -> Dict[str, Any]:
    a, b, a_inv = validate_key(a_val, b_val)
    clean_c = sanitize_text(ciphertext)
    plaintext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, char in enumerate(clean_c):
        c_val = letter_to_num(char)
        p_val = (a_inv * (c_val - b)) % 26
        p_char = num_to_letter(p_val)
        plaintext_chars.append(p_char)
        if i < 20:
            steps.append({
                "index": i,
                "cipher_char": char,
                "c": c_val,
                "calculation": f"{a_inv} * ({c_val} - {b}) mod 26 = {p_val}",
                "plain_char": p_char
            })

    return {
        "plaintext": "".join(plaintext_chars),
        "a": a,
        "b": b,
        "a_inv": a_inv,
        "input_length": len(clean_c),
        "steps": steps
    }
