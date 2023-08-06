# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_encoder import SislEncoder, TypeValidationError
from pysisl.deep_merger import ListTuple


class NotSislClass:
    def __init__(self):
        self.name = "unknown object"


class SislParsingTests(unittest.TestCase):
    def test_basic_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{}", SislEncoder.dumps({}))

    def test_string_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !str \"string\"}", SislEncoder.dumps({"field_one": "string"}))
        self.assertEqual("{field_one: !str \"string\", field_two: !str \"string2\"}",
                         SislEncoder.dumps({"field_one": "string", "field_two": "string2"}))

    def test_int_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !int \"123\"}", SislEncoder.dumps({"field_one": 123}))

    def test_float_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !float \"1.23\"}", SislEncoder.dumps({"field_one": 1.23}))
        self.assertEqual("{field_one: !float \"-0.123\"}", SislEncoder.dumps({"field_one": -0.123}))
        self.assertEqual("{field_one: !float \"1.0\"}", SislEncoder.dumps({"field_one": 1.0}))

    def test_bool_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !bool \"true\"}", SislEncoder.dumps({"field_one": True}))
        self.assertEqual("{field_one: !bool \"false\"}", SislEncoder.dumps({"field_one": False}))

    def test_single_element_integer_list_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !list {_0: !int \"1\"}}", SislEncoder.dumps({"field_one": [1]}))

    def test_list_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !list {_0: !int \"1\", _1: !int \"2\", _2: !int \"3\"}}", SislEncoder.dumps({"field_one": [1, 2, 3]}))
        self.assertEqual("{field_one: !list {_0: !list {_0: !int \"4\"}, _1: !int \"2\", _2: !int \"3\"}}", SislEncoder.dumps({"field_one": [[4], 2, 3]}))

    def test_basic_nested_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !obj {}}", SislEncoder.dumps({"field_one": {}}))

    def test_nested_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !obj {field_two: !int \"123\"}}", SislEncoder.dumps({"field_one": {"field_two": 123}}))

    def test_multiple_nested_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !obj {field_two: !int \"123\", field_three: !str \"field_three string\"}}",
                         SislEncoder.dumps({"field_one": {"field_two": 123, "field_three": "field_three string"}}))
        self.assertEqual("{field_one: !obj {field_two: !int \"123\", field_three: !obj {field_four: !str \"field_four string\"}}}",
                         SislEncoder.dumps({"field_one": {"field_two": 123, "field_three": {"field_four": "field_four string"}}}))

    def test_unknown_types_in_dictionary_should_throw_error(self):
        self.assertRaises(TypeValidationError, SislEncoder.dumps, {"field_two": NotSislClass()})

    def test_none_type_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !null \"\"}", SislEncoder.dumps({"field_one": None}))

    def test_escaped_backslash_successful_converted_to_sisl(self):
        self.assertEqual(r'{field_one: !str "te\\st"}', SislEncoder.dumps({"field_one": "te\\st"}))

    def test_escaped_dbquote_successful_converted_to_sisl(self):
        self.assertEqual(r'{field_one: !str "te\"st"}', SislEncoder.dumps({"field_one": "te\"st"}))

    def test_8_bit_unicode_characters(self):
        self.assertEqual(r'{field_one: !str "\xe7\xe4"}', SislEncoder.dumps({"field_one": "çä"}))

    def test_16_bit_unicode_characters(self):
        self.assertEqual(r'{field_one: !str "\u04e7\u02b6"}', SislEncoder.dumps({"field_one": "ӧʶ"}))

    def test_32_bit_unicode_characters(self):
        self.assertEqual(r'{field_one: !str "\U0001f602\U0001f525"}', SislEncoder.dumps({"field_one": "😂🔥"}))

    def test_list_tuple_value_successfully_converted_to_sisl(self):
        # [value1, value2]
        self.assertEqual("{field_one: !list {_0: !str \"value1\", _1: !str \"value2\"}}",
                         SislEncoder.dumps({"field_one": [ListTuple("value1", 0), ListTuple("value2", 1)]}))

    def test_nested_list_tuple_successfully_converted_to_sisl(self):
        # [[value1]]
        self.assertEqual("{field_one: !list {_0: !list {_0: !str \"value1\"}}}",
                         SislEncoder.dumps({"field_one": [ListTuple([ListTuple("value1", 0)], 0)]}))

    def test_deeply_nested_list_tuple_successfully_converted_to_sisl(self):
        # {"field_one": [value1, [[[value2]]]]}
        self.assertEqual("{field_one: !list {_0: !str \"value1\", _1: !list {_0: !list {_0: !list {_0: !str \"value2\"}}}}}",
                         SislEncoder.dumps({"field_one": [ListTuple("value1", 0), ListTuple([ListTuple([ListTuple([ListTuple("value2", 0)], 0)], 0)], 1)]}))

    def test_list_of_dicts_successfully_converted_to_sisl(self):
        # {"list_one": [{"dict_1": "value_1"}, {"dict_2": "value_2"}, {'dict_3': 'value_3'}]
        self.assertEqual("{list_one: !list {_0: !obj {dict_1: !str \"value_1\"}, _1: !obj {dict_2: !str \"value_2\"}, _2: !obj {dict_3: !str \"value_3\"}}}",
                         SislEncoder.dumps({"list_one": [ListTuple({"dict_1": "value_1"}, 0),
                                                         ListTuple({"dict_2": "value_2"}, 1),
                                                         ListTuple({'dict_3': 'value_3'}, 2)]}))

    def test_list_of_nested_items_successfully_converted_to_sisl(self):
        # {"field_one": ["A",
        #               [[["nested", "list"]]],
        #               {"lvl1": {"lvl2": {"item_1": "nested",
        #                                  "item_2": "dict"}}}
        #               ]}
        input_dict = {"field_one": [ListTuple("A", 0),
                                    ListTuple([ListTuple([ListTuple([ListTuple("nested", 0), ListTuple("list", 1)], 0)], 0)], 1),
                                    ListTuple({"lvl1": {"lvl2": {"item_1": "nested", "item_2": "dict"}}}, 2)]}

        self.assertEqual("{field_one: !list {_0: !str \"A\", "
                                            "_1: !list {_0: !list {_0: !list {_0: !str \"nested\", _1: !str \"list\"}}}, "
                                            "_2: !obj {lvl1: !obj {lvl2: !obj {item_1: !str \"nested\", "
                                                                              "item_2: !str \"dict\"}}}}}",
                         SislEncoder.dumps(input_dict))

    def test_list_of_nested_items_with_dicts_and_lists(self):
        # {"nested_list": [{"item1": {"nest_field_1": "nest_item_1_value"}}, ["item5", {"item5_2": "value_2"}]]}
        input_dict = {"nested_list": [ListTuple({"item1": {"nest_field_1": "nest_item_1_value"}}, 0),
                                      ListTuple([ListTuple("item5", 0),
                                                 ListTuple({"item5_2": "value_2"}, 1)], 1)]}

        self.assertEqual("{nested_list: !list {_0: !obj {item1: !obj {nest_field_1: !str \"nest_item_1_value\"}}, "
                                              "_1: !list {_0: !str \"item5\", "
                                                         "_1: !obj {item5_2: !str \"value_2\"}}}}",
                         SislEncoder.dumps(input_dict))

    def test_nested_dict_that_contains_nested_list(self):
        # {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"},
        #                                       "lvl2_2": [["value_8"],
        #                                                  {"lvl3": {"lvl4": "value_9"}},
        #                                                  {"lvl3": "value_10"}]},
        #                              "lvl1_3": {"lvl2_1": {"lvl3_1": {"lvl4_1": "value_12"}}}}}
        input_dict = {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"},
                                               "lvl2_2": [ListTuple([ListTuple("value_8", 0)], 0),
                                                          ListTuple({"lvl3": {"lvl4": "value_9"}}, 1),
                                                          ListTuple({"lvl3": "value_10"}, 2)]},
                                      "lvl1_3": {"lvl2_1": {"lvl3_1": {"lvl4_1": "value_12"}}}}}

        self.assertEqual("{nested_dict: !obj {lvl1: !obj {lvl2_1: !obj {lvl3: !str \"value_6\"}, "
                                                         "lvl2_2: !list {_0: !list {_0: !str \"value_8\"}, "
                                                                        "_1: !obj {lvl3: !obj {lvl4: !str \"value_9\"}}, "
                                                                        "_2: !obj {lvl3: !str \"value_10\"}}"
                                                        "}, "
                                             "lvl1_3: !obj {lvl2_1: !obj {lvl3_1: !obj {lvl4_1: !str \"value_12\"}}}}}",
                         SislEncoder.dumps(input_dict))


if __name__ == '__main__':
    unittest.main()
