from example_hanjies import tabled as puzzle
from line_algorithms import check_overlaps, check_edge_hints
from visualise import visualise_puzzle


for row_index, row in enumerate(puzzle.rows):
    overlap_result = check_overlaps(row, puzzle.row_clues[row_index])
    puzzle.apply_row_changes(overlap_result, row_index)

for column_index in range(len(puzzle.rows[0])):
    column = puzzle.get_column(column_index)
    overlap_result = check_overlaps(column, puzzle.column_clues[column_index])
    puzzle.apply_column_changes(overlap_result, column_index)


print(visualise_puzzle(puzzle))


for row_index, row in enumerate(puzzle.rows):
    overlap_result = check_edge_hints(row, puzzle.row_clues[row_index])
    puzzle.apply_row_changes(overlap_result, row_index)

print(visualise_puzzle(puzzle))

for column_index in range(len(puzzle.rows[0])):
    column = puzzle.get_column(column_index)
    overlap_result = check_edge_hints(column, puzzle.column_clues[column_index])
    puzzle.apply_column_changes(overlap_result, column_index)


print(visualise_puzzle(puzzle))




# print(row_index.__str__() + ''.join([square.get_grid_char() for square in overlap_result]))