import pygame
class Piece:
    """
    Implementation of a chess piece
    
    Attributes
    -----------
    row : int
        The y position of the current piece, has to be either 0 <= row < chessboard.height or -1 for 
        piece textures that dont appear on the board
    column : int
        The x position of the current piece, has to be either 0 <= column < chessboard.width or -1 for 
        piece textures that dont appear on the board
    position : tuple (int,int)
        A tuple representing the position based on row and column (see above)
    pieceType : Rook, Queen, King, Pawn, Bishop, Night
        The type of piece, used to display its texture and color
    currentPossibilities : set
        The grid squares the current piece has access to. Ensures all possibilities are in the form
        tuple(int x,int y), and all ints are 0 <= x < chessboard.width and 0 <= y < chessboard.height
        
    
    Methods
    -------
    getTexture(self)
        Returns the texture of the piece
    """
    
    def __init__(self,row,column,pieceType):
        self.row = row
        self.column = column
        self.position = (column,row)
        self.pieceType = pieceType
        self.currentPossibilities = set()
    
    def getTexture(self):
        """
        Getter of the current pieces texture
        
        Returns
        pygame.image
            The .png associated to the piece, to be found in the assets folder
        """
        return self.pieceType.texture

    def getPieceInfo(self):
        return self.pieceType.color + " " + str(type(self.pieceType))
        
    def setPosition(self,x,y):
        self.position = (x,y)
        self.row = y
        self.column = x
class Rook:
    """
    Class that implements the rook piece. Can move up, down, left and right until the end of the board is found 
    or if a piece is found in its path. If the piece is of the opposite color, it can also move into that piece,
    "eating" it.
    
    Attributes
    -----------
    color : str
        The color of the piece. Ensures thats its value is either "white" or "black"
    texture : pygame.image
        The texture associated to the piece. Its a png file found in the assets folder
    
    
    Raises
    -------
    TypeError
        If the input data is invalid
    ValidError 
        If color is neither white or black
    """
    
    def __init__(self,color):
        if type(color) != str:
            raise ValueError("color must be of type string, current type is " + str(type(color)))
        
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteRook.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackRook.png")
        else:
            raise ValueError("Invalid Piece Color for Rook")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class Bishop:
    """
    Class that implements the bishop piece. Can move up-left, down-left, up-right and down-right until the end of the board is found 
    or if a piece is found in its path. If the piece is of the opposite color, it can also move into that piece,
    "eating" it.
    
    Attributes
    -----------
    color : str
        The color of the piece. Ensures thats its value is either "white" or "black"
    texture : pygame.image
        The texture associated to the piece. Its a png file found in the assets folder
    
    
    Raises
    -------
    TypeError
        If the input data is invalid
    ValidError 
        If color is neither white or black
    """
    
    def __init__(self,color):
        if type(color) != str:
            raise ValueError("color must be of type string, current type is " + str(type(color)))
        
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteBishop.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackBishop.png")
        else:
            raise Exception("Invalid Piece Color for Bishop")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class Pawn:
    """
    Class that implements the pawn piece. 
    Possible movements:
        - If the square in front is clear, it can move one square forward
        - If both the square in front and the one in front of that one are clear, it can also move there
        - It can move forward-left and forward-right if there is a piece of the opposite color placed there, (eating it)
        - It can move forward-left or forward-right if that square is the target en passant square (found in the Chessboard class)
    
    Attributes
    -----------
    color : str
        The color of the piece. Ensures thats its value is either "white" or "black"
    texture : pygame.image
        The texture associated to the piece. Its a png file found in the assets folder
    
    
    Raises
    -------
    TypeError
        If the input data is invalid
    ValidError 
        If color is neither white or black
    """
    
    def __init__(self,color):
        if type(color) != str:
            raise ValueError("color must be of type string, current type is " + str(type(color)))
        
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whitePawn.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackPawn.png")
        else:
            raise Exception("Invalid Piece Color for Pawn")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class Queen:
    """
    Class that implements the queen piece. It can move as the combination of the Rook and Bishop class (see above).
    
    Attributes
    -----------
    color : str
        The color of the piece. Ensures thats its value is either "white" or "black"
    texture : pygame.image
        The texture associated to the piece. Its a png file found in the assets folder
    
    
    Raises
    -------
    TypeError
        If the input data is invalid
    ValidError 
        If color is neither white or black
    """
    
    def __init__(self,color):
        if type(color) != str:
            raise ValueError("color must be of type string, current type is " + str(type(color)))
        
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteQueen.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackQueen.png")
        else:
            raise Exception("Invalid Piece Color for Queen")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
    
class Night:
    """
    Class that implements the knight piece. It can move in an L shape in all eight directions. (2-forward-1 to the side)
    
    Attributes
    -----------
    color : str
        The color of the piece. Ensures thats its value is either "white" or "black"
    texture : pygame.image
        The texture associated to the piece. Its a png file found in the assets folder
    
    
    Raises
    -------
    TypeError
        If the input data is invalid
    ValidError 
        If color is neither white or black
    """
    
    def __init__(self,color):
        if type(color) != str:
            raise ValueError("color must be of type string, current type is " + str(type(color)))
        
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteKnight.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackKnight.png")
        else:
            raise Exception("Invalid Piece Color for Knight")
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
class King:
    """
    Class that implements the King piece. Can move in all 8 directions but only one square at a time.
    
    Attributes
    -----------
    color : str
        The color of the piece. Ensures thats its value is either "white" or "black"
    texture : pygame.image
        The texture associated to the piece. Its a png file found in the assets folder
    
    
    Raises
    -------
    TypeError
        If the input data is invalid
    ValidError 
        If color is neither white or black
    """
    
    def __init__(self,color):
        if type(color) != str:
            raise ValueError("color must be of type string, current type is " + str(type(color)))
        
        self.color = color
        if self.color == "white":
            self.texture = pygame.image.load("assets/whiteKing.png")
        elif self.color == "black":
            self.texture = pygame.image.load("assets/blackKing.png")
        else:
            raise Exception("Invalid Piece Color for King")       
        self.texture = pygame.transform.scale_by(self.texture,1.5)
        
