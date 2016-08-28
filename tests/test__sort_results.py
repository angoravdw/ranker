import unittest
import calculate_rank


class TestSortResults(unittest.TestCase):
    """
    Test class to run unit tests on _sort_results function.
    """

    def test__sort_results(self):

        # Run scenarios for sorting against function. Since we are testing an internal function, it is assumed that
        # inputs will be well formed (NOT always a good assumption!)

        test_cases = [
            # Scenario: Check returned order strings for a single match, team 1 wins.
            {
                'input': {'Alpha': 3, 'Zeta': 0},
                'result': ['1. Alpha, 3 pts', '2. Zeta, 0 pts']
            },

            # Scenario: Check returned order strings for a single match, team 2 wins.
            {
                'input': {'Alpha': 0, 'Zeta': 3},
                'result': ['1. Zeta, 3 pts', '2. Alpha, 0 pts']
            },

            # Scenario: Check returned order strings for one match, being a draw.
            # NOTE! We are also testing the "pts" vs "pt" bit here...
            {
                'input': {'Alpha': 1, 'Zeta': 1},
                'result': ['1. Alpha, 1 pt', '1. Zeta, 1 pt']
            },

            # Scenario: Multiple similar points. Tests Alphabetical order some more.
            {
                'input': {'Alpha': 3, 'Zeta': 3, 'Gamma': 3},
                'result': ['1. Alpha, 3 pts', '1. Gamma, 3 pts', '1. Zeta, 3 pts']
            },

            # Scenario: Same Points, very similar names. Alphabet differs on last letter.
            {
                'input': {'Alpha A': 3, 'Alpha B': 3},
                'result': ['1. Alpha A, 3 pts', '1. Alpha B, 3 pts']
            },

            # Scenario: Odd team names. Nobody is a "real" winner but some have more points. Specifically check
            #           "Rank numbers" with this one too.
            {
                'input': {'Wingzz': 3, 'I wish I could WIN': 1, 'Help Us': 1, 'N0T 1nV4l1d': 3},
                'result': [
                    '1. N0T 1nV4l1d, 3 pts', '1. Wingzz, 3 pts',
                    '3. Help Us, 1 pt', '3. I wish I could WIN, 1 pt'
                ]
            },

            # Scenario: Odd team names. Specifically testing names staring with characters other than alphabet.
            # The ordering of team-names are done via the ascii character set.... so for reference:
            #
            # chr:      !   "   #   $   %   &   '   (   )   *   +   ,   -   .   /
            # asc: 32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47
            #
            # So any team name that starts with an odd character will be ordered as such.
            # NB! NOT part of the brief. Was decided to investigate this since it is part of the heapq functionality.
            # It is assumed that our "well formed" inputs will mean we do not need to check this out...
            {
                'input': {'!a': 1, '&a': 1, '#a': 1, '$a': 1, '%a': 1, ')a': 1, '+a': 1},
                'result': [
                    '1. !a, 1 pt', '1. #a, 1 pt', '1. $a, 1 pt',
                    '1. %a, 1 pt', '1. &a, 1 pt', '1. )a, 1 pt', '1. +a, 1 pt'
                ]
            },

            # Scenario: Capital letters. vs small letters. We are making the assumption that team names will always
            # be proper names.... hence we will not deal with ascii issues for this particular case.
            # It does not make much sense, from a readability perspective, why "a" should be after "Z" when
            # ordered alphabetically.
            #
            # HOWEVER. To confirm ascii behaviour, the following shows what will happen with capital vs lower case
            # names....
            #
            # We did not cater for such things since "input is well formed". It is understood that this means the
            # Names of teams are also well formed.
            {
                'input': {'alpha': 1, 'Alpha': 1},
                'result': ['1. Alpha, 1 pt', '1. alpha, 1 pt']
            },

            # Scenario: Sample input (from brief)
            {
                'input': {'Tarantulas': 6, 'FC Awesome': 1, 'Lions': 5, 'Snakes': 1, 'Grouches': 0},
                'result': [
                    '1. Tarantulas, 6 pts',
                    '2. Lions, 5 pts',
                    '3. FC Awesome, 1 pt',
                    '3. Snakes, 1 pt',
                    '5. Grouches, 0 pts'
                ]
            }
        ]

        for test in test_cases:
            result = calculate_rank._sort_results(test['input'])

            # The returned value is an array of strings. The strings must match exactly, and the array entries
            # must match exactly (since it is now ordered).
            for count, value in enumerate(result):
                self.assertEqual(value, test['result'][count],
                                 "Returned result did not match expectations. "
                                 "Rank position in list: {}, "
                                 "String Found at position: {}, "
                                 "Expected String at position: {}".format(
                                     count, value, test['result'][count]
                                 ))

