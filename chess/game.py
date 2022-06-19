import pygame
import gc

from .constants import *
from .board import Board
from .piece import Piece

class Game:
    def __init__(self, win):
        self.win = win
        self.state = []
        self._init(self.win, self.state)
        #stalemate if all pieces are gone except the two kings
        #all_pieces = dict(w_num_P = 8, w_num_N = 2, w_num_B = 2, w_num_R = 2, w_num_Q = 1, b_num_P = 8, b_num_N = 2, b_num_B = 2, b_num_R = 2, b_num_Q = 1)

    def _init(self, win, state):
        self.turn = WHITE
        self.board = Board()
        self.board.new_board(win, state)

        self.checkmate = None
        self.check = False
        self.black_castle = True
        self.white_castle = True
        self.en_passant = False
        self.promotion = False

        self.selected = False
        self.selected_x, self.selected_y = None, None

        self.available_moves = []

    def update(self):
        pygame.display.update()

    def mouseclick(self, row, col):
        successful_turn = False
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
                #erase previously coloured boxes
                self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
                erase = True
                self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)
                self.selected = None

                #make the switch
                self.state[self.selected_x][self.selected_y], self.state[row][col] = self.state[row][col], self.state[self.selected_x][self.selected_y]
                self.state[row][col].row = row
                self.state[row][col].col = col
                self.state[row][col].calc_pos()
                self.board.draw_square(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN)
                self.board.draw_selected_piece(row, col, self.win, GREY if (row + col) % 2 == 0 else GREEN, self.state)

                #reset
                self.selected = None
                self.selected_x, self.selected_y = None, None
                self.available_moves = []
                successful_turn = True

            # capturing another piece
            elif(self.state[row][col] and (row, col) in self.available_moves):
                #erase previously coloured boxes
                self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
                erase = True
                self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)
                self.selected = None

                #make the switch, delete the opponent piece in square
                taken_piece = self.state[row][col]
                self.state[row][col] = 0
                del(taken_piece)
                gc.collect()
                self.state[self.selected_x][self.selected_y], self.state[row][col] = self.state[row][col], self.state[self.selected_x][self.selected_y]
                self.state[row][col].row = row
                self.state[row][col].col = col
                self.state[row][col].calc_pos()
                self.board.draw_square(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN)
                self.board.draw_selected_piece(row, col, self.win, GREY if (row + col) % 2 == 0 else GREEN, self.state)

                #reset
                self.selected = None
                self.selected_x, self.selected_y = None, None
                self.available_moves = []
                successful_turn = True
                successful_turn = True
            
            # selecting another piece when one was already selected/clicking on another ally piece
            elif(self.state[row][col]):
                if(self.state[row][col].colour == self.turn):
                    # erase previously coloured in boxes
                    self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
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
                    self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
                    erase = True
                    self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)
                    self.selected = None

            else:
                # erase previously coloured in boxes
                self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
                erase = True
                self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)
                self.selected = None

            
            if(successful_turn):
                if(self.turn == WHITE):
                    self.turn = BLACK
                    self.display_move(row, col)
                    print("Black's Turn")
                else:
                    self.turn = WHITE
                    self.display_move(row, col)
                    print("White's Turn")
    
    #display move that was made
    def display_move(self, row, col):
        # IMPORTANT NOTE: When reading, the file letter comes first and THEN the rank number (e.g. d4), so it reads as Column THEN Row
        if(self.state[row][col].name == 'P'):
            print("{}{}".format(FILE[col], row+1))
        else:
            print("{}{}{}".format(self.state[row][col].name, FILE[col], row+1))

            #need to implement rest of notation for checks, checkmates, captures, castles, etc.
            
            #need to check for if check occurs due to move