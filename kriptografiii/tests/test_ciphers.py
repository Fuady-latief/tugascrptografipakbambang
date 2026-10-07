import unittest
from app.crypto import shift, substitution, affine, vigenere, hill, permutation, otp, utils
from app.cryptanalysis import frequency, solver

class TestCryptoAlgorithms(unittest.TestCase):

    def test_shift_cipher(self):
        pt = "HELLO WORLD"
        k = 3
        enc = shift.encrypt(pt, k)
        self.assertEqual(enc["ciphertext"], "KHOORZRUOG")
        dec = shift.decrypt(enc["ciphertext"], k)
        self.assertEqual(dec["plaintext"], "HELLOWORLD")

    def test_substitution_cipher(self):
        pt = "DEFEND THE EAST WALL"
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        enc = substitution.encrypt(pt, key)
        dec = substitution.decrypt(enc["ciphertext"], key)
        self.assertEqual(dec["plaintext"], "DEFENDTHEEASTWALL")

        # Test duplicate key error
        with self.assertRaises(ValueError):
            substitution.encrypt("TEST", "QQERTYUIOPASDFGHJKLZXCVBNM")

        # Test wrong length key
        with self.assertRaises(ValueError):
            substitution.encrypt("TEST", "ABC")

    def test_affine_cipher(self):
        pt = "AFFINE CIPHER"
        a, b = 5, 8
        enc = affine.encrypt(pt, a, b)
        self.assertEqual(enc["a_inv"], 21)
        dec = affine.decrypt(enc["ciphertext"], a, b)
        self.assertEqual(dec["plaintext"], "AFFINECIPHER")

        # Test non-coprime 'a'
        with self.assertRaises(ValueError):
            affine.encrypt("TEST", 4, 7)

    def test_vigenere_cipher(self):
        pt = "ATTACK AT DAWN 123 !?"
        key = "LEMON"
        enc = vigenere.encrypt(pt, key)
        self.assertEqual(enc["ciphertext"], "LXFOPVEFRNHR")
        dec = vigenere.decrypt(enc["ciphertext"], key)
        self.assertEqual(dec["plaintext"], "ATTACKATDAWN")

    def test_hill_cipher_2x2(self):
        pt = "HELP"
        matrix = [[3, 3], [2, 5]]
        enc = hill.encrypt(pt, matrix)
        dec = hill.decrypt(enc["ciphertext"], matrix)
        self.assertEqual(dec["plaintext"], "HELP")

    def test_hill_cipher_padding(self):
        pt = "HEL"
        matrix = [[3, 3], [2, 5]]
        enc = hill.encrypt(pt, matrix)
        self.assertEqual(enc["padding_added"], 1)
        dec = hill.decrypt(enc["ciphertext"], matrix)
        self.assertEqual(dec["plaintext"], "HELX")

    def test_hill_cipher_3x3(self):
        pt = "ACT"
        matrix = [
            [6, 24, 1],
            [13, 16, 10],
            [20, 17, 15]
        ]
        val = hill.validate_matrix(matrix)
        self.assertEqual(val["size"], 3)
        enc = hill.encrypt(pt, matrix)
        dec = hill.decrypt(enc["ciphertext"], matrix)
        self.assertEqual(dec["plaintext"], "ACT")

    def test_permutation_cipher(self):
        pt = "CRYPTOGRAPHY"
        key = [3, 1, 4, 2]
        enc = permutation.encrypt(pt, key)
        dec = permutation.decrypt(enc["ciphertext"], key)
        self.assertEqual(dec["plaintext"], "CRYPTOGRAPHY")

    def test_otp(self):
        pt = "CONFIDENTIAL MESSAGE"
        key = otp.generate_random_key(100)
        enc = otp.encrypt(pt, key)
        dec = otp.decrypt(enc["ciphertext"], key)
        self.assertEqual(dec["plaintext"], "CONFIDENTIALMESSAGE")

        # Test too short key
        with self.assertRaises(ValueError):
            otp.encrypt("LONG MESSAGE", "SHORT")

    def test_cryptanalysis_frequency(self):
        # Generate some ciphertext using substitution
        pt = "RAHASIA NEGARA SANGAT PENTING UNTUK DIJAGA DENGAN SEGENAP JIWA DAN RAGA"
        key = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        enc = substitution.encrypt(pt, key)
        analysis = frequency.analyze_frequency(enc["ciphertext"], language="id")
        self.assertGreater(analysis["total_chars"], 0)
        self.assertIn("unigrams", analysis)
        self.assertIn("ioc", analysis)
        self.assertGreater(len(analysis["sorted_unigrams"]), 0)

if __name__ == "__main__":
    unittest.main()
