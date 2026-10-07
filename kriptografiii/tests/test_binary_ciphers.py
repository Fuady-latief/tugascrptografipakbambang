import unittest
import os
from app.crypto import binary_ciphers

class TestBinaryCiphers(unittest.TestCase):

    def setUp(self):
        # 1024 bytes of random binary data
        self.sample_binary = os.urandom(1024)
        self.sample_png_fake = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00\x08\x06\x00\x00\x00" + os.urandom(500)
        self.sample_text_bytes = "Halo Dunia! Ini adalah uji coba file sembarang dengan simbol @#$%^&*() 12345 dan karakter khusus.".encode('utf-8')

    def test_binary_shift(self):
        key = 137
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_shift_bytes(data, key)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_shift_bytes(enc, key)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

    def test_binary_substitution(self):
        key = "RAHASIA_SUPER_KUAT_2026"
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_substitution_bytes(data, key)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_substitution_bytes(enc, key)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

    def test_binary_affine(self):
        a = 15  # gcd(15, 256) == 1
        b = 73
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_affine_bytes(data, a, b)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_affine_bytes(enc, a, b)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

        # Test even 'a' must raise error
        with self.assertRaises(ValueError):
            binary_ciphers.encrypt_affine_bytes(self.sample_binary, 4, 10)

    def test_binary_vigenere(self):
        key = "KUNCI_VIGENERE_BINER"
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_vigenere_bytes(data, key)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_vigenere_bytes(enc, key)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

    def test_binary_hill_2x2(self):
        # det = 3*7 - 2*5 = 21 - 10 = 11 (odd, gcd(11, 256) = 1)
        matrix = [[3, 2], [5, 7]]
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_hill_bytes(data, matrix)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_hill_bytes(enc, matrix)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

    def test_binary_hill_3x3(self):
        # 3x3 matrix with odd determinant mod 256
        # Let's check a valid 3x3 matrix:
        # [1, 2, 0], [0, 1, 1], [1, 0, 1] -> det = 1*(1) - 2*(-1) = 3 (gcd(3, 256) == 1)
        matrix = [[1, 2, 0], [0, 1, 1], [1, 0, 1]]
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_hill_bytes(data, matrix)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_hill_bytes(enc, matrix)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

    def test_binary_permutation(self):
        key = [3, 1, 4, 2]
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            enc = binary_ciphers.encrypt_permutation_bytes(data, key)
            self.assertNotEqual(enc, data)
            dec = binary_ciphers.decrypt_permutation_bytes(enc, key)
            self.assertEqual(dec, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec), binary_ciphers.sha256_hash(data))

    def test_binary_otp(self):
        key = binary_ciphers.generate_random_bytes(2000)
        for data in [self.sample_binary, self.sample_png_fake, self.sample_text_bytes]:
            # Test XOR mode
            enc_xor, unused = binary_ciphers.encrypt_otp_bytes(data, key, mode="xor")
            self.assertNotEqual(enc_xor, data)
            dec_xor, _ = binary_ciphers.decrypt_otp_bytes(enc_xor, key, mode="xor")
            self.assertEqual(dec_xor, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec_xor), binary_ciphers.sha256_hash(data))

            # Test Add mod 256 mode
            enc_add, _ = binary_ciphers.encrypt_otp_bytes(data, key, mode="add")
            self.assertNotEqual(enc_add, data)
            dec_add, _ = binary_ciphers.decrypt_otp_bytes(enc_add, key, mode="add")
            self.assertEqual(dec_add, data)
            self.assertEqual(binary_ciphers.sha256_hash(dec_add), binary_ciphers.sha256_hash(data))

if __name__ == "__main__":
    unittest.main()
