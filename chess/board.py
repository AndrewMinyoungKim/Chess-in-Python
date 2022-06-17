import pygame

from .constants import *
from .piece import Piece

class Board:
    def __init__(self):
        pass

    def draw_new_board(self, win, state):
        win.fill(GREEN)
        for row in range(ROW):
            for col in range(row % 2, ROW, 2):
                pygame.draw.rect(win, GREY, (row*SQUARE, col*SQUARE, SQUARE, SQUARE))

    def new_board(self, win, state):
        self.draw_new_board(win, state)
        for row in range(ROW):
            state.append([])
            for col in range(COL):
                if(row == 0):
                    state[row].append(Piece(BACK_RANK_SETUP[col], row, col, BLACK, win))
                elif(row == 7):
                    state[row].append(Piece(BACK_RANK_SETUP[col], row, col, WHITE, win))
                elif(row == 1):
                    state[row].append(Piece('P', row, col, BLACK, win))
                elif(row == 6):
                    state[row].append(Piece('P', row, col, WHITE, win))
                else:
                    state[row].append(0)