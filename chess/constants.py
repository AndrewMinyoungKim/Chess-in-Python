# dimensions and such
WIDTH, HEIGHT = 800, 800
ROW, COL = 8, 8
SQUARE = HEIGHT//COL
#SQUARE = pygame.display.get_window_size() // ROW # not initialized

# the players
WHITE = 0xFFFFFF
BLACK = 0x000

# board square/tile colours
GREY, GREEN = (240, 233, 216), (110, 235, 125)
TILE_A, TILE_B = GREY, GREEN

# other colours used
ORANGE = 0xf5a031 # used for normal move display
RED = 0xed0c1b # used for check display
GOLD = 0xFFD700 # Winning Checkmate Colour!
BROWN = 0xDAA06D # Losing Checkmate Colour :(
PURPLE = 0x6134eb # highlight selected piece
NAVY = (15, 28, 48) # padding/borders
MOVES, CHECK, MATE, LOSE, PIECE_SELECTED, PADDING = ORANGE, RED, GOLD, BROWN, PURPLE, NAVY

# back rank setup order at start of match
BACK_RANK_SETUP = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
# set of the back rank pieces, and add pawns, thus a set containing every piece type
PIECE_TYPE = set(BACK_RANK_SETUP)
PIECE_TYPE.add('P')
#PIECE_TYPE.update('PO')

# dictionary for file names
FILE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

# ---

# CUSTOMIZABLE BOARD COLOURS!
# choose any colour codes and set them to the variables below however you'd like. Have fun with it :)
# comment out the very last line below to begin!

# customize board colours here:
TILE_A = (240, 233, 216)
TILE_B = 0x425fe3
MOVES = 0xf2cf66
CHECK = 0xa60515
MATE = 0xe0d31b
LOSE = 0xa3926f
PIECE_SELECTED = 0x193852
PADDING = 0x2e1f4f

TILE_A, TILE_B, MOVES, CHECK, MATE, LOSE, PIECE_SELECTED, PADDING = GREY, GREEN, ORANGE, RED, GOLD, BROWN, PURPLE, NAVY