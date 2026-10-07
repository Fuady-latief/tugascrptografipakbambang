import math
from typing import Tuple, List, Optional

def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a: int, m: int = 26) -> Optional[int]:
    """Returns the modular multiplicative inverse of a modulo m, or None if it doesn't exist."""
    a = a % m
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def sanitize_text(text: str, keep_spaces: bool = False) -> str:
    """Keep only uppercase alphabetic letters A-Z (and optionally spaces)."""
    if keep_spaces:
        return "".join([c.upper() for c in text if c.isalpha() or c == ' '])
    return "".join([c.upper() for c in text if c.isalpha()])

def letter_to_num(char: str) -> int:
    return ord(char.upper()) - ord('A')

def num_to_letter(num: int) -> str:
    return chr((num % 26) + ord('A'))
