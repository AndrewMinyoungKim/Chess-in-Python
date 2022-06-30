import pygame

from .constants import *
from .piece import Piece

class Board:
    def __init__(self):
        pass

    def draw_square(self, row, col, win, colour):
        pygame.draw.rect(win, colour, (col*SQUARE, row*SQUARE, SQUARE, SQUARE))
        pygame.draw.rect(win, PADDING, (col*SQUARE, row*SQUARE, SQUARE, SQUARE), 1) # borders

    def draw_new_board(self, win, state):
        win.fill(TILE_B)
        for row in range(ROW):
            for col in range(COL):
                if(not (row + col) % 2):
                    pygame.draw.rect(win, TILE_A, (row*SQUARE, col*SQUARE, SQUARE, SQUARE))
                pygame.draw.rect(win, PADDING, (row*SQUARE, col*SQUARE, SQUARE, SQUARE), 1) # borders

    def new_board(self, win, state):
        self.draw_new_board(win, state)
        for row in range(ROW):
            state.append([])
            for col in range(COL):
                if(row == 0):
                    state[row].append(Piece(BACK_RANK_SETUP[col], row, col, WHITE, win))
                elif(row == 7):
                    state[row].append(Piece(BACK_RANK_SETUP[col], row, col, BLACK, win))
                elif(row == 1):
                    state[row].append(Piece('P', row, col, WHITE, win))
                elif(row == 6):
                    state[row].append(Piece('P', row, col, BLACK, win))
                else:
                    state[row].append(0)

    def draw_selected_piece(self, row, col, win, colour, state):
        self.draw_square(row, col, win, colour)
        state[row][col].draw_piece(win)