import time
from example_hanjies import poolside as puzzle
from line_algorithms import LineAlgorithm, LineChanges, check_visible_blocks_for_dots, check_overlaps, check_edge_hints
from square import Square
from visualise import visualise_puzzle


def has_changes(line_changes: LineChanges, line_squares: list[Square]) -> bool:
    for square_index, new_value in enumerate(line_changes):
        if new_value != Square.UNKNOWN and line_squares[square_index] != new_value:
            return True

    return False



frame_sleep_time = 0.25

print(visualise_puzzle(puzzle))

line_algorithm_list: list[LineAlgorithm] = [check_overlaps, check_edge_hints, check_visible_blocks_for_dots]

anything_has_changed_this_round = True
while anything_has_changed_this_round:
    anything_has_changed_this_round = False

    for line_algorithm in line_algorithm_list:
        for row_index, row in enumerate(puzzle.get_rows()):
            algorithm_result = line_algorithm(row)
            result_causes_changes = has_changes(algorithm_result, row.squares)
            anything_has_changed_this_round = result_causes_changes or anything_has_changed_this_round
            if result_causes_changes:
                puzzle.apply_line_changes(algorithm_result, row_index=row_index)
                print(visualise_puzzle(puzzle))
                time.sleep(frame_sleep_time)

        for column_index, column in enumerate(puzzle.get_columns()):
            algorithm_result = line_algorithm(column)
            result_causes_changes = has_changes(algorithm_result, column.squares)
            anything_has_changed_this_round = result_causes_changes or anything_has_changed_this_round
            if result_causes_changes:
                puzzle.apply_line_changes(algorithm_result, column_index=column_index)
                print(visualise_puzzle(puzzle))
                time.sleep(frame_sleep_time)
