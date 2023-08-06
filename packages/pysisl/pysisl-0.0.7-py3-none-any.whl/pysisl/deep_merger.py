# Copyright PA Knowledge Ltd 2021

from deepmerge import Merger
from collections import namedtuple
import copy
ListTuple = namedtuple('ListTuple', ['value', 'position'])


class DeepMerger:
    @classmethod
    def merge(cls, base, nxt):
        base_copy = copy.deepcopy(base[-1])
        deep_merger = Merger([(list, cls.list_strategy), (dict, ["merge"])], ["override"], ["override"])
        deep_merger.merge(base_copy, nxt)
        return base_copy

    @classmethod
    def list_strategy(cls, config, path, base, nxt):
        list_merger = Merger([(list, cls.list_strategy), (dict, ["merge"])], ["override"], ["override"])

        if nxt[0].position == base[-1].position:
            cls.merge_list_tuples(base, nxt, list_merger)
        else:
            base.append(nxt[0])

        return base

    @classmethod
    def merge_list_tuples(cls, base, nxt, list_tuple_merger):
        if type(base[-1].value) is dict and type(nxt[0].value) is dict:
            list_tuple_merger.merge(base[-1].value, nxt[0].value)
        else:
            # remove outer ListTuple
            base = base[-1].value
            nxt = nxt[0].value

            if nxt[0].position == base[-1].position:
                cls.merge_list_tuples(base, nxt, list_tuple_merger)
            else:
                base.append(nxt[0])

        return base

