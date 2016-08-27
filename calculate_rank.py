# -*- coding: utf-8 -*-

"""
Python "Determine Rank" file.

This file will facilitate a command-line application that will calculate the ranking table for a soccer league.


Input/output
------------
This tool assumes that input will be in the form of text files. It will also write the output to a text file in the
same location as the input file.

It is assumed that input will be well formed - thus this tool will not check for any bad input scenarios.

PS - it was not specifically stipulated that output could be a text file. This option is assumed.

The rules
---------
To confirm the ranking points:
A draw (tie) is worth 1 point and a win is worth 3 points. A loss is worth 0 points.

Output will rank the teams in order and where teams are tied in points, the teams will be printed in alphabetical
order. It does not donate a "better" performance in a tie event.

"""


# We want to use a good sorting algorithm (for insertions) so make use of Python's "heapq" library. Don't reinvent
# the wheel....
import heapq
import os
import argparse


class InputPath(Exception):
    """
    Exception that is raised if any input path issues are found.
    """


class EmptyResults(Exception):
    """
    Exception that is raised if empty results files are passed.
    """


def _determine_points(results):
    """
    Function will read in match results and proceed to determine points and results as stipulated by the rules
    (see file commentary above)

    :param results: An array containing all team results, as read from file.

    :return: Dictionary object containing available teams and points scored in league.
    """

    # Establish a new dictionary.
    match_points = {}

    for result in results:
        # We assume the results are in string format, and well parsed. No checks will be done for that.
        # Typical format has teams and their score total separated by a command, with spaced between
        # the team and it's score. Time to parse...

        split_results = result.split(", ")          # Include the space after that comma for simpler code....
        team_1_split = split_results[0].split(" ")
        team_2_split = split_results[1].split(" ")

        # Reconstruct... since our team names may have spaces and thus be split above as well...
        team_1_data = [" ".join(team_1_split[0:-1]), team_1_split[-1]]
        team_2_data = [" ".join(team_2_split[0:-1]), team_2_split[-1]]

        # Now compare the two and assign valid points. Team results are stored against their team names.
        # Winning team takes 3. Losing team takes 0. Draws take 1 each
        if team_1_data[-1] > team_2_data[-1]:
            if team_1_data[0] not in match_points:
                match_points[team_1_data[0]] = 3
            else:
                match_points[team_1_data[0]] += 3
            # Be sure the loser team is at least in our list... if not there...
            if team_2_data[0] not in match_points:
                match_points[team_2_data[0]] = 0

        elif team_2_data[-1] > team_1_data[-1]:
            if team_2_data[0] not in match_points:
                match_points[team_2_data[0]] = 3
            else:
                match_points[team_2_data[0]] += 3
            # Be sure the loser team is at least in our list... if not there...
            if team_1_data[0] not in match_points:
                match_points[team_1_data[0]] = 0

        else:
            # Gotta assume the draw here...
            if team_1_data[0] not in match_points:
                match_points[team_1_data[0]] = 1
            else:
                match_points[team_1_data[0]] += 1

            if team_2_data[0] not in match_points:
                match_points[team_2_data[0]] = 1
            else:
                match_points[team_2_data[0]] += 1

    # At this point in time our points are matched against the teams...
    return match_points


def _get_file_params():
    """
    Get the file input parameter from the command line. Since this uses "argparse", it will facilitate the full
    CLI experience...

    :return: full file path input value
    """

    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='This script will calculate your rank results given team match results in a file.')

    # Add arguments
    parser.add_argument(
        '-f', '--filename', type=str, help='Full file location path', required=True)

    # Find our args array from the passed in parameters.
    args = parser.parse_args()

    # Determine the file's name and the location.
    full_path = args.filename

    # Return all variable values
    return full_path


def _read_file(filename):
    """
    Read our given filename and return results.

    :param filename: Full file path that contains match results.

    :return: An array containing all team results, as read from file.
    """

    with open(filename) as input_file:
        # Read all entries, remove newline characters.
        match_results = [line.rstrip('\n') for line in input_file]

    if not match_results:
        raise EmptyResults("Empty results file given. Exiting Program.")

    return match_results


