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


# It's getting increasingly complicated to get the limits... This really is an algorithm. But what really is an algorithm?
def get_limits(clued_block: CluedBlock, line: Line) -> tuple[int, int]:
    return (_get_min_start(clued_block, line), _get_max_end(clued_block, line))


def get_preceding_clued_blocks(clued_block: CluedBlock, line: Line) -> list[CluedBlock]:
    index = index_of(line.clued_blocks, clued_block)
    if index == -1:
        raise Exception('This CluedBlock is not part of this line')
    return line.clued_blocks[:index]


# def get_candidate_visible_blocks(clued_block: CluedBlock, line: Line) -> list[VisibleBlock]:
#     pass


# def is_found(clued_block: CluedBlock, line: Line) -> bool:
#     pass # We may never need this



# ========================= Line Deductions ========================


def get_visible_blocks(line: Line) -> list[VisibleBlock]:
    squares = line.squares
    visible_blocks: list[VisibleBlock] = []
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


def get_span(visible_blocks: list[VisibleBlock]) -> int:
    limits = get_span_limits(visible_blocks)
    return limits[1] - limits[0] + 1


def get_span_limits(visible_blocks: list[VisibleBlock]) -> tuple[int, int]:
    return (
        min(map(lambda visible_block: visible_block.start, visible_blocks)),
        max(map(lambda visible_block: visible_block.end, visible_blocks))
    )



# ==================================================================
# ======================== Private Functions ========================
# ==================================================================



def _get_min_start(target_clued_block: CluedBlock, line: Line) -> int:
    possible_start = 0

    for clued_block in line.clued_blocks:
        possible_start = _get_next_possible_start_for_block(clued_block, line, possible_start)
        if clued_block is target_clued_block:
            return possible_start
        possible_start += clued_block.length + 1 # + 1 ensures there's a gap after the block we just dropped

    raise Exception('No min-start found')


def _get_max_end(target_clued_block: CluedBlock, line: Line) -> int:
    reversed_line = get_reversed_line(line)
    inverted_min_start = _get_min_start(target_clued_block, reversed_line)
    return len(line.squares) - inverted_min_start - 1


def _get_next_possible_start_for_block(clued_block: CluedBlock, line: Line, possible_start: int) -> int:
    visible_blocks = get_visible_blocks(line)

    while possible_start < len(line.squares):
        possible_start = _get_next_index_where_block_fits(line, clued_block.length, possible_start)
        visible_block_immediately_after = _get_visible_block_immediately_after(clued_block, possible_start, visible_blocks)
        if visible_block_immediately_after == None:
            return possible_start
        else:
            if visible_block_immediately_after.get_length() > clued_block.length:
                # It's fine, this just means this visible-block is an earlier clued-block, and we have to go past it
                possible_start = visible_block_immediately_after.end + 2
            else:
                # This visible-block might be this clued-block, but we have to nudge forward a bit so we don't make it too long
                return visible_block_immediately_after.end - clued_block.length + 1

    raise Exception("Didn't expect to ever get here. Looking for a space for a block but didn't find any.")


def _get_next_index_where_block_fits(line: Line, block_length: int, start: int) -> int:
    sub_line = line.squares[start:start + block_length]
    sub_index_of_wall = index_of(sub_line, Square.KNOWN_BLANK)
    if sub_index_of_wall > -1:
        return _get_next_index_where_block_fits(line, block_length, start + sub_index_of_wall + 1)

    return start
    # Any failure cases here?


def _get_visible_block_immediately_after(clued_block: CluedBlock, start: int, visible_blocks: list[VisibleBlock]) -> VisibleBlock|None:
    index_immediately_after_block = start + clued_block.length
    for visible_block in visible_blocks:
        if visible_block.start == index_immediately_after_block:
            return visible_block
    return None


def get_reversed_line(line: Line) -> Line:
    reversed_clues = rev_list(line.clued_blocks)
    reversed_squares = rev_list(line.squares)
    return Line(reversed_clues, reversed_squares)