from dataclasses import dataclass
import math
import pygame
import multiprocessing as mp
import time

from puzzle import Puzzle
from square import Square
from utils import rev_list


# I had some peculiar trouble running this a second time. This error message:
# [NSResponder initialize] may have been in progress in another thread when fork() was called
# And then another error message that ends with "Crashing instead."
# I've gotten it to run by doing this in terminal: export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES


window_size = (1200, 800)
grid_max_width = 1000
grid_max_height = 600
grid_color = (0, 0, 0)
fill_colour = (125, 125, 125)
default_line_width = 1
thick_line_width = 3
clue_text_font_size = 20
clue_text_width = 15
clue_text_height = 12

# Shouldn't need this, but I'm getting a weird error using the raw type as a function parameter type
type PuzzleQueue = mp.Queue[Puzzle]
type StrQueue = mp.Queue[str]


class PygamePuzzleVisualiser:
    def __init__(self, puzzle: Puzzle):
        self.puzzle_update_queue: PuzzleQueue = mp.Queue()
        self.init_result_queue: mp.Queue[str] = mp.Queue()

        self.display_process = mp.Process(target = pygame_puzzle_display_loop,
                   args = [puzzle, self.puzzle_update_queue, self.init_result_queue])
        self.display_process.start()

        while self.init_result_queue.empty():
            print("Waiting for display to init...")
            time.sleep(0.5)

        init_result = self.init_result_queue.get()
        if init_result == "done":
            print("Display process inited successfully, let's crack this puzzle")


    def visualise_puzzle(self, puzzle: Puzzle):
        self.puzzle_update_queue.put(puzzle)


class CachedPuzzleDisplayProps:
    def __init__(self, puzzle: Puzzle):
        self.num_columns = len(puzzle.get_columns())
        self.num_rows = len(puzzle.get_rows())
        self.max_column_width = math.floor(grid_max_width / self.num_columns)
        self.max_row_height = math.floor(grid_max_height / self.num_rows)
        self.cell_width = min(self.max_column_width, self.max_row_height)
        self.grid_width = self.num_columns * self.cell_width
        self.grid_height = self.num_rows * self.cell_width
        self.dot_offset = (self.cell_width / 2) - 1 + default_line_width

        max_column_clue_count = max([len(column.clued_blocks) for column in puzzle.get_columns()])
        max_row_clue_count = max([len(row.clued_blocks) for row in puzzle.get_rows()])
        self.height_for_column_clues = clue_text_height * max_column_clue_count
        self.width_for_row_clues = clue_text_width * max_row_clue_count


@dataclass
class DisplaySurfaces:
    window: pygame.Surface
    clues: pygame.Surface
    grid: pygame.Surface
    squares: pygame.Surface


def pygame_puzzle_display_loop(puzzle: Puzzle, puzzle_update_queue: PuzzleQueue, init_result_queue: StrQueue):
    props = CachedPuzzleDisplayProps(puzzle)

    print("Setup display...")
    surfaces = setup_display(puzzle, props)
    print("Display setup finished")

    init_result_queue.put("done")

    while True:
        if not puzzle_update_queue.empty():
                print("Queue is not empty, updating display")
                fill_solved_squares(surfaces.squares, puzzle_update_queue.get(), props)
                blit_all_and_flip(surfaces, props)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Pygame received a quit event, ending display process")
                pygame.quit()
                return


def setup_display(puzzle: Puzzle, props: CachedPuzzleDisplayProps) -> DisplaySurfaces:
    print("Pygame init...")
    pygame.init()

    print("Initialising display window...")
    window = pygame.display.set_mode(window_size)
    window.fill((255, 255, 255))

    clues_surface = draw_clues(puzzle, props)
    grid_surface = draw_grid(props)
    squares_surface = pygame.Surface((props.grid_width, props.grid_height), flags=pygame.SRCALPHA)
    squares_surface.fill((0, 0, 0, 0))

    surfaces = DisplaySurfaces(window, clues_surface, grid_surface, squares_surface)
    blit_all_and_flip(surfaces, props)

    return surfaces


def draw_clues(puzzle: Puzzle, props: CachedPuzzleDisplayProps) -> pygame.Surface:
    clue_surface = pygame.Surface((props.width_for_row_clues + props.grid_width, props.height_for_column_clues + props.grid_height))
    clue_surface.fill((255, 255, 255))

    font = pygame.font.SysFont('Roboto', clue_text_font_size)

    for column_index, column in enumerate(puzzle.get_columns()):
        for clue_index_inv, clue in enumerate(rev_list(column.clued_blocks)):
            clue_text = font.render(str(clue.length), False, (0, 0, 0))
            x = props.width_for_row_clues + (column_index * props.cell_width) + 1
            y = props.height_for_column_clues - ((clue_index_inv + 1) * clue_text_height)
            clue_surface.blit(clue_text, (x, y))

    for row_index, row in enumerate(puzzle.get_rows()):
        for clue_index_inv, clue in enumerate(rev_list(row.clued_blocks)):
            clue_text = font.render(str(clue.length), False, (0, 0, 0))
            x = props.width_for_row_clues - ((clue_index_inv + 1) * clue_text_width)
            y = props.height_for_column_clues + (row_index * props.cell_width) + 1
            clue_surface.blit(clue_text, (x, y))

    return clue_surface


def fill_solved_squares(window: pygame.Surface, puzzle: Puzzle, props: CachedPuzzleDisplayProps):
    for row_index, row in enumerate(puzzle.get_rows()):
        top = row_index * props.cell_width
        for column_index, cell_value in enumerate(row.squares):
            if cell_value == Square.FILLED:
                left = column_index * props.cell_width
                pygame.draw.rect(window, fill_colour, pygame.Rect(left, top, props.cell_width, props.cell_width))
            elif cell_value == Square.KNOWN_BLANK:
                left = column_index * props.cell_width
                pygame.draw.rect(window, fill_colour, pygame.Rect(left + props.dot_offset, top + props.dot_offset, 2, 2))


def draw_grid(props: CachedPuzzleDisplayProps) -> pygame.Surface:
    print("Draw grid...")
    grid_surface = pygame.Surface((props.grid_width, props.grid_height), flags=pygame.SRCALPHA)
    grid_surface.fill((0, 0, 0, 0))

    # Draw vertical lines
    for column_index in range(0, props.num_columns):
        x = column_index * props.cell_width
        line_width = thick_line_width if column_index % 5 == 0 else default_line_width
        pygame.draw.line(grid_surface, grid_color, (x, 0), (x, props.grid_height), line_width)

    # Draw horizontal lines
    for row_index in range(0, props.num_rows):
        y = row_index * props.cell_width
        line_width = thick_line_width if row_index % 5 == 0 else default_line_width
        pygame.draw.line(grid_surface, grid_color, (0, y), (props.grid_width, y), line_width)

    return grid_surface


def blit_all_and_flip(surfaces: DisplaySurfaces, props: CachedPuzzleDisplayProps):
    # On each update, we blit all the surfaces again, in the order we want to layer them
    print("Blit all and flip")

    surfaces.window.blit(surfaces.clues, (0, 0))

    grid_start = (props.width_for_row_clues, props.height_for_column_clues)
    surfaces.window.blit(surfaces.squares, grid_start)
    surfaces.window.blit(surfaces.grid, grid_start)
    pygame.display.flip()