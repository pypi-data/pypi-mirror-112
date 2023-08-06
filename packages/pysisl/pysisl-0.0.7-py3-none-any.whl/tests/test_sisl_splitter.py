# Copyright PA Knowledge Ltd 2021

import unittest

from pysisl.sisl_splitter import SplitSisl


class SislSplitterTests(unittest.TestCase):
    def test_basic_dict_is_parsed_successfully_without_splitting(self):
        self.assertEqual(['{abc: !int "2"}'], SplitSisl(20).split_sisl({"abc": 2}))

    def test_simple_sisl_string_longer_than_max_length_returns_list_of_two_sisl_strings_of_valid_length(self):
        self.assertEqual(["{field_one: !str \"string\"}","{field_two: !str \"string2\"}"],
                         SplitSisl(30).split_sisl({"field_one": "string", "field_two": "string2"}))

    def test_splitter_splits_to_fit_long_second_nested_object(self):
        self.assertEqual(["{field_one: !obj {field_two: !str \"hello\"}}", "{field_one: !obj {field_three: !str \"superlooooooooooooooooooooooooooooooooong\"}}"],
                         SplitSisl(81).split_sisl({"field_one": {"field_two": "hello", "field_three": "superlooooooooooooooooooooooooooooooooong"}}))

    def test_splitter_raises_an_error_if_object_cannot_be_parsed(self):
        with self.subTest("splitter_raises_an_error_if_length_is_set_too_low"):
            self.assertRaises(Exception, SplitSisl(41).split_sisl, {"field_one": {"field_two": "hello"}})
        with self.subTest("splitter_raises_an_error_if_second_nested_object_is_too_long"):
            self.assertRaises(Exception, SplitSisl(60).split_sisl, {"field_one": {"field_two": "hello", "field_three": "superlooooooooooooooooooooooooooooooooong"}})

    def test_nested_dict_is_parsed_successfully_without_splitting(self):  # p5
        self.assertEqual(['{abc: !int "2", def: !obj {efw: !str "wer", ggg: !int "234"}, adsfs: !str "hsadfklsdjlskdfjkl"}', '{ykies: !obj {whoami: !str "user", oooh: !obj {another: !float "123.2"}}}'],
                         SplitSisl(95).split_sisl({"abc": 2, "def": {"efw":"wer", "ggg": 234}, "adsfs": "hsadfklsdjlskdfjkl", "ykies": {"whoami": "user", "oooh": {"another": 123.2}}}))

    def test_nested_dict_split_up(self):
        self.assertEqual(['{field_one: !obj {field_two: !int "123"}}', '{field_one: !obj {field_three: !obj {field_four: !str "field_four string"}}}'],
                         SplitSisl(95).split_sisl({"field_one": {"field_two": 123, "field_three": {"field_four": "field_four string"}}}))

    def test_super_nested_items_can_be_fitted(self):
        self.assertEqual(["{field_one: !obj {field_two: !obj {field_three: !obj {field_four: !str \"value_1\"}}}}",
                         "{field_one: !obj {field_two: !obj {field_three: !obj {field_five: !obj {field_six: !obj {field_seven: !obj {field_eight: !str \"value_2\"}}}}}}}",
                         "{field_one: !obj {field_two: !obj {field_three: !obj {field_five: !obj {field_six: !obj {field_seven: !obj {field_nine: !str \"value_3\"}}}}}}}",
                         "{field_one: !obj {field_two: !obj {field_ten: !str \"value_4\"}}}"],
                         SplitSisl(142).split_sisl({"field_one": {"field_two": {"field_three": {"field_four": "value_1",
                                                                                               "field_five": {"field_six": {"field_seven": {"field_eight": "value_2", "field_nine": "value_3"}}}},
                                                                               "field_ten": "value_4"}}}))

    def test_multi_nested_and_long_value_dict_is_split(self):
        test_json = {"nest_one": {"sub_nest_one": {"nested_field_one": "test 1", "nested_field_two": "testing this long string still fits"}}}
        self.assertEqual(["{nest_one: !obj {sub_nest_one: !obj {nested_field_one: !str \"test 1\"}}}",
                         "{nest_one: !obj {sub_nest_one: !obj {nested_field_two: !str \"testing this long string still fits\"}}}"],
                         SplitSisl(100).split_sisl(test_json))

    def test_simple_list_is_handled(self):
        self.assertEqual(["{field_one: !list {_0: !str \"I\", _1: !str \"am\", _2: !str \"a\", _3: !str \"list\"}}"],
                         SplitSisl().split_sisl({"field_one": ["I", "am", "a", "list"]}))

    def test_simple_list_is_split_in_half(self):
        self.assertEqual(["{field_one: !list {_0: !str \"I\", _1: !str \"am\"}}", "{field_one: !list {_2: !str \"a\", _3: !str \"list\"}}"],
                         SplitSisl(50).split_sisl({"field_one": ["I", "am", "a", "list"]}))

    def test_simple_nested_list_is_split_in_half(self):
        self.assertEqual(["{field_one: !list {_0: !str \"I\", _1: !list {_0: !str \"am\"}}}", "{field_one: !list {_1: !list {_1: !str \"a\"}, _2: !str \"list\"}}"],
                         SplitSisl(65).split_sisl({"field_one": ["I", ["am", "a"], "list"]}))

    def test_long_list_item_is_split(self):
        self.assertEqual(["{field_one: !list {_0: !str \"I\", _1: !str \"am\", _2: !str \"a\"}}",
                         "{field_one: !list {_3: !str \"supeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerlist\"}}"],
                         SplitSisl(120).split_sisl({"field_one": ["I", "am", "a", "supeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerlist"]}))

    def test_splitter_splits_complex_and_multiple_nesting(self):
        test_json = {"nest_one": {"field_one": "hello",
                                  "field_two_nest": {"nested_field_one": "brave",
                                                     "nested_field_two": "new"},
                                  "field_three": "world"},
                     "nest_two": {"field_one": "world",
                                  "field_two": "wide"}}
        self.assertEqual(["{nest_one: !obj {field_one: !str \"hello\", field_two_nest: !obj {nested_field_one: !str \"brave\"}}}",
                         "{nest_one: !obj {field_two_nest: !obj {nested_field_two: !str \"new\"}, field_three: !str \"world\"}}",
                         "{nest_two: !obj {field_one: !str \"world\", field_two: !str \"wide\"}}"],
                         SplitSisl(100).split_sisl(test_json))

    def test_list_of_different_types_is_converted_to_sisl_and_split(self):
        self.assertEqual(["{nest_one: !list {_0: !int \"1\", _1: !str \"string1\", _2: !bool \"true\", _3: !list {_0: !list {_0: !str \"nested_list\"}}}}",
                         "{nest_one: !list {_3: !list {_0: !list {_1: !int \"2\"}, _1: !bool \"false\", _2: !float \"3.0\"}}}",
                         "{nest_one: !list {_4: !obj {field_one: !bool \"false\", field_two: !str \"string3\"}}}",
                         "{nest_two: !obj {field_one: !str \"string4\", sub_nest_one: !obj {field_two: !obj {field_three: !float \"4.0\"}}}}",
                         "{nest_two: !obj {field_four: !bool \"true\", sub_nest_two: !obj {field_five: !int \"3\"}}}"],
                         SplitSisl(120).split_sisl({"nest_one": [1, "string1", True, [["nested_list", 2], False, 3.0],
                                                                 {"field_one": False, "field_two": "string3"}],
                                                   "nest_two": {"field_one": "string4", "sub_nest_one": {"field_two": {"field_three": 4.0}}, "field_four": True, "sub_nest_two": {"field_five": 3}}}))

    def test_list_of_nested_dicts_converted_sisl(self):
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

        self.assertEqual([line_1, line_2, line_3],
                         SplitSisl(300).split_sisl({"list_one": ["item_0", "item_1", item_2_dict, item_3_dict, item_4_dict]}))


if __name__ == '__main__':
    unittest.main()


