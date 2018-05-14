from Tkinter import *
from random import randint

class Ball:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.posx = (x1+x2)/2
        self.posy = (y1+y2)/2
        self.size = (x2-x1)
        self.canvas = canvas
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="red")

    def move_ball(self):
        global movementBall, p1Board, p2Board, p1Score, p2Score
        deltax = movementBall[0]
        deltay = movementBall[1]
        if (deltax + self.posx - self.size/2 < widthBoard or deltax + self.posx + self.size/2 > widthCanvas - widthBoard):
            if ((p1Board.get_pos() + heightBoard/2 >= self.posy and self.posy >= p1Board.get_pos() - heightBoard/2 and self.posx > widthCanvas) or
                (p2Board.get_pos() + heightBoard/2 >= self.posy and self.posy >= p2Board.get_pos() - heightBoard/2 and self.posx < widthCanvas)):
                print 'hit @', p1Board.get_pos(), p2Board.get_pos(), ':', self.posx, self.posy
                if (deltax < 0):
                    deltax = movementBall[0] = -(deltax-2)
                else:
                    deltax = movementBall[0] = -(deltax+2)
            else:
                print 'missed @', p1Board.get_pos(), p2Board.get_pos(), ':', self.posy,  'ball speed re-adjusted'
                print p1Board.get_pos() + heightBoard/2, self.posy, p1Board.get_pos() - heightBoard/2
                print (p1Board.get_pos() + heightBoard/2 >= self.posy, self.posy >= p1Board.get_pos() - heightBoard/2, self.posx > widthCanvas)
                print ''
                print p2Board.get_pos() + heightBoard/2, self.posy, p2Board.get_pos() - heightBoard/2
                print (p2Board.get_pos() + heightBoard/2 >= self.posy, self.posy >= p2Board.get_pos() - heightBoard/2, self.posx < widthCanvas)
                if (self.posx < widthCanvas):
                    p1Score += 1
                    p1ScoreText.set("Player 1 : "+str(p1Score))
                else:
                    p2Score += 1
                    p2ScoreText.set("Player 2 : "+str(p2Score))
                    
                deltax = movementBall[0] = -(deltax/2)
                deltay = movementBall[1] = -(deltay/2)
                
        if (deltay + self.posy - self.size/2 < 0 or deltay + self.posy + self.size/2 > heightCanvas):
            if (deltay < 0):
                deltay = movementBall[1] = -(deltay-2)
            else:
                deltay = movementBall[1] = -(deltay+2)
            
                
        self.posx += movementBall[0]
        self.posy += movementBall[1]
        self.canvas.move(self.ball, deltax, deltay)
        self.canvas.after(100, self.move_ball)

class Board:
    def __init__(self, canvas, x1, y1, x2, y2, no):
        self.no = no
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.pos = (y1+y2)/2
        self.canvas = canvas
        self.ball = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="black")

    def move_board(self):
        deltay = movementBoards[(self.no+1)%2]
        if (self.pos + deltay - heightBoard/2 < 0 or self.pos + deltay + heightBoard/2 > heightCanvas):
            movementBoards[(self.no+1)%2] = deltay = 0
        else:
            self.pos += deltay
        
        self.canvas.move(self.ball, 0, deltay)
        self.canvas.after(100, self.move_board)

    def get_pos(self):
        return self.pos
    
def setFocus():
    global movementBall
    movementBall = [randint(5, 10), randint(-5, 5)]
    gameCanvas.focus_set()

# key events  
def keydown(e):
    global movementBoards    
    if (e.char == 'q'):
        if (movementBoards[0] == -10):
            movementBoards[0] = -15
        elif (movementBoards[0] == -5):
            movementBoards[0] = -10
        else:
            movementBoards[0] = -5
            
    if (e.char == 'a'):
        movementBoards[0] = 0
            
    if (e.char == 'z'):
        if (movementBoards[0] == 10):
            movementBoards[0] = 15
        elif (movementBoards[0] == 5):
            movementBoards[0] = 10
        else:
            movementBoards[0] = 5
            
    if (e.char == 'o'):
        if (movementBoards[1] == -10):
            movementBoards[1] = -15
        elif (movementBoards[1] == -5):
            movementBoards[1] = -10
        else:
            movementBoards[1] = -5
            
    if (e.char == 'k'):
        movementBoards[1] = 0
            
    if (e.char == 'm'):
        if (movementBoards[1] == 10):
            movementBoards[1] = 15
        elif (movementBoards[1] == 5):
            movementBoards[1] = 10
        else:
            movementBoards[1] = 5
            
root = Tk()
root.title("Pong")
root.resizable(False,False)

# game frame
upFrame = Frame(root) 
upFrame.pack(side = TOP)

# score and setting frame
dwnFrame = Frame(root)
dwnFrame.pack(side = BOTTOM)

# basic measures
widthCanvas = 800
heightCanvas = 450
widthBoard = 20
heightBoard = 100

# score and setting canvas
otherCanvas = Canvas(dwnFrame, width = 800, height = 50) 

p1ScoreText = StringVar()
p1Label = Label(otherCanvas, textvariable = p1ScoreText)
p1Score = 0
p1ScoreText.set("Player 1 : "+str(p1Score))
p1Label.pack(side = LEFT, padx = 150)

newGameButton = Button(otherCanvas, text = "New Game", command = setFocus)
newGameButton.pack(side = LEFT)

p2ScoreText = StringVar()
p2Label = Label(otherCanvas, textvariable = p2ScoreText)
p2Score = 0
p2ScoreText.set("Player 2 : "+str(p2Score))
p2Label.pack(side = RIGHT, padx = 150)
otherCanvas.pack()

# game canvas
gameCanvas = Canvas(upFrame, width = widthCanvas, height = heightCanvas)

# binding keys for playing
gameCanvas.bind("<KeyPress>", keydown) 
gameCanvas.pack()

# create board object and animate it
movementBoards = [0, 0]

p1BoardPos = heightCanvas/2
p1Board = Board(gameCanvas, 5, p1BoardPos - heightBoard/2, widthBoard, p1BoardPos + heightBoard/2, 1)
p1Board.move_board()

p2BoardPos = heightCanvas/2
p2Board = Board(gameCanvas, widthCanvas - widthBoard, p2BoardPos - heightBoard/2, widthCanvas - 5, p2BoardPos + heightBoard/2, 2)
p2Board.move_board()

# create ball object and animate it
movementBall = [0, 0]

ball = Ball(gameCanvas, widthCanvas/2-25, heightCanvas/2-25, widthCanvas/2+25, heightCanvas/2+25)
ball.move_ball()



root.mainloop()

