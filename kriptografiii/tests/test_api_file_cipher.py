import urllib.request
import io
import os
import unittest
import json

class TestFileCipherAPI(unittest.TestCase):

    def test_file_cipher_api_reversibility(self):
        orig_data = b"%PDF-1.4 Fake PDF Header \x00\x01\x02\xff\xfe\xfd binary test data" + os.urandom(256)
        boundary = '----WebKitFormBoundaryTest7MA4YWxkTrZu0gW'

        # 1. Inspect endpoint
        body = io.BytesIO()
        body.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.pdf"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
        body.write(orig_data)
        body.write(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

        req = urllib.request.Request(
            'http://127.0.0.1:8000/api/file-cipher/inspect',
            data=body.getvalue(),
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
        )
        with urllib.request.urlopen(req) as resp:
            info = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(info['success'])
            self.assertEqual(info['size'], len(orig_data))
            orig_sha = info['sha256']

        # 2. Test all 7 ciphers through the API
        ciphers_to_test = [
            ("shift", {"key": "55"}),
            ("substitution", {"key": "MY_SECRET_KEY_123"}),
            ("affine", {"key_a": "15", "key_b": "77"}),
            ("vigenere", {"key": "POLYALPHABETIC_BINARY_KEY"}),
            ("hill", {"key": "[[3, 2], [5, 7]]"}),
            ("permutation", {"key": "3, 1, 4, 2"})
        ]

        for c_name, c_params in ciphers_to_test:
            # Encrypt
            body_enc = io.BytesIO()
            body_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="cipher"\r\n\r\n{c_name}\r\n'.encode('utf-8'))
            body_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\nencrypt\r\n'.encode('utf-8'))
            for pk, pv in c_params.items():
                body_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="{pk}"\r\n\r\n{pv}\r\n'.encode('utf-8'))
            body_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.pdf"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
            body_enc.write(orig_data)
            body_enc.write(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

            req_enc = urllib.request.Request(
                'http://127.0.0.1:8000/api/file-cipher/process',
                data=body_enc.getvalue(),
                headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
            )
            with urllib.request.urlopen(req_enc) as resp_enc:
                enc_data = resp_enc.read()
                self.assertNotEqual(enc_data, orig_data)

            # Decrypt
            body_dec = io.BytesIO()
            body_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="cipher"\r\n\r\n{c_name}\r\n'.encode('utf-8'))
            body_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\ndecrypt\r\n'.encode('utf-8'))
            for pk, pv in c_params.items():
                body_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="{pk}"\r\n\r\n{pv}\r\n'.encode('utf-8'))
            body_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.pdf.enc"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
            body_dec.write(enc_data)
            body_dec.write(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

            req_dec = urllib.request.Request(
                'http://127.0.0.1:8000/api/file-cipher/process',
                data=body_dec.getvalue(),
                headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
            )
            with urllib.request.urlopen(req_dec) as resp_dec:
                dec_data = resp_dec.read()
                dec_sha = resp_dec.headers.get('X-Processed-SHA256')
                self.assertEqual(dec_data, orig_data, f"Reversibility failed for {c_name}!")
                self.assertEqual(dec_sha, orig_sha, f"SHA256 mismatch for {c_name}!")

        # 3. Test OTP with binary key file upload
        otp_key_data = os.urandom(len(orig_data) + 128)
        body_otp_enc = io.BytesIO()
        body_otp_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="cipher"\r\n\r\notp\r\n'.encode('utf-8'))
        body_otp_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\nencrypt\r\n'.encode('utf-8'))
        body_otp_enc.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.pdf"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
        body_otp_enc.write(orig_data)
        body_otp_enc.write(f'\r\n--{boundary}\r\nContent-Disposition: form-data; name="otp_file"; filename="otp_key.bin"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
        body_otp_enc.write(otp_key_data)
        body_otp_enc.write(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

        req_otp = urllib.request.Request(
            'http://127.0.0.1:8000/api/file-cipher/process',
            data=body_otp_enc.getvalue(),
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
        )
        with urllib.request.urlopen(req_otp) as resp_otp:
            enc_otp_data = resp_otp.read()

        # Decrypt OTP
        body_otp_dec = io.BytesIO()
        body_otp_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="cipher"\r\n\r\notp\r\n'.encode('utf-8'))
        body_otp_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\ndecrypt\r\n'.encode('utf-8'))
        body_otp_dec.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.pdf.enc"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
        body_otp_dec.write(enc_otp_data)
        body_otp_dec.write(f'\r\n--{boundary}\r\nContent-Disposition: form-data; name="otp_file"; filename="otp_key.bin"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
        body_otp_dec.write(otp_key_data)
        body_otp_dec.write(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

        req_otp_dec = urllib.request.Request(
            'http://127.0.0.1:8000/api/file-cipher/process',
            data=body_otp_dec.getvalue(),
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
        )
        with urllib.request.urlopen(req_otp_dec) as resp_otp_dec:
            dec_otp_data = resp_otp_dec.read()
            self.assertEqual(dec_otp_data, orig_data, "Reversibility failed for OTP!")

if __name__ == '__main__':
    unittest.main()
