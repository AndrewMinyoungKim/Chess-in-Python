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
        self.winner = None

        self.selected = False

    def update(self):
        pygame.display.update()

    def mouseclick(self, row, col):
        if(not self.selected and self.state[row][col]):
            pass
            #write code for choosing a piece to move
        elif(self.selected):
            if(not self.state[row][col]):
                pass
                #empty space
            elif(self.state[row][col].colour != self.turn):
                pass
                #capturing another piece
            
            #need to check for if check occurs due to move