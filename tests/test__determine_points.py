import unittest
import calculate_rank


class TestDeterminePoints(unittest.TestCase):
    """
    Test class to run unit tests on _determine_points function.
    """

    def test__determine_points(self):

        # We simulate a bunch of test cases to ensure the points calculation mechanism performs as expected.
        # The function assumes well-formed input (NB. In real life this assumption is NOT GOOD)

        test_cases = [
            # Scenario: Check rank when one match result is played only. Team 1 wins.
            {
                'input': ['Alpha 1, Zeta 0'],
                'result': {'Alpha': 3, 'Zeta': 0}
            },

            # Scenario: Check rank when one match result is played only. Team 2 wins.
            {
                'input': ['Alpha 0, Zeta 1'],
                'result': {'Alpha': 0, 'Zeta': 3}
            },

            # Scenario: Check rank when one match result is played only. Teams draw. Zero points all.
            {
                'input': ['Alpha 0, Zeta 0'],
                'result': {'Alpha': 1, 'Zeta': 1}
            },

            # Scenario: Two matches played. Each team wins one.
            {
                'input': ['Alpha 1, Zeta 0', 'Alpha 0, Zeta 1'],
                'result': {'Alpha': 3, 'Zeta': 3}
            },

            # Scenario: Two matches played. One team wins all.
            {
                'input': ['Alpha 1, Zeta 0', 'Alpha 1, Zeta 0'],
                'result': {'Alpha': 6, 'Zeta': 0}
            },

            # Scenario: Two matches played. Draws for all.
            {
                'input': ['Alpha 0, Zeta 0', 'Alpha 0, Zeta 0'],
                'result': {'Alpha': 2, 'Zeta': 2}
            },

            # Scenario: Three matches played. Team points vary greatly. Each team wins one.
            {
                'input': ['Alpha 5, Zeta 2', 'Zeta 4, Gamma 1', 'Gamma 4, Alpha 0'],
                'result': {'Alpha': 3, 'Zeta': 3, 'Gamma': 3}
            },

            # Scenario: Odd team names.
            {
                'input': [
                    'I wish I could WIN 0, N0T 1nV4l1d 3',
                    '#Help Us 1, Wingzz 23',
                    'I wish I could WIN 1, #Help Us 1'
                ],
                'result': {'Wingzz': 3, 'I wish I could WIN': 1, '#Help Us': 1, 'N0T 1nV4l1d': 3}
            },

            # Scenario: Sample input (from brief)
            {
                'input': [
                    'Lions 3, Snakes 3',
                    'Tarantulas 1, FC Awesome 0',
                    'Lions 1, FC Awesome 1',
                    'Tarantulas 3, Snakes 1',
                    'Lions 4, Grouches 0'
                ],
                'result': {'Tarantulas': 6, 'FC Awesome': 1, 'Lions': 5, 'Snakes': 1, 'Grouches': 0}
            }

        ]

        for test in test_cases:
            result = calculate_rank._determine_points(test['input'])

            # Dictionaries are returned. Dictionary order can be random. The calculate points function is not
            # concerned with order, only with points. Be ure to assert the functions accordingly.
            for key, value in test['result'].iteritems():
                self.assertIn(key, result, "A Team was not found in results. Expected team was [{}], "
                              "results showed {}".format(key, result))

                self.assertEqual(value, result[key],
                                 "Points awarded to teams did not match expectations. Expected point(s) for team [{}] "
                                 "was [{}], returned result was {}".format(key, value, result))
