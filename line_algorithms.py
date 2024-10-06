from typing import Callable
from block_utils import get_reversed_line, get_limits, get_preceding_clued_blocks, get_span, get_visible_blocks
from data_classes import CluedBlock, Line, VisibleBlock
from square import Square
from utils import index_of, rev_list

# A LineAlgorithm considers a line and returns a list of deduced changes
# The form of these changes is the same as a Line, but we give it its own type to communicate its purpose
# We don't want to mislead a developer that the output of an algorithm is the final result. It must be added.
type LineChanges = list[Square]
type LineAlgorithm = Callable[[Line], LineChanges]


def check_overlaps(line: Line) -> LineChanges:
    line_changes = _get_blank_line_changes(line)
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
                _surround_with_known_blanks(line_changes, max_start, min_end)

    return line_changes


# I think there may be a more powerful version of this, which can go deeper in the line
# For one thing, if we have an edge block, and a dot, we can apply the same check after the dot
def check_edge_hints(line: Line) -> LineChanges:
    line_changes = _get_blank_line_changes(line)
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
            _surround_with_known_blanks(line_changes, 0, block_length - 1)

    block_length = block_lengths[len(block_lengths) - 1]
    subline_start = len(squares) - block_length
    inverted_filled_index = index_of(rev_list(squares[subline_start:]), Square.FILLED)
    if inverted_filled_index > -1:
        filled_index = len(squares) - inverted_filled_index - 1
        for index in range(subline_start, filled_index):
            if squares[index] != Square.FILLED:
                line_changes[index] = Square.FILLED

        if inverted_filled_index == 0:
            _surround_with_known_blanks(line_changes, subline_start, filled_index)

    return line_changes


# With a visible block, we can narrow down which clued-blocks it could be
# We may find that it must be complete, or that an edge is complete
def check_visible_blocks_for_dots(line: Line) -> LineChanges:
    line_changes = _get_blank_line_changes(line)

    possible_block_mappings = _get_possible_block_mappings(line)

    for visible_block, candidate_clued_blocks in possible_block_mappings.items():
        candidate_lengths = {clued_block.length for clued_block in candidate_clued_blocks}
        visible_block_length = visible_block.end - visible_block.start + 1
        if len(candidate_lengths) == 1 and candidate_lengths.pop() == visible_block_length:
            _surround_with_known_blanks(line_changes, visible_block.start, visible_block.end)
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


def _get_possible_block_mappings(line: Line) -> dict[VisibleBlock, set[CluedBlock]]:
    visible_blocks = get_visible_blocks(line)
    
    visible_to_clued_block_map: dict[VisibleBlock, set[CluedBlock]] = {}
    for visible_block in visible_blocks:
        clued_blocks = get_candidate_clued_blocks(visible_block, line)
        visible_to_clued_block_map[visible_block] = clued_blocks

    visible_to_clued_block_map = _get_mapping_without_forward_clue_violations(visible_blocks, visible_to_clued_block_map, line)
    visible_to_clued_block_map = _get_mapping_without_forward_clue_violations(rev_list(visible_blocks), visible_to_clued_block_map, get_reversed_line(line))

    return visible_to_clued_block_map


def get_candidate_clued_blocks(visible_block: VisibleBlock, line: Line) -> set[CluedBlock]:
    candidates: set[CluedBlock] = set()

    for clued_block in line.clued_blocks:
        visible_block_length = visible_block.end - visible_block.start + 1
        if visible_block_length <= clued_block.length:
            clued_block_limits = get_limits(clued_block, line)
            if visible_block.start >= clued_block_limits[0] and visible_block.end <= clued_block_limits[1]:
                candidates = candidates | {clued_block}

    return candidates


def _get_mapping_without_forward_clue_violations(visible_blocks: list[VisibleBlock], visible_to_clued_block_map: dict[VisibleBlock, set[CluedBlock]], line: Line) -> dict[VisibleBlock, set[CluedBlock]]:
    for visible_block_index, visible_block in enumerate(visible_blocks):
        for clued_block in visible_to_clued_block_map[visible_block]:
            # Logic: If this visible-block is this clued-block, all later visible blocks cannot be it, or any preceding clued-blocks
            # If this leaves them with no candidate clued-blocks, it's impossible that this visible-block is this clued-block
            preceding_clued_blocks = set(get_preceding_clued_blocks(clued_block, line))
            clued_blocks_to_check = preceding_clued_blocks | {clued_block}
            for later_visible_block in visible_blocks[visible_block_index + 1:]:
                # Special case: this clued-block could span both these visible blocks
                if clued_block in visible_to_clued_block_map[later_visible_block]:
                    # The if already checks if this clued-block's limits include both visible-blocks
                    span = get_span([visible_block, later_visible_block])
                    if clued_block.length >= span:
                        continue # Move on to next later-visible-block

                if len(visible_to_clued_block_map[later_visible_block] - clued_blocks_to_check) == 0:
                    # We now modifying a set we are iterating over, which is sus. But testing indicates it works fine.
                    visible_to_clued_block_map[visible_block] = visible_to_clued_block_map[visible_block] - {clued_block}

    return visible_to_clued_block_map


def _get_blank_line_changes(line: Line) -> LineChanges:
    return [Square.UNKNOWN] * len(line.squares)


def _surround_with_known_blanks(line_changes:LineChanges, start: int, end: int) -> None:
    if start > 0:
        line_changes[start - 1] = Square.KNOWN_BLANK
    if end < len(line_changes) - 1:
        line_changes[end + 1] = Square.KNOWN_BLANK
