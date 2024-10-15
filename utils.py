def rev_list[T](list_to_reverse:list[T]) -> list[T]:
    return list(reversed(list_to_reverse))


def index_of[T](container: list[T], value: T, start_index: int = 0) -> int:
    for index in range(start_index, len(container)):
        if container[index] == value:
            return index
    return -1


def index_of_any[T](container: list[T], values: list[T], start_index: int = 0) -> int:
    for index in range(start_index, len(container)):
        for target_value in values:
            if container[index] == target_value:
                return index

    return -1
