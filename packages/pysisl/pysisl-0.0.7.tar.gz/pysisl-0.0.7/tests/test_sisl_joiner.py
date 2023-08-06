# Copyright PA Knowledge Ltd 2021

import unittest

from pysisl.sisl_joiner import JoinSisl


class SislJoinerTests(unittest.TestCase):
    def test_join_list_with_empty_value(self):
        list_of_dicts = [{"field_one": {"type": "type", "value": {}}}]
        expected_output = {"field_one": {"type": "type", "value": {}}}

        self.assertEqual(expected_output, JoinSisl.join(list_of_dicts))

    def test_join_list_with_only_one_dict(self):
        list_of_dicts = [{"field_one": {"type": "type", "value": "value1"}}]
        expected_output = {"field_one": {"type": "type", "value": "value1"}}

        self.assertEqual(expected_output, JoinSisl.join(list_of_dicts))

    def test_join_list_of_multiple_dicts(self):
        first_dict = {"abc": {"type": "type", "value": "value1"}}
        second_dict = {"def": {"type": "type", "value": "value2"}}
        third_dict = {"ghi": {"type": "type", "value": "value3"}}
        expected_output = {'abc': {'type': 'type', 'value': 'value1'},
                           'def': {'type': 'type', 'value': 'value2'},
                           "ghi": {"type": "type", "value": "value3"}}

        self.assertEqual(expected_output, JoinSisl.join([first_dict, second_dict, third_dict]))

    def test_join_list_of_nested_dicts(self):
        list_of_dicts = [{"field_one": {"type": "type", "value": {"field_one_nested": {"type": "type", "value": "value1"}}}},
                         {"field_two": {"type": "type", "value": {"field_two_nested": {"type": "type", "value": "value2"}}}}]

        expected_output = {"field_one": {"type": "type", "value": {"field_one_nested": {"type": "type", "value": "value1"}}},
                           "field_two": {"type": "type", "value": {"field_two_nested": {"type": "type", "value": "value2"}}}}

        self.assertEqual(expected_output, JoinSisl.join(list_of_dicts))

    def test_join_simple_list_structure(self):
        list_of_dicts = [{"abc": {"type": "type", "value": {"_0": {"type": "type", "value": "value1"}}}},
                         {"abc": {"type": "type", "value": {"_1": {"type": "type", "value": "value2"}}}}]

        expected_output = {"abc": {"type": "type", "value": {"_0": {"type": "type", "value": "value1"},
                                                             "_1": {"type": "type", "value": "value2"}}}}

        self.assertEqual(expected_output, JoinSisl.join(list_of_dicts))

    def test_join_list_containing_separate_nested_list_elements(self):
        # [[1]], [[2]] -> [[1], [2]]
        list_of_dicts = [{"abc": {"type": "type", "value": {"_0": {"type": "type", "value": {"_0": {"type": "type", "value": "value1"}}}}}},
                         {"abc": {"type": "type", "value": {"_1": {"type": "type", "value": {"_0": {"type": "type", "value": "value2"}}}}}}]

        expected_output = {"abc": {"type": "type", "value": {
            "_0": {"type": "type", "value": {"_0": {"type": "type", "value": "value1"}}},
            "_1": {"type": "type", "value": {"_0": {"type": "type", "value": "value2"}}}
        }}}

        self.assertEqual(expected_output, JoinSisl.join(list_of_dicts))

    def test_join_nested_list_structure_that_is_split_in_nested_list(self):
        # [1, [2]], [[3], 4] -> [1, [2, 3], 4]
        list_of_dicts = [{"abc": {"type": "type", "value": {"_0": {"type": "type", "value": "value1"},
                                                            "_1": {"type": "type", "value": {"_0": {"type": "type", "value": "value2"}}}}}},
                         {"abc": {"type": "type", "value": {"_1": {"type": "type", "value": {"_1": {"type": "type", "value": "value3"}}},
                                                            "_2": {"type": "type", "value": "value4"}}}}]

        expected_output = {"abc": {"type": "type", "value": {"_0": {"type": "type", "value": "value1"},
                                                             "_1": {"type": "type", "value": {"_0": {"type": "type", "value": "value2"},
                                                                                              "_1": {"type": "type", "value": "value3"}}},
                                                             "_2": {"type": "type", "value": "value4"}}}}

        self.assertEqual(expected_output, JoinSisl.join(list_of_dicts))

    def test_join_deeply_nested_structure_with_key_value_pairs_at_multiple_different_levels(self):
        # {"field_one": {"field_two_one": {"field_three": {"field_four": "value1"}}}},
        # {"field_one": {"field_two_one": {"field_three": {"field_five": "value2"}}}},
        # {"field_one": {"field_two_two": "value3"}} ->
        # {"field_one": {"field_two_one": {"field_three": {"field_four": "value1", "field_five": "value2"}},
        #                "field_two_two": "value3"}}

        first_dict = {"field_one": {"type": "type", "value": {"field_two_one": {"type": "type", "value": {"field_three": {"type": "type", "value": {"field_four": {"type": "type", "value": "value1"}}}}}}}}
        second_dict = {"field_one": {"type": "type", "value": {"field_two_one": {"type": "type", "value": {"field_three": {"type": "type", "value": {"field_five": {"type": "type", "value": "value2"}}}}}}}}
        third_dict = {"field_one": {"type": "type", "value": {"field_two_two": {"type": "type", "value": "value3"}}}}

        expected_output = {"field_one": {"type": "type", "value": {"field_two_one": {"type": "type", "value": {"field_three": {"type": "type", "value": {"field_four": {"type": "type", "value": "value1"},
                                                                                                                                                         "field_five": {"type": "type", "value": "value2"}}}}},
                                                                   "field_two_two": {"type": "type", "value": "value3"}}}}

        self.assertEqual(expected_output, JoinSisl.join([first_dict, second_dict, third_dict]))

    def test_list_of_nested_dicts_can_be_merged(self):
        # field_one: [dict_1, dict_2, dict_3]
        first_dict = {"field_one": {"type": "type", "value": {"field_one_nested": {"type": "type", "value": "value1"}}}}
        second_dict = {"field_one": {"type": "type", "value": "value2"}}
        third_dict = {"field_one": {"type": "type", "value": {"field_two": {"type": "type", "value": {"_0": {"type": "type", "value": "nested_item_0"},
                                                                                                      "_1": {"type": "type", "value": "nested_item_1"},
                                                                                                      "_2": {"type": "type", "value": "nested_item_2"}}}}}}

        input_list = [{"list_1": {"type": "type", "value": {"_0": {"type": "type", "value": first_dict}}}},
                      {"list_1": {"type": "type", "value": {"_1": {"type": "type", "value": second_dict}}}},
                      {"list_1": {"type": "type", "value": {"_2": {"type": "type", "value": third_dict}}}}]

        expected_output = {"list_1": {"type": "type", "value": {"_0": {"type": "type", "value": first_dict},
                                                                "_1": {"type": "type", "value": second_dict},
                                                                "_2": {"type": "type", "value": third_dict}}}}

        self.assertEqual(expected_output, JoinSisl.join(input_list))


if __name__ == '__main__':
    unittest.main()
