from typing import Callable
from block_utils import get_amount_extended_forward, get_reversed_line, get_naive_limits, get_preceding_clued_blocks, get_span, get_span_limits, get_visible_blocks, is_extended_backward, is_on_a_dot
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
    block_limits_list = [get_naive_limits(clued_block, line) for clued_block in line.clued_blocks]

    for block_index, block_limits in enumerate(block_limits_list):
        block_length = line.clued_blocks[block_index].length
        max_start = block_limits[1] - block_length + 1
        min_end = block_limits[0] + block_length - 1 
        found_length = min_end - max_start + 1

        if found_length > 0:
            line_changes[max_start:min_end + 1] = [Square.FILLED] * found_length

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
# We may find that it must be complete, or that an edge is complete, etc
def check_possible_visible_clued_mappings(line: Line) -> LineChanges:
    line_changes = _get_blank_line_changes(line)

    possible_block_mappings = get_possible_block_mappings(line)

    # First check possible dots at either end
    for visible_block, candidate_clued_blocks in possible_block_mappings.items():
        candidate_lengths = {clued_block.length for clued_block in candidate_clued_blocks}
        if len(candidate_lengths) == 1 and candidate_lengths.pop() == visible_block.get_length():
            # We may not know exactly which CluedBlock this is, but we know it is now complete
            _surround_with_known_blanks(line_changes, visible_block.start, visible_block.end)
        else:
            # We now check if we can put a dot at either end, if all possible CluedBlocks must end there
            candidate_limits = [get_naive_limits(clued_block, line) for clued_block in candidate_clued_blocks]

            if visible_block.start > 0:
                candidate_starts = {limits[0] for limits in candidate_limits}
                if len(candidate_starts) == 1 and candidate_starts.pop() == visible_block.start:
                    line_changes[visible_block.start - 1] = Square.KNOWN_BLANK

            if visible_block.end < len(line.squares) - 1:
                candidate_ends = {limits[1] for limits in candidate_limits}
                if len(candidate_ends) == 1 and candidate_ends.pop() == visible_block.end:
                    line_changes[visible_block.end + 1] = Square.KNOWN_BLANK

    # If a clued-block is the only option for 2 or more visible-blocks, we can connect them
    for clued_block in line.clued_blocks:
        visible_blocks_with_only_this_candidate: list[VisibleBlock] = []
        for visible_block, candidate_clued_blocks in possible_block_mappings.items():
            if len(candidate_clued_blocks) == 1 and clued_block in candidate_clued_blocks:
                visible_blocks_with_only_this_candidate.append(visible_block)
        
        if len(visible_blocks_with_only_this_candidate) > 1:
            limits = get_span_limits(visible_blocks_with_only_this_candidate)
            _fill_range(line_changes, limits[0], limits[1])

    # If the visible-block is near a dot, we may be able to extend it based on minimum candidate length
    for visible_block, candidate_clued_blocks in possible_block_mappings.items():
        minimum_candidate_length = min([clued_block.length for clued_block in candidate_clued_blocks])
        visible_block_length = visible_block.get_length()
        if visible_block_length < minimum_candidate_length:
            index_of_next_dot = index_of(line.squares, Square.KNOWN_BLANK, visible_block.end + 1)
            index_of_previous_dot = len(line.squares) - index_of(rev_list(line.squares), Square.KNOWN_BLANK, len(line.squares) - visible_block.start) - 1

            # If there's either no dot before or after, we replace it with the index of the edge of the line
            # I'm not convinced this needs handling, thanks to knowing that we run the simple check_edge_hints algorithm earlier
            # But can't hurt, might avoid some bug cases
            index_of_next_dot = index_of_next_dot if index_of_next_dot > -1 else len(line.squares)
            # interestingly, we don't have to do this with previous dot, since the index we would assign it is -1 anyway

            distance_to_next_dot = index_of_next_dot - visible_block.end
            distance_to_previous_dot = visible_block.start - index_of_previous_dot

            if distance_to_next_dot < distance_to_previous_dot:
                new_start_index = index_of_next_dot - minimum_candidate_length
                new_length = visible_block.end - new_start_index + 1
                if new_length <= minimum_candidate_length:
                    line_changes[new_start_index:visible_block.start] = [Square.FILLED] * (visible_block.start - new_start_index)
            else:
                new_end_index = index_of_previous_dot + minimum_candidate_length
                new_length = new_end_index - visible_block.start + 1
                if new_length <= minimum_candidate_length:
                    line_changes[visible_block.end + 1:new_end_index + 1] = [Square.FILLED] * (new_end_index - visible_block.end)

    # If a visible-block only has one possible clued-block, we may be able to fill in some squares
    for visible_block, candidate_clued_blocks in possible_block_mappings.items():
        if len(candidate_clued_blocks) == 1:
            for clued_block in candidate_clued_blocks:
                # First get all the starts where this clued-block is valid, given that it is this visible-block
                start_search_range = (visible_block.end - clued_block.length + 1, visible_block.start)
                possible_starts = get_possible_starts_in_range(clued_block, get_visible_blocks(line), line, start_search_range)
                filled_square_search_range = (start_search_range[0], visible_block.start + clued_block.length - 1)
                for square_index in range(filled_square_search_range[0], filled_square_search_range[1]):
                    # Check this square is in every possible position for this clued_block
                    if is_in_every_possible_clued_block_position(square_index, possible_starts, clued_block):
                        line_changes[square_index] = Square.FILLED

    return line_changes


