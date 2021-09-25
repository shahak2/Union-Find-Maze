import pygame as pg
import random
import sys

n = 30
width = 800
height = 600
side = (height-100)/n

#Union-find data structre using path compression and successive linking.
class MakeSet:
    def __init__(self, key):
        self.key = key
        self.p = self
        self.rank = 0
        
    def union(self, y):
        if self.find() != y.find():
            self.find().link(y.find())
        
    def link(self,y):
        if self.rank > y.rank:
            y.p = self
        else:
            self.p = y
            if self.rank == y.rank:
                y.rank += 1    
    
    def find(self):
        if self.p != self:
            self.p = self.p.find()
        return self.p
    
    def __repr__(self):
        return "key:" + str(self.key)

class Maze:
    def __init__(self):
    #Init a maze as a matrix of n x n size, where each cell is a set representing a cell in the maze
    # and walls indicate up, right, down, left = True if they exist.
        self.board = []
        for i in range(n):
            boardRow = []
            for j in range(n):
                boardRow.append([MakeSet(i*n+j),True,True,True,True])
            self.board.append(boardRow)

    def animate_build_maze(self, pg, background, screen):
        # Randomly removes edges until starting point and end point meet.
        self.board[0][0][1] = False
        self.board[n-1][n-1][3] = False
        while self.board[0][0][0].find() != self.board[n-1][n-1][0].find():
            if game_events_handler(pg):
                sys.exit(0)
            background = reset_screen(background)
            row1 = random.randint(0,n-1)
            col1 = random.randint(0,n-1)
            row2, col2, pos = Maze.rand_neighbor(self, row1, col1)
            if self.board[row1][col1][0].find() != self.board[row2][col2][0].find():
                self.board[row1][col1][0].union(self.board[row2][col2][0])
                self.board[row1][col1][pos] = False
                if pos == 1:
                    pos2 = 3
                elif pos == 3:
                    pos2 = 1
                elif pos == 4:
                    pos2 = 2
                else:
                    pos2 = 4
                self.board[row2][col2][pos2] = False
            
            self.blit_maze(background)
            screen.blit(background, (0, 0))
            pg.display.flip()

    def rand_neighbor(self, row, col):
    # Returns a valod random neighbor of cell (row, col) in the matrix
    # or none if none exist.
        arr = [(row-1,col), (row,col+1), (row+1,col), (row,col-1)]
        while True:
            i = random.randint(0,len(arr)-1)
            if arr[i] is not None:
                row2,col2 = arr[i]
                if Maze.in_range(row2,col2):
                    return row2,col2, (i+1)
                else:
                    arr[i] = None
        
    def in_range(row, col):
        if row >= n or col >= n or row < 0 or col < 0:
            return False
        return True 

    def blit_maze(self, background):
        current_pos = (100,50)
        for row in self.board:
            current_pos = (150, current_pos[1])
            for col in row:
                if col[1]:
                    pg.draw.line(background, (0,0,0), current_pos,(current_pos[0] + side,current_pos[1]), 1)
                if col[2]:
                    pg.draw.line(background, (0,0,0), (current_pos[0] + side, current_pos[1]),(current_pos[0] + side,current_pos[1] + side), 1)
                if col[3]:
                    pg.draw.line(background, (0,0,0), (current_pos[0],current_pos[1] + side), (current_pos[0] + side,current_pos[1] + side), 1)
                if col[4]:
                    pg.draw.line(background, (0,0,0), current_pos, (current_pos[0],current_pos[1] + side), 1)              
                current_pos = (current_pos[0] + side, current_pos[1])
            current_pos = (current_pos[0] ,current_pos[1] + side)
        return background

def reset_screen(background):
    # Fill background
    background = background.convert()
    background.fill((240, 240, 240))
    # Display text
    font = pg.font.Font(None, 36)
    text = font.render("A-MAZE-ING", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, (textpos[0], textpos[1] + 10))
    return background

def game_events_handler(pg):
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return True
    else:
        return False


def main():
    m = Maze()
    pg.init()
    pg.display.set_caption('Union-Find Maze')
    screen = pg.display.set_mode((width, height))
    background = pg.Surface(screen.get_size())
    background = reset_screen(background)
    m.animate_build_maze(pg, background, screen)

    # Event loop
    while True:
        if game_events_handler(pg):
            sys.exit(1)


if __name__ == '__main__':
    main()
