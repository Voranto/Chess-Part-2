# client.py
import socket
import threading
import pygame
from graphics import Graphics
from chessboard import Chessboard
import pickle
from clientInterface import ClientInterface
from button import Button
import time

HOST = '127.0.0.1'

PORT = 5555
secondPos = [400,300]
lock = threading.Lock()

color = None
pygame.init()
pygame.mixer.init()
pygame.font.init()

board = Chessboard(8,8)
graphics = Graphics(1000,800,board)
interface = ClientInterface(board,graphics)
FEN = None
toMove = None

"""
Function to convert grid coordinates based on color
Server side color doesnt matter, but client side, for rendering and otherwise,
black has an updated grid position.
Examples:

(1,1,"white") => (1,1)
(1,1,"black") => (6,6)
"""
def convertGridCoords(x,y,color):
    if (x,y) == (-1,-1):
        return (-1,-1)
    if color == "white":
        return (x,y)
    else:
        return (7-x , 7-y)
    

#Variables to send data and recieve data
selectedPiecePos = (-1,-1)
dataToSend = {"clickPos": (-1,-1),"color": None,"wantsToPlay": None}
quit = False
quit_event = threading.Event()
moveMade = False
clickDone = False
restart = False
#Function that runs a second thread in charge of the interchange of data with the server
def receive_data(conn):
    global secondPos,color,FEN,toMove,selectedPiecePos,interface,restart,dataToSend,quit
    """
        Handles the recieving and sending of data with the server

        Parameters
        ----------
        conn : socket
            The connection to the socket
        """
    
    while not quit_event.is_set():
        
        
        """
        Recieving 1024 bytes of data through the connection
        The data is a dictionary with the following format:
        
        - "FEN" Is a string displaying the Forsyth–Edwards Notation that describes a current chess game state. 
            Format is described in the FENToBoard Method in the Chessboard class
        - "toMove" is a string either "white" or "black" that displays the color to move in the current chess match
        - "selectedPiecePos" is a integer tuple the current grid position of the selected piece. Has to be within
            the range of 0 and 7 (both inclusive) the selected piece is intended to have its square have a red color
        - "eaten" is a dictionary representing the pieces that have been eaten during the current chess match
        """
        if interface.checkmate != "black" and interface.checkmate != "white":
            data = conn.recv(1024)
            if data:
                #Remember to lock the thread to prevent multiple threads grabbing the same data
                with lock:
                    
                    #Load the data using pickle
                    data = pickle.loads(data)
                    
                    #First data is to asign color to the client
                    if data =="white" or data =="black":
                        color = data
                        graphics.clientColor = color
                    else:
                        
                        #If the FEN has changed, update the client. If the FEN remains the same, no further changes are needed
                        if FEN != data["FEN"] and FEN:
                            moveMade = True

                        #Take the data sent and integrate it to the itnerface
                        FEN = data["FEN"]
                        toMove = data["toMove"]
                        selectedPiecePos = data["selectedPiecePos"]
                        interface.eaten = data["eaten"]
                        interface.checkmate = data["checkmate"]
                        #Update the client side selected position
                        if selectedPiecePos != (-1,-1) and interface.chessboard.board[selectedPiecePos[1]][selectedPiecePos[0]].pieceType.color == color:
                            interface.selectedPiece = interface.chessboard.board[selectedPiecePos[1]][selectedPiecePos[0]]
                        else:
                            interface.selectedPiece = None
            
            
            
                #Send the values to the server using pickle
                conn.send(pickle.dumps(dataToSend))
        else:
            with lock:
                data = conn.recv(1024)
                if data:
                    data = pickle.loads(data)
                    if data["restart"]:
                        restart = True
                    if data["quit"]:
                        quit = True
                        quit_event.set()
                conn.send(pickle.dumps(dataToSend))
                time.sleep(0.1)
                    
                
