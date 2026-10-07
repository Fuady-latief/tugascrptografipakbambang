import secrets
import string
from typing import Dict, Any, List
from .utils import letter_to_num, num_to_letter, sanitize_text

def generate_random_key(length: int = 1000) -> str:
    """Generate a cryptographically secure random uppercase string for OTP key file."""
    return "".join(secrets.choice(string.ascii_uppercase) for _ in range(length))

def clean_key_text(key_raw: str) -> str:
    return sanitize_text(key_raw)

def encrypt(plaintext: str, key_content: str) -> Dict[str, Any]:
    clean_p = sanitize_text(plaintext)
    clean_k = clean_key_text(key_content)

    if len(clean_k) < len(clean_p):
        raise ValueError(
            f"Panjang key dari file ({len(clean_k)} huruf) tidak mencukupi untuk panjang pesan ({len(clean_p)} huruf). "
            f"Sesuai prinsip One-Time Pad, key harus minimal sama panjang dengan pesan."
        )

    used_key = clean_k[:len(clean_p)]
    unused_key_count = len(clean_k) - len(clean_p)

    ciphertext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, p_char in enumerate(clean_p):
        k_char = used_key[i]
        p_val = letter_to_num(p_char)
        k_val = letter_to_num(k_char)
        c_val = (p_val + k_val) % 26
        c_char = num_to_letter(c_val)
        ciphertext_chars.append(c_char)

        if i < 20:
            steps.append({
                "index": i,
                "plain_char": p_char,
                "key_char": k_char,
                "p": p_val,
                "k": k_val,
                "calculation": f"({p_val} + {k_val}) mod 26 = {c_val}",
                "cipher_char": c_char
            })

    return {
        "ciphertext": "".join(ciphertext_chars),
        "used_key": used_key,
        "total_key_length": len(clean_k),
        "used_key_length": len(used_key),
        "unused_key_length": unused_key_count,
        "steps": steps
    }

def decrypt(ciphertext: str, key_content: str) -> Dict[str, Any]:
    clean_c = sanitize_text(ciphertext)
    clean_k = clean_key_text(key_content)

    if len(clean_k) < len(clean_c):
        raise ValueError(
            f"Panjang key dari file ({len(clean_k)} huruf) tidak mencukupi untuk panjang ciphertext ({len(clean_c)} huruf)."
        )

    used_key = clean_k[:len(clean_c)]
    unused_key_count = len(clean_k) - len(clean_c)

    plaintext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, c_char in enumerate(clean_c):
        k_char = used_key[i]
        c_val = letter_to_num(c_char)
        k_val = letter_to_num(k_char)
        p_val = (c_val - k_val) % 26
        p_char = num_to_letter(p_val)
        plaintext_chars.append(p_char)

        if i < 20:
            steps.append({
                "index": i,
                "cipher_char": c_char,
                "key_char": k_char,
                "c": c_val,
                "k": k_val,
                "calculation": f"({c_val} - {k_val}) mod 26 = {p_val}",
                "plain_char": p_char
            })

    return {
        "plaintext": "".join(plaintext_chars),
        "used_key": used_key,
        "total_key_length": len(clean_k),
        "used_key_length": len(used_key),
        "unused_key_length": unused_key_count,
        "steps": steps
    }
