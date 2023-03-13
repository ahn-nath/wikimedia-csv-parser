# Unit tests for main.py
import unittest


class TestMain(unittest.TestCase):
    # test_files the get preferred engines with the default file
    def test_get_preferred_engines(self):
        """
            Test the get_preferred_engines function from the main.py file that, given an input file, returns a dictionary with the
            preferred engines for each language pair
        """
        pass

    # test_files the generate file with standard input
    def test_generate_csv_standard(self):
        """
            Test the generate_csv function from the main.py file that, given a dictionary with the preferred engines,
            iterates over another list of files generates a CSV.

            This test will focus specifically on input files that do not require special parsing or the logic of a
            handler.
        """
        pass

    # test_files the generate file with non-standard input
    def test_generate_csv_non_standard(self):
        """
            Test the generate_csv function from the main.py file that, given a dictionary with the preferred engines,
            iterates over another list of files generates a CSV.

            This test will focus specifically on input files that require special parsing or the logic of a handler. As
             of now, the only handler used with the JavaScript logic is 'config_files/transform.js'.
        """
        pass