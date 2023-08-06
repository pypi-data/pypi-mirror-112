# Copyright PA Knowledge Ltd 2021

from .explode_structure import ExplodeStructure


class RemoveData:

    @classmethod
    def subtract_data_from_input(cls, current_input, sisl_dict_elements_to_delete):
        leaves_to_delete = ExplodeStructure.enum_paths(sisl_dict_elements_to_delete)

        return cls.remove_matching_elements(current_input, leaves_to_delete)

    @classmethod
    def remove_matching_elements(cls, current_input, leaves_to_delete):
        for each_leaf in leaves_to_delete:
            current_input = cls.do_remove(current_input, each_leaf)

        return current_input

    @classmethod
    def do_remove(cls, current_input, each_leaf):
        if hasattr(each_leaf, 'items'):
            cls.handle_each_dict(current_input, each_leaf)
        else:
            cls.handle_each_list(current_input, each_leaf)

        return current_input

    @classmethod
    def handle_each_dict(cls, current_input, each_leaf):
        for key in each_leaf:
            if hasattr(each_leaf[key], 'items'):
                cls.do_remove(current_input[key], each_leaf[key])
                if current_input[key] == {}:
                    del current_input[key]
            if type(each_leaf[key]) is list:
                if hasattr(each_leaf[key][0].value, 'items'):
                    cls.do_remove(current_input[key][0].value, each_leaf[key][0].value)
                    if current_input[key][0].value == {}:
                        current_input[key].pop(0)

                if type(each_leaf[key][0].value) is list:
                    cls.do_remove(current_input[key][0].value, each_leaf[key][0].value)

                    if not current_input[key][0].value:
                        current_input[key].pop(0)

                if not current_input[key]:
                    del current_input[key]

            if key in current_input and each_leaf[key] == current_input[key]:
                del current_input[key]

            elif key in current_input and type(each_leaf[key]) is list and each_leaf[key][0] in current_input[key]:
                current_input[key].pop(0)

    @classmethod
    def handle_each_list(cls, current_input, each_leaf):
        for index, value in enumerate(each_leaf):
            if hasattr(each_leaf[index].value, 'items'):
                cls.do_remove(current_input[index].value, each_leaf[index].value)
                if current_input[index].value == {}:
                    del current_input[index]
            if type(each_leaf[index].value) is list:
                cls.do_remove(current_input[index].value, each_leaf[index].value)
                if not current_input[index].value:
                    current_input.pop(0)
            if each_leaf[index] in current_input:
                current_input.pop(0)
