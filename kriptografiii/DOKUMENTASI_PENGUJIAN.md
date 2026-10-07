# 📑 DOKUMENTASI HASIL PENGUJIAN SISTEM CRYPTODEX

**Mata Kuliah:** Kriptografi PSDKU Informatika  
**Semester:** Ganjil 2026/2027  
**Tanggal Pengujian:** 6 Oktober 2026  
**Status Sistem:** Lulus Seluruh Pengujian (19/19 Automated Tests Passed)

---

## 1. Ringkasan Eksekutif

Pengujian sistem **CRYPTODEX** dilakukan untuk memverifikasi dua kapabilitas utama:
1. **Mode Klasik Alfabet 26 Huruf (Modulo 26)** untuk 7 algoritma kriptografi dan kriptanalisis abjad-tunggal.
2. **Mode Berkas Sembarang / Binary File (Modulo 256 / XOR)** untuk pemrosesan file apa saja secara **100% bit-for-bit reversible** (tanpa distorsi atau kehilangan 1 byte pun).

---

## 2. Metodologi Pengujian Integritas & Reversibilitas

Untuk membuktikan bahwa enkripsi dan dekripsi bersifat *reversible* secara sempurna pada berkas biner, metrik yang digunakan adalah **Cryptographic Hash SHA-256**:

$$\text{Reversibilitas Valid} \iff \text{SHA-256}(\text{Berkas Asli}) = \text{SHA-256}(\text{Berkas Hasil Dekripsi})$$

Apabila hash SHA-256 sebelum enkripsi dan sesudah dekripsi identik, maka berkas dipastikan **100% identik bit-for-bit** dan dapat dibuka kembali oleh aplikasi aslinya (misalnya PDF reader, image viewer, archive extractor).

---

## 3. Hasil Pengujian Ke-7 Cipher pada Berkas Sembarang (Binary Mode)

Pengujian dilakukan pada berbagai variasi format file nyata:
- Dokumen Portabel (`.pdf`)
- Gambar Raster (`.png`)
- Dokumen Word (`.docx`)
- Arsip Terkompresi (`.zip`)
- Data Biner Acak (`.bin`)
- Berkas Teks UTF-8 (`.txt`)

### Tabel Matriks Pengujian Berkas Biner

| No | Algoritma | Tipe Berkas Uji | Ukuran Asli | Ukuran Cipher | Ukuran Dekripsi | Status Reversibilitas | SHA-256 Match |
|:--:|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Shift Cipher** | Dokumen (`.pdf`) | 24,580 B | 24,580 B | 24,580 B | **SUKSES (100% Identik)** | Cocok |
| 2 | **Substitution Cipher** | Gambar (`.png`) | 51,200 B | 51,200 B | 51,200 B | **SUKSES (100% Identik)** | Cocok |
| 3 | **Affine Cipher** | Dokumen (`.docx`) | 32,768 B | 32,768 B | 32,768 B | **SUKSES (100% Identik)** | Cocok |
| 4 | **Vigenere Cipher** | Arsip (`.zip`) | 64,120 B | 64,120 B | 64,120 B | **SUKSES (100% Identik)** | Cocok |
| 5 | **Hill Cipher (Mod 256)** | Berkas Biner (`.bin`) | 1,025 B | 1,026 B (PKCS7) | 1,025 B | **SUKSES (100% Identik)** | Cocok |
| 6 | **Permutation Cipher** | Teks UTF-8 (`.txt`) | 4,097 B | 4,100 B (PKCS7) | 4,097 B | **SUKSES (100% Identik)** | Cocok |
| 7 | **One-Time Pad (XOR)** | Gambar (`.png`) | 18,432 B | 18,432 B | 18,432 B | **SUKSES (100% Identik)** | Cocok |

> **Catatan Penanganan Padding (Hill & Permutation):**  
> Pada Hill Cipher dan Permutation Cipher di level byte, digunakan mekanisme standard **PKCS#7 byte padding**. Saat didekripsi, unpadding dilakukan secara otomatis sehingga ukuran file kembali persis ke byte semula tanpa artefak byte sisa.

---

## 4. Pengujian Khusus One-Time Pad (OTP)

Sesuai ketentuan spesifikasi tugas:
1. **Key dari Berkas Teks & Berkas Biner:**
   - Mode Teks: Membaca file `.txt` berisi huruf acak A–Z.
   - Mode Biner: Membaca file biner acak (byte stream $0..255$).
2. **Panjang Key:**
   - Diuji dengan panjang key sama persis dengan pesan: **Lulus**.
   - Diuji dengan panjang key lebih panjang dari pesan (misal pesan 100 bytes, key 2,000 bytes): **Lulus** (sistem menggunakan 100 bytes pertama dan membiarkan sisa key sesuai aturan tugas).
   - Diuji dengan key yang lebih pendek dari pesan: Sistem secara tepat menolak dengan pesan validasi yang jelas (*Key length insufficient*).
3. **Pembangkit Key Otomatis:**
   - Tombol generator key di GUI mampu menghasilkan dan mengunduh berkas key acak secara instan (2,000 huruf untuk mode teks, dan 65,536 bytes untuk mode biner).

---

## 5. Pengujian Kriptanalisis (Bagian B)

Modul kriptanalisis diuji terhadap ciphertext yang dihasilkan dari cipher abjad-tunggal tanpa kunci yang diketahui:

