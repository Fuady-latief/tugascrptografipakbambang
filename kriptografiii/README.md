# 🔐 CRYPTODEX — Implementasi Kriptosistem & Kriptanalisis Web App

Project Tugas Besar Mata Kuliah **Kriptografi PSDKU Informatika**  
Semester Ganjil 2026/2027.

---

## 👥 Anggota Kelompok (4 Orang)

| No | Nama Mahasiswa | NIM | Peran & Tanggung Jawab |
|:--:|:---|:---:|:---|
| 1 | **[Nama Anggota 1]** | `2308561001` | Lead Developer, Arsitektur REST API & Bagian A (Cipher 1–4) |
| 2 | **[Nama Anggota 2]** | `2308561002` | Bagian A (Hill Cipher, Permutation Cipher & Aljabar Matriks Modulo 26) |
| 3 | **[Nama Anggota 3]** | `2308561003` | Bagian A (One-Time Pad, File I/O Handling, UI/UX Layout) |
| 4 | **[Nama Anggota 4]** | `2308561004` | Bagian B (Kriptanalisis Frekuensi, IoC, N-gram & Hill Climbing Solver) |

*(Nama dan NIM dapat disesuaikan langsung di web GUI pada tab **Kelompok & Info** dan akan tersimpan secara otomatis).*

---

## 🚀 Fitur Utama Aplikasi

### 🅰️ Bagian A — 7 Kriptosistem Klasik (Alfabet 26 Huruf)
1. **Shift Cipher (Caesar)**:
   - Enkripsi: $C = (P + k) \pmod{26}$
   - Dekripsi: $P = (C - k) \pmod{26}$
   - Input key adaptif (Slider 0–25 & Numeric Input).
   - Penjelasan matematis per-karakter.
2. **Substitution Cipher (Monoalfabetik)**:
   - Validasi ketat: 26 karakter alfabet unik tanpa duplikasi.
   - Fitur **Acak / Randomize Key** instan.
3. **Affine Cipher**:
   - Enkripsi: $C = (a \cdot P + b) \pmod{26}$
   - Dekripsi: $P = a^{-1} \cdot (C - b) \pmod{26}$
   - Validasi otomatis syarat keterbalikan $\gcd(a, 26) = 1$.
   - Perhitungan invers perkalian modular $a^{-1} \pmod{26}$ dengan *Extended Euclidean Algorithm*.
4. **Vigenere Cipher**:
   - Enkripsi & Dekripsi polialfabetik dengan kata kunci.
   - Sesuai ketentuan tugas: **Angka, spasi, dan tanda baca diabaikan** dan tidak disimpan pada ciphertext.
5. **Hill Cipher**:
   - Mendukung matriks ukuran $2 \times 2$ dan $3 \times 3$.
   - Validasi determinan $\gcd(\det(K), 26) = 1$.
   - Invers matriks modular $K^{-1} = \det(K)^{-1} \cdot \text{adj}(K) \pmod{26}$.
   - Auto-padding huruf `'X'` jika panjang pesan bukan kelipatan ukuran matriks.
   - Tersedia tombol *Preset Matriks Valid*.
6. **Permutation Cipher (Transposisi Blok)**:
   - Mendukung urutan permutasi angka (misal `3, 1, 4, 2` atau `3142`) maupun kata kunci (*keyword rank*).
   - Validasi kelengkapan angka indeks blok.
7. **One-Time Pad (OTP)**:
   - Input teks langsung atau unggah file berkas key (`.txt`).
   - Fitur **Generate & Download File Key Acak** (2000 karakter).
   - Mengikuti panjang pesan, sisa karakter key dibiarkan sesuai spesifikasi tugas.

---

