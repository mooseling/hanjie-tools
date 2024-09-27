from common_types import LineChanges, SideClues
from square import Square

def copy_side_clues(side_clues: SideClues) -> SideClues:
    return [line_clues.copy() for line_clues in side_clues]


def rev_list[T](list_to_reverse:list[T]) -> list[T]:
    return list(reversed(list_to_reverse))


def index_of[T](container: list[T], value: T) -> int | bool:
    return next((index for index, square in enumerate(container) if square == value), False)


def has_changes(line_changes: LineChanges) -> bool:
    first_change_index = next((index for index, square in enumerate(line_changes) if square != Square.UNKNOWN), False)
    return type(first_change_index) == int
