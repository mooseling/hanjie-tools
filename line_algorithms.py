from typing import Callable
from block_utils import get_candidate_clued_blocks, get_limits, get_visible_blocks
from data_classes import Line
from square import Square
from utils import index_of, rev_list

# A LineAlgorithm considers a line and returns a list of deduced changes
# The form of these changes is the same as a Line, but we give it its own type to communicate its purpose
# We don't want to mislead a developer that the output of an algorithm is the final result. It must be added.
type LineChanges = list[int]
type LineAlgorithm = Callable[[Line], LineChanges]


def check_overlaps(line: Line) -> LineChanges:
    line_changes = get_blank_line_changes(line)
    block_limits_list = [get_limits(clued_block, line) for clued_block in line.clued_blocks]

    for block_index, block_limits in enumerate(block_limits_list):
        block_length = line.clued_blocks[block_index].length
        max_start = block_limits[1] - block_length + 1
        min_end = block_limits[0] + block_length - 1 
        found_length = min_end - max_start + 1

        if found_length > 0:
            line_changes[max_start:min_end] = [Square.FILLED] * found_length

            # If we've found the entire block, it's easy to put the dots in now
            if found_length == block_length:
                surround_with_known_blanks(line_changes, max_start, min_end)

    return line_changes


# I think there may be a more powerful version of this, which can go deeper in the line
# For one thing, if we have an edge block, and a dot, we can apply the same check after the dot
def check_edge_hints(line: Line) -> LineChanges:
    line_changes = get_blank_line_changes(line)
    block_lengths = [clued_block.length for clued_block in line.clued_blocks]
    squares = line.squares

    if len(block_lengths) == 0:
        return line_changes

    block_length = block_lengths[0]
    filled_index = index_of(squares[:block_length], Square.FILLED)
    if filled_index > -1:
        for index in range(filled_index, block_length):
            if squares[index] != Square.FILLED:
                line_changes[index] = Square.FILLED

        # We may have just done the whole block, in which case we could put in a dot
        if filled_index == 0:
            surround_with_known_blanks(line_changes, 0, block_length - 1)

    block_length = block_lengths[len(block_lengths) - 1]
    subline_start = len(squares) - block_length
    inverted_filled_index = index_of(rev_list(squares[subline_start:]), Square.FILLED)
    if inverted_filled_index > -1:
        filled_index = len(squares) - inverted_filled_index - 1
        for index in range(subline_start, filled_index):
            if squares[index] != Square.FILLED:
                line_changes[index] = Square.FILLED

        if inverted_filled_index == 0:
            surround_with_known_blanks(line_changes, subline_start, filled_index)

    return line_changes


# With a visible block, we can narrow down which clued-blocks it could be
# We may find that it must be complete, or that an edge is complete
def check_candidate_clued_blocks_for_dots(line: Line) -> LineChanges:
    line_changes = get_blank_line_changes(line)

    for visible_block in get_visible_blocks(line):
        candidate_clued_blocks = get_candidate_clued_blocks(visible_block, line)

        candidate_lengths = {clued_block.length for clued_block in candidate_clued_blocks}
        visible_block_length = visible_block.end - visible_block.start + 1
        if len(candidate_lengths) == 1 and candidate_lengths.pop() == visible_block_length:
            surround_with_known_blanks(line_changes, visible_block.start, visible_block.end)
        else:
            candidate_limits = [get_limits(clued_block, line) for clued_block in candidate_clued_blocks]

            if visible_block.start > 0:
                candidate_starts = {limits[0] for limits in candidate_limits}
                if len(candidate_starts) == 1 and candidate_starts.pop() == visible_block.start:
                    line_changes[visible_block.start - 1] = Square.KNOWN_BLANK

            if visible_block.end < len(line.squares) - 1:
                candidate_ends = {limits[1] for limits in candidate_limits}
                if len(candidate_ends) == 1 and candidate_ends.pop() == visible_block.end:
                    line_changes[visible_block.end + 1] = Square.KNOWN_BLANK

    return line_changes



def check_complete_blocks(line: Line) -> LineChanges:
    # TODO this is actually kinda hard now... We have to deduce which blocks are which in the line...
    # Or narrow the possibilities
    pass


def get_blank_line_changes(line: Line) -> LineChanges:
    return [Square.UNKNOWN] * len(line.squares)


def surround_with_known_blanks(line_changes:LineChanges, start: int, end: int) -> LineChanges:
    if start > 0:
        line_changes[start - 1] = Square.KNOWN_BLANK
    if end < len(line_changes) - 1:
        line_changes[end + 1] = Square.KNOWN_BLANK


def has_changes(line_changes: LineChanges) -> bool:
    first_change_index = next((index for index, square in enumerate(line_changes) if square != Square.UNKNOWN), False)
    return type(first_change_index) == int