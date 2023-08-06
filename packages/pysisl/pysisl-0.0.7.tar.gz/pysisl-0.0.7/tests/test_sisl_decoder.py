# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_decoder import SislDecoder, SislValidationError


class SislParsingTests(unittest.TestCase):
    def test_basic_sisl_structures_successful_parse(self):
        self.assertEqual({"abc": {"results": {"result": 123}}}, SislDecoder().loads("{abc: !obj {results: !obj {result: !int \"123\"}}}"))

    def test_successful_parse_with_schema(self):
        schema = {
            "properties": {
                "field_one": {
                    "type": "string"
                },
                "field_two": {
                    "type": "number"
                }
            }
        }
        self.assertEqual({"field_one": "string", "field_two": 2},
                         SislDecoder().loads("{field_one: !str \"string\", field_two: !int \"2\"}", schema=schema))

    def test_parse_with_schema_fails_throws_error(self):
        schema = {
            "properties": {
                "field_one": {
                    "type": "number"
                },
                "field_two": {
                    "type": "number"
                }
            }
        }
        self.assertRaises(SislValidationError,
                          SislDecoder().loads, "{field_one: !str \"string\", field_two: !int \"2\"}", schema=schema)

    def test_sisl_with_escaped_backslash_successful_parse(self):
        self.assertEqual({"abc": "te\\st"}, SislDecoder().loads("{abc: !str \"te\\st\"}"))

    def test_sisl_with_escaped_quotes_successful_parse(self):
        self.assertEqual({"abc": "te\"st"}, SislDecoder().loads(r'{abc: !str "te\"st"}'))

    def test_escaped_backslash_before_closing_quote_sisl(self):
        self.assertEqual({"abc": "test\\"}, SislDecoder().loads(r'{abc: !str "test\\"}'))

    def test_escaped_quote_before_closing_quote_sisl(self):
        self.assertEqual({"abc": "test\""}, SislDecoder().loads(r'{abc: !str "test\""}'))

    def test_sisl_with_8_bit_unicode_successful_parse(self):
        self.assertEqual({"abc": "çä"}, SislDecoder().loads(r'{abc: !str "\xe7\xe4"}'))

    def test_sisl_with_16_bit_unicode_successful_parse(self):
        self.assertEqual({"abc": "ӧʶ"}, SislDecoder().loads(r'{abc: !str "\u04e7\u02b6"}'))

    def test_sisl_with_32_bit_unicode_successful_parse(self):
        self.assertEqual({"abc": "😂🔥"}, SislDecoder().loads(r'{abc: !str "\U0001f602\U0001f525"}'))

    def test_basic_split_sisl_string_parsed_using_joiner(self):
        self.assertEqual({"abc": 2, "def": 3}, SislDecoder().loads(['{abc: !int "2"}', '{def: !int "3"}']))

    def test_split_nested_dict_rejoined(self):
        self.assertEqual({"field_one": {"field_two": 123, "field_three": {"field_four": "field_four string"}}},
                         SislDecoder().loads(['{field_one: !obj {field_two: !int "123"}}', '{field_one: !obj {field_three: !obj {field_four: !str "field_four string"}}}']))

    def test_split_deeply_nested_dict_rejoined(self):
        input_sisl = ["{field_one: !obj {field_two: !obj {field_three: !obj {field_four: !str \"value_1\"}}}}",
                      "{field_one: !obj {field_two: !obj {field_three: !obj {field_five: !obj {field_six: !obj {field_seven: !obj {field_eight: !str \"value_2\"}}}}}}}",
                      "{field_one: !obj {field_two: !obj {field_three: !obj {field_five: !obj {field_six: !obj {field_seven: !obj {field_nine: !str \"value_3\"}}}}}}}",
                      "{field_one: !obj {field_two: !obj {field_ten: !str \"value_4\"}}}"]
        expected_output = {"field_one": {"field_two": {"field_three": {"field_four": "value_1",
                                                                       "field_five": {"field_six": {"field_seven": {"field_eight": "value_2", "field_nine": "value_3"}}}},
                                                       "field_ten": "value_4"}}}
        self.assertEqual(expected_output,
                         SislDecoder().loads(input_sisl))

    def test_split_nested_dict_with_long_values_rejoined(self):
        expected_output = {"nest_one": {"sub_nest_one": {"nested_field_one": "test 1", "nested_field_two": "testing this long string still fits"}}}
        input_sisl = ["{nest_one: !obj {sub_nest_one: !obj {nested_field_one: !str \"test 1\"}}}",
                      "{nest_one: !obj {sub_nest_one: !obj {nested_field_two: !str \"testing this long string still fits\"}}}"]
        self.assertEqual(expected_output, SislDecoder().loads(input_sisl))

    def test_basic_list_that_is_parsed_using_joiner(self):
        self.assertEqual({"field_one": ["I", "am", "a", "list"]},
                         SislDecoder().loads(["{field_one: !list {_0: !str \"I\", _1: !str \"am\"}}", "{field_one: !list {_2: !str \"a\", _3: !str \"list\"}}"]))

    def test_basic_split_nested_list_is_parsed_using_joiner(self):
        self.assertEqual({"field_one": ["I", ["am", "a"], "list"]},
                         SislDecoder().loads(["{field_one: !list {_0: !str \"I\", _1: !list {_0: !str \"am\"}}}", "{field_one: !list {_1: !list {_1: !str \"a\"}, _2: !str \"list\"}}"]))

    def test_split_list_of_different_types_is_rejoined(self):
        input_sisl = ["{nest_one: !list {_0: !int \"1\", _1: !str \"string1\", _2: !bool \"true\", _3: !list {_0: !list {_0: !str \"nested_list\"}}}}",
                      "{nest_one: !list {_3: !list {_0: !list {_1: !int \"2\"}, _1: !bool \"false\", _2: !float \"3.0\"}}}",
                      "{nest_one: !list {_4: !obj {field_one: !bool \"false\", field_two: !str \"string3\"}}}",
                      "{nest_two: !obj {field_one: !str \"string4\", sub_nest_one: !obj {field_two: !obj {field_three: !float \"4.0\"}}}}",
                      "{nest_two: !obj {field_four: !bool \"true\", sub_nest_two: !obj {field_five: !int \"3\"}}}"]
        expected_output = {"nest_one": [1, "string1", True, [["nested_list", 2], False, 3.0],
                                        {"field_one": False, "field_two": "string3"}],
                           "nest_two": {"field_one": "string4", "sub_nest_one": {"field_two": {"field_three": 4.0}}, "field_four": True, "sub_nest_two": {"field_five": 3}}}
        self.assertEqual(expected_output, SislDecoder().loads(input_sisl))

    def test_complex_list_of_nested_dicts_that_is_split_is_parsed_using_joiner(self):
        list = "{list_one: !list {"
        item_0 = "_0: !str \"item_0\", "
        item_1 = "_1: !str \"item_1\", "
        item_2 = "_2: !obj {item_2: !obj {nest_field_1: !str \"nest_item_1_value\"}}, "
        item_3_part1 = "_3: !obj {item_3: !obj {nest_field_1: !obj {nest_field_2: !obj {nest_field_3: !obj {nest_field_4: !obj {nest_field_5: !str \"nest_field_5_value\"}}}}}}"
        item_3_part2 = "_3: !obj {item_3: !obj {nest_field_1: !obj {nest_field_2: !obj {nest_field_3: !obj {nest_field_4_key_2: !obj {nest_field_5_key_2: !str \"nest_field_5_value_2\"}}}}}}, "
        item_4_part1 = "_4: !obj {item_4: !obj {nest_field_1: !obj {nest_field_2: !str \"nest_field_2_value\"}}}"
        item_4_part2 = "_4: !obj {item_4: !obj {nest_field_1_key_2: !str \"nest_item_2\"}, nest_field_2_key_2: !obj {nest_field_3_key_2: !str \"nest_field_3_key_2_value_2\"}}"

        line_1 = list + item_0 + item_1 + item_2 + item_3_part1 + "}}"
        line_2 = list + item_3_part2 + item_4_part1 + "}}"
        line_3 = list + item_4_part2 + "}}"

        item_2_dict = {"item_2": {"nest_field_1": "nest_item_1_value"}}
        item_3_dict = {"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                     "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        item_4_dict = {"item_4": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                                  "nest_field_1_key_2": "nest_item_2"},
                       "nest_field_2_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}

        input_sisl = [line_1, line_2, line_3]
        expected_output = {"list_one": ["item_0", "item_1", item_2_dict, item_3_dict, item_4_dict]}
        self.assertEqual(expected_output, SislDecoder().loads(input_sisl))


if __name__ == '__main__':
    unittest.main()
