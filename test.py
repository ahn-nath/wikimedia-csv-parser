# Unit tests for main.py
import unittest

import main


class TestMain(unittest.TestCase):
    # test_files the get preferred engines with the default file
    def test_get_preferred_engines(self):
        """
            Test the get_preferred_engines function from the main.py file that, given an input file, returns a dictionary with the
            preferred engines for each language pair
        """
        expected_output = {'af-nl': 'Apertium', 'ar-mt': 'Apertium', 'be-ru': 'Apertium', 'bg-mk': 'Apertium',
                           'ca-fr': 'Apertium', 'ca-oc': 'Apertium', 'ca-pt': 'Apertium', 'ca-sc': 'Apertium',
                           'en-gl': 'Apertium', 'es-ca': 'Apertium', 'es-fr': 'Apertium', 'es-gl': 'Apertium',
                           'es-it': 'Apertium', 'es-pt': 'Apertium', 'fr-oc': 'Apertium', 'gl-pt': 'Apertium',
                           'hi-ur': 'Apertium', 'id-ms': 'Apertium', 'is-sv': 'Apertium', 'it-sc': 'Apertium',
                           'kk-tt': 'Apertium', 'mk-bg': 'Apertium', 'mk-sr': 'Apertium', 'ms-id': 'Apertium',
                           'mt-ar': 'Apertium', 'nl-af': 'Apertium', 'pt-ca': 'Apertium', 'sh-sl': 'Apertium',
                           'sl-sr': 'Apertium', 'sv-da': 'Apertium', 'sv-is': 'Apertium', 'tt-kk': 'Apertium',
                           'ur-hi': 'Apertium'}
        actual_output = main.get_preferred_engines(file_path='test_files/mt-defaults.wikimedia_test.yaml', debug=True)

        self.assertEqual(expected_output, actual_output)

    # test_files the generate file with standard input
    def test_generate_csv_standard(self):
        """
            Test the generate_csv function from the main.py file that, given a dictionary with the preferred engines,
            iterates over another list of files generates a CSV.

            This test will focus specifically on input files that do not require special parsing or the logic of a
            handler as well as on those that do.
        """
        preferred_engines = {'af-nl': 'Apertium', 'ar-mt': 'Apertium', 'be-ru': 'Apertium', 'bg-mk': 'Apertium',
                             'ca-fr': 'Apertium', 'ca-oc': 'Apertium', 'ca-pt': 'Apertium', 'ca-sc': 'Apertium',
                             'en-gl': 'Apertium', 'es-ca': 'Apertium', 'es-fr': 'Apertium', 'es-gl': 'Apertium',
                             'es-it': 'Apertium', 'es-pt': 'Apertium', 'fr-oc': 'Apertium', 'gl-pt': 'Apertium',
                             'hi-ur': 'Apertium', 'id-ms': 'Apertium', 'is-sv': 'Apertium', 'it-sc': 'Apertium',
                             'kk-tt': 'Apertium', 'mk-bg': 'Apertium', 'mk-sr': 'Apertium', 'ms-id': 'Apertium',
                             'mt-ar': 'Apertium', 'nl-af': 'Apertium', 'pt-ca': 'Apertium', 'sh-sl': 'Apertium',
                             'sl-sr': 'Apertium', 'sv-da': 'Apertium', 'sv-is': 'Apertium', 'tt-kk': 'Apertium',
                             'ur-hi': 'Apertium'}

        main.generate_csv(preferred_engines, output_file_name='output_files/cx_server_parsed_test.csv',
                          source_file_path='test_files')

        with open('test_files/expected_output_test.csv') as file:
            expected_output = file.read()

        with open('output_files/cx_server_parsed_test.csv') as file:
            actual_test_output = file.read()

        # assert expected output
        self.assertEqual(expected_output, actual_test_output)


if __name__ == '__main__':
    unittest.main()
