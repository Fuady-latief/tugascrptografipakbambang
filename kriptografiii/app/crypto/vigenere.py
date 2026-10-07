from typing import Dict, Any, List
from .utils import letter_to_num, num_to_letter, sanitize_text

def validate_key(key: str) -> str:
    cleaned = sanitize_text(key)
    if not cleaned:
        raise ValueError("Key untuk Vigenere Cipher harus berisi minimal satu huruf alfabet (A-Z).")
    return cleaned

def encrypt(plaintext: str, key: str) -> Dict[str, Any]:
    valid_key = validate_key(key)
    # Aturan tugas: angka, spasi, tanda baca diabaikan dan TIDAK disimpan di ciphertext
    clean_p = sanitize_text(plaintext)
    ciphertext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []
    key_len = len(valid_key)

    for i, char in enumerate(clean_p):
        k_char = valid_key[i % key_len]
        p_val = letter_to_num(char)
        k_val = letter_to_num(k_char)
        c_val = (p_val + k_val) % 26
        c_char = num_to_letter(c_val)
        ciphertext_chars.append(c_char)
        if i < 20:
            steps.append({
                "index": i,
                "plain_char": char,
                "key_char": k_char,
                "p": p_val,
                "k": k_val,
                "calculation": f"({p_val} + {k_val}) mod 26 = {c_val}",
                "cipher_char": c_char
            })

    return {
        "ciphertext": "".join(ciphertext_chars),
        "key": valid_key,
        "input_length": len(clean_p),
        "ignored_characters_note": "Semua spasi, angka, dan tanda baca telah diabaikan sesuai ketentuan tugas.",
        "steps": steps
    }

def decrypt(ciphertext: str, key: str) -> Dict[str, Any]:
    valid_key = validate_key(key)
    clean_c = sanitize_text(ciphertext)
    plaintext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []
    key_len = len(valid_key)

    for i, char in enumerate(clean_c):
        k_char = valid_key[i % key_len]
        c_val = letter_to_num(char)
        k_val = letter_to_num(k_char)
        p_val = (c_val - k_val) % 26
        p_char = num_to_letter(p_val)
        plaintext_chars.append(p_char)
        if i < 20:
            steps.append({
                "index": i,
                "cipher_char": char,
                "key_char": k_char,
                "c": c_val,
                "k": k_val,
                "calculation": f"({c_val} - {k_val}) mod 26 = {p_val}",
                "plain_char": p_char
            })

    return {
        "plaintext": "".join(plaintext_chars),
        "key": valid_key,
        "input_length": len(clean_c),
        "steps": steps
    }