def _sort_results(points):
    """
    Function will take in a point results set and proceed to sort the results via points.

    :param points: Dictionary that contains team names and associated points

    :return:    Array containing strings in the format of "<Rank>. <Team name>: <Points> pt(s)".
                Array is sorted where entry 0 is the highest scoring team.
    """

    # Let us at least assume that we want to do sorting efficiently....
    # Therefore, let us also not re-invent the wheel. We opted on a O(1) insertion sort... in the form of the
    # Heap. Python provides us such a luxury. Enter HeapQ....

    # Also enter an unbelievable result. (Soliloquy time):
    # After some investigation into accepted "max heap" solutions, it turns out a "standard" (kludge?) solution
    # is to simply create the negative number of the points for storage in the heap. The highest number will
    # thus be the one on top - a very cool trick to save time and sort your data as well.
    #
    # The next part was unexpected though. By pushing a tuple it seems that the heap system itself
    # understands to place the children in alphabetical order in the tree....
    #
    # Further investigation shows that it is ordered by ascii value - and since we are assuming that the input is
    # well formed (always capital letters for team names....) the ascii ordering will work for us.
    #
    # In other words, when we push (-1, "Zorro") and then (-1, "Alpha") the subsequent "pops" will return
    # (-1, "Alpha") and (-1, "Zorro") in this order.
    #
    # Thus, at popping time we can once again invert the points and our entire sorting algorithm is done... by simply
    # using the heapq library and good 'ol "-1".
    heap = []
    for key, value in points.iteritems():
        heapq.heappush(heap, (-1*value, key))

    # Now that we have it all pushed, proceed to pop it for the final array.
    sorted_array = []
    current_position = 0
    old_points = 0
    for entry in range(len(heap)):
        # Pop the items, and reconstruct the "String" that we need for our file storage.
        heap_item = heapq.heappop(heap)

        # For the whole "pts or pt" human readable part, we will need to check what the point is and act accordingly
        # Remember we store the heap values as a negative...
        current_points = heap_item[0]
        suffix = "pts"
        if current_points == -1:
            suffix = "pt"

        # We need to prepend the position in the rank. Remember to only change the position if it is
        # then next number in our list!
        if current_points != old_points:
            current_position = entry + 1
            old_points = current_points
        prefix = str(current_position) + "."

        # Now join our various string parts to make up the "rank display"
        strings_to_join = [
            prefix,
            heap_item[1] + ",",
            str(-1 * heap_item[0]),
            suffix]

        final_string = " ".join(strings_to_join)

        sorted_array.append(final_string)

    # Return the final array for response.
    return sorted_array


def _write_file(filename, results):
    """
    Writes results to a particular filename

    :param filename:    Full file path that will contain league point results.
    :param results:     Array containing strings to write to file.
    """
    with open(filename, 'w') as file_handler:
        for item in results:
            file_handler.write("{}\n".format(item))


def calculate(final_name):
    """
    Main function that will orchestrate the calculation and storing of the soccer league results.
    Results will be stored to given file name and same location as input filename

    :param final_name: File name where final results will be stored.
    """

    full_path = _get_file_params()
    file_location = os.path.dirname(full_path)
    file_name = os.path.basename(full_path)

    # Just check that we get full paths here...
    if not file_location or file_location == "":
        raise InputPath("Please specify full file path as input")

    if not file_name or file_name == "":
        raise InputPath("Please specify full file path, not just the file location. Perhaps a trailing slash?")

    match_results = _read_file(full_path)

    # Read in our data
    points = _determine_points(match_results)

    # Proceed to sort it.
    sort_results = _sort_results(points)

    # And write to your file!
    write_file_name = os.path.join(file_location, final_name)
    _write_file(write_file_name, sort_results)

    # We are done!


if __name__ == "__main__":
    # This is your main entry point when using console access...

    # TODO: Maybe make this an input parameter? Wasn't part of the brief...
    final_result_name = "rank_results.txt"

    calculate(final_result_name)

    print ("Calculation Process Complete")
