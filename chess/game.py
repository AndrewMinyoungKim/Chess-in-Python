import pygame

from .constants import *
from .board import Board
from .piece import Piece

class Game:
    def __init__(self, win):
        self.win = win
        self.state = []
        self._init(self.win, self.state)
        dict(num_P = 8, num_N = 2, num_B = 2, num_R = 2, num_Q = 1)

    def _init(self, win, state):
        self.turn = WHITE
        self.board = Board()
        self.board.new_board(win, state)

        self.checkmate = None
        self.check = False
        self.black_castle = True
        self.white_castle = True

        self.selected = False
        #self.selected_x, self.selected_y = None #row and col of selected piece

    def update(self):
        pygame.display.update()

    def mouseclick(self, row, col):
        if(not self.selected and self.state[row][col]):
            pass
            #write code for choosing a piece to move
            if(self.state[row][col].colour == self.turn):
                self.board.draw_square(row, col, self.win, PURPLE)
                self.state[row][col].draw_piece(self.win)
        elif(self.selected):
            if(not self.state[row][col]):
                pass
                #empty space
                #if no check
            elif(self.state[row][col].colour != self.turn):
                pass
                #capturing another piece
                #if no check
                #self.state[row][col], self.state[self.selected_x][self.selected_y] = self.state[self.selected_x][self.selected_y], self.state[row][col]
            
            #need to check for if check occurs due to move