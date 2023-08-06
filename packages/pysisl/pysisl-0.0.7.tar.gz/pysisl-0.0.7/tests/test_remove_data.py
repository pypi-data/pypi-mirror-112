# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.remove_data import RemoveData
from pysisl.deep_merger import ListTuple


class RemoveDataTests(unittest.TestCase):
    def test_remove_only_key_value_pair_in_dict(self):
        self.assertEqual({}, RemoveData.subtract_data_from_input({"field_one": "I"}, {"field_one": "I"}))

    def test_remove_simple_key_value_pair(self):
        self.assertEqual({"field_two": "a"},
                         RemoveData.subtract_data_from_input({"field_one": "I", "field_two": "a"}, {"field_one": "I"}))

    def test_remove_part_of_list(self):
        self.assertEqual({"field_one": [ListTuple("a", 2), ListTuple("list", 3)]},
                         RemoveData.subtract_data_from_input({"field_one": [ListTuple("I", 0), ListTuple("am", 1),
                                                                            ListTuple("a", 2), ListTuple("list", 3)]},
                                                             {"field_one": [ListTuple("I", 0), ListTuple("am", 1)]}))

    def test_remove_two_dicts_from_list_of_dicts(self):
        # {"list_one": [{"item_1": "value_1"}, {"item_2": "value_2"}, {"item_3": "value_3"}]}
        input_dict = {"list_one": [ListTuple({"item_1": "value_1"}, 0), ListTuple({"item_2": "value_2"}, 1), ListTuple({"item_3": "value_3"}, 2)]}
        section_to_remove = {"list_one": [ListTuple({"item_1": "value_1"}, 0), ListTuple({"item_2": "value_2"}, 1)]}
        expected_output = {"list_one": [ListTuple({"item_3": "value_3"}, 2)]}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_single_nested_dict_from_list_of_dicts(self):
        # {"list_one": [{"item_1": "value_1"}, {"item_2": {"item_2_nested": "value_2"}}, {"item_3": "value_3"}]}
        input_dict = {"list_one": [ListTuple({"item_1": "value_1"}, 0), ListTuple({"item_2": {"item_2_nested": "value_2"}}, 1), ListTuple({"item_3": "value_3"}, 2)]}
        section_to_remove = {"list_one": [ListTuple({"item_1": "value_1"}, 0), ListTuple({"item_2": {"item_2_nested": "value_2"}}, 1)]}
        expected_output = {"list_one": [ListTuple({"item_3": "value_3"}, 2)]}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_items_at_different_nesting_levels(self):
        # {"list_one": ["item_1", ["item_2, "item_3"], "item_4"]}
        self.assertEqual({"list_one": [ListTuple([ListTuple("item_3", 1)], 1), ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple("item_2", 0), ListTuple("item_3", 1)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0), ListTuple([ListTuple("item_2", 0)], 1)]}))

    def test_remove_deeply_nested_item_in_list(self):
        # {"list_one": [[["item_1"]], "item_2]}
        self.assertEqual({"list_one": [ListTuple("item_2", 1)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple([ListTuple([ListTuple([ListTuple("item_1", 0)], 0)], 0)], 0),
                                                                           ListTuple("item_2", 1)]},
                                                             {"list_one": [ListTuple([ListTuple([ListTuple([ListTuple("item_1", 0)], 0)], 0)], 0)]}))

    def test_remove_nested_and_non_nested_items_in_list(self):
        # {"list_one": ["item_1", ["item_2, "item_3"], "item_4"]}
        self.assertEqual({"list_one": [ListTuple([ListTuple("item_3", 1)], 1), ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple("item_2", 0), ListTuple("item_3", 1)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0), ListTuple([ListTuple("item_2", 0)], 1)]}))

    def test_remove_nested_dict_inside_of_nested_list(self):
        # {"list_one": ["item_1", [{"item_2": {"item_2_2": "item_2_2_value"}}, "item_3"], "item_4"]}
        self.assertEqual({"list_one": [ListTuple([ListTuple("item_3", 1)], 1), ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple({"item_2": {"item_2_2": "item_2_2_value"}}, 0), ListTuple("item_3", 1)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0), ListTuple([ListTuple({"item_2": {"item_2_2": "item_2_2_value"}}, 0)], 1)]}))

    def test_remove_list_items_that_are_nested_within_a_nested_dict(self):
        # {"list_one": ["item_1", [{"item_2": {"item_2_2": ["value_2_2_0", "value_2_2_1", "value_2_2_2"]}}, "item_3"], "item_4"]}
        self.assertEqual({"list_one": [ListTuple([ListTuple({"item_2": {"item_2_2": [ListTuple("value_2_2_2", 2)]}}, 0), ListTuple("item_3", 1)], 1), ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple({"item_2": {"item_2_2": [ListTuple("value_2_2_0", 0),
                                                                                                                         ListTuple("value_2_2_1", 1),
                                                                                                                         ListTuple("value_2_2_2", 2)]}}, 0),
                                                                                      ListTuple("item_3", 1)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple({"item_2": {"item_2_2": [ListTuple("value_2_2_0", 0),
                                                                                                                         ListTuple("value_2_2_1", 1)]}}, 0)], 1)]}))

    def test_remove_nested_list_item_that_is_nested_within_a_list(self):
        # {"list_one": ["item_1", [["item_2", "item_3"]], "item_4"]}
        self.assertEqual({"list_one": [ListTuple([ListTuple([ListTuple("item_3", 1)], 0)], 1),
                                       ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple([ListTuple("item_2", 0),
                                                                                                 ListTuple("item_3", 1)], 0)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 1)]}))

    def test_remove_dict_key_value_pairs_nested_in_list_item_that_is_nested_within_a_list(self):
        # {"list_one": ["item_1", [{"item_2": {"item_2_1": {"item_2_2": "value_1", "item_2_3": "value_3"}}}, "item_3"], "item_4"]}
        self.assertEqual({"list_one": [ListTuple([ListTuple("item_3", 1)], 1),
                                       ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple({"item_2": {"item_2_1": {"item_2_2": "value_1", "item_2_3": "value_3"}}}, 0),
                                                                                                 ListTuple("item_3", 1)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple({"item_2": {"item_2_1": {"item_2_2": "value_1", "item_2_3": "value_3"}}}, 0)], 1)]}))

    def test_remove_deeply_nested_item_inside_nested_list(self):
        # {"list_one": ["item_1", ["item_2, [["item_3"]]], "item_4"]}
        self.assertEqual({"list_one": [ListTuple("item_4", 2)]},
                         RemoveData.subtract_data_from_input({"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple("item_2", 0), ListTuple([ListTuple([ListTuple("item_3", 0)], 0)], 1)], 1),
                                                                           ListTuple("item_4", 2)]},
                                                             {"list_one": [ListTuple("item_1", 0),
                                                                           ListTuple([ListTuple("item_2", 0),
                                                                                      ListTuple([ListTuple([ListTuple("item_3", 0)], 0)], 1)], 1)]}))

    def test_remove_part_of_list_that_contains_nested_dicts(self):
        input_dict = {"list_one": [ListTuple({"item_0": {"field_5_1": "field_5_value_1", "field_5_2": "field_5_value_2"}}, 0)]}

        section_to_remove = {"list_one": [ListTuple({"item_0": {"field_5_1": "field_5_value_1"}}, 0)]}
        expected_output = {"list_one": [ListTuple({"item_0": {"field_5_2": "field_5_value_2"}}, 0)]}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_several_parts_of_list_that_contains_nested_dicts(self):
        input_dict = {"list_one": [ListTuple({"item_0": {"field_5_1": "field_5_value_1", "field_5_2": "field_5_value_2"}}, 0)]}

        section_to_remove = {"list_one": [ListTuple({"item_0": {"field_5_1": "field_5_value_1", "field_5_2": "field_5_value_2"}}, 0)]}
        expected_output = {}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_section_of_list_that_contains_nested_dicts(self):
        input_dict = {"list_one": [ListTuple({"item_0": {"field_5_1": "field_5_value_1", "field_5_2": "field_5_value_2"},
                                              "item_1": [ListTuple({"field_6_1": "field_6_value_1"}, 0)]}, 0)]}

        section_to_remove = {"list_one": [ListTuple({"item_1": [ListTuple({"field_6_1": "field_6_value_1"}, 0)]}, 0)]}
        expected_output = {"list_one": [ListTuple({"item_0": {"field_5_1": "field_5_value_1", "field_5_2": "field_5_value_2"}}, 0)]}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_single_key_value_pair_of_nested_dict(self):
        # {"field_one": {"nest_1": {"nest_2": "value_1", "nest_2_2": "value_2"}}}
        input_dict = {"field_one": {"nest_1": {"nest_2": "value_1", "nest_2_2": "value_2"}}}
        section_to_remove = {"field_one": {"nest_1": {"nest_2": "value_1"}}}
        expected_output = {"field_one": {"nest_1": {"nest_2_2": "value_2"}}}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_single_key_value_pair_of_deeply_nested_dict(self):
        dict_1 = {"field_1": {"nest_field_1": "nest_item_1_value"}}
        dict_2 = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        dict_3 = {"field_3": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                              "nest_field_1_key_2": "nest_item_2"},
                  "field_3_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}

        input_dict = {"dict_1": dict_1, "dict_2": dict_2, "dict_3": dict_3}

        section_to_remove = {"dict_2": {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"}}}}}}}

        dict_2_output = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        expected_output = {"dict_1": dict_1, "dict_2": dict_2_output, "dict_3": dict_3}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_single_key_value_pair_of_deeply_nested_dict_of_single_item_in_list(self):
        dict_2 = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}

        input_dict = {"list_one": [ListTuple(dict_2, 0)]}

        section_to_remove = {"list_one": [ListTuple({"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"}}}}}}, 0)]}

        dict_2_output = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        expected_output = {"list_one": [ListTuple(dict_2_output, 0)]}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))

    def test_remove_items_in_a_list_that_include_single_key_value_pair_of_deeply_nested_dict_in_a_list(self):
        dict_1 = {"field_1": {"nest_field_1": "nest_item_1_value"}}
        dict_2 = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        dict_3 = {"field_3": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                              "nest_field_1_key_2": "nest_item_2"},
                  "field_3_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}

        input_dict = {"list_one": [ListTuple(dict_1, 0), ListTuple(dict_2, 1), ListTuple(dict_3, 2)]}

        section_to_remove = {"list_one": [ListTuple({"field_1": {"nest_field_1": "nest_item_1_value"}}, 0), ListTuple({"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"}}}}}}, 1)]}

        dict_2_output = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        expected_output = {"list_one": [ListTuple(dict_2_output, 1), ListTuple(dict_3, 2)]}

        self.assertEqual(expected_output, RemoveData.subtract_data_from_input(input_dict, section_to_remove))


if __name__ == '__main__':
    unittest.main()
