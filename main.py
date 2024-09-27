import time
from example_hanjies import tabled as puzzle
from line_algorithms import LineAlgorithm, check_overlaps, check_edge_hints
from utils import has_changes
from visualise import visualise_puzzle


print(visualise_puzzle(puzzle))

line_algorithm_list: list[LineAlgorithm] = [check_overlaps, check_edge_hints]

anything_has_changed = True
while anything_has_changed:
    anything_has_changed = False

    for line_algorithm in line_algorithm_list:
        for row_index, row in enumerate(puzzle.rows):
            algorithm_result = line_algorithm(row, puzzle.row_clues[row_index])
            anything_has_changed = has_changes(algorithm_result)
            if anything_has_changed:
                puzzle.apply_row_changes(algorithm_result, row_index)
                print(visualise_puzzle(puzzle))
                time.sleep(0.5)

        for column_index in range(len(puzzle.rows[0])):
            column = puzzle.get_column(column_index)
            algorithm_result = line_algorithm(column, puzzle.column_clues[column_index])
            anything_has_changed = has_changes(algorithm_result)
            if anything_has_changed:
                puzzle.apply_column_changes(algorithm_result, column_index)
                print(visualise_puzzle(puzzle))
                time.sleep(0.5)
