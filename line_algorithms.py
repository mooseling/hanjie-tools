from typing import Callable
from common_types import Line, LineClues
from square import Square

# A LineAlgorithm considers a line and returns a list of deduced changes
# The form of these changes is the same as a Line, but we give it its own type to communicate its purpose
# We don't want to mislead a developer that the output of an algorithm is the final result. It must be added.
type LineChanges = Line
type LineAlgorithm = Callable[[Line, LineClues], LineChanges]


def check_overlaps(line: Line, block_lengths: LineClues) -> LineChanges:
    # For each block in a line, we will get its bounds. If there is overlap, we've found some squares
    # First step is to get min_end and max_start for each block
    block_bound_list = [BlockBounds()] * len(block_lengths)
    distance_travelled = 0

    # TODO account for known blanks in the line

    for block_index, block_length in enumerate(block_lengths):
        block_bound_list[block_index].min_end = distance_travelled + block_length
        distance_travelled += block_length + 1

    distance_travelled = len(line)

    for block_index, block_length in reversed(enumerate(block_lengths)):
        block_bound_list[block_index].max_start = distance_travelled - block_length
        distance_travelled -= block_length + 1

    # Now we have the bounds for each block, so we check for overlaps
    line_changes: LineChanges = [Square.UNKNOWN] * len(line)

    for block_index, block_bounds in enumerate(block_bound_list):
        block_length = block_lengths[block_index]
        found_length = block_bounds.min_end - block_bounds.max_start
        
        if found_length > 0:
            for square_index in range(block_bounds.max_start, block_bounds.min_end):
                line_changes[square_index] = Square.FILLED

            # If we've found the entire block, it's easy to put the dots in now
            if found_length == block_length:
                if block_bounds.max_start > 0:
                    line_changes[block_bounds.max_start - 1] = Square.BLANK
                if block_bounds.min_end < len(line) - 1:
                    line_changes[block_bounds.min_end + 1] = Square.BLANK


def check_complete_blocks(line: Line, block_lengths: LineClues) -> LineChanges:
    # TODO this is actually kinda hard now... We have to deduce which blocks are which in the line...
    # Or narrow the possibilities
    pass





class BlockBounds:
    max_start: int
    min_end: int