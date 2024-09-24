from enum import Enum

class Square(Enum):
    UNKNOWN = ' ', 'unknown'
    FILLED = '#', 'filled'
    BLANK = '/', 'blank'

    def getGridChar(self):
        return self.value[0]
    
    def getFriendlyString(self):
        return self.value[1]