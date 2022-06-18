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
        self.turn = BLACK
        self.board = Board()
        self.board.new_board(win, state)

        self.checkmate = None
        self.check = False
        self.black_castle = True
        self.white_castle = True
        self.en_passant = False
        self.promotion = False

        self.selected = False
        self.selected_x = 0
        self.selected_y = 0

        self.available_moves = []

    def update(self):
        pygame.display.update()

    def mouseclick(self, row, col):
        erase = False

        # selecting a piece when it's your turn
        if(not self.selected and self.state[row][col]):
            
            # write code for choosing a piece to move
            if(self.state[row][col].colour == self.turn):
                self.board.draw_selected_piece(row, col, self.win, PURPLE, self.state)
                
                self.selected = True
                self.selected_x, self.selected_y = row, col

                erase = False
                self.state[row][col].movement(erase, self.board, self.state, self.win)

        # actions when a piece is already selected
        elif(self.selected):
            # moving to an empty space
            if(not self.state[row][col]):
                pass
                
                #if no check
                self.selected = None

            # capturing another piece
            elif(self.state[row][col].colour != self.turn):
                pass
                
                #if no check
                #self.state[row][col], self.state[self.selected_x][self.selected_y] = self.state[self.selected_x][self.selected_y], self.state[row][col]
                
                self.selected = None

            # selecting another piece when one was already selected 
            elif(self.state[row][col].colour == self.turn):
                # erase previously coloured in boxes
                self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREEN if (self.selected_x + self.selected_y) % 2 else GREY, self.state)
                erase = True
                self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)

                # write code for choosing a piece to move
                self.board.draw_selected_piece(row, col, self.win, PURPLE, self.state)
                
                self.selected_x, self.selected_y = row, col

                erase = False
                self.state[row][col].movement(erase, self.board, self.state, self.win)

            
            #need to check for if check occurs due to move