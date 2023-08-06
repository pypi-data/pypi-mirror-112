# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.explode_structure import ExplodeStructure
from pysisl.deep_merger import ListTuple


class ExplodeStructureTests(unittest.TestCase):

    def test_explode_structure_for_flat_list(self):
        self.assertEqual([{"field_one": [ListTuple("I", 0)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("I", 0)]}))

        self.assertEqual([{"field_one": [ListTuple("I", 0)]},
                          {"field_one": [ListTuple("I", 0), ListTuple("am", 1)]},
                          {"field_one": [ListTuple("I", 0), ListTuple("am", 1), ListTuple("a", 2)]},
                          {"field_one": [ListTuple("I", 0), ListTuple("am", 1), ListTuple("a", 2), ListTuple("list", 3)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("I", 0), ListTuple("am", 1), ListTuple("a", 2), ListTuple("list", 3)]}))

    def test_explode_structure_for_simple_dict(self):
        # {"field_one": "value_1", "field_two": "value_2"}
        self.assertEqual([{"field_one": "value_1"}, {"field_one": "value_1", "field_two": "value_2"}],
                         ExplodeStructure.explode_structure({"field_one": "value_1", "field_two": "value_2"}))

    def test_explode_structure_for_nested_list(self):
        # {"field_one": ["item_1", ["item_2"]]}
        self.assertEqual([{"field_one": [ListTuple("item_1", 0)]},
                          {"field_one": [ListTuple("item_1", 0), ListTuple([ListTuple("item_2", 0)], 1)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("item_1", 0),
                                                                                         ListTuple([ListTuple("item_2", 0)], 1)]}))

    def test_explode_structure_for_nested_list_with_multiple_items(self):
        # {"field_one": ["item_1", ["item_2", "item_3"]]}
        self.assertEqual([{"field_one": [ListTuple("item_1", 0)]},
                          {"field_one": [ListTuple("item_1", 0), ListTuple([ListTuple("item_2", 0)], 1)]},
                          {"field_one": [ListTuple("item_1", 0), ListTuple([ListTuple("item_2", 0),
                                                                            ListTuple("item_3", 1)], 1)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("item_1", 0),
                                                                                         ListTuple([ListTuple("item_2", 0),
                                                                                                    ListTuple("item_3", 1)], 1)]}))

    def test_explode_structure_for_nested_dicts(self):
        # {"field_one": {"nest_1": {"nest_2": "value_1", "nest_2_2": "value_2"}}}
        self.assertEqual([{"field_one": {"nest_1": {"nest_2": "value_1"}}},
                          {"field_one": {"nest_1": {"nest_2": "value_1", "nest_2_2": "value_2"}}}],
                         ExplodeStructure.explode_structure({"field_one": {"nest_1": {"nest_2": "value_1", "nest_2_2": "value_2"}}}))

    def test_explode_structure_preserves_list_item_indexing(self):
        # {"field_one": ["item_3", ["item_4"]]}
        self.assertEqual([{"field_one": [ListTuple("item_3", 2)]},
                          {"field_one": [ListTuple("item_3", 2), ListTuple("item_4", 3)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("item_3", 2),
                                                                                         ListTuple("item_4", 3)]}))

        self.assertEqual([{"field_one": [ListTuple("item_3", 2)]},
                          {"field_one": [ListTuple("item_3", 2), ListTuple([ListTuple("item_4", 0)], 3)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("item_3", 2),
                                                                                         ListTuple([ListTuple("item_4", 0)], 3)]}))

    def test_explode_structure_for_multi_nested_lists(self):
        # {"field_one": [50, "am", [[["a", "nested"]]], True]}
        self.assertEqual([{"field_one": [ListTuple(50, 0)]},
                          {"field_one": [ListTuple(50, 0), ListTuple("am", 1)]},
                          {"field_one": [ListTuple(50, 0), ListTuple("am", 1),
                                         ListTuple([ListTuple([ListTuple([ListTuple("a", 0)], 0)], 0)], 2)]},
                          {"field_one": [ListTuple(50, 0), ListTuple("am", 1),
                                         ListTuple([ListTuple([ListTuple([ListTuple("a", 0), ListTuple("nested", 1)], 0)], 0)], 2)]},
                          {"field_one": [ListTuple(50, 0), ListTuple("am", 1),
                                         ListTuple([ListTuple([ListTuple([ListTuple("a", 0), ListTuple("nested", 1)], 0)], 0)], 2),
                                         ListTuple(True, 3)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple(50, 0),
                                                                                         ListTuple("am", 1),
                                                                                         ListTuple([ListTuple([ListTuple([ListTuple("a", 0),
                                                                                                                          ListTuple("nested", 1)], 0)], 0)], 2),
                                                                                         ListTuple(True, 3)]}))

    def test_explode_structure_for_list_of_multi_nested_dicts(self):
        item_2_dict = {"item_2": {"nest_field_1": "nest_item_1_value"}}
        item_3_dict = {"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                     "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        item_4_dict = {"item_4": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                                  "nest_field_1_key_2": "nest_item_2"},
                       "item_4_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}

        input_dict = {"list_one": [ListTuple("item_0", 0), ListTuple("item_1", 1), ListTuple(item_2_dict, 2), ListTuple(item_3_dict, 3), ListTuple(item_4_dict, 4)]}

        self.assertEqual([{"list_one": [ListTuple("item_0", 0)]},
                          {"list_one": [ListTuple("item_0", 0), ListTuple("item_1", 1)]},
                          {"list_one": [ListTuple("item_0", 0), ListTuple("item_1", 1), ListTuple({"item_2": {"nest_field_1": "nest_item_1_value"}}, 2)]},
                          {"list_one": [ListTuple("item_0", 0), ListTuple("item_1", 1), ListTuple({"item_2": {"nest_field_1": "nest_item_1_value"}}, 2),
                                        ListTuple({"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"}}}}}}, 3)]},
                          {"list_one": [ListTuple("item_0", 0), ListTuple("item_1", 1), ListTuple({"item_2": {"nest_field_1": "nest_item_1_value"}}, 2),
                                        ListTuple({"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}, 3)]},
                          {"list_one": [ListTuple("item_0", 0),
                                        ListTuple("item_1", 1),
                                        ListTuple({"item_2": {"nest_field_1": "nest_item_1_value"}}, 2),
                                        ListTuple({"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}, 3),
                                        ListTuple({"item_4": {"nest_field_1": {"nest_field_2": "nest_field_2_value"}}}, 4)]},
                          {"list_one": [ListTuple("item_0", 0),
                                        ListTuple("item_1", 1),
                                        ListTuple({"item_2": {"nest_field_1": "nest_item_1_value"}}, 2),
                                        ListTuple({"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}, 3),
                                        ListTuple({"item_4": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                                                              "nest_field_1_key_2": "nest_item_2"}}, 4)]},
                          {"list_one": [ListTuple("item_0", 0),
                                        ListTuple("item_1", 1),
                                        ListTuple({"item_2": {"nest_field_1": "nest_item_1_value"}}, 2),
                                        ListTuple({"item_3": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}, 3),
                                        ListTuple({"item_4": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                                                              "nest_field_1_key_2": "nest_item_2"},
                                                   "item_4_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}, 4)]}],
                         ExplodeStructure.explode_structure(input_dict))

    def test_explode_structure_handles_dict_of_nested_dicts(self):
        dict_1 = {"field_1": {"nest_field_1": "nest_item_1_value"}}
        dict_2 = {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                 "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}
        dict_3 = {"field_3": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                              "nest_field_1_key_2": "nest_item_2"},
                  "field_3_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}

        input_dict = {"dict_1": dict_1, "dict_2": dict_2, "dict_3": dict_3}
        self.assertEqual([{"dict_1": {"field_1": {"nest_field_1": "nest_item_1_value"}}},
                          {"dict_1": {"field_1": {"nest_field_1": "nest_item_1_value"}},
                           "dict_2": {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"}}}}}}},
                          {"dict_1": {"field_1": {"nest_field_1": "nest_item_1_value"}},
                           "dict_2": {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                     "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}}},
                          {"dict_1": {"field_1": {"nest_field_1": "nest_item_1_value"}},
                           "dict_2": {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                     "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}},
                           "dict_3": {"field_3": {"nest_field_1": {"nest_field_2": "nest_field_2_value"}}}},
                          {"dict_1": {"field_1": {"nest_field_1": "nest_item_1_value"}},
                           "dict_2": {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                     "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}},
                           "dict_3": {"field_3": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                                                  "nest_field_1_key_2": "nest_item_2"}}},
                          {"dict_1": {"field_1": {"nest_field_1": "nest_item_1_value"}},
                           "dict_2": {"field_2": {"nest_field_1": {"nest_field_2": {"nest_field_3": {"nest_field_4": {"nest_field_5": "nest_field_5_value"},
                                                                                                     "nest_field_4_key_2": {"nest_field_5_key_2": "nest_field_5_value_2"}}}}}},
                           "dict_3": {"field_3": {"nest_field_1": {"nest_field_2": "nest_field_2_value"},
                                                  "nest_field_1_key_2": "nest_item_2"},
                                      "field_3_key_2": {"nest_field_3_key_2": "nest_field_3_key_2_value_2"}}}],
                         ExplodeStructure.explode_structure(input_dict))

    def test_explode_structure_for_list_of_nested_lists_and_dicts(self):
        # {"field_one": ["A", [["nested", "list"]], "item"], {"lvl1": {"lvl2": {"item_1": "nested",
                                                                              # "item_2": [["item_2_nested"]]}}}]}
        self.assertEqual([{"field_one": [ListTuple("A", 0)]},
                          {"field_one": [ListTuple("A", 0), ListTuple([ListTuple([ListTuple([ListTuple("nested", 0)], 0)], 0)], 1)]},
                          {"field_one": [ListTuple("A", 0),
                                         ListTuple([ListTuple([ListTuple([ListTuple("nested", 0), ListTuple("list", 1)], 0)], 0)], 1)]},
                          {"field_one": [ListTuple("A", 0),
                                         ListTuple([ListTuple([ListTuple([ListTuple("nested", 0), ListTuple("list", 1)], 0)], 0), ListTuple("item", 1)], 1)]},
                          {"field_one": [ListTuple("A", 0),
                                         ListTuple([ListTuple([ListTuple([ListTuple("nested", 0), ListTuple("list", 1)], 0)], 0), ListTuple("item", 1)], 1),
                                         ListTuple({"lvl1": {"lvl2": {"item_1": "nested"}}}, 2)]},
                          {"field_one": [ListTuple("A", 0),
                                         ListTuple([ListTuple([ListTuple([ListTuple("nested", 0), ListTuple("list", 1)], 0)], 0), ListTuple("item", 1)], 1),
                                         ListTuple({"lvl1": {"lvl2": {"item_1": "nested", "item_2": ListTuple([ListTuple([ListTuple("item_2_nested", 0)], 0)], 0)}}}, 2)]}],
                         ExplodeStructure.explode_structure({"field_one": [ListTuple("A", 0),
                                                                                         ListTuple([ListTuple([ListTuple([ListTuple("nested", 0),
                                                                                                                          ListTuple("list", 1)], 0)], 0),
                                                                                                    ListTuple("item", 1)], 1),
                                                                                         ListTuple({"lvl1": {"lvl2": {"item_1": "nested", "item_2": ListTuple([ListTuple([ListTuple("item_2_nested", 0)], 0)], 0)}}}, 2)]}))

    # def test_explode_structure_handles_wide_and_deep_nested_mixtures_of_lists_and_dicts(self):
    #     nested_dict = {"lvl1": {"lvl2_1": {"lvl3": "value_6"},
    #                             "lvl2_2": "value_7",
    #                             "lvl2_3": [["value_8"],
    #                                        {"lvl3": {"lvl4": "value_9"}},
    #                                        {"lvl3": "value_10"}]},
    #                    "lvl1_2": {"lvl2_1": "value_11"},
    #                    "lvl1_3": {"lvl2_1": {"lvl3_1": {"lvl4_1": "value_12"}}}}
    #     main_dict = {"nested_dict": nested_dict}
    #
    #     self.assertEqual([{"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}}}},
    #                       {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}, "lvl2_2": "value_7"}}},
    #                       {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}, "lvl2_2": "value_7", "lvl2_3": [ListTuple([ListTuple("value_8", 0)], 0)]}}},
    #                       {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}, "lvl2_2": "value_7", "lvl2_3": [ListTuple([ListTuple("value_8", 0)], 0), ListTuple({"lvl3": {"lvl4": "value_9"}}, 1)]}}},
    #                       {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}, "lvl2_2": "value_7", "lvl2_3": [ListTuple([ListTuple("value_8", 0)], 0), ListTuple({"lvl3": {"lvl4": "value_9"}}, 1), ListTuple({"lvl3": "value_10"}, 2)]}}},
    #                       {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}, "lvl2_2": "value_7", "lvl2_3": [ListTuple([ListTuple("value_8", 0)], 0), ListTuple({"lvl3": {"lvl4": "value_9"}}, 1), ListTuple({"lvl3": "value_10"}, 2)]}, "lvl1_2": {"lvl2_1": "value_11"}}},
    #                       {"nested_dict": {"lvl1": {"lvl2_1": {"lvl3": "value_6"}, "lvl2_2": "value_7", "lvl2_3": [ListTuple([ListTuple("value_8", 0)], 0), ListTuple({"lvl3": {"lvl4": "value_9"}}, 1), ListTuple({"lvl3": "value_10"}, 2)]}, "lvl1_2": {"lvl2_1": "value_11"}, "lvl1_3": {"lvl2_1": {"lvl3_1": {"lvl4_1": "value_12"}}}}}],
    #                      ExplodeStructure.explode_structure(main_dict))


if __name__ == '__main__':
    unittest.main()
