# Copyright PA Knowledge Ltd 2021
import unittest
import pysisl
from pysisl import sisl_wrapper
from binascii import unhexlify


class SislWrapperTests(unittest.TestCase):
    def test_simple_unwrapping_with_key(self):
        wrapped_data = b"\xd1\xdf\x5f\xff\x00\x01\x00\x00\x00\x00\x00\x30\x00\x00\x00\x01" \
                       b"\x00\x03\x00\x08\x80\x7f\xd4\x1f\x1b\x51\x27\xa9\x00\x00\x00\x00" \
                       b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x5f\xdf\xd1" \
                       b"\xe8\x1a\xb8\x73\x74"
        self.assertEqual(pysisl.unwraps(wrapped_data), b'hello')

    def test_wrap_then_unwrap_returns_original_data(self):
        data = 'hello'
        wrapped_data = pysisl.wraps(data)
        self.assertEqual(len(wrapped_data), 53)
        self.assertEqual(wrapped_data[:4], b"\xd1\xdf\x5f\xff")
        unwrapped_data = pysisl.unwraps(wrapped_data)
        self.assertEqual(data, unwrapped_data.decode('utf-8'))

    def test_wrapped_data_includes_cloaked_dagger_header(self):
        data = 'hello'
        wrapper = sisl_wrapper.SislWrapper(SislWrapperTests.fake_key())
        wrapped_data = wrapper.wraps(data)
        self.assertEqual(len(wrapped_data), 53)
        self.assertEqual(wrapped_data[:4], b"\xd1\xdf\x5f\xff")
        self.assertEqual(SislWrapperTests.fake_key(), wrapped_data[20:28])

    def test_empty_payload_returns_only_cloaked_dagger_header(self):
        data = ""
        wrapper = sisl_wrapper.SislWrapper(SislWrapperTests.fake_key())
        wrapped_data = wrapper.wraps(data)
        self.assertEqual(len(wrapped_data), 48)
        self.assertEqual(wrapped_data[:4], b"\xd1\xdf\x5f\xff")

    def test_one_char_payload_returns_wrapped_string(self):
        data = "a"
        wrapper = sisl_wrapper.SislWrapper()
        wrapped_data = wrapper.wraps(data)
        self.assertEqual(len(wrapped_data), 49)
        self.assertEqual(wrapped_data[:4], b"\xd1\xdf\x5f\xff")

    def test_key_generator_does_not_include_0(self):
        for i in range(10):
            self.assertTrue(b'\x00' not in sisl_wrapper.SislWrapper.key_generation())

    @staticmethod
    def fake_key():
        return unhexlify(b"0123456789ABCDEF")


if __name__ == '__main__':
    unittest.main()
