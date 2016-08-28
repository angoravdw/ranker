from mock import call, patch, mock_open
import unittest

import calculate_rank


class TestWriteFile(unittest.TestCase):
    """
    Test class to run unit tests on _write_file function.
    """

    def test__write_file(self):
        """
        Test that our write function still writes as we need it to.
        """

        # So this seems a painful waste of testing time - but ultimately we want to be sure that the file writer
        # writes to the file in a specific way, given some input.
        #
        # Since this is an internal function (supposed to be) we don't check for bad input.
        # Of course this is python... nothing is internal....
        destination_file_full = "/tmp/test_result_file.txt"
        write_data = ["1. TEAM A, 6", "2. TEAM B, 3", "3. TEAM C, 0"]

        open_mock = mock_open()
        # Patch the open action. We will now see if our various scenarios work. Code coverage is key.
        with patch('calculate_rank.open', open_mock):
            calculate_rank._write_file(destination_file_full, write_data)

        # Now check that we are writing to the right location...
        open_mock.assert_called_once_with(destination_file_full, 'w')

        # Also check that we are calling the write in the correct way. Order of calls are important. Exact data too.
        # And remember that we are appending \n. Also good to check.
        handle = open_mock()
        handle_mocks = handle.write.mock_calls
        for position, data in enumerate(write_data):
            expected_call = call(
                data + '\n'
            )

            self.assertEqual(
                handle_mocks[position], expected_call,
                "Mock called with different values. Expected: {}, Called: {}".format(
                    expected_call, handle_mocks[position]
                )
            )

