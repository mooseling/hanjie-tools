from data_classes import CluedBlock, Line, VisibleBlock
from square import Square
from utils import index_of, index_of_any, rev_list


# With CluedBlocks, Lines, and VisibleBlocks, we can derive some useful information about these same objects
# This includes positional limits of blocks, and how clued and visible blocks relate to eachother
# To progress with the puzzle, we can build line-algorithms around this information
# This module contains functions for deducing this information
# We leave working out more squares to other modules


# ==================================================================
# ======================== Public Functions ========================
# ==================================================================


# ====================== CluedBlock Deductions =====================


def get_limits(clued_block: CluedBlock, line: Line) -> tuple[int, int]:
    return [_get_min_start(clued_block, line), _get_max_end(clued_block, line)]


def get_candidate_visible_blocks(clued_block: CluedBlock, line: Line) -> list[VisibleBlock]:
    pass


def is_found(clued_block: CluedBlock, line: Line) -> bool:
    pass # We may never need this



# ========================= Line Deductions ========================


def get_visible_blocks(line: Line) -> list[VisibleBlock]:
    visible_blocks = []
    search_start = 0

    while search_start < len(line):
        next_filled_index = index_of(line, Square.FILLED, search_start)
        if next_filled_index == -1:
            break # no more blocks visible in this line

        next_unfilled_index = index_of_any(line, [Square.KNOWN_BLANK, Square.UNKNOWN], search_start)
        if next_unfilled_index == -1:
            visible_blocks.append(VisibleBlock(next_filled_index, len(line.squares) - 1))
            break
        
        visible_blocks.append(VisibleBlock(next_filled_index, next_unfilled_index - 1))
        search_start = next_unfilled_index + 1

    return visible_blocks



# ========================= VisibleBlock Deductions ========================


def get_candidate_clued_blocks(visible_block: VisibleBlock, line: Line) -> list[CluedBlock]:
    pass



# ==================================================================
# ======================== Private Functions ========================
# ==================================================================



def _get_min_start(target_clued_block: CluedBlock, line: Line) -> int:
    possible_start = 0

    for clued_block in line.clued_blocks:
        possible_start = _get_next_index_where_block_fits(line, clued_block.length, possible_start)
        if clued_block == target_clued_block:
            return possible_start
        possible_start += clued_block.length + 1

    # TODO throw exception? We should never get here.


def _get_max_end(target_clued_block: CluedBlock, line: Line) -> int:
    reversed_line = _get_reversed_line(line)
    inverted_min_start = _get_min_start(target_clued_block, reversed_line)
    return len(line.squares) - inverted_min_start - 1







def _get_next_index_where_block_fits(line: Line, block_length: int, start: int) -> int:
    sub_line = line.squares[start:block_length]
    sub_index_of_wall = index_of(sub_line, Square.KNOWN_BLANK)
    if sub_index_of_wall != False:
        return _get_next_index_where_block_fits(line, block_length, start + sub_index_of_wall + 1)

    return start
    # Any failure cases here?


def _get_reversed_line(line: Line) -> Line:
    reversed_clues = rev_list(line.clued_blocks)
    reversed_squares = rev_list(line.squares)
    return Line(reversed_clues, reversed_squares)