### 🅱️ Bagian B — Kriptanalisis Cipher Abjad-Tunggal
1. **Index of Coincidence (IoC)**:
   - Menghitung $IoC = \frac{\sum f_i(f_i - 1)}{N(N - 1)}$ untuk memverifikasi apakah ciphertext merupakan cipher abjad-tunggal ($IoC \approx 0.06 - 0.08$) atau polialfabetik/acak ($IoC \approx 0.038$).
2. **Visualisasi Distribusi Frekuensi Huruf**:
   - Grafik batang interaktif membandingkan persentase frekuensi huruf ciphertext vs frekuensi acuan bahasa secara berdampingan.
   - Mendukung dua bahasa acuan: **Bahasa Indonesia** dan **Bahasa Inggris**.
3. **Analisis N-Gram (Bigram & Trigram)**:
   - Tabel perbandingan kemunculan pasangan huruf (*Top Bigrams & Trigrams*) di ciphertext vs n-gram bahasa acuan.
4. **Interactive Substitution Workbench**:
   - 26 kotak pemetaan huruf ciphertext $\to$ tebakan plaintext.
   - Pratinjau teks dekripsi *real-time*: huruf yang sudah ditebak berwarna **hijau**, huruf yang belum ditebak berwarna abu-abu.
5. **Automated Heuristic Solver (Hill Climbing AI)**:
   - Mampu memecahkan ciphertext substitusi dengan kunci tidak diketahui secara otomatis dalam hitungan milidetik menggunakan optimasi heuristik pertukaran kunci dan penilaian plausibilitas n-gram.
   - Hasil tebakan kunci dapat langsung ditransfer ke Workbench dengan satu klik.

### 📁 Mode Berkas Sembarang / Binary File (Byte-Level Modulo 256 / XOR)
Mendukung enkripsi dan dekripsi berkas sembarang (gambar `.png`, dokumen `.pdf`, `.docx`, arsip `.zip`, biner `.bin`, teks `.txt`, dll) secara **100% bit-for-bit reversible**:
- **Shift Cipher (Byte-Level)**: $C = (B + k) \pmod{256}$
- **Substitution Cipher (Byte-Level)**: Permutasi S-Box 256 byte reversibel dari seed/password
- **Affine Cipher (Byte-Level)**: $C = (a \cdot B + b) \pmod{256}$ dengan syarat $a$ ganjil ($\gcd(a, 256) = 1$)
- **Vigenere Cipher (Byte-Level)**: $C_i = (B_i + K_{i \pmod{|K|}}) \pmod{256}$
- **Hill Cipher (Byte-Level)**: Matriks modular $2 \times 2$ mod 256 dengan PKCS#7 padding
- **Permutation Cipher (Byte-Level)**: Transposisi blok byte dengan PKCS#7 unpadding
- **One-Time Pad (Binary)**: Byte XOR $C_i = B_i \oplus K_i$ dan Modulo 256 dengan berkas key acak
- **Integritas Reversibilitas**: Verifikasi hash SHA-256 sebelum enkripsi dan sesudah dekripsi terjamin 100% identik.

---

### 🧮 Bagian Tambahan — Kalkulator Aljabar Kripto
- **Extended Euclidean Algorithm**: Menghitung Bezout equation $a \cdot x + m \cdot y = \gcd(a, m)$ dan $a^{-1} \pmod m$.
- **Modular Matrix Inverter**: Menghitung determinan, adjugate, dan invers matriks $2 \times 2$ & $3 \times 3$ pada modulo 26.

---

