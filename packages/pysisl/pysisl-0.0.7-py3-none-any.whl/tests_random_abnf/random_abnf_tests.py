# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_encoder import SislEncoder
from pysisl.sisl_decoder import SislDecoder
import subprocess
import os


class RandomABNFTests(unittest.TestCase):
    def test_basic_sisl_parsed_through_pysisl(self):
        for abnf_generated_file in os.listdir("test_files/"):
            with open(f"test_files/{abnf_generated_file}", "r") as input_sisl:
                test_sisl = r'{}'.format((input_sisl.read()))
            converted = SislEncoder.dumps(SislDecoder().parse_raw_types(test_sisl))
            with open(f"test_output_files/{abnf_generated_file}", "w") as output_sisl:
                output_sisl.write(converted)

            result = subprocess.check_output(["./grammar.exe", "-d", "0", f"test_output_files/{abnf_generated_file}"],
                                             stderr=subprocess.STDOUT)
            if 'PASS' not in str(result):
                print(f"Failed on file:\n{abnf_generated_file}\nContents:\n{test_sisl[:20]}...")
                print(f"Error Message:\n{result}")
            self.assertTrue('PASS' in str(result))


if __name__ == '__main__':
    unittest.main()