def main():
    global interface,quit,dataToSend,moveMade,restart
    # Pygame setup
    
    clock = pygame.time.Clock()
    playAgainButton = Button(145, 600,100,300,"gray","Click here to play again",graphics)
    quitButton = Button(465, 600,100,300,"gray","Click here to quit",graphics)
    # Connect to server
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    
    #Initialize secondary thread to handle server side interactions
    threading.Thread(target=receive_data, args=(conn,)).start()
    
    #Main loop handling chess-side stuff, not socket stuff
    running = True
    while running:
        if restart:
            print("GAME RESTARTED")
            interface.checkmate = None
            playAgainButton = Button(145, 600,100,300,"gray","Click here to play again",graphics)
            quitButton = Button(465, 600,100,300,"gray","Click here to quit",graphics)
            restart = False
            dataToSend["wantsToPlay"] = None
        
        #If no checkmate, game is running
        if interface.checkmate != "black" and interface.checkmate != "white":
            #Recieve the server side FEN, and apply it to the client side chessboard, remembering locking the thread        
            if FEN:
                with lock:
                    graphics.getEvents()
                    
                    previousWhiteMaterial = interface.chessboard.whiteMaterial
                    previousBlackMaterial = interface.chessboard.blackMaterial
                    interface.chessboard.FENToBoard(FEN)
                    if moveMade:
                        
                        
                        #Compare previous material to current material to look for captures to play the sound
                        captureOcurred = False
                        for piece in previousWhiteMaterial:
                            if previousWhiteMaterial[piece] != interface.chessboard.whiteMaterial[piece]:
                                captureOcurred = True
                                graphics.playCaptureSound()
                                break
                        for piece in previousBlackMaterial:
                            if previousBlackMaterial[piece] != interface.chessboard.blackMaterial[piece]:
                                captureOcurred = True
                                graphics.playCaptureSound()
                                break
                        if not captureOcurred:
                            graphics.playDefaultSound()
                        moveMade = False
                
            #Constant graphic updates
            
            """
            Asign values of data to send to the server, which consists of the following:
            - "color" represents the color of the client, for server side comparisons
            - "clickPos" is the current Mouse position in case of a click, else (-1,-1) as discard values
            """
            dataToSend["color"] = color
            if graphics.checkForClick() and color == toMove:
                dataToSend["clickPos"] = graphics.getPos()
            else:
                dataToSend["clickPos"] = (-1,-1)
            
            if quit or graphics.checkForQuit():
                quit_event.set()
                running = False
            
            graphics.fillScreen("gray")
            graphics.drawBoard(interface.chessboard)
            
            #Drawing the selectedPiece square
            if interface.selectedPiece and graphics:
                convertedPos = convertGridCoords(*selectedPiecePos,color)
                graphics.drawSquare("red",(convertedPos[0]* graphics.pixelsPerSquare, convertedPos[1]* graphics.pixelsPerSquare, graphics.pixelsPerSquare, graphics.pixelsPerSquare))
            
            #Draw the pieces of the current state
            if color:
                graphics.drawPieces(interface.chessboard,color)
            
            #Render the circles that represents the possibilities of the current piece
            with lock:
                if interface.selectedPiece:
                    interface.selectedPiece.currentPossibilities.clear()
                    interface.renderSelectedPiece(True,None,None,False)
            
            graphics.renderToMove()
            if interface.eaten:
                interface.renderEatenPieces()
                
            
            
            #Render more constant textures
            
            if color:
                graphics.renderOwnColor(color)
            
            
            graphics.updateDisplay()
            clock.tick(60)
        #checkmate has been achieved, check for new game
        else:
            with lock:
                
                graphics.getEvents()
                
                interface.chessboard.FENToBoard(FEN)
                if graphics.checkForClick():
                    if playAgainButton.posInButton(graphics.getPos()):
                        dataToSend["wantsToPlay"] = "p"
                        playAgainButton.outline = "red" 
                        quitButton.outline = None                  
                    if quitButton.posInButton(graphics.getPos()):
                        dataToSend["wantsToPlay"] = "q"
                        quitButton.outline = "red"
                        playAgainButton.outline = None
                        
                if quit or graphics.checkForQuit():
                    quit_event.set()
                    running = False
                graphics.fillScreen("gray")
                graphics.drawBoard(interface.chessboard)
                graphics.drawPieces(interface.chessboard,color)
                interface.renderEatenPieces()
                graphics.renderToMove()
                if color:
                    graphics.renderOwnColor(color)
                if interface.checkmate:
                    interface.graphics.displayEndScreen(interface.checkmate)
                playAgainButton.drawButton()
                quitButton.drawButton()
                clock.tick(60)
                graphics.updateDisplay()
            
        
    #Close connection at the end of the loop
    pygame.quit()
    exit()
    conn.close()

if __name__ == "__main__":
    main()
