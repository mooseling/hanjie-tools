from typing import Callable
from common_types import Line, LineClues
from square import Square
from utils import rev_list

# A LineAlgorithm considers a line and returns a list of deduced changes
# The form of these changes is the same as a Line, but we give it its own type to communicate its purpose
# We don't want to mislead a developer that the output of an algorithm is the final result. It must be added.
type LineChanges = Line
type LineAlgorithm = Callable[[Line, LineClues], LineChanges]


def check_overlaps(line: Line, block_lengths: LineClues) -> LineChanges:
    # For each block in a line, we will get its bounds. If there is overlap, we've found some squares
    # First step is to get min_end and max_start for each block
    min_ends_of_blocks = get_min_ends_of_blocks(line, block_lengths)
    inverted_min_ends = rev_list(get_min_ends_of_blocks(rev_list(line), rev_list(block_lengths)))
    max_starts_of_blocks = [len(line) - inv - 1 for inv in inverted_min_ends]

    # Now we have the bounds for each block, so we check for overlaps
    line_changes: LineChanges = [Square.UNKNOWN] * len(line)

    for block_index, block_length in enumerate(block_lengths):
        min_end = min_ends_of_blocks[block_index]
        max_start = max_starts_of_blocks[block_index]
        found_length = min_end - max_start + 1
        
        if found_length > 0:
            line_changes[max_start:min_end] = [Square.FILLED] * found_length

            # If we've found the entire block, it's easy to put the dots in now
            if found_length == block_length:
                if max_start > 0:
                    line_changes[max_start - 1] = Square.KNOWN_BLANK
                if min_end < len(line) - 1:
                    line_changes[min_end + 1] = Square.KNOWN_BLANK

    return line_changes


def check_complete_blocks(line: Line, block_lengths: LineClues) -> LineChanges:
    # TODO this is actually kinda hard now... We have to deduce which blocks are which in the line...
    # Or narrow the possibilities
    pass


def get_min_ends_of_blocks(line: Line, block_lengths: list[int]) -> list[int]:
    block_bound_list = []
    start_index = 0

    for block_length in block_lengths:
        start_index = get_next_index_where_block_fits(line, block_length, start_index)
        block_bound_list.append(start_index + block_length - 1)
        start_index = start_index + block_length + 1

    return block_bound_list


def get_next_index_where_block_fits(line: Line, block_length: int, start: int) -> int:
    sub_line = line[start:block_length]
    sub_index_of_wall = next((index for index, square in enumerate(sub_line) if square == Square.KNOWN_BLANK), False)
    if sub_index_of_wall != False:
        return get_next_index_where_block_fits(line, block_length, start + sub_index_of_wall + 1)
    
    return start




class BlockBounds:
    max_start: int
    min_end: int