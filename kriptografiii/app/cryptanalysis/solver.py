import random
import time
import string
from collections import Counter
from typing import Dict, Any, List, Tuple
from ..crypto.utils import sanitize_text
from .corpora import (
    FREQ_INDONESIAN, FREQ_ENGLISH,
    ID_PATTERNS, EN_PATTERNS
)

STANDARD_ALPHABET = list(string.ascii_uppercase)

def get_initial_key_by_frequency(ciphertext: str, language: str = "id") -> str:
    """Generate an initial substitution key by aligning letter frequencies."""
    clean_c = sanitize_text(ciphertext)
    counts = Counter(clean_c)
    sorted_cipher_letters = [item[0] for item in counts.most_common()]

    # Append any remaining letters not in ciphertext
    for ch in STANDARD_ALPHABET:
        if ch not in sorted_cipher_letters:
            sorted_cipher_letters.append(ch)

    # Reference letters sorted by frequency descending
    ref_freq = FREQ_INDONESIAN if language.lower() == "id" else FREQ_ENGLISH
    sorted_ref_letters = sorted(STANDARD_ALPHABET, key=lambda c: ref_freq.get(c, 0.0), reverse=True)

    # Map cipher letters to reference letters: key[i] = cipher letter that maps to STANDARD_ALPHABET[i]
    # In standard substitution: C = key[P_idx] -> P = key_inv[C_idx]
    # We want a candidate substitution key K such that STANDARD_ALPHABET[i] -> K[i]
    # If cipher letter C maps to plain letter P, then K[P_idx] = C
    candidate_key = list(STANDARD_ALPHABET)
    for c_ch, p_ch in zip(sorted_cipher_letters, sorted_ref_letters):
        p_idx = ord(p_ch) - ord('A')
        candidate_key[p_idx] = c_ch

    # Ensure all 26 letters are unique
    seen = set()
    missing = []
    for ch in candidate_key:
        if ch in seen:
            missing.append(ch)
        seen.add(ch)

    if len(seen) != 26:
        # Fallback to standard alphabet
        return string.ascii_uppercase

    return "".join(candidate_key)

def decrypt_with_key(ciphertext: str, key: str) -> str:
    # key maps standard alphabet A-Z -> key[0..25]
    # To decrypt: char C -> find position in key -> that index is plain char
    rev_map = {key[i]: STANDARD_ALPHABET[i] for i in range(26)}
    return "".join([rev_map.get(ch, ch) for ch in ciphertext])

def score_text(text: str, language: str = "id") -> float:
    """Evaluate linguistic plausibility of decrypted candidate text."""
    n = len(text)
    if n == 0:
        return -9999.0

    score = 0.0
    ref_freq = FREQ_INDONESIAN if language.lower() == "id" else FREQ_ENGLISH
    patterns = ID_PATTERNS if language.lower() == "id" else EN_PATTERNS

    # 1. Unigram correlation score (Chi-squared or frequency match)
    counts = Counter(text)
    for ch, count in counts.items():
        obs_pct = (count / n) * 100
        exp_pct = ref_freq.get(ch, 0.01)
        # Penalize difference
        score -= abs(obs_pct - exp_pct) * 1.5

    # 2. High-frequency n-gram matching
    for pat, weight in patterns.items():
        pat_len = len(pat)
        occurrences = 0
        for i in range(n - pat_len + 1):
            if text[i:i + pat_len] == pat:
                occurrences += 1
        score += occurrences * (weight * -15.0)

    return score

def auto_crack_substitution(
    ciphertext: str,
    language: str = "id",
    max_iterations: int = 1500,
    restarts: int = 3
) -> Dict[str, Any]:
    start_time = time.time()
    clean_c = sanitize_text(ciphertext)

    if len(clean_c) < 15:
        return {
            "error": "Ciphertext terlalu pendek untuk kriptanalisis otomatis (minimal 15 huruf).",
            "best_key": string.ascii_uppercase,
            "decrypted_text": clean_c,
            "mapping": {},
            "fitness_score": 0.0
        }

    global_best_key = string.ascii_uppercase
    global_best_score = -float('inf')

    for restart in range(restarts):
        if restart == 0:
            current_key = list(get_initial_key_by_frequency(clean_c, language))
        else:
            current_key = list(string.ascii_uppercase)
            random.shuffle(current_key)

        current_decrypted = decrypt_with_key(clean_c, "".join(current_key))
        current_score = score_text(current_decrypted, language)

        for _ in range(max_iterations // restarts):
            # Pick two random positions to swap
            i, j = random.sample(range(26), 2)
            # Swap
            current_key[i], current_key[j] = current_key[j], current_key[i]

            candidate_decrypted = decrypt_with_key(clean_c, "".join(current_key))
            candidate_score = score_text(candidate_decrypted, language)

            if candidate_score > current_score:
                current_score = candidate_score
            else:
                # Revert swap
                current_key[i], current_key[j] = current_key[j], current_key[i]

        if current_score > global_best_score:
            global_best_score = current_score
            global_best_key = "".join(current_key)

    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    final_decrypted = decrypt_with_key(clean_c, global_best_key)

    # Build mapping: Ciphertext char -> Guessed Plaintext char
    # Standard: Plain 'A' -> key[0], so key[i] is Cipher char for Plain STANDARD_ALPHABET[i]
    mapping = {global_best_key[i]: STANDARD_ALPHABET[i] for i in range(26)}

    return {
        "best_key": global_best_key,
        "decrypted_text": final_decrypted,
        "mapping": mapping,
        "fitness_score": round(global_best_score, 2),
        "language": language.upper(),
        "execution_time_ms": elapsed_ms,
        "iterations": max_iterations
    }

def apply_interactive_mapping(ciphertext: str, mapping: Dict[str, str]) -> Dict[str, Any]:
    """Applies a user-specified partial or full mapping from ciphertext letters to plaintext letters.
    Unmapped letters remain unmapped or lowercase.
    """
    clean_c = sanitize_text(ciphertext)
    result_chars: List[str] = []
    mapped_count = 0

    for ch in clean_c:
        if ch in mapping and mapping[ch]:
            result_chars.append(mapping[ch].upper())
            mapped_count += 1
        else:
            result_chars.append(ch.lower())

    return {
        "preview_text": "".join(result_chars),
        "total_letters": len(clean_c),
        "mapped_letters_count": mapped_count,
        "mapping": mapping
    }
