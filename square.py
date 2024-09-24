from enum import Enum

class Square(Enum):
    UNKNOWN = ' ', 'unknown'
    FILLED = '#', 'filled'
    KNOWN_BLANK = '/', 'blank'

    def get_grid_char(self):
        return self.value[0]
    
    def get_fiendly_string(self):
        return self.value[1]