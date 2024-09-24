type SideClues = list[list[int]]

def copySideClues(sideClues: SideClues) -> SideClues:
    sideCluesCopy: SideClues = []
    for lineClues in sideClues:
        sideCluesCopy.append(lineClues.copy())
    
    return sideCluesCopy