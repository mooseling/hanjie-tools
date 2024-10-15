def rev_list[T](list_to_reverse:list[T]) -> list[T]:
    return list(reversed(list_to_reverse))


def index_of[T](container: list[T], value: T, start_index: int = 0) -> int:
    for index, item in enumerate(container[start_index:]):
        if item == value:
            return index + start_index
    return -1


def index_of_any[T](container: list[T], values: list[T], start_index: int = 0) -> int:

    for index, item in enumerate(container[start_index:]):
        for target_value in values:
            if item == target_value:
                return index + start_index

    return -1
