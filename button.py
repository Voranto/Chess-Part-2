from graphics import Graphics
#edit
class Button:
    """
    Class for a button to display on the screen, can be interacted with
    
    Attributes
    ----------
    x : int
        The x position in pixels of the object
    y : int
        The y position in pixels of the object
    width : int
        The width in pixels of the button
    height : int
        The height in pixels of the button
    color : str
        A string representing a valid pygame color that maps to the color of the inside of the button
    text : str
        The text of the button
    graphics : Graphics
        The graphics object where everything is rendered on
    outline : str
        The outline of the button. Can be set to none for no outline
        
    Methods
    ---------
    setText(self,newText)
        Changes the text to be drawn
    drawButton(self)
        Draws the button, the outline and the text onto the screen
    posInButton(self,pos)
        Checks if a position is inside the button
    """
    
    def __init__(self,x,y,height,width,color,text,graphics):
        """
        The constructor for the class
        
        Parameters
        ---------
        See attributes
        
        Raises
        ------
        TypeError
            If input data is invalid
        ValueError
            If color is invalid for pygame
        """
        if type(x) != int:
            raise TypeError("x must be of type int, current type is {}".format(type(x)))
        self.x = x
        if type(y) != int:
            raise TypeError("y must be of type int, current type is {}".format(type(y)))
        self.y = y
        if type(width) != int:
            raise TypeError("width must be of type int, current type is {}".format(type(width)))
        self.width = width
        if type(height) != int:
            raise TypeError("height must be of type int, current type is {}".format(type(height)))
        self.height = height
        if type(color) != str:
            raise TypeError("color must be of type string, current type is {}".format(type(color)))
        
        if type(text) != str:
            raise TypeError("text must be of type string, current type is {}".format(type(text)))
        self.text = text
        if type(graphics) != Graphics:
            raise TypeError("graphics must be of type string, current type is {}".format(type(graphics)))
        self.graphics = graphics
        
        if not self.graphics.testColor(color):
            raise ValueError("Pygame color is invalid, current color is {}".format(color))
        self.color = color
        
        self.outline = None
    
    def setText(self,newText):
        
        """
        Changes button text
        
        Parameters
        ----------
        newText : str
            The new text to be set
        
        Raises
        ------ 
        TypeError
            Input data of invalid format
        """
        
        if type(newText) != str:
            raise TypeError("newText must be of type string, current type is {}".format(type(newText)))
        self.text = newText
        
    def drawButton(self):
        """
        Draws the button onto the screen. Text must fit in the button (no wrapping around)
        
        Raises
        ------
        ValueError
            If the text is too big
        """
        
        text_width,text_height = self.graphics.getSizeOfSmallText(self.text)
        
        if text_width > self.width: 
            raise ValueError("width of text cant be bigger than width of button")
        if text_height > self.height: 
            raise ValueError("width of text cant be bigger than width of button")
        
        dx = self.width - text_width
        dy = self.height - text_height
        if self.outline:
            self.graphics.drawSquare(self.outline,(self.x-3,self.y-3 , self.width+6,self.height +6))
        self.graphics.drawSquare(self.color,(self.x,self.y,self.width,self.height))
        self.graphics.drawSmallText(self.text,self.x + dx//2, self.y +dy//2)
        
    def posInButton(self,pos):
        """
        Checks if a position is within the bounds of the button
        
        Parameters
        ------------
        pos : tuple(int,int)
            The position to compare it with
            
        Returns
        --------
        bool 
            True if it is within the bounds, False otherwise
        
        Raises
        ------
        TypeError 
            If invalid input format
        """
        if type(pos) != tuple or type(pos[0]) != int or type(pos[1]) != int or len(pos) != 2:
            raise TypeError("pos must be of type tuple(int,int),current format is {}".format(pos))
        
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y+self.height:
            return True
        return False
        