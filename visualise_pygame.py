import math
import pygame
import multiprocessing as mp

from puzzle import Puzzle
from square import Square


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

# Shouldn't need this, but I'm getting a weird error using the raw type as a function parameter type
type PuzzleQueue = mp.Queue[Puzzle]


class PygamePuzzleVisualiser:
    def __init__(self, puzzle: Puzzle):
        self.puzzle_update_queue: PuzzleQueue = mp.Queue()
        self.display_process = mp.Process(target = pygame_puzzle_display_loop,
                   args = [puzzle, self.puzzle_update_queue])
        self.display_process.start()


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


def pygame_puzzle_display_loop(puzzle: Puzzle, puzzle_update_queue: PuzzleQueue):
    cached_props = CachedPuzzleDisplayProps(puzzle)

    print("Pygame init...")
    pygame.init()
    print("Set display mode, which inits pyagme display...")
    window = pygame.display.set_mode(window_size)
    print("Fill window with white")
    window.fill((255, 255, 255))

    while True:
        if not puzzle_update_queue.empty():
                print("Queue is not empty, updating display")
                display_puzzle(window, puzzle_update_queue.get(), cached_props)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Pygame received a quit event, ending display process")
                pygame.quit()
                return


def display_puzzle(window: pygame.Surface, puzzle: Puzzle, props: CachedPuzzleDisplayProps):
    fill_solved_squares(window, puzzle, props)
    draw_grid(window, props)
    pygame.display.flip()


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


def draw_grid(window: pygame.Surface, props: CachedPuzzleDisplayProps):
    # Draw vertical lines
    for column_index in range(0, props.num_columns):
        x = column_index * props.cell_width
        line_width = thick_line_width if column_index % 5 == 0 else default_line_width
        pygame.draw.line(window, grid_color, (x, 0), (x, props.grid_height), line_width)
    
    # Draw horizontal lines
    for row_index in range(0, props.num_rows):
        y = row_index * props.cell_width
        line_width = thick_line_width if row_index % 5 == 0 else default_line_width
        pygame.draw.line(window, grid_color, (0, y), (props.grid_width, y), line_width)
