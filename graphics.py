import pygame
from chessboard import Chessboard
from pieces import Piece,King,Bishop,Queen,Rook,Pawn,Night
from location import Square

class Graphics:
    """
    The Graphics class handles all interactions with pygame, and with it, its interactions with the screen
    Requires for initialization a width and height for the screen resolution (in pixels), and a 
    Chessboard object that represents the board to be displayed
    ...

    Attributes
    ----------
    width : int
        The width of the screen, in pixels
    height : int
        The height of the screen, in pixels
    board : Chessboard
        The current game state of the chessboard to be displayed
    clientColor : str | None
        Represents the color of the client. Can be either "black", "white" or None if client hasnt been initialized
    screen : pygame.display
        Screen where all the textures and objects are drawn onto. Is initialized with the width and height from above
    pixelsPerSquare : int
        Constant, to represent how many pixels per square in the chessboards grid
    running : bool
        If the video system is running or not
    smallFont : pygame.font
        Small font used to render the difference in material between players
    my_font : pygame.font
        General font for general usage 
    bigFont : pygame.font
        Upscaled font for displaying checkmate
    defaultMove : pygame.mixer.Sound
        mp3 of the default moving sound from chess.com
    capture : pygame.mixer.Sound
        Sound made when capturing a piece in chess.com 
    specialSound : pygame.mixer.Sound
        Sound used for promotions
    Raises
    ------
    TypeError
        If the input data is not of the correct type
    
    Methods
    -------
    getScreenHeight(self)
        Returns the screens height
    getScreenWidth(self)
        Returns the screens width
    getScreen(self)
        Returns the screen object
    playDefaultSound(self)
        Plays the default sound, set in __init__
    playCaptureSound(self)
        Plays the capture sound, set in __init__
    playSpecialSound(self)
        Plays the special sound, set in __init__
    convertGridCoords(self,x,y,color)
        Converts grid coordinates depending on the color.
        Example:
            (1,1,"white) -> (1,1)
            (1,1,"black") -> (6,6)
    drawSmallPiece(self,pieceType,x,y)
        Draws a chess piece in a small size, done to render eaten material for each player
    drawPossibilityCircle(self,y,x)
        Draws a gray circle in a grid square to represent where selectedPiece can move
    checkForClick(self)
        Checks if in the current frame the user has clicked his mouse
    getPos(self)
        Returns current mouse position
    fillScreen(self,color)
        Fills the entire screen with a color. Used to "overwrite" the previous frame
    getEvents(self)
        Saves the events of the frame onto self.events
    checkForQuit(self)
        Detects if the user has closed the window
    drawSquare(self,color,rect)
        Draws a square of dimensions rect, of color color, on the screen
    renderToMove(self)
        Renders the text that displays which color has to move
    updateDisplay(self)
        Updates the display onto the clients screen
    drawSmallText(self,text, x,y)
        Draws a text of font size 15 in the x,y position in the screen
    getSizeOfSmallText(self,text)
        Returns the height and width the rect formed by the text
    renderOwnColor(self,color)
        Render the color you are playing in the chess match as text
    displayCheckmate(self,color)
        In case of checkmate, display the checkmate screen
    drawBoard(self,chessboard)
        Draws the squares of the chessboard onto client side screen
    printBoard(self)
        Prints board information for debugging purposes into the console
    drawPieces(self,chessboard,color)
        Draws the pieces of the chessboard onto the screen
    testColor(self,color)
        Returns true if color is valid pygame color false else
    drawText(self,text,x,y)
        Draws a text onto the screen with my_font
    getSizeOfText(self,text)
        Gets size of a text with my_font
    displayPromotionMenu(self,pieceList)
        Displays the promotion screen
    """
    def __init__(self, width, height,board):


        #Validate construction data
        if type(width) != int:
            raise TypeError("The width must be of type int, current type is: " + str(type(width)))
        if type(height) != int:
            raise TypeError("The height must be of type int, current type is: " + str(type(height)))
        if type(board) != Chessboard:
            raise TypeError("The board must be of type Chessboard, current type is: " + str(type(height)))
        
        self.screenHeight = height
        self.screenWidth = width
        self.board = board
        self.clientColor = None
        self.screen = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight))
        
        self.pixelsPerSquare = min(self.screenHeight,self.screenWidth) // 8
        
        
        
        self.running = True
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 15)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.bigFont = pygame.font.SysFont("Comic Sans MS", 100)
        self.defaultMove =  pygame.mixer.Sound('assets/defaultMove.mp3')
        self.capture =  pygame.mixer.Sound('assets/capture.mp3')
        self.specialSound =  pygame.mixer.Sound('assets/specialSound.mp3')
        
        
        self.events = []
        pygame.display.set_caption("Chess Board")
        
    def getScreenHeight(self):
        """
        Getter returning the screens height in pixels
            
        Returns
        -------
        int
            The height of the screen in pixels
        
        """
        return self.screenHeight
    
    def getScreenWidth(self):
        """
        Getter returning the screens width in pixels
            
        Returns
        -------
        int
            The width of the screen in pixels
        
        """
        return self.screenWidth
    
    def getScreen(self):
        """
        Getter returning the screen object of the graphics class
            
        Returns
        -------
        pygame.display
            The pygame screen object where everything is drawn onto
        
        """
        return self.screen

    def playDefaultSound(self):
        """
        Plays the default sound of a chess move. Default sound is built in class initialization in self.defaultMove
        """
        self.defaultMove.play()
    
    def playCaptureSound(self):
        """
        Plays the default sound of a chess capture. Capture sound is built in class initialization in self.capture
        """
        self.capture.play()
    
    def playSpecialSound(self):
        """
        Plays the default sound of a chess capture. Capture sound is built in class initialization in self.capture
        """
        self.specialSound.play()
    
    def convertGridCoords(self,x,y,color):
        """
        Function to convert grid coordinates based on color
        Server side color doesnt matter, but client side, for rendering and otherwise,
        black has an updated grid position.
        Examples:

        (1,1,"white") => (1,1)
        (1,1,"black") => (6,6)
        
        Parameters
        -----------
        x : int
            The x position of the piece. Ensures that 0 <= x < self.board.width
        y : int
            The y position of the piece. Ensures that 0 <= y < self.board.height
        color : str
            The color of the client. Ensures that it is either "white" or "black"
        
        Returns
        ---------
        tuple(int,int)
            The updated position in the form of a 2-tuple
        
        Raises
        ----------
        ValueError
            If the position isnt in the correct  range, or the color doesnt have the appropiate value
        TypeError
            If the input parameters are not of the correct type, as shown above
        """
        
        #validating position input data
        if type(x) != int :
            raise TypeError("x must be of type int, current type is " + str(type(x)) + " ,and has a value of: " + str(x))
        if type(y) != int :
            raise TypeError("x must be of type int, current type is " + str(type(y)) + " ,and has a value of: " + str(y))
        if x < 0 or x >= self.board.width or y < 0 or y > self.board.height:
            raise ValueError("Coordinate input was invalid. Must be in range 0 <= x < " + str(self.board.width) + " , 0 <= y < " + str(self.board.height) + " .Current position is: " +str(x) + ", " + str(y))
        
        
        
        #Validating color
        if type(color) != str:
            raise TypeError("color must be of type string, current type is " + str(type(color)) + " and has a value of " + str(color))
        if color != "white" and color != "black":
            raise ValueError("Color must be either white or black, current color is: " + color)
        
        
        if (x,y) == (-1,-1):
            return (-1,-1)
        if color == "white":
            return (x,y)
        else:
            return (7-x , 7-y)
    
    def drawSmallPiece(self,pieceType,x,y):
        """
        Draws a piece with a size of 27 pixels (as an arbitrary value). Used to display the eaten material client side
        
        Parameters
        -----------
        pieceType : Queen, Rook, Bishop, Night, Pawn, King
            The piece type of the piece to be drawn
        x : int
            The x position of the piece. 
        y : int
            The y position of the piece.
        
        
        Raises
        ----------
        TypeError
            If the input parameters are not of the correct type, as shown above
        """
        #Validating correct input type
        if type(pieceType) != Queen and type(pieceType) != Rook and type(pieceType) != Pawn and type(pieceType) != King and type(pieceType) != Night and type(pieceType) != Bishop:
            raise TypeError("pieceType doesnt have a type that appears in a chessboard, its current type is " + str(type(pieceType)))
        if type(x) != int:
            raise TypeError("x coordinate is not of type integer, current type is " + str(type(x)) + " and its value is " + str(x))
        if type(y) != int:
            raise TypeError("y coordinate is not of type integer, current type is " + str(type(y)) + " and its value is " + str(y))
        
        
        pieceSize = 27
        currentPiece = Piece(-1,-1,pieceType)
        texture = currentPiece.getTexture()
        texture = pygame.transform.scale(texture,(pieceSize,pieceSize))
        self.screen.blit(texture, (x,y))
    
    def drawPossibilityCircle(self,y,x):
        """
        Draws a small gray circle that represents the grid square where the selected piece can move to
        
        Parameters
        -----------
        x : int
            The x grid position of the piece. Ensures that 0 <= x < self.board.width
        y : int
            The y grid position of the piece. Ensures that 0 <= y < self.board.height
        
        
        Raises
        ----------
        TypeError
            If the input parameters are not of the correct type, as shown above
        ValueError
            If the grid coordinates (x,y) are out of their range
        """
        #Validating correct input type
        if type(x) != int:
            raise TypeError("x coordinate is not of type integer, current type is " + str(type(x)) + " and its value is " + str(x))
        if type(y) != int:
            raise TypeError("y coordinate is not of type integer, current type is " + str(type(y)) + " and its value is " + str(y))
        
        #validating data values
        if x < 0 or x >= self.board.width or y < 0 or y > self.board.height:
            raise ValueError("Coordinate input was invalid. Must be in range 0 <= x < " + str(self.board.width) + " , 0 <= y < " + str(self.board.height) + " .Current position is: " +str(x) + ", " + str(y))
        
        
        x,y = self.convertGridCoords(x,y,self.clientColor)
        pygame.draw.circle(self.screen, pygame.Color(80,80,80,2),(x*self.pixelsPerSquare + self.pixelsPerSquare // 2, y* self.pixelsPerSquare + self.pixelsPerSquare // 2),15)
    
    def checkForClick(self):
        """
        Detects if a click has been made
        
        Returns
        ---------
        bool
            If the left mouse click has been pressed
        """
        return pygame.mouse.get_pressed()[0]
    
    def getPos(self):
        """
        Returns the current mouse position relative to the screen
        
        Returns
        ---------
        tuple(int,int)
            A tuple in the form of (x,y) where x represents the horizontal distance to 
            the upper left corner and y the vertical distance to the upper left corner, in pixels
        """
        return pygame.mouse.get_pos()
    
    def fillScreen(self,color):
        """
        Fills the screen of a specific color, used to overwrite the previous frame
        
        Parameters
        -----------
        color : str
            The color which the screen is filled with. Ensures it is a valid color
        
        Raises
        --------
        ValueError
            If the input color is not accepted by pygame
        TypeError
            If the input color is not a string
        """
        if type(color) != str:
            raise TypeError("color must be of type string. Current type is " + str(type(color)) + " , and has a value of " + str(color))
        
        try:
            self.screen.fill(color)
        except:
            raise ValueError("Invalid color, ensure it is accepted by pygame. Current color: " + str(color))
    
    def getEvents(self):
        """
        Saves the current events of the frame onto self.events
        """
        self.events = pygame.event.get()
    
    def checkForQuit(self):
        """
        Checks if the pygame video system has been quit or not
        
        Returns
        ----------
        bool
            True if it has quit, False for the opposite
        """
        
        if not self.running:
            return True
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
                return True
        return False
    
    def drawSquare(self,color,rect):
        """
        Draws a square onto the screen. Used to display the squared grid of the chess game
        
        Parameters
        ---------------
        color : str , Pygame.color
            A string representing the pygame color of the current square. Ensures that its a color accepted by pygame
        rect : tuple(int,int,int,int)
            A 4-tuple where the values represent the following:
            - Horizontal distance (in pixels) from the upper left corner of the screen to the upper left corner of the square
            - Vertical distance (in pixels) from the upper left corner of the screen to the upper left corner of the square
            - Width of the square in pixels
            - Height of the square in pixels
        
        Raises
        --------
        TypeError
            If color is not of type string or rect is not a four tuple made of integers
        ValueError
            If color is neither "white" or "black"
        """
        
        #validating input data
        if type(color) != str and type(color) != pygame.Color:
            raise TypeError("color must be of type string. Current type is " + str(type(color)) + " , and has a value of " + str(color))
        if type(rect) != tuple or len(rect) != 4:
            raise TypeError("rect must be a tuple of length four, current  value is ", rect)

        #validating elements inside rect
        for i in range(4):
            if type(rect[i]) != int:
                raise TypeError("Elements inside tuple must all be of type int, the element in index " + str(i) + " is of type " + str(type(rect[i])))
        
        try:
            pygame.draw.rect(self.screen,color,rect)
        except:
            raise ValueError("Invalid color, ensure it is accepted by pygame. Current color: " + str(color))
        
    def renderToMove(self):
        """
        Renders which player is able to move in the chessboard
        """
        
        text1 = self.my_font.render("To move: ", False, (0, 0, 0))
        text2 = self.my_font.render(str(self.board.toMove).upper(), False, (0, 0, 0))
        self.screen.blit(text1, (820,10))
        self.screen.blit(text2, (830,50))
        
    def updateDisplay(self):
        """
        Updates the display onto the clients screen
        """
        pygame.display.update()
            
    def drawSmallText(self,text, x,y):
        """
        Draws a string with font size 15 (as an arbitrary value). Used to display how much material above the other the client has
        
        Parameters
        -----------
        text : str
            The text to be blitted onto the screen
        x : int
            The x position of the piece. 
        y : int
            The y position of the piece.
        
        
        Raises
        ----------
        TypeError
            If the input parameters are not of the correct type, as shown above
        """
        
        #Validating correct input type
        if type(text) != str:
            raise TypeError("text must piece of type string, its current type is " + str(type(text)))
        if type(x) != int:
            raise TypeError("x coordinate is not of type integer, current type is " + str(type(x)) + " and its value is " + str(x))
        if type(y) != int:
            raise TypeError("y coordinate is not of type integer, current type is " + str(type(y)) + " and its value is " + str(y))
        
        
        textToBlit = self.smallFont.render(text,False,(0,0,0))
        self.screen.blit(textToBlit,(x,y))
    
    def getSizeOfSmallText(self,text):
        """
        Gets the dimensions of a text object
        
        Params
        -------
        text : str
            The text you want the size of
        
        Returns
        --------
        int,int 
            The width and height of the text object
        
        Raises
        -------
        TypeError
            Input data is invalid
        """
        if type(text) != str:
            raise TypeError("Input data is invalid, type must be string and current type is {}".format(type(text)))
        
        return self.smallFont.size(text)
    
    def renderOwnColor(self,color):
        """
        Draws a string using my_font as its font to display the clients color in the game
        
        Parameters
        -----------
        color : str
            The color of the client
        
        Raises
        ----------
        TypeError
            If the input parameters are not of the correct type, as shown above
        """
        
        if type(color) != str:
            raise TypeError("color must be of type string, its current type is " + str(type(color)))
        
        text1 = self.my_font.render("You are: ", False, (0, 0, 0))
        text2 = self.my_font.render(str(color).upper(), False, (0, 0, 0))
        self.screen.blit(text1, (820,100))
        self.screen.blit(text2, (830,140))
        
    def displayCheckmate(self,color):
        """
        In case of checkmate, displays in the screen who has won
        
        Parameters
        -----------
        color : str
            The color of the client
        
        Raises
        ----------
        TypeError
            If the input parameters are not of the correct type, as shown above
        """
        
        if type(color) != str:
            raise TypeError("color must be of type string, its current type is " + str(type(color)))
        
        
        text1 = self.bigFont.render("CHECKMATE",False,(0,0,0))
        text2 = self.bigFont.render(str(color).upper() + " WINS",False,(0,0,0))
        pygame.draw.rect(self.screen, "lightgray",(80,230,700,350))
        self.screen.blit(text1,(100,250))
        self.screen.blit(text2,(80,400))
    
    def drawBoard(self,chessboard):
        """
        Draws the grid squares of the board in a checkboard pattern.
        Colors of the grid squares are declared below
        
        Parameters
        ------------
        chessboard : Chessboard
            The board to be displayed
            
        Raises
        ------ 
        TypeError 
            If the input type are incorrect
        """
        
        if type(chessboard) != Chessboard:
            raise TypeError("chessboard must be of type Chessboard, current type is: " + str(type(chessboard)))
        
        
        boardHeight = chessboard.height
        boardWidth = chessboard.width
        
        clearColor = "cornsilk2"
        darkColor = "chartreuse4"
        
        pixelsPerSquare = min(self.screenHeight,self.screenWidth) // boardHeight 
        
        
        """
        Iterates through the entire board, calculates the rect value of the current square, 
        checks wich color to pick for current square and applies accordingly
        
        """
        for i in range(boardHeight):
            for j in range(boardWidth):
                rectValues = (j*pixelsPerSquare,i*pixelsPerSquare,pixelsPerSquare,pixelsPerSquare)
                color = pygame.Color(darkColor) if (i+j)%2 == 1 else pygame.Color(clearColor)
                pygame.draw.rect(self.screen,color,rectValues)
    
    def printBoard(self):
        """
        Prints the boards information for debugging purposes
        """
        
        for row in self.board.board:
            for obj in row:
                if obj is None:
                    print("None", end=" ")
                else:
                    print(type(obj.pieceType), end=" ")
    
    def drawPieces(self,chessboard,color):
        """
        Draws the pieces of the chessboard onto the screen. Will be reversed for black
        
        Parameters
        ------------
        chessboard : Chessboard
            Currently unused, the board to be displayed
        color : str
            The color of the client. Ensures that its either "black" or "white"
        
        Raises
        ---------
        TypeError
            Input types are incorrect
        ValueError
            color is neither "black" or "white"
        """
        
        #Validating input data
        if type(chessboard) != Chessboard:
            raise TypeError("chessboard must be of type Chessboard, current type is: " + str(type(chessboard)))
        if type(color) != str:
            raise TypeError("color must be of type string, current type is: " + str(type(color)))
        
        if color != "white" and color != "black":
            raise ValueError("color must be either black or white, current color is: " + color)
        
        
        #Reverses the pieces for black
        pieces = self.board.getTempBoard()
        if color =="black":
            for i in range(len(pieces)):
                pieces[i] = pieces[i][::-1]
            pieces = pieces[::-1]
        boardHeight = chessboard.height
        boardWidth = chessboard.width
        
        pixelsPerSquare = min(self.screenHeight,self.screenWidth) // boardHeight 
        offset = 5
        n = len(pieces)
        m = len(pieces[0])
        
        for i in range(n):
            for j in range(m):
                currentPiece = pieces[i][j]
                if currentPiece == None:
                    continue
                
                self.screen.blit(currentPiece.getTexture(), (j*pixelsPerSquare + offset,i*pixelsPerSquare + offset))

    def testColor(self,color):
        """
        checks if a color is a valid pygame color
        
        Parameters
        ----------
        color : str
            The color to check
            
        Returns
        --------
        bool
            True if color is valid False otherwise
        
        Raises
        -------
        TypeError
            Input data invalid format
        """
        if type(color) != str:
            raise TypeError("Color must be of type string, current type is {}".format(type(color)))
        try:
            color = pygame.color.Color(color)
            return True
        except:
            return False
        
    def drawText(self,text, x,y):
        """
        Draws a string with regular sized font. 
        
        Parameters
        -----------
        text : str
            The text to be blitted onto the screen
        x : int
            The x position of the piece. 
        y : int
            The y position of the piece.
        
        
        Raises
        ----------
        TypeError
            If the input parameters are not of the correct type, as shown above
        """
        
        #Validating correct input type
        if type(text) != str:
            raise TypeError("text must piece of type string, its current type is " + str(type(text)))
        if type(x) != int:
            raise TypeError("x coordinate is not of type integer, current type is " + str(type(x)) + " and its value is " + str(x))
        if type(y) != int:
            raise TypeError("y coordinate is not of type integer, current type is " + str(type(y)) + " and its value is " + str(y))
        
        
        textToBlit = self.my_font.render(text,False,(0,0,0))
        self.screen.blit(textToBlit,(x,y))
    
    def getSizeOfText(self,text):
        """
        Gets the dimensions of a text object
        
        Params
        -------
        text : str
            The text you want the size of
        
        Returns
        --------
        int,int 
            The width and height of the text object
        
        Raises
        -------
        TypeError
            Input data is invalid
        """
        if type(text) != str:
            raise TypeError("Input data is invalid, type must be string and current type is {}".format(type(text)))
        
        return self.my_font.size(text)

    def displayPromotionMenu(self,pieceList):
        """
        Displays a promotion menu for the user to select the promoted piece.

        Parameters
        ----------
        graphics : Graphics
            The graphics object to handle rendering.
        color : str
            The color of the player ("white" or "black").
        Returns
        -------
        str
            The selected piece type ('q', 'r', 'b', 'n').
        """
        menu_running = True
        

        # Event loop to handle promotion selection
        while menu_running:
            self.screen.fill("white")
            self.drawText("Select a piece for promotion:", 300, 100)
            self.getEvents()
            for button in pieceList:
                button.drawButton("big")

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, button in enumerate(pieceList):
                        if button.posInButton(pos):
                            menu_running = False
                            return i

            self.updateDisplay()
    def darkenColor(self,colorStr):
        currentColor = pygame.Color(colorStr)
        return pygame.Color(int(currentColor.r * 0.7), int(currentColor.g * 0.7), int(currentColor.b * 0.7))