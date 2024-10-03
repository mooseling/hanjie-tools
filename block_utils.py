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
    squares = line.squares
    visible_blocks = []
    search_start = 0

    while search_start < len(squares):
        next_filled_index = index_of(squares, Square.FILLED, search_start)
        if next_filled_index == -1:
            break # no more blocks visible in this line

        next_unfilled_index = index_of_any(squares, [Square.KNOWN_BLANK, Square.UNKNOWN], next_filled_index + 1)
        if next_unfilled_index == -1:
            visible_blocks.append(VisibleBlock(next_filled_index, len(squares) - 1))
            break
        
        visible_blocks.append(VisibleBlock(next_filled_index, next_unfilled_index - 1))
        search_start = next_unfilled_index + 1

    return visible_blocks



# ========================= VisibleBlock Deductions ========================


def get_candidate_clued_blocks(visible_block: VisibleBlock, line: Line) -> list[CluedBlock]:
    candidates = []

    for clued_block in line.clued_blocks:
        visible_block_length = visible_block.end - visible_block.start + 1
        if visible_block_length <= clued_block.length:
            clued_block_limits = get_limits(clued_block, line)
            if visible_block.start >= clued_block_limits[0] and visible_block.end <= clued_block_limits[1]:
                candidates.append(clued_block)

    return candidates



# ==================================================================
# ======================== Private Functions ========================
# ==================================================================



def _get_min_start(target_clued_block: CluedBlock, line: Line) -> int:
    possible_start = 0

    for clued_block in line.clued_blocks:
        possible_start = _get_next_index_where_block_fits(line, clued_block.length, possible_start)
        possible_start = _get_next_index_where_block_is_not_made_longer(line, clued_block.length, possible_start)
        if clued_block is target_clued_block:
            return possible_start
        possible_start += clued_block.length + 1 # + 1 ensures there's a gap after the block we just dropped

    # TODO throw exception? We should never get here.


def _get_max_end(target_clued_block: CluedBlock, line: Line) -> int:
    reversed_line = _get_reversed_line(line)
    inverted_min_start = _get_min_start(target_clued_block, reversed_line)
    return len(line.squares) - inverted_min_start - 1


def _get_next_index_where_block_fits(line: Line, block_length: int, start: int) -> int:
    sub_line = line.squares[start:block_length]
    sub_index_of_wall = index_of(sub_line, Square.KNOWN_BLANK)
    if sub_index_of_wall > -1:
        return _get_next_index_where_block_fits(line, block_length, start + sub_index_of_wall + 1)

    return start
    # Any failure cases here?


# A block may fit in a space, but if there's squares immediately after that space, it doesn't really fit
def _get_next_index_where_block_is_not_made_longer(line: Line, block_length: int, start: int) -> int:
    next_square_index = start + block_length
    visible_blocks = get_visible_blocks(line)
    for visible_block in visible_blocks:
        if visible_block.start == next_square_index:
            visible_block_length = visible_block.end - visible_block.start + 1
            if visible_block_length > block_length:
                raise Exception(f'Trying to find the next spot for a block of length {block_length}, but encountered a longer visible block ({visible_block_length})')
            return visible_block.end - block_length + 1

    return start



def _get_reversed_line(line: Line) -> Line:
    reversed_clues = rev_list(line.clued_blocks)
    reversed_squares = rev_list(line.squares)
    return Line(reversed_clues, reversed_squares)