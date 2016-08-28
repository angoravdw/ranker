from mock import call, patch, MagicMock
import re
import unittest

import calculate_rank
from calculate_rank import EmptyResults


class TestReadFile(unittest.TestCase):
    """
    Test class to run unit tests on _read_file function.
    """

    def test__read_file(self):

        # This test wants to ensure we check for empty results. That is something that isn't mentioned....
        source_file_full = "/tmp/test_file.txt"
        valid_data = 'FIRST_LINE\nSECOND_LINE\nTHIRD_LINE'
        expected_exception = "Empty results file given. Exiting Program."

        expected_result = ['FIRST_LINE', 'SECOND_LINE', 'THIRD_LINE']
        # MUCH thanks be to the genius at stackoverflow for providing the quick solution to mock out an iterator
        # on a file "open" and doing so using a custom override to the iterator. Turns out this part isn't quite
        # organized in the whole mock library. Saved me a lot of time from having to figure this out myself.

        # THIS function is an iterator that mimics the "split line on \n character" functionality.
        def splitkeepsep(s, sep):
            return reduce(lambda acc, i: acc[:-1] + [acc[-1] + i] if i == sep else acc + [i],
                          re.split("(%s)" % re.escape(sep), s), [])

        # Patch the open action. We will now see if our various scenarios work. Code coverage is key.
        with patch('calculate_rank.open', create=True) as open_mock:
            open_mock.return_value = MagicMock(spec=file)
            handle = open_mock.return_value.__enter__.return_value
            handle.__iter__.return_value = iter(splitkeepsep(valid_data, "\n"))

            result = calculate_rank._read_file(source_file_full)

            self.assertEqual(
                result, expected_result,
                " Expected result was {}, returned result was {}".format(expected_result, result)
            )

            # Now patch our "return value" for our iterator and test again. This simulates an empty file.
            handle.__iter__.return_value = []

            try:
                calculate_rank._read_file(source_file_full)
                self.assertFalse(True, "Exceptions were not hit. This is a failure.")
            except EmptyResults, error:
                self.assertEqual(
                    str(error),
                    expected_exception,
                    "Incorrect exception error returned. Expected: {}, Returned: {}".format(
                        expected_exception,
                        str(error)
                    ))
            except Exception, error:
                self.assertFalse(True, "Exception returned that we did not expect. Error was {}".format(
                    error
                ))
