# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.deep_merger import DeepMerger, ListTuple


class ExplodeStructureTests(unittest.TestCase):
    def test_merge_appends_flat_dicts_as_items_in_list(self):
        # [{"dict_1": "value_1"}, {"dict_2": "value_2"}, {"dict_3": "value_3"}]
        base = [{"list_one": [ListTuple({"dict_1": "value_1"}, 0), ListTuple({"dict_2": "value_2"}, 1)]}]
        nxt = {'list_one': [ListTuple(value={'dict_3': 'value_3'}, position=2)]}
        self.assertEqual({"list_one": [ListTuple({"dict_1": "value_1"}, 0),
                                       ListTuple({"dict_2": "value_2"}, 1),
                                       ListTuple({'dict_3': 'value_3'}, 2)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_nested_list_within_list(self):
        # ["item1", "item2"]
        base = [{"lvl1": [ListTuple("item1", 0)]}]
        nxt = {'lvl1': [ListTuple("item_2", 1)]}
        self.assertEqual({'lvl1': [ListTuple("item1", 0), ListTuple("item_2", 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_deeply_nested_list_within_list(self):
        # ['item_1', [[['item_2']]]]
        base = [{"lvl1": [ListTuple("item1", 0)]}]
        nxt = {'lvl1': [ListTuple([ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 0)], 1)]}
        self.assertEqual({'lvl1': [ListTuple("item1", 0), ListTuple([ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 0)], 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_after_nested_list(self):
        # ['item_1', [[['item_2']]], "item_3"]
        base = [{'lvl1': [ListTuple('item_1', 0), ListTuple([ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 0)], 1)]}]
        self.assertEqual({'lvl1': [ListTuple('item_1', 0), ListTuple([ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 0)], 1), ListTuple("item_3", 2)]},
                         DeepMerger.merge(base, {'lvl1': [ListTuple("item_3", 2)]}))

    def test_merger_appends_within_nested_list(self):
        # ['item_1', ['item_2', "item_3"]]
        base = [{'lvl1': [ListTuple("item_1", 0), ListTuple([ListTuple('item_2', 0)], 1)]}]
        nxt = {'lvl1': [ListTuple([ListTuple("item_3", 1)], 1)]}
        self.assertEqual({'lvl1': [ListTuple('item_1', 0), ListTuple([ListTuple('item_2', 0), ListTuple('item_3', 1)], 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_merges_dicts_with_a_single_key_value_pair(self):
        # [item_1, {"lvl2" : "item_2"}, {"lvl3" : "item_3"}]
        base = [{'lvl1': [ListTuple('item_1', 0), ListTuple({"lvl2": "item_2"}, 1)]}]
        nxt = {'lvl1': [ListTuple({"lvl3": "item_3"}, 2)]}
        self.assertEqual({'lvl1': [ListTuple('item_1', 0), ListTuple({"lvl2": "item_2"}, 1), ListTuple({"lvl3": "item_3"}, 2)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_merges_dicts_with_multiple_key_value_pairs(self):
        # {lvl1: [item_1, {"lvl2" : "item_2", "lvl3" : "item_3"}]}
        base = [{'lvl1': [ListTuple('item_1', 0), ListTuple({"lvl2": "item_2"}, 1)]}]
        nxt = {'lvl1': [ListTuple({"lvl3": "item_3"}, 1)]}
        self.assertEqual({'lvl1': [ListTuple('item_1', 0), ListTuple({"lvl2": "item_2", "lvl3": "item_3"}, 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_merges_lists_at_depth(self):
        # ["item_0", ["item_1", [["item_2"]]]]
        base = [{"nested_list_1": [ListTuple("item_0", 0), ListTuple([ListTuple("item_1", 0)], 1)]}]
        nxt = {"nested_list_1": [ListTuple([ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 1)], 1)]}
        self.assertEqual({"nested_list_1": [ListTuple("item_0", 0),
                                            ListTuple([ListTuple("item_1", 0), ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 1)], 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_dict_at_correct_depth_when_previous_element_is_deeper(self):
        # {'nested_list_1': ['item_0', ['item_1', [['item_2']], {'item_3': {'lvl1': 'value_5'}}]]}
        base = [{'nested_list_1': [ListTuple("item_0", 0),
                                   ListTuple([ListTuple("item_1", 0), ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 1)], 1)]}]
        nxt = {'nested_list_1': [ListTuple([ListTuple({'item_3': {'lvl1': 'value_5'}}, 2)], 1)]}
        self.assertEqual({'nested_list_1': [ListTuple("item_0", 0),
                                            ListTuple([ListTuple("item_1", 0),
                                                       ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 1),
                                                       ListTuple({'item_3': {'lvl1': 'value_5'}}, 2)], 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_merges_dicts_with_lists(self):
        # {"lvl1": {"lvl2": {"lvl3_1": "value_1", "lvl3_2": [["value_2"]]
        base = [{'lvl1': {'lvl2': {'lvl3_1': 'value_1'}}}]
        nxt = {'lvl1': {'lvl2': {'lvl3_2': [ListTuple([ListTuple('value_2', 0)], 0)]}}}
        self.assertEqual({"lvl1": {"lvl2": {"lvl3_1": "value_1", "lvl3_2": [ListTuple([ListTuple('value_2', 0)], 0)]}}},
                         DeepMerger.merge(base, nxt))

    def test_merger_merges_dicts_with_nested_lists(self):
        # {"lvl1": {"lvl2": {"lvl3_1": "value_1", "lvl3_2": ["value_2", ['value_3]]}
        base = [{'lvl1': {'lvl2': {'lvl3_1': 'value_1', 'lvl3_2': [ListTuple("value_2", 0)]}}}]
        nxt = {'lvl1': {'lvl2': {'lvl3_2': [ListTuple([ListTuple('value_3', 0)], 1)]}}}
        self.assertEqual({"lvl1": {"lvl2": {"lvl3_1": 'value_1', "lvl3_2": [ListTuple("value_2", 0), ListTuple([ListTuple('value_3', 0)], 1)]}}},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_list_to_dict(self):
        # {"lvl1": {"lvl2": {"lvl3_1": {'key_1': ['value_1']},
        #                    "lvl3_2": {"lvl4_1": "value_2"},
        #                    "lvl3_3": [['value_3']]}}}

        base = [{'lvl1': {'lvl2': {'lvl3_1': {'key_1': [ListTuple('value_1', 0)]}, 'lvl3_2': {"lvl4_1": "value_2"}}}}]
        nxt = {'lvl1': {'lvl2': {'lvl3_3': [ListTuple([ListTuple('value_3', 0)], 0)]}}}
        self.assertEqual({"lvl1": {"lvl2": {"lvl3_1": {'key_1': [ListTuple('value_1', 0)]}, "lvl3_2": {"lvl4_1": "value_2"},
                                            "lvl3_3": [ListTuple([ListTuple('value_3', 0)], 0)]}}},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_list_to_dict_when_previous_element_is_list(self):
        # {"lvl1": {"lvl2": {"lvl3_1": ['value_1'],
        #                    "lvl3_2": [['value_2']]}}}

        base = [{'lvl1': {'lvl2': {'lvl3_1': [ListTuple('value_1', 0)]}}}]
        nxt = {'lvl1': {'lvl2': {'lvl3_2': [ListTuple([ListTuple('value_2', 0)], 0)]}}}
        self.assertEqual({"lvl1": {"lvl2": {"lvl3_1": [ListTuple('value_1', 0)], "lvl3_2": [ListTuple([ListTuple('value_2', 0)], 0)]}}},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_to_an_entire_list_at_depth(self):
        # {"nested_list_1": ["item1", 50, True, ["item2_1", "item2_2", {"item2_3": "value_1"}]]}
        base = [{"nested_list_1": [ListTuple("item1", 0), ListTuple(50, 1), ListTuple(True, 2), ListTuple([ListTuple("item2_1", 0), ListTuple("item2_2", 1)], 3)]}]
        nxt = {'nested_list_1': [ListTuple([ListTuple({'item2_3': 'value_1'}, 2)], 3)]}
        self.assertEqual({"nested_list_1": [ListTuple("item1", 0), ListTuple(50, 1), ListTuple(True, 2), ListTuple([ListTuple("item2_1", 0), ListTuple("item2_2", 1), ListTuple({'item2_3': 'value_1'}, 2)], 3)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_to_multiple_nested_list(self):
        # ["item_0", ["item_1", [["item_2", "item_3]]]]
        base = [{"nested_list_1": [ListTuple("item_0", 0),
                                   ListTuple([ListTuple("item_1", 0), ListTuple([ListTuple([ListTuple("item_2", 0)], 0)], 1)], 1)]}]
        nxt = {"nested_list_1": [ListTuple([ListTuple([ListTuple([ListTuple("item_3", 1)], 0)], 1)], 1)]}

        self.assertEqual({"nested_list_1": [ListTuple("item_0", 0),
                                            ListTuple([ListTuple("item_1", 0), ListTuple([ListTuple([ListTuple("item_2", 0), ListTuple("item_3", 1)], 0)], 1)], 1)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_dicts_in_nested_dicts_inside_a_list_item(self):
        # {'list1': [{'item_0': {'lvl1': {'lvl2_1': {'lvl3_1': 'value_1'},
        #                                 'lvl2_2': {'lvl3_2': 'value_2'}}}}]}

        base = [{'list1': [ListTuple({'item_0': {'lvl1': {'lvl2_1': {'lvl3_1': 'value_1'}}}}, 0)]}]
        nxt = {'list1': [ListTuple({'item_0': {'lvl1': {'lvl2_2': {'lvl3_2': 'value_2'}}}}, 0)]}
        self.assertEqual({'list1': [ListTuple({'item_0': {'lvl1': {'lvl2_1': {'lvl3_1': 'value_1'},
                                                         'lvl2_2': {'lvl3_2': 'value_2'}}}}, 0)]},
                         DeepMerger.merge(base, nxt))

    def test_merger_appends_dicts_in_dicts_inside_lists(self):
        # {'list1': [{'lvl1': {'list2': [{'item1': {'key1': 'value_1'},
        #                                 'item2': {'key2': 'value_2'}}]}}]}
        base = [{'list1': [ListTuple({'lvl1': {'list2': [ListTuple({'item1': {'key1': 'value_1'}}, 0)]}}, 0)]}]
        nxt = {'list1': [ListTuple({'lvl1': {'list2': [ListTuple({'item2': {'key2': 'value_2'}}, 0)]}}, 0)]}

        self.assertEqual({'list1': [ListTuple({'lvl1': {'list2': [ListTuple({'item1': {'key1': 'value_1'},
                                                                             'item2': {'key2': 'value_2'}}, 0)]}}, 0)]},
                         DeepMerger.merge(base, nxt))


if __name__ == '__main__':
    unittest.main()
