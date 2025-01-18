import pygame
import copy
from pieces import Piece,King,Night,Bishop,Queen,Rook,Pawn
from location import Square
class ServerInterface:
    """
    The ServerInterface class handles all chessboard interactions server side.
    A Chessboard object is required for initialization
    Doesnt interact with any graphics.
    ...

    Attributes
    ----------
    chessboard : Chessboard
        a chessboard object used to display the game board on the screen
    selectedPiece : Piece
        the piece that was clicked, to display its red square and all its possibilitie
    eaten : dict
        All the pieces that have been eaten throughout the game

    Methods
    -------
    rookPossiblities(self,draw,piece,board,renderAllPossibilities)
        Calculates and renders the possibilities of a piece with a pieceType Rook
    bishopPossiblities(self,draw,piece,board,renderAllPossibilities)
        Calculates and renders the possibilities of a piece with a pieceType Bishop
    kingPossibilities(self,draw,piece,board,renderAllPossibilities)
        Calculates and renders the possibilities of a piece with a pieceType King
    knightPossibilities(self,draw,piece,board,renderAllPossibilities)
        Calculates and renders the possibilities of a piece with a pieceType Night
    pawnPossibilities(self,draw,piece,board,renderAllPossibilities)
        Calculates and renders the possibilities of a piece with a pieceType Pawn
    getBoard(self)
        Returns the board
    isValidBoard(self,board,whiteKingPos, blackKingPos,renderAllPossibilities)
        Checks board and returns an integer representing no checks, white in check or black in check
    move(self,x,y)
        All the process behind moving a piece
    renderSelectedPiece(self,draw = True,piece = None,board = None,renderAllPossibilities = True)
        Renders the possibilities of a piece no matter the type
    isCheckmate(self,color)
        Looks at a position in check and checks if it is salvagable or if its checkmate
    """
    def __init__(self,board):
        self.chessboard = board
        self.selectedPiece = None
        self.eaten = {"r":0 , "b": 0, "n":0,"q":0,"k":0,"p":0, "R":0 , "B": 0, "N":0,"Q":0,"K":0,"P":0}

    def rookPossiblities(self,piece,board,renderAllPossibilities):
        """
        Calculates the possibilities of movement for a Piece of pieceType Rook

        Parameters
        ----------
        piece : Piece
            The Piece to be rendered
            Ensures that 0 <= piece.column < self.chessboard.width
            Ensures that 0 <= piece.row < self.chessboard.height
        board : List<List<Piece>>>
            2D matrix that represents the chessboard of the game played
            Ensures all the items in array are either None or Piece objects
        renderAllPossibilities : bool
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal)
        
        Raises
        ------
        ValueError
            Either the board input size doesnt match the self.chessboard size, or the board input doesnt have the appropiate format
        """
        currentPosX,currentPosY = piece.column,piece.row
        
        #Ensures the piece position is correct
        if currentPosX < 0 or currentPosX >= self.chessboard.width:
            raise ValueError("The x current position is invalid, cant be lower than 0 or higher than the chessboards width - 1. Value is: "+ str(currentPosX))
        if currentPosY < 0 or currentPosY >= self.chessboard.height:
            raise ValueError("The y current position is invalid, cant be lower than 0 or higher than the chessboards height - 1. Value is: "+ str(currentPosY))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
                
        
        """
        Iterates through all four main directions of the rook (up,down,left,right)
        Second loop repeats until the position is out of the grid, or found a piece. If the piece is of a different color, allows 
            that possibility but stops anyway
        
        If renderAllPossibilities is disabled, it simulates the move and if the move puts you in check, doesnt allow it
        """
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            p = 1
            while currentPosX  + p*dx < self.chessboard.width and currentPosY  + p*dy < self.chessboard.height and currentPosX  + p*dx >= 0 and currentPosY  + p*dy >= 0:
                
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+p*dx,currentPosY+p*dy)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+p*dy][currentPosX+p*dx] or  board[currentPosY+p*dy][currentPosX+p*dx].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((currentPosX+p*dx,currentPosY+p*dy))
                
                if board[currentPosY+p*dy][currentPosX+p*dx] != None:
                    break
                
                p+= 1
                  
    def bishopPossiblities(self,piece,board,renderAllPossibilities):
        """
        Calculates the possibilities of movement for a Piece of pieceType Bishop

        Parameters
        ----------
        piece : Piece
            The Piece to be rendered
            Ensures that 0 <= piece.column < self.chessboard.width
            Ensures that 0 <= piece.row < self.chessboard.height
        board : List<List<Piece>>>
            2D matrix that represents the chessboard of the game played
            Ensures all the items in array are either None or Piece objects
        renderAllPossibilities : bool
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal)
        
        Raises
        ------
        ValueError
            Either the board input size doesnt match the self.chessboard size, or the board input doesnt have the appropiate format
        """
        currentPosX,currentPosY = piece.column,piece.row
        
        #Ensures the piece position is correct
        if currentPosX < 0 or currentPosX >= self.chessboard.width:
            raise ValueError("The x current position is invalid, cant be lower than 0 or higher than the chessboards width - 1. Value is: "+ str(currentPosX))
        if currentPosY < 0 or currentPosY >= self.chessboard.height:
            raise ValueError("The y current position is invalid, cant be lower than 0 or higher than the chessboards height - 1. Value is: "+ str(currentPosY))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
        
        """
        Iterates through all four main directions of the bishop (top-left,top-right,bottom-left,bottom-right)
        Second loop repeats until the position is out of the grid, or found a piece. If the piece is of a different color, allows 
            that possibility but stops anyway
        
        If renderAllPossibilities is disabled, it simulates the move and if the move puts you in check, doesnt allow it
        """
        for dx,dy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            p = 1
            while currentPosX  + p*dx < len(board) and currentPosY  + p*dy < len(board[0]):
                
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+p*dx,currentPosY+p*dy)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+p*dy][currentPosX+p*dx] or  board[currentPosY+p*dy][currentPosX+p*dx].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((currentPosX+p*dx,currentPosY+p*dy))
                
                if board[currentPosY+p*dy][currentPosX+p*dx] != None:
                    break
                
                p+= 1
        
    def kingPossibilities(self,piece,board,renderAllPossibilities):
        """
        Calculates the possibilities of movement for a Piece of pieceType King

        Parameters
        ----------
        piece : Piece
            The Piece to be rendered
            Ensures that 0 <= piece.column < self.chessboard.width
            Ensures that 0 <= piece.row < self.chessboard.height
        board : List<List<Piece>>>
            2D matrix that represents the chessboard of the game played
            Ensures all the items in array are either None or Piece objects
        renderAllPossibilities : bool
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal)
        
        Raises
        ------
        ValueError
            Either the board input size doesnt match the self.chessboard size, or the board input doesnt have the appropiate format
        """
        currentPosX,currentPosY = piece.column,piece.row
        
        #Ensures the piece position is correct
        if currentPosX < 0 or currentPosX >= self.chessboard.width:
            raise ValueError("The x current position is invalid, cant be lower than 0 or higher than the chessboards width - 1. Value is: "+ str(currentPosX))
        if currentPosY < 0 or currentPosY >= self.chessboard.height:
            raise ValueError("The y current position is invalid, cant be lower than 0 or higher than the chessboards height - 1. Value is: "+ str(currentPosY))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
                
        
        """
        Iterates through all eight main directions of the king (up,down,left,right,top-left,top-right,bottom-left,bottom-right)
            and ensures it is within the boards bounds.If the the target square has a piece of the same color, the move isnt added
        If renderAllPossibilities is disabled, it simulates the move and if the move puts you in check, doesnt allow it
        """
        for x,y in [(-1,0),(-1,1),(1,-1),(0,-1),(1,0),(0,1),(1,1),(-1,-1)]:
            dx = currentPosX + x
            dy = currentPosY + y
            if 0 <= dy < len(board) and 0 <= dx < len(board[0]):
                
                if not renderAllPossibilities:
                    
                    if self.selectedPiece.pieceType.color == "white":
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(dx,dy)),(dx,dy),self.chessboard.blackKingPos,True)
                    else:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(dx,dy)),self.chessboard.whiteKingPos,(dx,dy),True)
                
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[dy][dx] or board[dy][dx].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((dx,dy))
                    
                    
        #Check for castling
        if piece.pieceType.color == "white":
            if self.chessboard.whiteQueenCastling and self.chessboard.board[7][1] == self.chessboard.board[7][2]  == self.chessboard.board[7][3] == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(2,7)),(2,7),self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[2][7] or board[2][7].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((2,7))
                                
            if self.chessboard.whiteKingCastling and self.chessboard.board[7][5] == self.chessboard.board[7][6]  == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(6,7)),(6,7),self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[7][6] or board[7][6].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((6,7))
                    
        else:
            if self.chessboard.blackQueenCastling and self.chessboard.board[0][1] == self.chessboard.board[0][2]  == self.chessboard.board[0][3] == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(2,0)),self.chessboard.whiteKingPos,(2,0),True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[0][2] or board[0][2].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((2,0))
            if self.chessboard.blackKingCastling and self.chessboard.board[0][5] == self.chessboard.board[0][6]  == None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(6,0)),self.chessboard.whiteKingPos,(6,0),True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[0][6] or board[0][6].pieceType.color != piece.pieceType.color:
                        piece.currentPossibilities.add((6,0))
    
    def knightPossibilities(self,piece,board,renderAllPossibilities):
        """
        Calculates the possibilities of movement for a Piece of pieceType Night

        Parameters
        ----------
        piece : Piece
            The Piece to be rendered
            Ensures that 0 <= piece.column < self.chessboard.width
            Ensures that 0 <= piece.row < self.chessboard.height
        board : List<List<Piece>>>
            2D matrix that represents the chessboard of the game played
            Ensures all the items in array are either None or Piece objects
        renderAllPossibilities : bool
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal)
        
        Raises
        ------
        ValueError
            Either the board input size doesnt match the self.chessboard size, or the board input doesnt have the appropiate format
        """
        currentPosX,currentPosY = piece.column,piece.row
        
        #Ensures the piece position is correct
        if currentPosX < 0 or currentPosX >= self.chessboard.width:
            raise ValueError("The x current position is invalid, cant be lower than 0 or higher than the chessboards width - 1. Value is: "+ str(currentPosX))
        if currentPosY < 0 or currentPosY >= self.chessboard.height:
            raise ValueError("The y current position is invalid, cant be lower than 0 or higher than the chessboards height - 1. Value is: "+ str(currentPosY))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
                
        
        """
        Iterates through all eight main directions of the knight (2-up-1-left,2-up-1-right,2-down-1-left,
            2-down-1-right,2-left-1-up,2-left-1-down,2-right-1-up,2-right-1-down) and ensures it is within the
            boards bounds. If the the target square has a piece of the same color, the move isnt added
        If renderAllPossibilities is disabled, it simulates the move and if the move puts you in check, doesnt allow it
        """
        for x,y in [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]:
            dx = currentPosX + x
            dy = currentPosY + y
            
            if 0 <= dy < len(board) and 0 <= dx < len(board[0]):
                if not board[dy][dx] or board[dy][dx].pieceType.color != piece.pieceType.color:
                    
                    if not renderAllPossibilities:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(dx,dy)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                    
                    if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                        if not board[dy][dx] or  board[dy][dx].pieceType.color != piece.pieceType.color:
                            piece.currentPossibilities.add((dx,dy))
                        
    def pawnPossibilities(self,piece,board,renderAllPossibilities):
        """
        Calculates the possibilities of movement for a Piece of pieceType Pawn

        Parameters
        ----------
        piece : Piece
            The Piece to be rendered
            Ensures that 0 <= piece.column < self.chessboard.width
            Ensures that 0 <= piece.row < self.chessboard.height
        board : List<List<Piece>>>
            2D matrix that represents the chessboard of the game played
            Ensures all the items in array are either None or Piece objects
        renderAllPossibilities : bool
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal)
        
        Raises
        ------
        ValueError
            Either the board input size doesnt match the self.chessboard size, or the board input doesnt have the appropiate format
        """
        currentPosX,currentPosY = piece.column,piece.row
        
        #Ensures the piece position is correct
        if currentPosX < 0 or currentPosX >= self.chessboard.width:
            raise ValueError("The x current position is invalid, cant be lower than 0 or higher than the chessboards width - 1. Value is: "+ str(currentPosX))
        if currentPosY < 0 or currentPosY >= self.chessboard.height:
            raise ValueError("The y current position is invalid, cant be lower than 0 or higher than the chessboards height - 1. Value is: "+ str(currentPosY))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
                
        
        """
        For each pawn, the following checks are made:
        - For one square forward, checking if the square in front is empty 
        - For two squares forward, that the pawn is in its initial rank (either the second row for black or the seventh for white).
            and that the two squares in front are empty
        -For diagonal captures, that there is a piece of the opposite color in said diagonal
        -For en passant, that the diagonal is the en Passant Target square (found in self.chessboard.enPassantSquare)
        
        For all the previous check, the move isnt added if not renderAllPossibilities and the move puts you in check
            or if the move puts you out of the bounds of the board
        """
        if piece.pieceType.color == "white":
            #One and two squares forward
            if currentPosY > 0 and board[currentPosY-1][currentPosX] == None:
                if not renderAllPossibilities:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY-1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY-1][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY-1))
            if currentPosY == 6  and board[currentPosY-2][currentPosX] == None == board[currentPosY-1][currentPosX] :
                
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY-2)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY-2][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY-2))
                
            #diagonals
            if currentPosX > 0 and currentPosY > 0 and board[currentPosY-1][currentPosX-1] != None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY-1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY-1][currentPosX-1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX-1,currentPosY-1))
            if currentPosX < len(board[0])-1 and currentPosY > 0 and board[currentPosY-1][currentPosX+1] != None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY-1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY-1][currentPosX+1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX+1,currentPosY-1))
                    
            #look for en passant 
            if currentPosX > 0 and currentPosY > 0 and (currentPosX-1,currentPosY-1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY-1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    piece.currentPossibilities.add((currentPosX-1,currentPosY-1))
            if currentPosX < len(board[0])-1 and currentPosY > 0 and (currentPosX+1,currentPosY-1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY-1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                        piece.currentPossibilities.add((currentPosX+1,currentPosY-1))

        else:
            #One and two squares forward
            if currentPosY < len(board)-1 and board[currentPosY+1][currentPosX] == None:
                if not renderAllPossibilities:
                        validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY+1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+1][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY+1))
            if currentPosY == 1  and board[currentPosY+2][currentPosX] == None == board[currentPosY+1][currentPosX]:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX,currentPosY+2)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if not board[currentPosY+2][currentPosX]:
                        piece.currentPossibilities.add((currentPosX,currentPosY+2))
                
            #diagonals
            if currentPosX > 0 and currentPosY < len(board)-1 and board[currentPosY+1][currentPosX-1] != None:
                #check for oposite color
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY+1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY+1][currentPosX-1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX-1,currentPosY+1))
            if currentPosX < len(board[0])-1 and currentPosY < len(board)-1 and board[currentPosY+1][currentPosX+1] != None:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY+1)),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    if piece.pieceType.color != board[currentPosY+1][currentPosX+1].pieceType.color:
                        piece.currentPossibilities.add((currentPosX+1,currentPosY+1))
            
            #EN PASSANT
            if currentPosX > 0 and currentPosY < len(board)-1 and (currentPosX-1,currentPosY+1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX-1,currentPosY+1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                    piece.currentPossibilities.add((currentPosX-1,currentPosY+1))
            if currentPosX < len(board[0])-1 and currentPosY < len(board)-1 and (currentPosX+1,currentPosY+1) == self.chessboard.enPassantSquare:
                if not renderAllPossibilities:
                    validBoardStatus = self.isValidBoard(self.chessboard.simulateMoveTempBoard(piece,(currentPosX+1,currentPosY+1),True),self.chessboard.whiteKingPos,self.chessboard.blackKingPos,True)
                if renderAllPossibilities or validBoardStatus == 0 or (self.chessboard.toMove == "black" and validBoardStatus == 1) or (self.chessboard.toMove == "white" and validBoardStatus == 2):
                        piece.currentPossibilities.add((currentPosX+1,currentPosY+1))
   
    def getBoard(self):
        """
        Getter returning the board
            
        Returns
        -------
        Chessboard
            The board of the interface
        
        """
        return self.chessboard

    def isValidBoard(self,board,whiteKingPos, blackKingPos,renderAllPossibilities):
        """
        Checks if a current board position has any checks or not
        
        Returns 0 if no checks, returns 1 if white is in check, returns 2 if black is in check

        Parameters
        ----------
        board : <List<List<Piece>>>
            2D Matrix representing a chess board
        whiteKingPos : tuple(int,int)
            A tuple of (x,y) integers that represents the current grid position of the white king
            Ensures that 0 <= x < self.chessboard.width and 0 <= y < self.chessboard.height
        blackKingPos : tuple(int,int)
            A tuple of (x,y) integers that represents the current grid position of the black king
            Ensures that 0 <= x < self.chessboard.width and 0 <= y < self.chessboard.height
        renderAllPossibilities : bool
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal)
        
        Returns
        -------
        int
            0 represents no checks, 1 represents white is in check and 2 represents black is in check
        
        Raises
        -------
        ValueError
            If the board has an invalid format (wrong size or values) or the king positions arent valid
        """
        #Validate the kings positions
        if whiteKingPos[0] < 0 or whiteKingPos[0] >= self.chessboard.width:
            raise ValueError("White kings position has an invalid x value: ", str(whiteKingPos[0]))
        if whiteKingPos[1] < 0 or whiteKingPos[1] >= self.chessboard.height:
            raise ValueError("White kings position has an invalid y value: ", str(whiteKingPos[1]))
        
        if blackKingPos[0] < 0 or blackKingPos[0] >= self.chessboard.width:
            raise ValueError("White kings position has an invalid x value: ", str(whiteKingPos[0]))
        if blackKingPos[1] < 0 or blackKingPos[1] >= self.chessboard.height:
            raise ValueError("Black kings position has an invalid y value: ", str(whiteKingPos[1]))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
                
        
        
        """
        Loops through the entire board. If the current square has a value, we render its possibilities and look if any 
            of those possibilities include the opposite kings position.
            
        Return accordingly
        If nothing is found, no checks
        """
        for i in range(len(board)):
            for j in range(len(board[0])):
                #If the square isnt empty, look at what its targeting and check if the opposite king position is there
                if board[i][j] != None:
                    temporarySelectedPiece = board[i][j]
                    temporarySelectedPiece.currentPossibilities.clear()
                    self.renderSelectedPiece(temporarySelectedPiece,board,renderAllPossibilities)
                    if temporarySelectedPiece.pieceType.color == "black" and whiteKingPos in temporarySelectedPiece.currentPossibilities:
                        return 1
                    if temporarySelectedPiece.pieceType.color == "white" and blackKingPos in temporarySelectedPiece.currentPossibilities:
                        return 2
        return 0
    
    def move(self,x,y):
        if self.chessboard.board[y][x] == None:
            pass
        else:
            self.chessboard.halfMoves = 0
            pieceTypeLetter = str(type(self.chessboard.board[y][x].pieceType))[15]
            if self.chessboard.board[y][x].pieceType.color == "white":
                self.chessboard.whiteMaterial[pieceTypeLetter] -= 1
                self.eaten[pieceTypeLetter] += 1
            else:
                self.chessboard.blackMaterial[pieceTypeLetter.lower()] -= 1
                self.eaten[pieceTypeLetter.lower()] += 1
        
        #delete pawn when in en passant
        if self.selectedPiece.pieceType.color == "white":
            if type(self.selectedPiece.pieceType) == Pawn and (x,y) == self.chessboard.enPassantSquare:
                self.chessboard.blackMaterial["p"]-=1
                self.eaten["p"] += 1
                self.chessboard.board[y+1][x] = None
        else:
            if type(self.selectedPiece.pieceType) == Pawn and (x,y) == self.chessboard.enPassantSquare:
                self.chessboard.whiteMaterial["P"]-=1
                self.eaten["P"] += 1
                self.chessboard.board[y-1][x] = None
        
        
        #check either to disable or keep en passant square
        if type(self.selectedPiece.pieceType) == Pawn and abs(y-self.selectedPiece.row) == 2:
            print("KEEP EN PASSANT SQUARE")
            if self.selectedPiece.pieceType.color == "white":
                self.chessboard.enPassantSquare = (self.selectedPiece.column,self.selectedPiece.row-1)
            else:
                self.chessboard.enPassantSquare = (self.selectedPiece.column,self.selectedPiece.row+1)
        else:
            self.chessboard.enPassantSquare = None
        
        
        
        if self.chessboard.toMove == "white":
            if type(self.selectedPiece.pieceType) == King:
                
                self.chessboard.whiteKingPos = (x,y)
                if abs(self.selectedPiece.position[0] - x) != 2:
                    self.chessboard.whiteKingCastling = False
                    self.chessboard.whiteQueenCastling = False
                else:
                    if (x,y) == (6,7) and self.chessboard.whiteKingCastling:
                        self.chessboard.board[7][5] = self.chessboard.board[7][7]
                        self.chessboard.board[7][7] = None
                        self.chessboard.board[7][5].position = (5,7)
                    elif (x,y) == (2,7) and self.chessboard.whiteQueenCastling:
                        self.chessboard.board[7][3] = self.chessboard.board[7][0]
                        self.chessboard.board[7][0] = None
                        self.chessboard.board[7][3].position = (3,7)
                
            #Disable castling in case rook is moved
            if type(self.selectedPiece.pieceType) == Rook:
                if (self.selectedPiece.column, self.selectedPiece.row) == (0,7):
                    self.chessboard.whiteQueenCastling = False
                elif (self.selectedPiece.column, self.selectedPiece.row) == (7,7):
                    self.chessboard.whiteKingCastling = False
                
            self.chessboard.toMove = "black"
        else:
            if type(self.selectedPiece.pieceType) == King:
                
                self.chessboard.blackKingPos = (x,y)
                if abs(self.selectedPiece.position[0] - x) != 2:
                    self.chessboard.blackKingCastling = False
                    self.chessboard.blackQueenCastling = False
                else:
                    if (x,y) == (6,0) and self.chessboard.blackKingCastling:
                        self.chessboard.board[0][5] = self.chessboard.board[0][7]
                        self.chessboard.board[0][7] = None
                        self.chessboard.board[0][5].position = (5,0) 
                    elif (x,y) == (2,0) and self.chessboard.whiteQueenCastling:
                        self.chessboard.board[0][3] = self.chessboard.board[0][0]
                        self.chessboard.board[0][0] = None
                        self.chessboard.board[0][3].position = (3,0)
            #Disable castling in case rook is moved
            if type(self.selectedPiece.pieceType) == Rook:
                if (self.selectedPiece.column, self.selectedPiece.row) == (0,0):
                    self.chessboard.blackQueenCastling = False
                elif (self.selectedPiece.column, self.selectedPiece.row) == (7,0):
                    self.chessboard.blackKingCastling = False
            self.chessboard.toMove = "white"
        self.chessboard.board[self.selectedPiece.row][self.selectedPiece.column] = None
        self.selectedPiece.row = y
        self.selectedPiece.column = x
        self.chessboard.board[y][x] = self.selectedPiece
        self.selectedPiece.position = (x,y)
        
        
            #check for promotions
        if type(self.selectedPiece.pieceType) == Pawn:
            self.chessboard.halfMoves = 0
            if (self.selectedPiece.pieceType.color == "white" and y == 0) or (self.selectedPiece.pieceType.color == "black" and y == 7):
                print("PROMOTION!")
                newType = None
                while newType != "n" and newType != "b" and newType != "q" and newType != "r":
                    newType = input("Type n for knight, b for bishop, q for queen and r for rook: ")   
                    if newType == "n":
                        self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Night(self.selectedPiece.pieceType.color))
                    elif newType == "b":
                        self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Bishop(self.selectedPiece.pieceType.color))
                    elif newType == "r":
                        
                        self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Rook(self.selectedPiece.pieceType.color))
                    elif newType == "q":
                        self.chessboard.board[y][x] = Piece(self.selectedPiece.row,self.selectedPiece.column,Queen(self.selectedPiece.pieceType.color))
                    else:
                        print("INCORRECT INPUT")

        
            
        
        self.selectedPiece = None
        
    def renderSelectedPiece(self,piece = None,board = None,renderAllPossibilities = True):
        """
        Renders the possibilities of a piece, no matter its type. Acts like a parent method for the methods with
            the name <PieceType>Possibilities

        Parameters
        ----------
        draw : bool , optional
            If the pssibility circles should be drawn onto the screen or not. Defaults to True
        piece : Piece, optional
            The piece to be rendered, if left blank, defaults to None, which defaults to self.selectedPiece
            Ensures valid position
        board : <List<List<Piece>>>, optional
            The board which to which the piece is compared. If left blank defaults to none, which 
            defaults to self.chessboard.board
            Ensures the board size matches the self.chessboard size and all its pieceTypes are valid or None
        renderAllPossibilities : bool, optional
            If false, excludes those possibilities that puts you in a discovered check (which would be illegal).
            Defaults to true
        
        Raises
        -------
        TypeError
            If the input of the piece not of the allowed values, this will be triggered
        ValueError
            Will appear if either the pieces position is invalid, the boards size is invalid or the boards contents are invalid
        """
        
        #Defaulting the variables
        if not piece:
            piece = self.selectedPiece
        if not board:
            board = self.chessboard.board
            
            
        if piece.column < 0 or piece.column >= self.chessboard.width:
            raise ValueError("piece position has an invalid x value: ", str(piece.column))
        if piece.row < 0 or piece.row >= self.chessboard.height:
            raise ValueError("piece position has an invalid y value: ", str(piece.row))
        
        #Ensures board is valid
        if len(board) != self.chessboard.height or len(board[0]) != self.chessboard.width:
            raise ValueError("Input board size doesnt align with chessboard size. Input board height: ",str(len(board)) ,", chessboard height: ", str(self.chessboard.height), "Input board width: ",str(len(board[0])) ,", chessboard width: ", str(self.chessboard.width))
        for row in board:
            for item in row:
                if item != None and type(item) != Piece:
                    raise ValueError("Item in board is invalid: " + item)
        
        """
        Looks at the type of the piece and triggers the children methods accordingly
        
        Note: a queen is seen as the combination of rook and bishop, not its own method
        """
        if type(piece.pieceType) == Rook:
            self.rookPossiblities(piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Bishop:
            self.bishopPossiblities(piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Queen:
            self.bishopPossiblities(piece,board,renderAllPossibilities)
            self.rookPossiblities(piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == King:
            self.kingPossibilities(piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Night:
            self.knightPossibilities(piece,board,renderAllPossibilities)
        elif type(piece.pieceType) == Pawn:
            self.pawnPossibilities(piece,board,renderAllPossibilities)
        else:
            raise TypeError("Piece has no correct type")
    
    def isCheckmate(self,color):
        """
        Taking the self.chessboard.board as the current board, and assuming the position is already in check
        Checks if the position is a checkmate or not

        Parameters
        ----------
        color : str
            Represents the color the pieces that are being checked for checkmate
            Ensures it is either "black" or "white"
            
        Returns
        --------
        bool
            True if its checkmate False if its not    
        
        Raises
        -------
        ValueError
            If color is not "black" or "white"
        TypeError
            color is not of type string
        """
        
        #Validating data
        if type(color) != str:
            raise TypeError("color is not of type string, its value is: ", color, "and its type is: " ,type(color))
        
        if color != "black" and color != "white":
            raise ValueError("the value of color is neither black or white, its: ", color)
        
        """
        Iterates through the entire move, and for each piece do the following
        
        Calculate all its possibilities. And simulate each of the possibilities.
        If any of those possibilities stop the check, return False inmediatly
        
        In case none of the moves of any of the pieces stop the check, return False
        """
        for i in range(len(self.chessboard.board)):
            for j in range(len(self.chessboard.board[0])):
                
                temporaryBoard = self.chessboard.getTempBoard()
                currentPiece = temporaryBoard[i][j]
                
                if currentPiece and currentPiece.pieceType.color == color:
                    
                    self.renderSelectedPiece(currentPiece,temporaryBoard)
                    whiteKingPos = self.chessboard.whiteKingPos
                    blackKingPos = self.chessboard.blackKingPos
                    
                    movesToCheck = copy.copy(currentPiece.currentPossibilities)
                    for moves in movesToCheck:
                        
                        if type(currentPiece.pieceType) == King:
                            if color == "white":
                                whiteKingPos = moves
                            else:
                                blackKingPos = moves
                                
                        temporaryBoard = self.chessboard.getTempBoard()
                        temporaryBoard[i][j] = None
                        temporaryBoard[moves[1]][moves[0]] = currentPiece
                        currentPiece.position = moves
                        
                        if self.isValidBoard(temporaryBoard,whiteKingPos,blackKingPos,True) == 0:

                            return False
        return True
    
