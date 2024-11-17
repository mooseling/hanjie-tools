from example_hanjies import poolside as puzzle
from line_algorithms import LineAlgorithm, LineChanges, check_possible_visible_clued_mappings, check_overlaps, check_edge_hints, fill_in_finished_line, find_known_blank_regions
from square import Square
from visualise_pygame import PygamePuzzleVisualiser
import multiprocessing as mp


def has_changes(line_changes: LineChanges, line_squares: list[Square]) -> bool:
    for square_index, new_value in enumerate(line_changes):
        if new_value != Square.UNKNOWN and line_squares[square_index] != new_value:
            return True

    return False


def main():

    visualiser = PygamePuzzleVisualiser(puzzle)

    line_algorithm_list: list[LineAlgorithm] = [check_overlaps, check_edge_hints, check_possible_visible_clued_mappings, find_known_blank_regions, fill_in_finished_line]

    anything_has_changed_this_round = True
    while anything_has_changed_this_round:
        anything_has_changed_this_round = False

        print("Top of puzzle solving loop...")

        for line_algorithm in line_algorithm_list:
            for row_index, row in enumerate(puzzle.get_rows()):
                algorithm_result = line_algorithm(row)
                result_causes_changes = has_changes(algorithm_result, row.squares)
                anything_has_changed_this_round = result_causes_changes or anything_has_changed_this_round
                if result_causes_changes:
                    puzzle.apply_line_changes(algorithm_result, row_index=row_index)
                    visualiser.visualise_puzzle(puzzle)

            for column_index, column in enumerate(puzzle.get_columns()):
                algorithm_result = line_algorithm(column)
                result_causes_changes = has_changes(algorithm_result, column.squares)
                anything_has_changed_this_round = result_causes_changes or anything_has_changed_this_round
                if result_causes_changes:
                    puzzle.apply_line_changes(algorithm_result, column_index=column_index)
                    visualiser.visualise_puzzle(puzzle)

    print("Done. Joining display process...")

    visualiser.display_process.join()


# I'm using a second process to run the pygame visualiser. Getting that to work has required this:
if __name__ == '__main__':
    print("Setting process start method")
    mp.set_start_method('spawn')
    main()