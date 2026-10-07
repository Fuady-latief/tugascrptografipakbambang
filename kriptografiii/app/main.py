from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
import os
import math
import json

from .crypto import shift, substitution, affine, vigenere, hill, permutation, otp, utils, binary_ciphers
from .cryptanalysis import frequency, solver

app = FastAPI(
    title="Kriptografi & Kriptanalisis Web App",
    description="Implementasi 7 Cipher Klasik dan Kriptanalisis Abjad-Tunggal",
    version="1.0.0"
)

# ----------------- Models -----------------

class ShiftRequest(BaseModel):
    text: str
    key: int

class SubstitutionRequest(BaseModel):
    text: str
    key: str

class AffineRequest(BaseModel):
    text: str
    a: int
    b: int

class VigenereRequest(BaseModel):
    text: str
    key: str

class HillRequest(BaseModel):
    text: str
    matrix: List[List[int]]

class MatrixCheckRequest(BaseModel):
    matrix: List[List[int]]

class PermutationRequest(BaseModel):
    text: str
    key: Union[str, List[int]]

class OtpRequest(BaseModel):
    text: str
    key_text: str

class FrequencyAnalysisRequest(BaseModel):
    ciphertext: str
    language: str = "id"

class AutoCrackRequest(BaseModel):
    ciphertext: str
    language: str = "id"
    iterations: int = 1500

class InteractiveMappingRequest(BaseModel):
    ciphertext: str
    mapping: Dict[str, str]

class EgcdRequest(BaseModel):
    a: int
    m: int = 26

# ----------------- Exception Handler -----------------

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc)}
    )

# ----------------- Cipher Endpoints -----------------

@app.post("/api/cipher/shift/encrypt")
def shift_encrypt(req: ShiftRequest):
    res = shift.encrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/shift/decrypt")
def shift_decrypt(req: ShiftRequest):
    res = shift.decrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/substitution/encrypt")
def substitution_encrypt(req: SubstitutionRequest):
    res = substitution.encrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/substitution/decrypt")
def substitution_decrypt(req: SubstitutionRequest):
    res = substitution.decrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/affine/encrypt")
def affine_encrypt(req: AffineRequest):
    res = affine.encrypt(req.text, req.a, req.b)
    return {"success": True, "data": res}

@app.post("/api/cipher/affine/decrypt")
def affine_decrypt(req: AffineRequest):
    res = affine.decrypt(req.text, req.a, req.b)
    return {"success": True, "data": res}

@app.post("/api/cipher/vigenere/encrypt")
def vigenere_encrypt(req: VigenereRequest):
    res = vigenere.encrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/vigenere/decrypt")
def vigenere_decrypt(req: VigenereRequest):
    res = vigenere.decrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/hill/validate")
def hill_validate(req: MatrixCheckRequest):
    res = hill.validate_matrix(req.matrix)
    return {"success": True, "data": res}

@app.post("/api/cipher/hill/encrypt")
def hill_encrypt(req: HillRequest):
    res = hill.encrypt(req.text, req.matrix)
    return {"success": True, "data": res}

@app.post("/api/cipher/hill/decrypt")
def hill_decrypt(req: HillRequest):
    res = hill.decrypt(req.text, req.matrix)
    return {"success": True, "data": res}

@app.post("/api/cipher/permutation/encrypt")
def permutation_encrypt(req: PermutationRequest):
    res = permutation.encrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/permutation/decrypt")
def permutation_decrypt(req: PermutationRequest):
    res = permutation.decrypt(req.text, req.key)
    return {"success": True, "data": res}

@app.post("/api/cipher/otp/encrypt")
def otp_encrypt(req: OtpRequest):
    res = otp.encrypt(req.text, req.key_text)
    return {"success": True, "data": res}

@app.post("/api/cipher/otp/decrypt")
def otp_decrypt(req: OtpRequest):
    res = otp.decrypt(req.text, req.key_text)
    return {"success": True, "data": res}

@app.get("/api/cipher/otp/generate-key")
def otp_generate(length: int = 1000):
    k = otp.generate_random_key(max(10, min(length, 100000)))
    return {"success": True, "key": k, "length": len(k)}

# ----------------- Arbitrary File / Binary Cipher Endpoints -----------------

@app.post("/api/file-cipher/inspect")
async def file_cipher_inspect(file: UploadFile = File(...)):
    content = await file.read()
    sha256 = binary_ciphers.sha256_hash(content)
    return {
        "success": True,
        "filename": file.filename,
        "size": len(content),
        "sha256": sha256
    }