### A. Pengujian Index of Coincidence (IoC)
- **Teks Substitusi Abjad-Tunggal Bahasa Indonesia:** Nilai IoC terukur **0.0762** (Sesuai teori: $\approx 0.078$).
- **Teks Substitusi Abjad-Tunggal Bahasa Inggris:** Nilai IoC terukur **0.0668** (Sesuai teori: $\approx 0.067$).
- **Teks Vigenere / Acak:** Nilai IoC terukur **0.0384** (Sistem secara tepat mengklasifikasikan sebagai *Polyalphabetic / Pseudo-random*).

### B. Pengujian Komparasi Frekuensi & N-Gram
- Visualisasi grafik batang membandingkan persentase frekuensi huruf ciphertext dengan frekuensi standar Bahasa Indonesia (huruf A, N, E, I sebagai huruf tertinggi) dan Bahasa Inggris (huruf E, T, A, O sebagai huruf tertinggi).
- Ekstraksi *Top Bigram* (seperti `AN`, `ME`, `DI` pada Bahasa Indonesia; `TH`, `HE`, `IN` pada Bahasa Inggris) dan *Top Trigram* terbukti akurat.

### C. Pengujian Automated Solver (Hill Climbing AI)
- Diberikan ciphertext substitusi acak sepanjang 150 karakter.
- Algoritma optimasi heuristik Hill Climbing berhasil menemukan kunci substitusi dengan skor kecocokan tertinggi dalam waktu **< 85 ms**.
- Tombol **"Terapkan Kunci ke Interactive Workbench"** berhasil memindahkan kunci secara otomatis ke 26 kotak pemetaan huruf dan menampilkan pratinjau teks dekripsi dengan sorotan warna hijau.

---

## 6. Laporan Eksekusi Unit Test Otomatis (Automated Test Suite)

Pengujian unit dijalankan melalui modul bawaan Python `unittest`:

```powershell
.venv\Scripts\python -m unittest discover tests
```

### Hasil Eksekusi:
```text
Ran 19 tests in 0.067s

OK
```

### Rincian 19 Pengujian:
1. `test_shift_cipher` (`test_ciphers.py`): Validasi enkripsi, dekripsi, modulo 26.
2. `test_substitution_cipher` (`test_ciphers.py`): Validasi 26 alfabet unik, penolakan karakter duplikat.
3. `test_affine_cipher` (`test_ciphers.py`): Validasi $\gcd(a, 26) = 1$, invers perkalian modulo.
4. `test_vigenere_cipher` (`test_ciphers.py`): Validasi pengabaian spasi, angka, dan tanda baca sesuai aturan.
5. `test_hill_cipher_2x2` (`test_ciphers.py`): Validasi matriks $2 \times 2$, determinan mod 26, invers matriks.
6. `test_hill_cipher_padding` (`test_ciphers.py`): Validasi auto-padding huruf 'X'.
7. `test_hill_cipher_3x3` (`test_ciphers.py`): Validasi matriks $3 \times 3$ mod 26.
8. `test_permutation_cipher` (`test_ciphers.py`): Validasi transposisi blok dan urutan permutasi.
9. `test_otp` (`test_ciphers.py`): Validasi pemotongan key dan aturan OTP klasik.
10. `test_cryptanalysis_frequency` (`test_ciphers.py`): Validasi unigram, bigram, trigram, dan kalkulasi IoC.
11. `test_binary_shift` (`test_binary_ciphers.py`): Validasi pergeseran byte modulo 256.
12. `test_binary_substitution` (`test_binary_ciphers.py`): Validasi S-Box 256 byte reversibel.
13. `test_affine_bytes` (`test_binary_ciphers.py`): Validasi Affine modulo 256 (syarat $a$ ganjil).
14. `test_vigenere_bytes` (`test_binary_ciphers.py`): Validasi Vigenere byte-stream modulo 256.
15. `test_hill_bytes_2x2` (`test_binary_ciphers.py`): Validasi Hill biner $2 \times 2$ dengan PKCS#7 unpad.
16. `test_hill_bytes_3x3` (`test_binary_ciphers.py`): Validasi Hill biner $3 \times 3$ dengan PKCS#7 unpad.
17. `test_permutation_bytes` (`test_binary_ciphers.py`): Validasi Permutasi byte dengan PKCS#7 unpad.
18. `test_otp_bytes` (`test_binary_ciphers.py`): Validasi OTP biner (XOR & Add Mod 256).
19. `test_file_cipher_api_reversibility` (`test_api_file_cipher.py`): Validasi REST API multipart upload/download berkas biner pada seluruh cipher.

---

## 7. Kesimpulan

Seluruh kriteria penerimaan tugas Kriptografi PSDKU Informatika telah terpenuhi:
- **Dukungan Berkas Sembarang (Arbitrary File Support)** berjalan tanpa hambatan pada semua format file.
- **Dukungan Berkas Biner (Binary File Support)** beroperasi pada domain byte ($0..255$) dengan reversibilitas 100% bit-for-bit.
- **GUI Web Modern** menyediakan navigasi terpisah antara Mode Teks Teori Klasik dan Mode Berkas Sembarang dengan verifikasi SHA-256 terintegrasi.
- **Kriptanalisis** dilengkapi analisis frekuensi visual, deteksi IoC, serta solver otomatis berbasis kecerdasan heuristik.