### 📑 Laporan Dokumentasi Pengujian Lengkap
Laporan pengujian detail matriks berkas biner, pengujian reversibilitas bit-for-bit, pengujian OTP, dan kriptanalisis tersedia di:
👉 **[DOKUMENTASI_PENGUJIAN.md](file:///d:/kriptografiii/DOKUMENTASI_PENGUJIAN.md)**

## 🛠️ Persyaratan Sistem & Instalasi

### 1. Prasyarat
- Python 3.10 atau lebih baru (Teruji pada Python 3.13)
- Web Browser modern (Chrome, Edge, Firefox, Safari)

### 2. Panduan Menjalankan Aplikasi

1. **Buka Terminal / PowerShell di direktori project**:
   ```powershell
   cd d:\kriptografiii
   ```

2. **Aktifkan Virtual Environment**:
   ```powershell
   # Di Windows (PowerShell):
   .venv\Scripts\Activate.ps1

   # Atau di Command Prompt:
   .venv\Scripts\activate.bat
   ```

3. **Install Dependensi (jika belum diinstal)**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Jalankan Web Server**:
   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

5. **Buka Aplikasi di Browser**:
   Buka URL berikut di browser Anda:
   👉 **`http://127.0.0.1:8000`** atau **`http://localhost:8000`**

6. **Akses Dokumentasi Interaktif API (Swagger UI)**:
   👉 **`http://127.0.0.1:8000/docs`**

---

## 🧪 Menjalankan Pengujian Otomatis (Unit Tests)

Untuk menjalankan seluruh unit test matematis dan algoritma:

```powershell
.venv\Scripts\python -m unittest tests/test_ciphers.py
```

Seluruh 10 unit test mencakup:
- Shift Cipher (enkripsi, dekripsi, modulo)
- Substitution Cipher (validasi 26 karakter unik, deteksi duplikasi)
- Affine Cipher (validasi nilai $a$ koprima, invers perkalian modulo)
- Vigenere Cipher (penghilangan spasi/angka/tanda baca sesuai aturan tugas)
- Hill Cipher $2 \times 2$ dan $3 \times 3$ (invers matriks mod 26, padding 'X')
- Permutation Cipher (permutasi blok angka & kata kunci)
- One-Time Pad (pembacaan file key, pemotongan key sesuai panjang pesan)
- Kriptanalisis Frekuensi & IoC

---

## 📁 Struktur Direktori Project

```text
d:\kriptografiii/
├── .venv/                         # Virtual environment Python
├── requirements.txt               # Daftar dependensi (FastAPI, Uvicorn, Pydantic)
├── README.md                      # Dokumentasi lengkap project
├── tests/
│   └── test_ciphers.py            # Unit test otomatis untuk 7 cipher & kriptanalisis
└── app/
    ├── __init__.py
    ├── main.py                    # Server FastAPI, routing REST API & static file server
    ├── crypto/                    # Modul 7 Kriptosistem
    │   ├── __init__.py
    │   ├── utils.py               # Extended Euclidean, mod_inverse, sanitasi huruf
    │   ├── shift.py               # 1. Shift Cipher
    │   ├── substitution.py        # 2. Substitution Cipher
    │   ├── affine.py              # 3. Affine Cipher
    │   ├── vigenere.py            # 4. Vigenere Cipher
    │   ├── hill.py                # 5. Hill Cipher (Matriks mod 26)
    │   ├── permutation.py         # 6. Permutation Cipher
    │   └── otp.py                 # 7. One-Time Pad
    ├── cryptanalysis/             # Modul Kriptanalisis Abjad-Tunggal
    │   ├── __init__.py
    │   ├── corpora.py             # Distribusi frekuensi huruf ID & EN, n-gram
    │   ├── frequency.py           # Kalkulasi unigram, bigram, trigram, IoC
    │   └── solver.py              # Hill Climbing Heuristic Solver & workbench
    └── static/                    # Frontend Modern Web GUI
        ├── index.html             # Antarmuka dashboard web
        ├── css/
        │   └── style.css          # Desain Cyber Slate Glassmorphism & Responsif
        └── js/
            ├── app.js             # Navigasi tab, upload file, copy, simpan tim
            ├── ciphers.js         # Input key dinamis, validasi & visualisasi langkah
            ├── cryptanalysis.js   # Chart frekuensi, IoC, workbench interaktif
            └── math_explorer.js   # Kalkulator EGCD & invers matriks mod 26
```
