import numpy as np

class Game:
    def __init__(self, xDim, yDim, bombCount, revealedCount) -> None:
        self.xDim = xDim
        self.yDim = yDim
        self.grid = [[Cell(x,y,self) for x in range(0,xDim)] for y in range(0,yDim)]
        self.bombs = []
        self.revealed = []
        # Select random cell, mark as revealed
        for i in range(revealedCount):
            row = np.random.randint(0,xDim)
            col = np.random.randint(0,yDim)
            cell = self.getCell(row,col)
            while self.revealed.__contains__(cell):
                row = np.random.randint(0,xDim)
                col = np.random.randint(0,yDim)
                cell = self.getCell(row,col)
            cell.reveal()
            self.revealed.append(cell)
        # Select random cell, mark as a bomb
        for i in range(bombCount):
            row = np.random.randint(0,xDim)
            col = np.random.randint(0,yDim)
            cell = self.getCell(row,col)
            while self.bombs.__contains__(cell) or self.revealed.__contains__(cell):
                row = np.random.randint(0,xDim)
                col = np.random.randint(0,yDim)
                cell = self.getCell(row,col)
            cell.isBomb = True
            self.bombs.append(cell)

    def getCell(self,x,y):
        if x > self.xDim - 1 or x < 0 or y > self.yDim - 1 or y < 0:
            return None
        else:
            return self.grid[y][x]
        
    def getBombNeighbors(self,cell):
        count = 0
        neighbors = [
            self.getCell(cell.x-1,cell.y), 
            self.getCell(cell.x,cell.y-1), 
            self.getCell(cell.x,cell.y+1),
            self.getCell(cell.x+1,cell.y),
            ]
        for neighbor in neighbors:
            if neighbor is not None:
                if neighbor.isBomb:
                    count += 1
        return count
    


class Cell:
    def __init__(self, x, y, game) -> None:
        self.isHidden = True
        self.x = x
        self.y = y
        self.isBomb = False
        self.isMarked = False
        self.bombNeighbors= -1
        self.game = game

    def reveal(self, event=None):
        self.isHidden = False
        self.isMarked = False

    def toggleMark(self, event=None):
        self.isMarked = not self.isMarked

    def revealZeroNeighbors(self, event=None):
        cells = [self]
        while len(cells) > 0:
            cell = cells[0]
            cell.reveal()
            neighbors = [
            self.game.getCell(cell.x-1,cell.y), 
            self.game.getCell(cell.x,cell.y-1), 
            self.game.getCell(cell.x,cell.y+1),
            self.game.getCell(cell.x+1,cell.y),
            ]
            if cell.bombNeighbors == 0:
                for neighbor in neighbors:
                    if neighbor is not None:
                        if neighbor.isHidden:
                            cells.append(neighbor)
            cells.pop(0)

    def __repr__(self):
        return f"Cell({self.x},{self.y})\n marked: {self.isMarked}, hidden: {self.isHidden}\n bombNeighbors: {self.bombNeighbors}"
    
