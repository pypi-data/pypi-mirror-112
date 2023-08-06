# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_encoder import SislEncoder
from pysisl.sisl_decoder import SislDecoder


class SislEncoderDecoderTests(unittest.TestCase):
    def test_empty_dict_is_transformed_successfully(self):
        encoder_input = {}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_string_as_value_is_transformed_successfully(self):
        encoder_input = {"field_one": "string"}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_unicode_string_value_is_transformed_successfully(self):
        encoder_input = {"abc": "ӧӧФ@፨=😂❤🔥❌£¥"}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder().dumps(encoder_input)))

    def test_multiple_nested_dict_as_value_is_transformed_successfully(self):
        encoder_input = {"field_one": {"field_two": 123, "field_three": {"field_four": "field_four string"}}}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_float_value_is_transformed_successfully(self):
        encoder_input = {"field_one": 1.0}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_nested_list_in_value_is_transformed_successfully(self):
        encoder_input = {"field_one": [1, [2, 3]]}
        dumps_outpout = SislEncoder.dumps(encoder_input)
        self.assertEqual(encoder_input, SislDecoder().loads(dumps_outpout))

    def test_escaped_backslash_in_value_is_transformed_successfully(self):
        encoder_input = {"abc": "te\\st"}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_nested_dict_structure_with_lists_in_value_is_transformed_successfully(self):
        encoder_input = {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"},
                                                  "lvl2_2": [["value_8"],
                                                             {"lvl3": {"lvl4": "value_9"}},
                                                             {"lvl3": "value_10"}]},
                                         "lvl1_3": {"lvl2_1": {"lvl3_1": {"lvl4_1": "value_12"}}}}}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_decoded_sisl_with_escaped_backslash_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "te\\st"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_quotes_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "te\"st"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_backslash_before_closing_quote_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "test\\"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_quote_before_closing_quote_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "test\""}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_quote_before_comma_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "te\"a,st"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_quote_just_before_comma_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "te\",st"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_quote_before_space_comma_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "te\" ,st"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_escaped_quote_before_brace_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "te\"}st"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))

    def test_decoded_sisl_with_unicode_string_is_encoded_successfully(self):
        decoder_input = r'{abc: !str "\u04e7\u04e7\u0424@\u1368=\U0001f602b\u2764\U0001f525\u274c\xa3\xa5"}'
        self.assertEqual(decoder_input, SislEncoder.dumps(SislDecoder().loads(decoder_input)))


if __name__ == '__main__':
    unittest.main()
