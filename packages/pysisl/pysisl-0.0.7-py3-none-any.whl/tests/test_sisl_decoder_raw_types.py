# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_decoder import SislDecoder
from pysisl.parser_error import ParserError


class SislRawTypesParsingTests(unittest.TestCase):
    def test_parser_error(self):
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{1abc: !type \"value\"}")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{abc: type \"value\"}")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{abc: !type \"value}")

    def test_basic_sisl_structures(self):
        self.assertEqual({}, SislDecoder().parse_raw_types("{}"))
        self.assertEqual({"abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !type \"value\"}"))
        self.assertEqual({
            "abc": {
                "type": "type",
                "value": {
                    "nested": {
                        "type": "type",
                        "value": "value"
                    }
                }
            }
        }, SislDecoder().parse_raw_types("{abc: !type {nested: !type \"value\"}}"))

        self.assertEqual({
            "abc": {
                "type": "type",
                "value": {
                    "nested": {
                        "type": "type",
                        "value": {
                            "nested": {
                                "type": "type",
                                "value": "value"
                            }
                        }
                    }
                }
            }
        }, SislDecoder().parse_raw_types("{abc: !type {nested: !type {nested: !type \"value\"}}}"))

    def test_basic_values(self):
        self.assertEqual({"abc": {"type": "type", "value": "value1"}}, SislDecoder().parse_raw_types("{abc: !type \"value1\"}"))
        self.assertEqual({"abc": {"type": "type", "value": "VALUE1"}}, SislDecoder().parse_raw_types("{abc: !type \"VALUE1\"}"))
        self.assertEqual({"abc": {"type": "type", "value": r'val\"ue'}}, SislDecoder().parse_raw_types(r'{abc: !type "val\"ue"}'))
        self.assertEqual({"abc": {"type": "type", "value": r'val\\ue'}}, SislDecoder().parse_raw_types(r'{abc: !type "val\\ue"}'))
        self.assertEqual({"abc": {"type": "type", "value": r'val ue'}}, SislDecoder().parse_raw_types(r'{abc: !type "val ue"}'))

    def test_basic_names(self):
        self.assertEqual({"aBc": {"type": "type", "value": "value1"}}, SislDecoder().parse_raw_types("{aBc: !type \"value1\"}"))
        self.assertEqual({"AbC": {"type": "type", "value": "value1"}}, SislDecoder().parse_raw_types("{AbC: !type \"value1\"}"))
        self.assertEqual({"_B.-": {"type": "type", "value": "value1"}}, SislDecoder().parse_raw_types("{_B.-: !type \"value1\"}"))

    def test_basic_types(self):
        self.assertEqual({"abc": {"type": "aBc", "value": "value1"}}, SislDecoder().parse_raw_types("{abc: !aBc \"value1\"}"))
        self.assertEqual({"abc": {"type": "AbC", "value": "value1"}}, SislDecoder().parse_raw_types("{abc: !AbC \"value1\"}"))
        self.assertEqual({"abc": {"type": "_B.-", "value": "value1"}}, SislDecoder().parse_raw_types("{abc: !_B.- \"value1\"}"))

        self.assertEqual({"abc": {"type": f"str{'r' * 252}", "value": "test"}}, SislDecoder().parse_raw_types(f'{{abc: !str{"r" * 252} \"test\"}}'))
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc: !str{"r" * 253} \"test\"}}')

    def test_lists(self):
        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\",def: !typeb \"value2\"}"))

        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"},
            "ghi": {"type": "typec", "value": "value3"}},
            SislDecoder().parse_raw_types("{abc: !type \"value\",def: !typeb \"value2\",ghi: !typec \"value3\"}"))

    def test_lists_with_whitespace_after_separator(self):
        self.assertEqual({
            "abc": {"type": "type", "value": "value"},
            "def": {"type": "typeb", "value": "value2"}
        }, SislDecoder().parse_raw_types("{abc: !type \"value\", def: !typeb \"value2\"}"))
        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\",  def: !typeb \"value2\"}"))

    def test_lists_with_whitespace_before_separator(self):
        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\" , def: !typeb \"value2\"}"))

        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\" , def: !typeb \"value2\"}"))

    def test_whitespace_limit(self):
        self.assertEqual({"abc": {"type": "type", "value": "test"}}, SislDecoder().parse_raw_types(f'{{{" " * 255}abc: !type \"test\"}}'))
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{{" " * 256}abc: !type \"test\"}}')

        self.assertEqual({"abc": {"type": "type", "value": "test"}}, SislDecoder().parse_raw_types(f'{{abc:{" " * 255}!type \"test\"}}'))
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, r'{abc:!type \"test\"}')
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc:{" " * 256}!type \"test\"}}')

        self.assertEqual({"abc": {"type": "type", "value": "test"}}, SislDecoder().parse_raw_types(f'{{abc: !type{" " * 255}\"test\"}}'))
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc: !type\"test\"}}')
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc: !type{" " * 300}\"test\"}}')

        self.assertEqual({"abc": {"type": "type", "value": "test1"}, "def": {"type": "type", "value": "test2"}}, SislDecoder().parse_raw_types(f'{{abc: !type \"test1\"{" " * 255}, def: !type \"test2\"{" " * 255}}}'))
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc: !type \"test\"{" " * 256}}}')
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc: !type \"test1\"{" " * 256}, def: !type \"test2\"}}')

        self.assertEqual({"abc": {"type": "type", "value": "test"}}, SislDecoder().parse_raw_types(f'{{abc: !type \"test\"}}{" " * 255}'))
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, f'{{abc: !type \"test\"}}{" " * 256}')

    def test_nested_lists(self):
        self.assertEqual({'field_one': {'type': 'list',
                                        'value': {'_0': {'type': 'int', 'value': '1'},
                                                  '_1': {'type': 'list',
                                                         'value': {'_0': {'type': 'int',
                                                                          'value': '2'}}}}}},
                         SislDecoder().parse_raw_types('{field_one: !list {_0: !int "1", _1: !list {_0: !int "2"}}}'))

    def test_name_special_chars(self):
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type \"value\"}"))
        self.assertEqual({"ab_c_": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ab_c_: !type \"value\"}"))
        self.assertEqual({"ab.c": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ab.c: !type \"value\"}"))
        self.assertEqual({"ab3c": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ab3c: !type \"value\"}"))

    def test_type_special_chars(self):
        self.assertEqual({"abc": {"type": "_abc", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !_abc \"value\"}"))
        self.assertEqual({"abc": {"type": "ab_c", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !ab_c \"value\"}"))
        self.assertEqual({"abc": {"type": "ab.c", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !ab.c \"value\"}"))
        self.assertEqual({"abc": {"type": "ab3c", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !ab3c \"value\"}"))
        self.assertEqual({"abc": {"type": "t", "value": "value1"}}, SislDecoder().parse_raw_types("{abc: !t \"value1\"}"))
        self.assertEqual({"c": {"type": "t", "value": "value1"}}, SislDecoder().parse_raw_types("{c: !t \"value1\"}"))

    def test_value_special_chars(self):
        self.assertEqual({"_abc": {"type": "type", "value": "value="}}, SislDecoder().parse_raw_types("{_abc: !type \"value=\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value-"}}, SislDecoder().parse_raw_types("{_abc: !type \"value-\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value:"}}, SislDecoder().parse_raw_types("{_abc: !type \"value:\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value."}}, SislDecoder().parse_raw_types("{_abc: !type \"value.\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value+"}}, SislDecoder().parse_raw_types("{_abc: !type \"value+\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value@"}}, SislDecoder().parse_raw_types("{_abc: !type \"value@\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value'"}}, SislDecoder().parse_raw_types("{_abc: !type \"value'\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value!"}}, SislDecoder().parse_raw_types("{_abc: !type \"value!\"}"))

    def test_value_unicode_chars(self):
        self.assertEqual({"_abc": {"type": "type", "value": "ӧӧФ@፨="}}, SislDecoder().parse_raw_types("{_abc: !type \"ӧӧФ@፨=\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "ӧ"}}, SislDecoder().parse_raw_types("{_abc: !type \"\u04E7\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "\u04E7"}}, SislDecoder().parse_raw_types("{_abc: !type \"\u04E7\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "U+274C"}}, SislDecoder().parse_raw_types("{_abc: !type \"U+274C\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "&#10060;"}}, SislDecoder().parse_raw_types("{_abc: !type \"&#10060;\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "£¥"}}, SislDecoder().parse_raw_types("{_abc: !type \"£¥\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "😂❤🔥❌"}}, SislDecoder().parse_raw_types("{_abc: !type \"😂❤🔥❌\"}"))

    def test_allow_space(self):
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type \"value\"} "))
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ _abc: !type \"value\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type \"value\" }"))
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type  \"value\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc:  !type \"value\"}"))

    def test_allow_escaped_quote_followed_by_space(self):
        self.assertEqual({"_abc": {"type": "type", "value": r'value\" '}}, SislDecoder().parse_raw_types(r'{_abc: !type "value\" " }'))

    def test_allow_escaped_quote_followed_by_commas(self):
        self.assertEqual({"_abc": {"type": "type", "value": r'\",'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\","}'))
        self.assertEqual({"_abc": {"type": "type", "value": r'\",\"'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\",\""}'))
        self.assertEqual({"_abc": {"type": "type", "value": r'\",\",'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\",\","}'))
        self.assertEqual({"_abc": {"type": "type", "value": r'\",KB'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\",KB"}'))
        self.assertEqual({"_abc": {"type": "type", "value": r'\\,KB'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\\,KB"}'))
        self.assertEqual({"_abc": {"type": "type", "value": r'\\\",KB'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\\\",KB"}'))

    def test_allow_escaped_characters_before_final_quotes(self):
        self.assertEqual({"_abc": {"type": "type", "value": r'\\'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\\"}'))
        self.assertEqual({"_abc": {"type": "type", "value": r'\\\"'}}, SislDecoder().parse_raw_types(r'{_abc: !type "\\\""}'))

    def test_example_syslog_sisl(self):
        self.assertEqual({'app-name': {'type': 'string', 'value': 'containerd'},
                          'date': {'type': 'string', 'value': '2019-08-08T13:50:14.170225+01:00'},
                          'host': {'type': 'string', 'value': 'centosvm'},
                          'message': {'type': 'string',
                                      'value': '  time=2020-12-09T16:47:16.358818934Z'}},
                         SislDecoder().parse_raw_types(r'{date: !string "2019-08-08T13:50:14.170225+01:00", host: !string "centosvm", app-name: !string "containerd", message: !string "  time=2020-12-09T16:47:16.358818934Z"}'))


if __name__ == '__main__':
    unittest.main()
