import time
import tkinter as tk
from MineSweeper import *

class GameLoop:
    def __init__(self):
        self.initialize()
        self.loadContent()
        prevTime = 0
        while True:
            curTime = time.time()
            elapsedTime = curTime - prevTime
            self.update(elapsedTime)
            self.draw(elapsedTime)
            prevTime = curTime
    
    def initialize(self):
        xDim = 20
        yDim = 20
        bombs = int(xDim * yDim / 3)
        revealed = int(xDim * yDim / 10)
        self.game = Game(25,25,bombCount=bombs,revealedCount=revealed)
        self.cellSize = 50 * 15//yDim
        self.gameWon = True
        self.gameLost = False
        for x in range(self.game.xDim):
            for y in range(self.game.yDim):
                cell = self.game.getCell(x,y)
                if not cell.isBomb:
                    cell.bombNeighbors = self.game.getBombNeighbors(cell)

    
    def loadContent(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True) # make main window full-screen
        width = int(self.game.xDim * self.cellSize)
        height = int((self.game.yDim + 3) * self.cellSize)
        self.canvas = tk.Canvas(self.root, bg="lightgray", height=str(height), width=str(width))

    def update(self,elapsedTime):
        # Check if game has been won or lost
        self.gameWon = True
        self.gameLost = False
        for x in range(self.game.xDim):
            for y in range(self.game.yDim):
                cell = self.game.getCell(x,y)
                # If cell is a bomb and is not marked, player hasn't won
                if cell.isBomb and not cell.isMarked:
                    self.gameWon = False
                # If cell is a bomb and is not hidden, player has lost
                if cell.isBomb and not cell.isHidden:
                    self.gameLost = True
                # If cell is not a bomb and the cell is hidden, player hasn't won
                if not cell.isBomb and cell.isHidden:
                    self.gameWon = False

    def draw(self, elapsedTime):
        self.canvas.delete("all")
        for x in range(self.game.xDim):
            for y in range(self.game.yDim):
                cell = self.game.getCell(x,y)
                cellImage = self.drawCell(self.canvas, cell, self.cellSize)
                # bind to an onclick
                if cell.bombNeighbors == 0:
                    self.canvas.tag_bind(cellImage,'<Button-1>', cell.revealZeroNeighbors)
                else:
                    self.canvas.tag_bind(cellImage,'<Button-1>', cell.reveal)
                self.canvas.tag_bind(cellImage,'<Button-3>', cell.toggleMark)
        if self.gameWon:
            self.canvas.create_text(self.cellSize * self.game.xDim/2,self.cellSize * (self.game.yDim + 1),anchor='center',font="Arial",text="You Win!")
            self.drawButton(self.canvas,self.cellSize * self.game.xDim/2,self.cellSize * (self.game.yDim + 2),120,25,lambda e: self.initialize())
        if self.gameLost:
            self.canvas.create_text(self.cellSize * self.game.xDim/2,self.cellSize * (self.game.yDim + 1),anchor='center',font="Arial",text="You Lose...")
            self.drawButton(self.canvas,self.cellSize * self.game.xDim/2,self.cellSize * (self.game.yDim + 2),120,25,lambda e: self.initialize())
        self.canvas.pack()
        self.root.update()

    def drawButton(self,canvas,x,y,width,height,callback):
        btn = canvas.create_rectangle(x-width/2,y-height/2,x+width/2, y+height/2, outline='lightgray', fill='gray', width=2)
        txt = canvas.create_text(x,y,font='Arial',text="Play Again")
        canvas.tag_bind(btn,"<Button-1>",callback)
        canvas.tag_bind(txt,"<Button-1>",callback)


    def drawCell(self, canvas, cell, cellSize):
        if cell.isHidden and not cell.isMarked:
            return canvas.create_rectangle(cellSize*cell.x,cellSize*cell.y,cellSize*(cell.x+1), cellSize*(cell.y+1), outline='darkgray', fill='gray', width=2)
        elif cell.isMarked:
            return canvas.create_rectangle(cellSize*cell.x,cellSize*cell.y,cellSize*(cell.x+1), cellSize*(cell.y+1), outline='darkgray', fill='red', width=2)
        elif cell.isBomb:
            return canvas.create_rectangle(cellSize*cell.x,cellSize*cell.y,cellSize*(cell.x+1), cellSize*(cell.y+1), outline='darkgray', fill='black', width=2)
        else:
            # draw rect
            rect = canvas.create_rectangle(cellSize*cell.x,cellSize*cell.y,cellSize*(cell.x+1), cellSize*(cell.y+1), outline='darkgray', fill='lightgray', width=2)
            # draw text
            canvas.create_text(cellSize*cell.x+cellSize/2,cellSize*cell.y+cellSize/2,anchor='center',font="Arial",text=str(cell.bombNeighbors))
            # canvas.create_text(cellSize*cell.x+cellSize/2,cellSize*cell.y+cellSize/2,anchor='center',font="Arial",text=f"({cell.x},{cell.y})")
            return rect

if __name__=="__main__":
    gameLoop = GameLoop()