from common_types import SideClues

def copy_side_clues(side_clues: SideClues) -> SideClues:
    return [line_clues.copy() for line_clues in side_clues]


def rev_list[T](list_to_reverse:list[T]) -> list[T]:
    return list(reversed(list_to_reverse))


def index_of[T](container: list[T], value: T) -> int | bool:
    return next((index for index, square in enumerate(container) if square == value), False)