import string
from typing import Dict, Any, List
from .utils import sanitize_text

STANDARD_ALPHABET = string.ascii_uppercase

def validate_key(key: str) -> str:
    cleaned = "".join([c.upper() for c in key if c.isalpha()])
    if len(cleaned) != 26:
        raise ValueError(f"Key Substitution harus memiliki panjang tepat 26 huruf alfabet (Diterima: {len(cleaned)} huruf).")
    if len(set(cleaned)) != 26:
        duplicates = [c for c in cleaned if cleaned.count(c) > 1]
        unique_dups = sorted(list(set(duplicates)))
        raise ValueError(f"Key Substitution tidak boleh memiliki huruf berulang: {', '.join(unique_dups)}")
    return cleaned

def encrypt(plaintext: str, key: str) -> Dict[str, Any]:
    valid_key = validate_key(key)
    clean_p = sanitize_text(plaintext)
    mapping = {STANDARD_ALPHABET[i]: valid_key[i] for i in range(26)}
    
    ciphertext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, char in enumerate(clean_p):
        c_char = mapping.get(char, char)
        ciphertext_chars.append(c_char)
        if i < 20:
            steps.append({
                "index": i,
                "plain_char": char,
                "cipher_char": c_char,
                "mapping": f"{char} -> {c_char}"
            })

    return {
        "ciphertext": "".join(ciphertext_chars),
        "key": valid_key,
        "mapping": mapping,
        "input_length": len(clean_p),
        "steps": steps
    }

def decrypt(ciphertext: str, key: str) -> Dict[str, Any]:
    valid_key = validate_key(key)
    clean_c = sanitize_text(ciphertext)
    rev_mapping = {valid_key[i]: STANDARD_ALPHABET[i] for i in range(26)}
    
    plaintext_chars: List[str] = []
    steps: List[Dict[str, Any]] = []

    for i, char in enumerate(clean_c):
        p_char = rev_mapping.get(char, char)
        plaintext_chars.append(p_char)
        if i < 20:
            steps.append({
                "index": i,
                "cipher_char": char,
                "plain_char": p_char,
                "mapping": f"{char} -> {p_char}"
            })

    return {
        "plaintext": "".join(plaintext_chars),
        "key": valid_key,
        "reverse_mapping": rev_mapping,
        "input_length": len(clean_c),
        "steps": steps
    }
