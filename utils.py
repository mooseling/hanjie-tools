from common_types import LineChanges, SideClues
from square import Square

def copy_side_clues(side_clues: SideClues) -> SideClues:
    return [line_clues.copy() for line_clues in side_clues]


def rev_list[T](list_to_reverse:list[T]) -> list[T]:
    return list(reversed(list_to_reverse))


def index_of[T](container: list[T], value: T, start_index = 0) -> int:
    return next((index + start_index for index, square in enumerate(container[start_index:]) if square == value), -1)


def index_of_any[T](container: list[T], values: list[T], start_index = 0) -> int:
    return next(
        (index + start_index for index, square in enumerate(container[start_index:]) if next(
            (index2 for index2, value in enumerate(values) if value == square), -1
            ) > -1),
        -1
    )


def has_changes(line_changes: LineChanges) -> bool:
    first_change_index = next((index for index, square in enumerate(line_changes) if square != Square.UNKNOWN), False)
    return type(first_change_index) == int
