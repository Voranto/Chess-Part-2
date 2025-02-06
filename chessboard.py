from pieces import Piece,King,Night,Bishop,Queen,Rook,Pawn
from location import Square



class Chessboard:
    """
    The Chessboard class represents a current chess game.
    
    Attributes
    ----------
    height : int
        The number of squares, vertically, of the chessboard. Ensures height = width
    width : int
        The number of squares, horizontally, of the chessboard. Ensures width = height
    board: List<List<Piece>>
        The current board of the chess game as a 2D matrix. All squares set to None at initialization
    toMove : str
        Whoevers turn is to move in the chess game. Must be either "white" or "black"
    fullMoves : int
        The total number of chess moves that have been done in the game
    halfMoves : int
        This is the number of moves since the last capture or pawn advance, or loss of castling rights
    whiteMaterial : dict[str] = int
        The material for the white player currently on the board
    blackMaterial : dict[str] = int
        The material for the black player currently on the board
    enPassantSquare : tuple(int,int)
        The square to where en Passant can be done. Is set to None at construction
    whiteKingPos : tuple(int,int)
        The square where the white king is currently placed at. Is set to None at construction
    blackKingPos : tuple(int,int)
        The square where the black king is currently placed at. Is set to None at construction
    whiteKingCastling : bool
        The ability to castle for the white king in the kings side (the short side)
    whiteQueenCastling : bool
        The ability to castle for the white queen in the kings side (the long side)
    blackKingCastling : bool
        The ability to castle for the black king in the kings side (the short side)
    blackQueenCastling : bool
        The ability to castle for the black queen in the kings side (the long side)
        
    
    Methods
    ---------
    getWidth(self)
        getter for the width of the chessboard
    getHeight(self)
        getter for the height of the chessboard
    getFEN(self)
        gets the Forsyth–Edwards Notation of the chessboard, represents a current game state
    setFEN(self,value)
        sets the chessboards FEN to the value
    getBoard(self)
        returns a copy of the board as a 2d matrix of size height and width
    setBoard(self,board)
        sets the board when given a 2D matrix
    FENToBoard(self,FEN)
        Converts a valid given FEN into its board equivalent (2D matrix)
    boardToFEN(self,board = None)
        Converts a valid 2D matrix into its FEN equivalent
    getTempBoard(self)
        Returns a perfect copy of the board without including any references
    printBoardInfo(self)
        Prints all the chessboards information, for debugging purposes
    simulateMoveTempBoard(self,piece,goToPosition,enPassant = False)
        Simulates a move on the temporary board and returns the updated board
    """
    def __init__(self, height, width):
        """
        Constructor for the Chessboard Class
        
        Parameters
        ----------
        height : int
            Height in squares of the chessboard. Ensures height = width
        width : int
            Width in squares of the chessboard. Ensures height = width
        
        Raises
        -------
        ValueError
            If height isnt equal to width
        TypeError
            If the input data is invalid
        """
        if type(height) != int:
            raise TypeError("height must be of type int, current type is " + str(type(height)))
        if type(width) != int:
            raise TypeError("width must be of type int, current type is " + str(type(width)))
        
        if (height != width):
            raise ValueError("The chess grid must be square")
        self.height = height
        self.width = width
        self.board = [[None]*width for _ in range(height)]
        
        self.toMove = "white"
        self.fullMoves = 1
        self.halfMoves = 0
        
        self.whiteMaterial = {"R":0 , "B": 0, "N":0,"Q":0,"K":0,"P":0}
        self.blackMaterial = {"r":0 , "b": 0, "n":0,"q":0,"k":0,"p":0}
        
        self.enPassantSquare = None
        
        self.whiteKingPos = None
        self.blackKingPos = None
        
        #Castling booleans
        self.whiteKingCastling = True
        self.whiteQueenCastling = True
        self.blackKingCastling = True
        self.blackQueenCastling = True
     
    def getWidth(self):
        """
        Getter for the width of the board
        
        Returns
        -------
        int
            The width of the board
        """
        return self.width
    
    def getHeight(self):
        """
        Getter for the height of the board
        
        Returns
        -------
        int
            The height of the board
        """
        return self.height
    
    def getFEN(self):
        """
        Getter for the FEN of the board
        
        Returns
        -------
        str
            The FEN of the board
        """
        return self.boardToFEN()

    def setFEN(self, value):
        """
        Setter for the FEN of the board
        
        Parameters
        -------
        str : value
            The FEN to be set
        """
        self.FEN = value

    def getBoard(self):
        """
        Getter for the current board as a 2D matrix
        
        Returns
        -------
        List<List<Piece>>>
            2D matrix of the board, making a copy of it (not a deep copy)
        """
        return self.board[:]
    
    def setBoard(self, board):
        """
        Sets a new board
        
        Parameters
        -------
        board : List<List<Piece>>> 
            2D matrix of the board to be set, must be valid
        
        Raises
        -----
        ValueError
            If the given board has invalid dimensions
        TypeError
            If the given board has invalid items inside of it
        """
        if len(board) != self.width or len(board[0]) != self.height:
            raise ValueError("Dimensions of the new board must match.  Current dimensions are {} x {}, dimensions that are trying to be set are {} x {}".format(self.width,self.height,len(board[0]),len(board)))
        
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise TypeError("Invalid item inside matrix: {}".format(item))
        
        self.board = board[:]

    def FENToBoard(self,FEN):
        """
        Function to convert a FEN into its appropiate 2D matrix. 
        A FEN record contains six fields, each separated by a space. The fields are as follows:

            -Piece placement data: Each rank is described, starting with rank 8 and ending with rank 1, with a 
                "/" between each one; within each rank, the contents of the squares are described in order from t
                he a-file to the h-file. Each piece is identified by a single letter taken from the standard 
                English names in algebraic notation (pawn = "P", knight = "N", bishop = "B", rook = "R", 
                queen = "Q" and king = "K"). White pieces are designated using uppercase letters ("PNBRQK"), 
                while black pieces use lowercase letters ("pnbrqk"). A set of one or more consecutive empty 
                squares within a rank is denoted by a digit from "1" to "8", corresponding to the number of 
                squares.
            - Active color: "w" means that White is to move; "b" means that Black is to move.
            - Castling availability: If neither side has the ability to castle, this field uses the character "-".
                Otherwise, this field contains one or more letters: "K" if White can castle kingside, "Q" if 
                White can castle queenside, "k" if Black can castle kingside, and "q" if Black can castle
                queenside.A situation that temporarily prevents castling does not prevent the use of this notation.
            - En passant target square: This is a square over which a pawn has just passed while moving two 
                squares; it is given in algebraic notation. If there is no en passant target square, this field 
                uses the character "-". This is recorded regardless of whether there is a pawn in position to 
                capture en passant.[6] An updated version of the spec has since made it so the target square is 
                recorded only if a legal en passant capture is possible, but the old version of the standard is 
                the one most commonly used.
            - Halfmove clock: The number of halfmoves since the last capture or pawn advance, used for the 
                fifty-move rule.
            - Fullmove number: The number of the full moves. It starts at 1 and is incremented after Black's 
                move.
        
        Parameters
        ------------
        FEN : str
            The string to be converted onto the board
        
        Raises
        ---------
        TypeError
            Invalid input type
        ValueError
            FEN doesnt have the format described above
        """
        if type(FEN) != str:
            raise TypeError("FEN must be of type string, current type is {}".format(type(FEN)))
        
        n = len(FEN)
        i = 0
        j = 0
        self.board = [[None]*8 for _ in range(8)]
        self.whiteKingPos = None
        self.blackKingPos = None
        self.whiteMaterial = {"R":0 , "B": 0, "N":0,"Q":0,"K":0,"P":0}
        self.blackMaterial = {"r":0 , "b": 0, "n":0,"q":0,"k":0,"p":0}
        #board part of FEN
        for p in range(n):
            if FEN[p] == " ":
                p+= 1
                break
            
            elif FEN[p]  == "/":
                j += 1
                i = 0 
            else:
                if FEN[p].isdigit():
                    i += int(FEN[p])
                else:
                    if FEN[p].lower() == "p":
                        self.board[j][i] = Piece(j,i,Pawn("white" if FEN[p] == "P" else "black"))
                    elif FEN[p].lower() == "r":
                        self.board[j][i] = Piece(j,i,Rook("white" if FEN[p] == "R" else "black"))
                    elif FEN[p].lower() == "n":
                        self.board[j][i] = Piece(j,i,Night("white" if FEN[p] == "N" else "black"))
                    elif FEN[p].lower() == "b":
                        self.board[j][i] = Piece(j,i,Bishop("white" if FEN[p] == "B" else "black"))
                    elif FEN[p].lower() == "q":
                        self.board[j][i] = Piece(j,i,Queen("white" if FEN[p] == "Q" else "black")) 
                    elif FEN[p].lower() == "k":
                        self.board[j][i] = Piece(j,i,King("white" if FEN[p] == "K" else "black"))
                        
                        if FEN[p] == "K":
                            if self.whiteKingPos:
                                raise ValueError("Already one king on the board of the same color")
                            self.whiteKingPos  = (i,j)
                        else:
                            if self.blackKingPos:
                                raise ValueError("Already one king on the board of the same color")
                            self.blackKingPos  = (i,j)
                    else:
                        raise ValueError(f"Invalid piece type '{FEN[p]}' at position {p} in FEN: {FEN}")

                    if FEN[p] in self.whiteMaterial:
                        self.whiteMaterial[FEN[p]] += 1
                    else:
                        self.blackMaterial[FEN[p]] += 1
                    i+= 1
        
        currentCheck = 0
        while p < n:
            if FEN[p] == " ":
                currentCheck += 1
            else:
                #Checking who is to move
                if currentCheck == 0:
                    if FEN[p] == "w":
                        self.toMove = "white"
                    elif FEN[p] == "b":
                        self.toMove = "black"
                    else:
                        raise ValueError("Invalid color when reading the FEN")
                    
                    
                elif currentCheck == 1:
                    self.whiteKingCastling = FEN[p] != "-"
                    self.whiteQueenCastling = FEN[p+1] != "-"
                    self.blackKingCastling = FEN[p+2] != "-"
                    self.blackQueenCastling = FEN[p+3] != "-"
                    p+= 3 
                elif currentCheck == 2:
                    if FEN[p] == "-":
                        pass
                    else:
                        self.enPassantSquare = (ord(FEN[p])-97, int(FEN[p+1]))
                        if not ( 0 <= self.enPassantSquare[0] < self.width and 0 <= self.enPassantSquare[1] < self.height):
                            raise ValueError("Invalid en passant square")
                        p+= 1
                
                elif currentCheck == 3:
                    self.halfMoves = int(FEN[p])
                
                elif currentCheck == 4:
                    self.fullMoves = int(FEN[p])
                
                else:
                    raise ValueError("currentCheck has too high a value. Too many spaces in the FEN")
            p+= 1
        
    def boardToFEN(self,board = None):
        """
        Converts 2D matrix into its appropiate FEN. Board must be valid. Defaults to None which
            defaults to self.board
        
        Parameters
        --------
        board : List<List<Piece>>
            The board to be converted
        
        Returns
        --------
        str
            The FEN of the 2d matrix
        
        Raises
        ------
        TypeError
            Invalid input type
        ValueError
            Board has incorrect pieces
        """
        
        
        if board == None: board = self.board
        
        if type(board) != list:
            raise TypeError("Input must be a list")
        
        if len(board) != self.height or len(board[0]) != self.width:
            raise TypeError("Board has invalid dimensions, current dimensions are {} x {}, and input dimensions are {} x {}".format(self.width,self.height,len(board[0]),len(board)))
        
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise TypeError("Invalid item inside matrix: {}".format(item))
        
        FEN = ""
        
        for i in range(len(board)):
            c = 0
            for j in range(len(board[0])):
                if board[i][j] == None:
                    c += 1
                else:
                    if c != 0:
                        FEN += str(c)
                    pieceTypeLetter = str(type(board[i][j].pieceType))[15]
                    if board[i][j].pieceType.color == "white":
                        FEN +=   pieceTypeLetter.upper()
                    else:
                        FEN += pieceTypeLetter.lower()
                    c = 0
            if c != 0:
                FEN += str(c)
            if i != len(board)-1:
                FEN += "/"
        FEN += " " + str(self.toMove)[0] + " "
        
        
        FEN += "K"if self.whiteKingCastling else "-"
        FEN += "Q"if self.whiteQueenCastling else "-"
        FEN += "k"if self.blackKingCastling else "-"
        FEN += "q"if self.blackQueenCastling else "-"
        
        FEN += " "
        
        if self.enPassantSquare:
            FEN += chr(self.enPassantSquare[0]+97)
            FEN += str(self.enPassantSquare[1])
        else:
            FEN += "-"
            
        FEN += " " + str(self.halfMoves)
        FEN += " " + str(self.fullMoves)
        return FEN
                                                             
    def getTempBoard(self):
        """
        Creates a deep copy of the board of the class. Used to simulate moves. No requirements because 
        the board already has the requirements built into it
        
        Returns
        --------
        List<List<Piece>>
            The deep copy of the board
        """
        
        
        temporaryBoard = []
        #create clone of board to not affect the main one
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                if self.board[i][j] == None:
                    temp.append(None)
                else:
                    curr = self.board[i][j]
                    temp.append(Piece(curr.row,curr.column, curr.pieceType))
            temporaryBoard.append(temp)
        return temporaryBoard         
                                
    def printBoardInfo(self):
        """
        Prints all the boards info, used for debugging purposes
        """
        
        for row in self.board:
            temp = [item.pieceType.color + str(type(item.pieceType)) if item else "None" for item in row]
            print(temp)
            
        print("Person to move is: ", self.toMove)
        print("White King Side Castling: ", self.whiteKingCastling)
        print("White Queen Side Castling: ", self.whiteQueenCastling)
        print("Black King Side Castling: ", self.blackKingCastling)
        print("Black Queen Side Castling: ", self.blackQueenCastling)
        print("White king pos: ", self.whiteKingPos)
        print("Black king pos: ", self.blackKingPos)
        if (self.enPassantSquare):
            print("En passant target square is: " ,self.enPassantSquare)
        else:
            print("No target en passant Square")
        
        print("Full moves: " ,self.fullMoves)
        print("Half moves: " ,self.halfMoves)
            
    def simulateMoveTempBoard(self,piece,goToPosition,enPassant = False):
        """
        Simulates a move on a temporary board with no effect on the real board, returns altered board
        
        Parameters
        ----------
        piece : Piece
            The piece that moves
        goToPosition : tuple(int,int)
            The position where the piece is moving, is guaranteed to be a valid position
        enPassant : bool
            Checks for en passant to delete piece that is affected. Defaults to false
        
        Returns 
        --------
        List<List<Piece>>
            The altere board
        
        Raises
        -------
        TypeError
            Invalid input type
        """
        if type(piece) != Piece:
            raise TypeError("piece must be of type Piece, current type is {}".format(type(piece)))
        if type(goToPosition) != tuple or type(goToPosition[0]) != int or type(goToPosition[1]) != int or len(goToPosition) != 2:
            raise TypeError("goToPosition must be of type tuple(int,int), current type is {}".format(goToPosition))
        
        x,y = goToPosition
        if (x,y) == (3,-1):
            print("ALERTTT")
        temporaryBoard = self.getTempBoard()
        temporaryPiece = Piece(piece.row,piece.column,piece.pieceType)
        temporaryBoard[piece.row][piece.column] = None
        temporaryBoard[y][x]= temporaryPiece
        temporaryPiece.setPosition(x,y)
        if enPassant:
            if piece.pieceType.color == "white":
                temporaryBoard[y+1][x] = None
            else:
                temporaryBoard[y-1][x] = None
        return temporaryBoard[:]
        