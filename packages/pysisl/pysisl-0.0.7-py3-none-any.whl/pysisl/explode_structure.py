# Copyright PA Knowledge Ltd 2021

from pysisl.deep_merger import DeepMerger, ListTuple


class ExplodeStructure:
    @classmethod
    def explode_structure(cls, structure, initial_explode=False):
        if initial_explode is True:
            leaves = cls.enum_paths_with_list_tuple(structure)
        else:
            leaves = cls.enum_paths(structure)

        output_list = [[next(leaves)][0]]

        for ii, each_element in enumerate(leaves):
            output_list.append(DeepMerger.merge(output_list, each_element))
        return output_list

    @classmethod
    def enum_paths_with_list_tuple(cls, p):
        if type(p) is list:
            for ii, list_item in enumerate(p):
                for item in cls.enum_paths_with_list_tuple(list_item):
                    yield [ListTuple(item, ii)]
        elif type(p) is dict:
            for key, value in p.items():
                for x in cls.enum_paths_with_list_tuple(value):
                    yield {key: x}
        else:
            yield p

    @classmethod
    def enum_paths(cls, p):
        if type(p) is list:
            for ii, list_item in enumerate(p):
                for item in cls.enum_paths(list_item):
                    yield [item]
        elif type(p) is dict:
            for key, value in p.items():
                for x in cls.enum_paths(value):
                    yield {key: x}
        elif type(p) is ListTuple:
            if type(p.value) is dict or type(p.value) is list:
                for value in cls.enum_paths(p.value):
                    yield ListTuple(value, p.position)
            else:
                yield p
        else:
            yield p
