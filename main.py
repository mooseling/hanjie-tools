import time
from example_hanjies import poolside as puzzle
from line_algorithms import LineAlgorithm, check_overlaps, check_edge_hints, has_changes
from visualise import visualise_puzzle

frame_sleep_time = 0.25

print(visualise_puzzle(puzzle))

line_algorithm_list: list[LineAlgorithm] = [check_overlaps, check_edge_hints]

anything_has_changed = True
while anything_has_changed:
    anything_has_changed = False

    for line_algorithm in line_algorithm_list:
        for row_index, row in enumerate(puzzle.get_rows()):
            algorithm_result = line_algorithm(row)
            anything_has_changed = has_changes(algorithm_result)
            if anything_has_changed:
                puzzle.apply_line_changes(algorithm_result, row_index=row_index)
                print(visualise_puzzle(puzzle))
                time.sleep(frame_sleep_time)

        for column_index, column in enumerate(puzzle.get_columns()):
            algorithm_result = line_algorithm(column)
            anything_has_changed = has_changes(algorithm_result)
            if anything_has_changed:
                puzzle.apply_line_changes(algorithm_result, column_index=column_index)
                print(visualise_puzzle(puzzle))
                time.sleep(frame_sleep_time)
