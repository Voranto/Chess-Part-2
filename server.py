import socket
import threading
import random
from chessboard import Chessboard
from serverInterface import ServerInterface
from graphics import Graphics
import pickle


HOST = '127.0.0.1'  # Localhost
PORT = 5555

# List to store client connections
clients = []
MAX_CONNECTIONS = 2  # Limit to 2 connections

def convertCoords(x,y,color):
    if color == "white":
        return (x,y)
    return (7-x,7-y)

def getDataToSend(interface,dataToSend):
    dataToSend["FEN"] = interface.chessboard.boardToFEN()
    dataToSend["toMove"] = interface.chessboard.toMove
    if interface.selectedPiece:
        dataToSend["selectedPiecePos"] = interface.selectedPiece.position
    else:
        dataToSend["selectedPiecePos"] = (-1,-1)
    dataToSend["eaten"] = interface.eaten
    return dataToSend


def runGame(FEN,board,interface,dataToSend,clients):
    while True:
        for conn, addr in clients:
            dataToSend = getDataToSend(interface,dataToSend)
            conn.send(pickle.dumps(dataToSend))
            
            data = conn.recv(1024)
            if data:
                data = pickle.loads(data)
                color =data["color"]
                #we got a click
                if data["clickPos"] != (-1,-1):
                    x,y = data["clickPos"]
                    
                    if 0 < x < 800 and 0 < y < 800:
                        gridx,gridy = convertCoords(x//100,y//100,color)
                        
                        if not interface.selectedPiece and board.board[gridy][gridx] and board.board[gridy][gridx].pieceType.color == board.toMove:
                            interface.selectedPiece = board.board[gridy][gridx]
                            interface.selectedPiece.currentPossibilities.clear()
                            interface.renderSelectedPiece(None,None,False)
                        elif interface.selectedPiece and board.board[gridy][gridx] and (gridx,gridy) not in interface.selectedPiece.currentPossibilities:
                            interface.selectedPiece = board.board[gridy][gridx]
                            interface.selectedPiece.currentPossibilities.clear()
                            interface.renderSelectedPiece(None,None,False)
                        elif interface.selectedPiece and not board.board[gridy][gridx] and (gridx,gridy) not in interface.selectedPiece.currentPossibilities :
                            interface.selectedPiece = None
                        elif interface.selectedPiece and (gridx,gridy) in interface.selectedPiece.currentPossibilities:
                            if board.toMove == "black":
                                board.fullMoves += 1
                                board.halfMoves += 1
                            print("The {} has moved from {} to {}".format(interface.selectedPiece.getPieceInfo(),interface.selectedPiece.position, (gridx,gridy)))
                            interface.move(gridx,gridy)
                            
        #Check for checkmate after move
        if interface.isValidBoard(interface.chessboard.board,interface.chessboard.whiteKingPos,interface.chessboard.blackKingPos,True) == 1:
            if interface.isCheckmate("white"):
                dataToSend["checkmate"] = "black"
                print("Game has been finished by checkmate")
                for conn, addr in clients:
                    dataToSend = getDataToSend(interface,dataToSend)
                    conn.send(pickle.dumps(dataToSend))
                    data = conn.recv(1024)
                return 0
        elif interface.isValidBoard(interface.chessboard.board,interface.chessboard.whiteKingPos,interface.chessboard.blackKingPos,True) == 2:
            if interface.isCheckmate("black"):
                dataToSend["checkmate"] = "white"
                print("Game has been finished by checkmate")
                for conn, addr in clients:
                    dataToSend = getDataToSend(interface,dataToSend)
                    conn.send(pickle.dumps(dataToSend))
                    data = conn.recv(1024)
                return 0
            else:
                print("no data")

def handle_clients(clients):
    """
    Function to execute after 2 connections are established.
    """
    print("2 clients connected. Starting the game!")
    # Example: Send a message to both clients

    #asign colors
    whitePlayerIdx = 0
    whitePlayer = clients[whitePlayerIdx]
    clients[whitePlayerIdx][0].send(pickle.dumps("white"))
    blackPlayer = clients[1] if whitePlayer == clients[0] else clients[0]
    clients[0 if whitePlayerIdx == 1 else 1][0].send(pickle.dumps("black"))
    

    playersWantToPlay = [True,True]
    while playersWantToPlay[0] and playersWantToPlay[1]:
        FEN = "rnbqkbnr/pppp1ppp/8/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1"
        board = Chessboard(8,8)
        interface = ServerInterface(board)
        board.FENToBoard(FEN)
        dataToSend = {"FEN":None, "toMove": None, "selectedPiecePos": None,"eaten":None,"checkmate" : None,"restart":False,"quit":False}
        runGame(FEN,board,interface,dataToSend,clients)
        playersWantToPlay = [None,None]
        while playersWantToPlay[0] == None or playersWantToPlay[1] == None:
            for i in range(len(clients)):
                conn,addr = clients[i]
                conn.send(pickle.dumps(dataToSend))
                data = pickle.loads(conn.recv(1024))
                if data["wantsToPlay"] == "p":
                    playersWantToPlay[i] =  True
                elif data["wantsToPlay"] == "q":
                    playersWantToPlay[i] =  False
        if playersWantToPlay[0] == True == playersWantToPlay[1]:
            print("Play again")
            dataToSend["restart"] = True
        else:
            print("Quit")
            dataToSend["quit"] = True
        for conn, addr in clients:
            conn.send(pickle.dumps(dataToSend))
            data = pickle.loads(conn.recv(1024))
    
    print("Server finished succesfully")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}, waiting for {MAX_CONNECTIONS} connections...")

    while len(clients) < MAX_CONNECTIONS:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        clients.append((conn, addr))

    # Stop accepting connections
    print("Max connections reached. No longer accepting new clients.")
    server.close()  # Close the server socket to stop new connections

    # Execute the function with the connected clients
    handle_clients(clients)

if __name__ == "__main__":
    start_server()
