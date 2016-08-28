from mock import call, patch
import unittest

import calculate_rank
from calculate_rank import InputPath


class TestCalculate(unittest.TestCase):

    """
    Our test class for the rank calculation program.
    """
    def test_calculate(self):

        # This unit test will technically do nothing more than check that the Exceptions are raised for the right
        # reasons. For all the other calls we are mocking things out - hence since we can literally return anything
        # with our mocks. The calculate function is literally just a call orchestrator so no use checking too much...

        # We just create proper return values. We could return junk if we wished...
        read_file_return = [
            "A-Team 1, C-Team 0",
            "B-Team 2, A-Team 3",
            "B-Team 4, C-Team 4"
        ]
        determine_points_return = {
            "A-Team": 6,
            "B-Team": 1,
            "C-Team": 1
        }

        sort_results_return = [
            "1. A - Team, 6 pts",
            "2. B - Team, 1 pt",
            "2. C - Team, 1 pt"
        ]

        source_file_full = "/tmp/test_file.txt"
        destination_filename = "test_results.txt"
        dest_file_full = "/tmp/test_results.txt"

        with patch('calculate_rank._get_file_params', return_value=source_file_full) as gfp_mock, \
                patch('calculate_rank._read_file', return_value=read_file_return) as rf_mock, \
                patch('calculate_rank._determine_points', return_value=determine_points_return) as dp_mock, \
                patch('calculate_rank._sort_results', return_value=sort_results_return) as sr_mock, \
                patch('calculate_rank._write_file') as wf_mock:

            # Now we are finally able to call that function without actually calling anything. only test the function
            # itself!
            calculate_rank.calculate(destination_filename)

        # Now check that certain functions are called with the correct variables. The only real thing to check is that
        # our "write file" function is called with the "destination filename" we gave the calculate function.
        expected_call = [call(
            dest_file_full, sort_results_return
        )]
        wf_mock.assert_has_calls(expected_call)

        # The next few tests are for our Exceptions. We wont patch out everything again since the asserts take place
        # before that. We will fake the return of the "get file params" function to test the asserts. This ties
        # in with bad input parameters - but we are not going to test the argparse function. That literally
        # does absolutely nothing else but return the given input filename

        source_file_full_returns = [
            "test_file.txt",
            "tmp/"
        ]

        # Now set it up with a side-effect to return different values on each call.
        first_exception = "Please specify full file path as input"
        second_exception = "Please specify full file path, not just the file location. Perhaps a trailing slash?"
        with patch('calculate_rank._get_file_params', side_effect=source_file_full_returns) as gfp_mock:

            try:
                calculate_rank.calculate(destination_filename)
                self.assertFalse(True, "Exception was not hit. This is unexpected.")
            except InputPath, error:
                self.assertEqual(
                    str(error),
                    first_exception,
                    "Incorrect exception error returned. Expected: {}, Returned: {}".format(
                        first_exception,
                        str(error)
                    ))
            except Exception, error:
                self.assertFalse(True, "Exception returned that we did not expect. Error was {}".format(
                    error
                ))

            try:
                calculate_rank.calculate(destination_filename)
                self.assertFalse(True, "Exception was not hit. This is unexpected.")
            except InputPath, error:
                self.assertEqual(
                    str(error),
                    second_exception,
                    "Incorrect exception error returned. Expected: {}, Returned: {}".format(
                        second_exception,
                        str(error)
                    ))
            except Exception, error:
                self.assertFalse(True, "Exception returned that we did not expect. Error was {}".format(
                    error
                ))












