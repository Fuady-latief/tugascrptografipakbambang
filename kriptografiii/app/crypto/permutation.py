from typing import Dict, Any, List, Union
from .utils import sanitize_text

def parse_permutation_key(key: Union[str, List[int]]) -> List[int]:
    """Parse permutation key into 0-indexed list of integers.
    Supports comma/space separated numbers (1-indexed or 0-indexed) or a word key.
    """
    if isinstance(key, list):
        nums = [int(x) for x in key]
    elif isinstance(key, str):
        # Check if comma or space separated numbers
        cleaned = key.strip()
        parts = cleaned.replace(",", " ").split()
        if parts and all(p.isdigit() for p in parts):
            nums = [int(p) for p in parts]
        elif cleaned.isdigit():
            # e.g. "3142"
            nums = [int(ch) for ch in cleaned]
        elif cleaned.isalpha():
            # Derive permutation from keyword (e.g. ZEBRA -> ranking)
            word = cleaned.upper()
            sorted_chars = sorted(list(enumerate(word)), key=lambda x: (x[1], x[0]))
            ranks = [0] * len(word)
            for rank, (orig_idx, _) in enumerate(sorted_chars):
                ranks[orig_idx] = rank
            return ranks
        else:
            raise ValueError("Format key permutasi tidak valid. Masukkan angka (contoh: 3, 1, 4, 2) atau kata kunci.")
    else:
        raise ValueError("Key harus berupa list angka atau string.")

    m = len(nums)
    if m < 2:
        raise ValueError("Panjang blok permutasi minimal 2.")

    # Determine if 1-indexed (e.g. 1 to m) or 0-indexed (0 to m-1)
    if set(nums) == set(range(1, m + 1)):
        # 1-indexed, convert to 0-indexed
        return [x - 1 for x in nums]
    elif set(nums) == set(range(0, m)):
        return nums
    else:
        raise ValueError(
            f"Key permutasi tidak valid! Harus berisi tepat setiap bilangan dari 1 hingga {m} "
            f"(atau 0 hingga {m - 1}) tanpa duplikasi. Diterima: {nums}"
        )

def get_inverse_permutation(perm: List[int]) -> List[int]:
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return inv

def encrypt(plaintext: str, key: Union[str, List[int]]) -> Dict[str, Any]:
    perm = parse_permutation_key(key)
    m = len(perm)
    clean_p = sanitize_text(plaintext)

    padding_count = (m - (len(clean_p) % m)) % m
    padded_p = clean_p + ("X" * padding_count if padding_count > 0 else "")

    ciphertext_blocks: List[str] = []
    block_steps: List[Dict[str, Any]] = []

    for i in range(0, len(padded_p), m):
        block = padded_p[i:i + m]
        # Apply permutation: cipher_block[j] = block[perm[j]]
        c_block = "".join([block[perm[j]] for j in range(m)])
        ciphertext_blocks.append(c_block)

        if len(block_steps) < 10:
            block_steps.append({
                "block_index": len(block_steps),
                "in_block": block,
                "out_block": c_block,
                "mapping": [f"{block[perm[j]]} (pos {perm[j]+1} -> {j+1})" for j in range(m)]
            })

    return {
        "ciphertext": "".join(ciphertext_blocks),
        "permutation_key_0indexed": perm,
        "permutation_key_1indexed": [p + 1 for p in perm],
        "block_size": m,
        "padding_added": padding_count,
        "padded_plaintext": padded_p,
        "block_steps": block_steps
    }

def decrypt(ciphertext: str, key: Union[str, List[int]]) -> Dict[str, Any]:
    perm = parse_permutation_key(key)
    inv_perm = get_inverse_permutation(perm)
    m = len(perm)
    clean_c = sanitize_text(ciphertext)

    if len(clean_c) % m != 0:
        raise ValueError(f"Panjang ciphertext ({len(clean_c)}) harus kelipatan ukuran blok ({m}).")

    plaintext_blocks: List[str] = []
    block_steps: List[Dict[str, Any]] = []

    for i in range(0, len(clean_c), m):
        block = clean_c[i:i + m]
        p_block = "".join([block[inv_perm[j]] for j in range(m)])
        plaintext_blocks.append(p_block)

        if len(block_steps) < 10:
            block_steps.append({
                "block_index": len(block_steps),
                "in_block": block,
                "out_block": p_block,
                "mapping": [f"{block[inv_perm[j]]} (pos {inv_perm[j]+1} -> {j+1})" for j in range(m)]
            })

    return {
        "plaintext": "".join(plaintext_blocks),
        "permutation_key_1indexed": [p + 1 for p in perm],
        "inverse_permutation_1indexed": [p + 1 for p in inv_perm],
        "block_size": m,
        "block_steps": block_steps
    }
