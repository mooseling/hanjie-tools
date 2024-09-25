from example_hanjies import tabled as puzzle
from line_algorithms import check_overlaps
from visualise import visualise_puzzle


for row_index, row in enumerate(puzzle.rows):
    overlap_result = check_overlaps(row, puzzle.row_clues[row_index])
    puzzle.apply_row_changes(overlap_result, row_index)

print(visualise_puzzle(puzzle))




# print(row_index.__str__() + ''.join([square.get_grid_char() for square in overlap_result]))