def rev_list[T](list_to_reverse:list[T]) -> list[T]:
    return list(reversed(list_to_reverse))


def index_of[T](container: list[T], value: T, start_index: int = 0) -> int:
    return next((index + start_index for index, square in enumerate(container[start_index:]) if square == value), -1)


def index_of_any[T](container: list[T], values: list[T], start_index: int = 0) -> int:
    return next(
        (index + start_index for index, square in enumerate(container[start_index:]) if next(
            (index2 for index2, value in enumerate(values) if value == square), -1
            ) > -1),
        -1
    )
