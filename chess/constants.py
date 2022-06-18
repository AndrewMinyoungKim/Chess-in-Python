import pygame

WIDTH, HEIGHT = 800, 800
ROW, COL = 8, 8
SQUARE = HEIGHT//COL
#SQUARE = pygame.display.get_window_size() // ROW # not initialized

WHITE = 0xFFFFFF
BLACK = 0x000

GREY = (240, 233, 216)
GREEN = (110, 235, 125)

ORANGE = 0xe39f46
PURPLE = 0x6134eb


BACK_RANK_SETUP = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
#PIECE_TYPE = {'R', 'N', 'B', 'Q', 'K'}
PIECE_TYPE = set(BACK_RANK_SETUP)
PIECE_TYPE.add('P')
#PIECE_TYPE.update('PO')