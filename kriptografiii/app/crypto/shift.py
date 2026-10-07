from typing import Dict, Any, List
from .utils import letter_to_num, num_to_letter, sanitize_text

def validate_key(key: Any) -> int:
    try:
        k = int(key)
        return k % 26
    except (ValueError, TypeError):
        raise ValueError("Key untuk Shift Cipher harus berupa bilangan bulat (0-25).")

def encrypt(plaintext: str, key: Any) -> Dict[str, Any]:
    k = validate_key(key)
    clean_p = sanitize_text(plaintext)
    ciphertext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, char in enumerate(clean_p):
        p_val = letter_to_num(char)
        c_val = (p_val + k) % 26
        c_char = num_to_letter(c_val)
        ciphertext_chars.append(c_char)
        if i < 20:  # store sample steps for visualization
            steps.append({
                "index": i,
                "plain_char": char,
                "p": p_val,
                "calculation": f"({p_val} + {k}) mod 26 = {c_val}",
                "cipher_char": c_char
            })

    return {
        "ciphertext": "".join(ciphertext_chars),
        "key": k,
        "input_length": len(clean_p),
        "steps": steps
    }

def decrypt(ciphertext: str, key: Any) -> Dict[str, Any]:
    k = validate_key(key)
    clean_c = sanitize_text(ciphertext)
    plaintext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, char in enumerate(clean_c):
        c_val = letter_to_num(char)
        p_val = (c_val - k) % 26
        p_char = num_to_letter(p_val)
        plaintext_chars.append(p_char)
        if i < 20:
            steps.append({
                "index": i,
                "cipher_char": char,
                "c": c_val,
                "calculation": f"({c_val} - {k}) mod 26 = {p_val}",
                "plain_char": p_char
            })

    return {
        "plaintext": "".join(plaintext_chars),
        "key": k,
        "input_length": len(clean_c),
        "steps": steps
    }
