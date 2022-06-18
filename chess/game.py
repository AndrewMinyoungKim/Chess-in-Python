import pygame

from .constants import *
from .board import Board
from .piece import Piece

class Game:
    def __init__(self, win):
        self.win = win
        self.state = []
        self._init(self.win, self.state)
        #dict(num_P = 8, num_N = 2, num_B = 2, num_R = 2, num_Q = 1)

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

        # selecting a piece when one is not selected yet
        if(not self.selected and self.state[row][col]):
            
            # selecting a piece when it's your turn
            if(self.state[row][col].colour == self.turn):

                # write code for choosing a piece to move
                self.board.draw_selected_piece(row, col, self.win, PURPLE, self.state)
                
                # set new selected x and y
                self.selected = True
                self.selected_x, self.selected_y = row, col

                # get moves for piece
                erase = False
                del(self.available_moves)
                self.available_moves = self.state[row][col].movement(erase, self.board, self.state, self.win)

                # CHECK FOR CHECKS
                # STOP IF NOT ALLOWED

                for i in range(len(self.available_moves)):
                    if(self.state[self.available_moves[i][0]][self.available_moves[i][1]]):
                        self.board.draw_selected_piece(self.available_moves[i][0], self.available_moves[i][1], self.win, ORANGE, self.state)
                    else:
                        self.board.draw_square(self.available_moves[i][0], self.available_moves[i][1], self.win, ORANGE)
            
        # actions when a piece is already selected
        elif(self.selected):

            # moving to an empty space
            if(not self.state[row][col] and (row, col) in self.available_moves):
                #if no check
                self.selected = None
            # capturing another piece
            elif(self.state[row][col] and (row, col) in self.available_moves):
                #if(self.state[row][col].colour != self.turn): #redundant because we only included opponent pieces among all pieces in avail_moves list
                #if no check
                #self.state[row][col], self.state[self.selected_x][self.selected_y] = self.state[self.selected_x][self.selected_y], self.state[row][col]
                self.selected = None
            
            # selecting another piece when one was already selected/clicking on another ally piece
            elif(self.state[row][col]):
                if(self.state[row][col].colour == self.turn):
                    # erase previously coloured in boxes
                    self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREEN if (self.selected_x + self.selected_y) % 2 else GREY, self.state)
                    erase = True
                    self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)

                    # write code for choosing a piece to move
                    self.board.draw_selected_piece(row, col, self.win, PURPLE, self.state)
                    
                    # set new selected x and y
                    self.selected_x, self.selected_y = row, col

                    # get moves for piece
                    erase = False
                    del(self.available_moves)
                    self.available_moves = self.state[row][col].movement(erase, self.board, self.state, self.win)

                    # CHECK FOR CHECKS
                    # STOP IF NOT ALLOWED

                    for i in range(len(self.available_moves)):
                        if(self.state[self.available_moves[i][0]][self.available_moves[i][1]]):
                            self.board.draw_selected_piece(self.available_moves[i][0], self.available_moves[i][1], self.win, ORANGE, self.state)
                        else:
                            self.board.draw_square(self.available_moves[i][0], self.available_moves[i][1], self.win, ORANGE)

                else:
                    # erase previously coloured in boxes
                    self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREEN if (self.selected_x + self.selected_y) % 2 else GREY, self.state)
                    erase = True
                    self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)
                    self.selected = None

            else:
                # erase previously coloured in boxes
                self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREEN if (self.selected_x + self.selected_y) % 2 else GREY, self.state)
                erase = True
                self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)
                self.selected = None
            
            #need to check for if check occurs due to move