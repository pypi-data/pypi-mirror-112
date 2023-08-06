# Copyright PA Knowledge Ltd 2021

from pysisl.deep_merger import ListTuple


class SislEncoder:

    @classmethod
    def dumps(cls, dict_to_encode):
        return "{" + cls._concatenate_sisl_triple(dict_to_encode) + "}"

    @classmethod
    def _concatenate_sisl_triple(cls, sisl_list):
        return ', '.join(cls._sisl_triple_list(sisl_list))

    @classmethod
    def _sisl_triple_list(cls, dict_to_encode):
        return [cls._construct_sisl_triple(k, v) for k, v in dict_to_encode.items()]

    @classmethod
    def _construct_sisl_triple(cls, key, value):
        return f"{key}: {cls._select_type_and_value(value)}"

    @classmethod
    def _select_type_and_value(cls, value):
        try:
            return {
                int: lambda val: f"!int \"{val}\"",
                float: lambda val: f"!float \"{val}\"",
                str: lambda val: f"!str \"{cls._escape(val)}\"",
                bool: lambda val: f"!bool \"{str(val).lower()}\"",
                list: lambda val: f"!list {{{cls._construct_sisl_for_list_object(val)}}}",
                dict: lambda val: f"!obj {cls.dumps(val)}",
                None.__class__: lambda val: f"!null \"\""
            }[type(value)](value)
        except KeyError as err:
            raise TypeValidationError(err)

    @classmethod
    def _escape(cls, value: str):
        return value.encode('unicode_escape').decode().replace(r'"', r'\"')

    @classmethod
    def _construct_sisl_for_list_object(cls, value):
        return ', '.join([cls._construct_sisl_triple(*cls._check_if_list_tuple(i, item)) for i, item in enumerate(value)])

    @classmethod
    def _check_if_list_tuple(cls, index, list_item):
        if type(list_item) is ListTuple:
            return f"_{list_item.position}", list_item.value

        return f"_{index}", list_item


class TypeValidationError(Exception):
    pass
