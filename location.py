class Square:
    def __init__(self, x, y=None):
        if isinstance(x, int) and isinstance(y, int):  # Vectorial notation
            self.x = x
            self.y = y
        elif isinstance(x, str) and y is None:  # Chess notation
            if len(x) == 2 and x[0].isalpha() and x[1].isdigit():
                self.x = ord(x[0].lower()) - ord('a') + 1
                self.y = int(x[1])
            else:
                raise ValueError("Invalid chess notation. Must be in the form 'e3'.")
        else:
            raise ValueError("Invalid arguments. Provide either (x, y) as integers or a single chess notation string.")
    
    def getSquareVector(self):
        return (self.x, self.y)
    
    def getSquareChessNotation(self):
        return f"{chr(self.x + ord('a') - 1)}{self.y}"



        