@app.post("/api/file-cipher/process")
async def file_cipher_process(
    file: UploadFile = File(...),
    cipher: str = Form(...),
    action: str = Form(...),
    key: Optional[str] = Form(None),
    key_a: Optional[int] = Form(None),
    key_b: Optional[int] = Form(None),
    otp_file: Optional[UploadFile] = File(None),
    otp_mode: Optional[str] = Form("xor")
):
    content = await file.read()
    orig_sha256 = binary_ciphers.sha256_hash(content)
    orig_filename = file.filename or "file.bin"

    if action not in ("encrypt", "decrypt"):
        raise ValueError("Aksi harus berupa 'encrypt' atau 'decrypt'.")

    if cipher == "shift":
        k_val = int(key or 3)
        if action == "encrypt":
            processed = binary_ciphers.encrypt_shift_bytes(content, k_val)
        else:
            processed = binary_ciphers.decrypt_shift_bytes(content, k_val)

    elif cipher == "substitution":
        sub_key = key or "DEFAULT_SUBSTITUTION_KEY"
        if action == "encrypt":
            processed = binary_ciphers.encrypt_substitution_bytes(content, sub_key)
        else:
            processed = binary_ciphers.decrypt_substitution_bytes(content, sub_key)

    elif cipher == "affine":
        a_val = int(key_a if key_a is not None else 15)
        b_val = int(key_b if key_b is not None else 10)
        if action == "encrypt":
            processed = binary_ciphers.encrypt_affine_bytes(content, a_val, b_val)
        else:
            processed = binary_ciphers.decrypt_affine_bytes(content, a_val, b_val)

    elif cipher == "vigenere":
        v_key = key or "LEMON"
        if action == "encrypt":
            processed = binary_ciphers.encrypt_vigenere_bytes(content, v_key)
        else:
            processed = binary_ciphers.decrypt_vigenere_bytes(content, v_key)

    elif cipher == "hill":
        if key:
            try:
                matrix = json.loads(key)
            except Exception:
                matrix = [[3, 2], [5, 7]]
        else:
            matrix = [[3, 2], [5, 7]]
        if action == "encrypt":
            processed = binary_ciphers.encrypt_hill_bytes(content, matrix)
        else:
            processed = binary_ciphers.decrypt_hill_bytes(content, matrix)

    elif cipher == "permutation":
        p_key = key or "3, 1, 4, 2"
        if action == "encrypt":
            processed = binary_ciphers.encrypt_permutation_bytes(content, p_key)
        else:
            processed = binary_ciphers.decrypt_permutation_bytes(content, p_key)

    elif cipher == "otp":
        if not otp_file:
            raise ValueError("File key One-Time Pad harus diunggah untuk enkripsi/dekripsi file.")
        key_bytes = await otp_file.read()
        mode_val = otp_mode or "xor"
        if action == "encrypt":
            processed, _ = binary_ciphers.encrypt_otp_bytes(content, key_bytes, mode=mode_val)
        else:
            processed, _ = binary_ciphers.decrypt_otp_bytes(content, key_bytes, mode=mode_val)

    else:
        raise ValueError(f"Algoritma cipher '{cipher}' tidak dikenali.")

    proc_sha256 = binary_ciphers.sha256_hash(processed)

    if action == "encrypt":
        out_filename = f"{orig_filename}.enc"
    else:
        if orig_filename.endswith(".enc"):
            out_filename = orig_filename[:-4]
        else:
            base, ext = os.path.splitext(orig_filename)
            out_filename = f"{base}_decrypted{ext}"

    headers = {
        "Content-Disposition": f'attachment; filename="{out_filename}"',
        "X-Original-Filename": orig_filename,
        "X-Output-Filename": out_filename,
        "X-Original-SHA256": orig_sha256,
        "X-Processed-SHA256": proc_sha256,
        "X-Original-Size": str(len(content)),
        "X-Processed-Size": str(len(processed)),
        "Access-Control-Expose-Headers": "X-Original-Filename, X-Output-Filename, X-Original-SHA256, X-Processed-SHA256, X-Original-Size, X-Processed-Size"
    }

    return Response(
        content=processed,
        media_type="application/octet-stream",
        headers=headers
    )

@app.get("/api/file-cipher/otp-generate-key")
def file_otp_generate_key(size: int = 65536):
    key_bytes = binary_ciphers.generate_random_bytes(max(16, min(size, 10000000)))
    headers = {
        "Content-Disposition": f'attachment; filename="otp_key_{len(key_bytes)}_bytes.bin"'
    }
    return Response(
        content=key_bytes,
        media_type="application/octet-stream",
        headers=headers
    )

# ----------------- Cryptanalysis Endpoints -----------------

@app.post("/api/cryptanalysis/frequency")
def cryptanalysis_frequency(req: FrequencyAnalysisRequest):
    res = frequency.analyze_frequency(req.ciphertext, req.language)
    return {"success": True, "data": res}

@app.post("/api/cryptanalysis/auto-crack")
def cryptanalysis_auto_crack(req: AutoCrackRequest):
    res = solver.auto_crack_substitution(req.ciphertext, req.language, req.iterations)
    return {"success": True, "data": res}

@app.post("/api/cryptanalysis/interactive-preview")
def cryptanalysis_interactive(req: InteractiveMappingRequest):
    res = solver.apply_interactive_mapping(req.ciphertext, req.mapping)
    return {"success": True, "data": res}

# ----------------- Math Helpers -----------------

@app.post("/api/math/egcd")
def math_egcd(req: EgcdRequest):
    gcd_val, x, y = utils.egcd(req.a, req.m)
    inv = utils.mod_inverse(req.a, req.m)
    return {
        "success": True,
        "a": req.a,
        "m": req.m,
        "gcd": gcd_val,
        "x": x,
        "y": y,
        "inverse": inv,
        "coprime": gcd_val == 1
    }

# ----------------- Static Files & Frontend -----------------

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Kriptografi Backend running. Static files not yet found."}
