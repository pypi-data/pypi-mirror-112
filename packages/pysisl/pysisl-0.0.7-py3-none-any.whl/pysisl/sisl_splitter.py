# Copyright PA Knowledge Ltd 2021

from pysisl.sisl_encoder import SislEncoder
from pysisl.explode_structure import ExplodeStructure
from pysisl.remove_data import RemoveData


class SplitSisl:
    def __init__(self, max_length=1000000):
        self.max_length = max_length

    def split_sisl(self, input_dict):
        sisl_file = []
        input_dict = ExplodeStructure.explode_structure(input_dict, initial_explode=True)[-1]

        while len(input_dict) > 0:
            sisl_file.append(self.generate_next_file(input_dict))
        return sisl_file

    def generate_next_file(self, input_dict):
        potential_sisl_file_candidates = ExplodeStructure.explode_structure(input_dict)

        test_sisl_file, successful_struct = self.try_a_sisl_file(potential_sisl_file_candidates, self.max_length)

        RemoveData.subtract_data_from_input(input_dict, successful_struct)

        return test_sisl_file

    @staticmethod
    def try_a_sisl_file(list_of_potential_sisl_files, max_bytes):
        trial_sisl = SislEncoder.dumps(list_of_potential_sisl_files[0])

        if len(trial_sisl) > max_bytes:
            raise Exception(f"Unable to split input. {trial_sisl} is greater than max size. ")

        previous_element = list_of_potential_sisl_files[0]
        for e in list_of_potential_sisl_files:
            test_sisl = SislEncoder.dumps(e)
            if len(test_sisl.encode('utf-8')) > max_bytes:
                return trial_sisl, previous_element
            else:
                trial_sisl = test_sisl
                previous_element = e

        return trial_sisl, list_of_potential_sisl_files[-1]