def is_in_every_possible_clued_block_position(square_index: int, possible_starts: set[int], clued_block: CluedBlock) -> bool:
    for start in possible_starts:
        if square_index < start or square_index > start + clued_block.length - 1:
            return False
    return True


def get_possible_starts_in_range(clued_block: CluedBlock,
                                 visible_blocks: list[VisibleBlock],
                                 line: Line,
                                 search_range: tuple[int, int]) -> set[int]:
    possible_start_index = search_range[0]
    possible_positions: set[int] = set()

    while possible_start_index <= search_range[1]:
        if is_extended_backward(clued_block, possible_start_index, visible_blocks):
            possible_start_index += 1
        else:
            amount_extended_forward = get_amount_extended_forward(clued_block, possible_start_index, visible_blocks)
            if amount_extended_forward > 0:
                possible_start_index += amount_extended_forward
            else:
                if not is_on_a_dot(clued_block, possible_start_index, line):
                    possible_positions.add(possible_start_index)
                possible_start_index += 1

    return possible_positions


def get_possible_block_mappings(line: Line) -> dict[VisibleBlock, set[CluedBlock]]:
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
        if visible_block.get_length() <= clued_block.length:
            clued_block_limits = get_naive_limits(clued_block, line)
            if visible_block.start >= clued_block_limits[0] and visible_block.end <= clued_block_limits[1]:
                candidates = candidates | {clued_block}

    return candidates


def _get_mapping_without_forward_clue_violations(visible_blocks: list[VisibleBlock], visible_to_clued_block_map: dict[VisibleBlock, set[CluedBlock]], line: Line) -> dict[VisibleBlock, set[CluedBlock]]:
    # We have to iterate the visible-blocks backwards to remove all invalid mappings
    # We find invalid mappings by checking if later visible blocks are left with no possible clued-blocks if we remove one
    # But this won't work if they have multiple invalid clued-block mappings, since removing just one will leave the others
    for visible_block_index, visible_block in reversed(list(enumerate(visible_blocks))):
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


def find_known_blank_regions(line: Line) -> LineChanges:
    line_changes = _get_blank_line_changes(line)
    block_limits_list = [get_naive_limits(clued_block, line) for clued_block in line.clued_blocks]

    for square_index, _ in enumerate(line_changes):
        if not _is_possibly_in_a_clued_block(square_index, block_limits_list):
            line_changes[square_index] = Square.KNOWN_BLANK

    return line_changes


# This one feels really dumb... Surely we can get this as part of a more general deduction
def fill_in_finished_line(line: Line) -> LineChanges:
    line_changes = _get_blank_line_changes(line)
    
    if all_blocks_match(line):
        for square_index, square_value in enumerate(line.squares):
            if square_value == Square.UNKNOWN:
                line_changes[square_index] = Square.KNOWN_BLANK

    return line_changes


def all_blocks_match(line: Line) -> bool:
    visible_blocks = get_visible_blocks(line)
    if len(visible_blocks) != len(line.clued_blocks):
        return False

    for index, clued_block in enumerate(line.clued_blocks):
        if get_span([visible_blocks[index]]) != clued_block.length:
            return False

    return True


def _is_possibly_in_a_clued_block(square_index: int, block_limits_list: list[tuple[int, int]]) -> bool:
    for limits in block_limits_list:
        if square_index >= limits[0] and square_index <= limits[1]:
            return True

    return False


def _get_blank_line_changes(line: Line) -> LineChanges:
    return [Square.UNKNOWN] * len(line.squares)


def _surround_with_known_blanks(line_changes:LineChanges, start: int, end: int) -> None:
    if start > 0:
        line_changes[start - 1] = Square.KNOWN_BLANK
    if end < len(line_changes) - 1:
        line_changes[end + 1] = Square.KNOWN_BLANK


def _fill_range(line_changes: LineChanges, start: int, end: int) -> None:
    line_changes[start:end + 1] = [Square.FILLED] * (end - start + 1)
