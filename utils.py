from common_types import SideClues

def copySideClues(sideClues: SideClues) -> SideClues:
    sideCluesCopy: SideClues = []
    for lineClues in sideClues:
        sideCluesCopy.append(lineClues.copy())
    
    return sideCluesCopy