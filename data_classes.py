from dataclasses import dataclass
from square import Square


# On the surface, a hanjie puzzle is about filling in squares to satisfy a bunch of clues about the lines
# But in my brain, I find I am always making deductions about "blocks", trying to figure out where they are
# This is the mental model for me solving a hanjie, and I think the code will be much easier to write if I capture this
# This module therefore provides the classes that match this model


@dataclass
class CluedBlock:
    length: int
    index: int # For debugging

    # Things we will compute:
    # --> Known limits
    # --> Visible blocks that could be it
    # --> Whether we've found it

    def __hash__(self) -> int:
        return id(self)


@dataclass
class VisibleBlock:
    start: int
    end: int
    index: int # For debugging

    # Things we will compute:
    # --> CluedBlocks that it could be

    def get_length(self) -> int:
        return self.end - self.start + 1

    def __hash__(self) -> int:
        return id(self)


@dataclass
class Line:
    clued_blocks: list[CluedBlock]
    squares: list[Square]
    index: int        # For debugging
    orientation: str  # For debugging
    is_reversed: bool # For debugging

    # Things we will compute:
    # --> Visible blocks
    # --> Known-blanks (Squares that no blocks can fall into)
    # --> Filled squares (Even if we don't know which CluedBlock it must be)
