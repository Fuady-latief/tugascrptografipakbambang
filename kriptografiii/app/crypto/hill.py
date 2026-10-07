import math
from typing import Dict, Any, List, Union
from .utils import letter_to_num, num_to_letter, sanitize_text, mod_inverse

MatrixType = List[List[int]]

def matrix_det_2x2(m: MatrixType) -> int:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]

def matrix_adj_2x2(m: MatrixType) -> MatrixType:
    return [
        [m[1][1] % 26, (-m[0][1]) % 26],
        [(-m[1][0]) % 26, m[0][0] % 26]
    ]

def matrix_det_3x3(m: MatrixType) -> int:
    a, b, c = m[0][0], m[0][1], m[0][2]
    d, e, f = m[1][0], m[1][1], m[1][2]
    g, h, i = m[2][0], m[2][1], m[2][2]
    det = (a * (e * i - f * h) -
           b * (d * i - f * g) +
           c * (d * h - e * g))
    return det

def matrix_adj_3x3(m: MatrixType) -> MatrixType:
    a, b, c = m[0][0], m[0][1], m[0][2]
    d, e, f = m[1][0], m[1][1], m[1][2]
    g, h, i = m[2][0], m[2][1], m[2][2]

    # Cofactors
    c00 = (e * i - f * h)
    c01 = -(d * i - f * g)
    c02 = (d * h - e * g)

    c10 = -(b * i - c * h)
    c11 = (a * i - c * g)
    c12 = -(a * h - b * g)

    c20 = (b * f - c * e)
    c21 = -(a * f - c * d)
    c22 = (a * e - b * d)

    # Adjugate is the transpose of the cofactor matrix
    adj = [
        [c00 % 26, c10 % 26, c20 % 26],
        [c01 % 26, c11 % 26, c21 % 26],
        [c02 % 26, c12 % 26, c22 % 26]
    ]
    return adj

def validate_matrix(matrix: MatrixType) -> Dict[str, Any]:
    n = len(matrix)
    if n not in (2, 3):
        raise ValueError("Hill Cipher saat ini mendukung matriks berukuran 2x2 atau 3x3.")
    for row in matrix:
        if len(row) != n:
            raise ValueError(f"Setiap baris matriks harus memiliki panjang {n} kolom.")

    # Compute determinant
    if n == 2:
        raw_det = matrix_det_2x2(matrix)
        adj = matrix_adj_2x2(matrix)
    else:
        raw_det = matrix_det_3x3(matrix)
        adj = matrix_adj_3x3(matrix)

    det_mod = raw_det % 26
    gcd_val = math.gcd(det_mod, 26)

    if gcd_val != 1:
        raise ValueError(
            f"Matriks tidak dapat diinvers modulo 26! "
            f"det(K) = {raw_det} = {det_mod} (mod 26), dan gcd({det_mod}, 26) = {gcd_val} != 1."
        )

    det_inv = mod_inverse(det_mod, 26)
    if det_inv is None:
        raise ValueError(f"Invers determinan {det_mod} mod 26 tidak ditemukan.")

    # Compute inverse matrix mod 26: det_inv * adj(K) mod 26
    inv_matrix: MatrixType = [
        [(det_inv * adj[r][c]) % 26 for c in range(n)]
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

def encrypt(plaintext: str, matrix: MatrixType) -> Dict[str, Any]:
    analysis = validate_matrix(matrix)
    n = analysis["size"]
    clean_p = sanitize_text(plaintext)

    # Padding with 'X' if length not multiple of n
    padded_p = clean_p
    padding_count = (n - (len(clean_p) % n)) % n
    if padding_count > 0:
        padded_p += "X" * padding_count

    ciphertext_chars: List[str] = []
    block_steps: List[Dict[str, Any]] = []

    for idx in range(0, len(padded_p), n):
        block = padded_p[idx:idx + n]
        vec = [letter_to_num(ch) for ch in block]
        # Row-vector multiplication: C = P * K mod 26
        out_vec = [
            sum(vec[r] * matrix[r][c] for r in range(n)) % 26
            for c in range(n)
        ]
        out_block = "".join([num_to_letter(v) for v in out_vec])
        ciphertext_chars.append(out_block)

        if len(block_steps) < 10:
            block_steps.append({
                "block_index": len(block_steps),
                "in_block": block,
                "in_vector": vec,
                "out_vector": out_vec,
                "out_block": out_block
            })

    return {
        "ciphertext": "".join(ciphertext_chars),
        "matrix": matrix,
        "matrix_size": n,
        "analysis": analysis,
        "padding_added": padding_count,
        "padded_plaintext": padded_p,
        "block_steps": block_steps
    }

def decrypt(ciphertext: str, matrix: MatrixType) -> Dict[str, Any]:
    analysis = validate_matrix(matrix)
    n = analysis["size"]
    inv_k = analysis["inverse_matrix"]
    clean_c = sanitize_text(ciphertext)

    if len(clean_c) % n != 0:
        raise ValueError(f"Panjang ciphertext ({len(clean_c)}) harus kelipatan ukuran matriks ({n}).")

    plaintext_chars: List[str] = []
    block_steps: List[Dict[str, Any]] = []

    for idx in range(0, len(clean_c), n):
        block = clean_c[idx:idx + n]
        vec = [letter_to_num(ch) for ch in block]
        # P = C * K^-1 mod 26
        out_vec = [
            sum(vec[r] * inv_k[r][c] for r in range(n)) % 26
            for c in range(n)
        ]
        out_block = "".join([num_to_letter(v) for v in out_vec])
        plaintext_chars.append(out_block)

        if len(block_steps) < 10:
            block_steps.append({
                "block_index": len(block_steps),
                "in_block": block,
                "in_vector": vec,
                "out_vector": out_vec,
                "out_block": out_block
            })

    return {
        "plaintext": "".join(plaintext_chars),
        "matrix": matrix,
        "inverse_matrix": inv_k,
        "analysis": analysis,
        "block_steps": block_steps
    }
