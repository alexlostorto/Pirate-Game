#  ____  _           _          ____
# |  _ \(_)_ __ __ _| |_ ___   / ___| __ _ _ __ ___   ___
# | |_) | | '__/ _` | __/ _ \ | |  _ / _` | '_ ` _ \ / _ \
# |  __/| | | | (_| | ||  __/ | |_| | (_| | | | | | |  __/
# |_|   |_|_|  \__,_|\__\___|  \____|\__,_|_| |_| |_|\___|

# CREDITS
# Author: Alex lo Storto
# Github: https://github.com/alexlostorto
# Website: https://alexlostorto.github.io/

# All code is mine and subject to the MIT License


import re
import sys
import random

import pygame.mouse
from pygame.locals import *
from Classes import *

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pirate Game')

# COLOURS
GOLD = '#FFD700'
BLACK = '#000000'
LIGHT_BROWN = '#E5AA70'
DARK_BROWN = '#B87333'
WHITE = '#FFFFFF'
GREEN = '#00FF00'
RED = '#FF0000'
GHOST_WHITE = '#C0C0C0'

# PYGAME VARIABLES
FPS = 60
MENU_STATE = 'title_screen'
CURSOR = pygame.mouse.get_pos()

# POSITION VARIABLES
SX = 100  # Top left X
SY = 150  # Top left Y
GRID_WIDTH = 490
GRID_HEIGHT = 490
SQUARE_SIZE = 70
STATS_WIDTH = WIDTH - GRID_WIDTH - SX

# GAME VARIABLES
GRID = []
ROW_COUNT = 7
COLUMN_COUNT = 7
PIECES = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
          200, 200, 200, 200, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 3000, 3000, 5000,
          'GRINCH', 'PUDDING', 'PRESENT', 'SNOWBALL', 'MISTLETOE', 'TREE', 'ELF', 'BAUBLE', 'TURKEY', 'CRACKER',
          'BANK']
POINTS = 0
BANK = 0
ELF_COLOUR = RED
ELF_ALPHA = 255
BAUBLE_COLOUR = RED
BAUBLE_ALPHA = 255
STEAL_COLOUR = WHITE
STEAL_HOVER = GHOST_WHITE
CHOOSE_COLOUR = WHITE
CHOOSE_HOVER = GHOST_WHITE
SWAP_COLOUR = WHITE
SWAP_HOVER = GHOST_WHITE
CHOSEN = []
COMBINATION = ''
COORDINATE = []
COMBINATIONS = []
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
LETTERS_DICT = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7
}
STATS_GROUP = []
GRID_ITEMS = []

# INPUT VARIABLES
INPUT_TEXT = ''
INPUT_FOCUS = False
INPUT_ACTIVE = False
INPUT_QUESTION = ''
INPUT_FONT = None
INPUT_POS = None
INPUT_ALIGN = ''
INPUT_BASE_COLOUR = None
INPUT_FOCUS_COLOUR = None
INPUT_FONT_COLOUR = None
INPUT_PURPOSE = None
INPUT_COUNTER = 0

# MESSAGE VARIABLES
MESSAGE_TEXT = ''
MESSAGE_ACTIVE = False
MESSAGE_FONT = None
MESSAGE_POS = None
MESSAGE_ALIGN = ''
MESSAGE_COLOUR = None
MESSAGE_BASE_COLOUR = None
MESSAGE_HOVER_COLOUR = None
MESSAGE_FONT_COLOUR = None
MESSAGE_RECT = None

# IMAGES
BG = pygame.image.load("assets/Background.png").convert_alpha()
exit_img = pygame.image.load("assets/Red_X.png").convert_alpha()
bauble_img = pygame.image.load("assets/Bauble.png").convert_alpha()
cracker_img = pygame.image.load("assets/Christmas Cracker.png").convert_alpha()
hat_img = pygame.image.load("assets/Christmas Hat.png").convert_alpha()
tree_img = pygame.image.load("assets/Christmas Tree.png").convert_alpha()
elf_img = pygame.image.load("assets/Elf.png").convert_alpha()
grinch_img = pygame.image.load("assets/Grinch.png").convert_alpha()
mistletoe_img = pygame.image.load("assets/Mistletoe.png").convert_alpha()
present_img = pygame.image.load("assets/Present.png").convert_alpha()
pudding_img = pygame.image.load("assets/Pudding.png").convert_alpha()
snowball_img = pygame.image.load("assets/Snowball.png").convert_alpha()
turkey_img = pygame.image.load("assets/Turkey.png").convert_alpha()
bank_img = pygame.image.load("assets/Bank.png").convert_alpha()


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass


def display_message(message, font, base_colour, hover_colour, font_colour, pos, align='centre'):
    global MESSAGE_ACTIVE
    global MESSAGE_TEXT
    global MESSAGE_FONT
    global MESSAGE_POS
    global MESSAGE_ALIGN
    global MESSAGE_BASE_COLOUR
    global MESSAGE_HOVER_COLOUR
    global MESSAGE_FONT_COLOUR
    global MESSAGE_COLOUR
    global MESSAGE_RECT

    MESSAGE_ACTIVE = True
    MESSAGE_TEXT = message
    MESSAGE_FONT = font
    MESSAGE_ALIGN = align
    MESSAGE_BASE_COLOUR = base_colour
    MESSAGE_HOVER_COLOUR = hover_colour
    MESSAGE_FONT_COLOUR = font_colour

    if MESSAGE_COLOUR is None:
        MESSAGE_COLOUR = MESSAGE_BASE_COLOUR

    text_surface = font.render(message, True, font_colour)
    width = max(100, text_surface.get_width() + 20)
    height = 50
    x, y = format_position(pos, width, height, MESSAGE_ALIGN)
    MESSAGE_POS = (x, y)

    # Creates the message box
    MESSAGE_RECT = pygame.Rect(x, y, width, height)

    # Creates a border around the message
    border_rect = pygame.Rect(x, y, width, height)
    border_width = 2

    pygame.draw.rect(SCREEN, MESSAGE_COLOUR, MESSAGE_RECT)
    pygame.draw.rect(SCREEN, font_colour, border_rect, border_width)
    SCREEN.blit(text_surface, (MESSAGE_RECT.x + 10, MESSAGE_RECT.y + 10))

    return False


def get_input(question, font, base_colour, focus_colour, font_colour, pos, align='centre'):
    global INPUT_TEXT
    global INPUT_FOCUS
    global INPUT_ACTIVE
    global INPUT_QUESTION
    global INPUT_FONT
    global INPUT_POS
    global INPUT_ALIGN
    global INPUT_BASE_COLOUR
    global INPUT_FOCUS_COLOUR
    global INPUT_FONT_COLOUR
    global INPUT_PURPOSE
    global MESSAGE_ACTIVE

    INPUT_ACTIVE = True
    MESSAGE_ACTIVE = False
    INPUT_QUESTION = question
    INPUT_FONT = font
    INPUT_POS = pos
    INPUT_ALIGN = align
    INPUT_BASE_COLOUR = base_colour
    INPUT_FOCUS_COLOUR = focus_colour
    INPUT_FONT_COLOUR = font_colour

    message = f"{question}: {INPUT_TEXT}"
    text_surface = font.render(message, True, font_colour)
    width = max(100, text_surface.get_width() + 20)
    height = 50
    x, y = format_position(pos, width, height, INPUT_ALIGN)

    # Creates the input box
    input_rect = pygame.Rect(x, y, width, height)

    # Creates a border around the input
    border_rect = pygame.Rect(x, y, width, height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                INPUT_FOCUS = True
            else:
                INPUT_FOCUS = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                INPUT_TEXT = INPUT_TEXT[:-1]
            elif event.key == pygame.K_RETURN:
                INPUT_ACTIVE = False
                return True
            elif event.key == pygame.K_ESCAPE:
                INPUT_ACTIVE = False
                return False
            else:
                INPUT_TEXT += event.unicode

    if INPUT_FOCUS:
        colour = focus_colour
        border_width = 3
    else:
        colour = base_colour
        border_width = 2

    pygame.draw.rect(SCREEN, colour, input_rect)
    pygame.draw.rect(SCREEN, font_colour, border_rect, border_width)
    SCREEN.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

    return False


def get_font(size):  # Returns font in desired size
    return pygame.font.Font("assets/cute_font.ttf", size)


def main_menu():
    global MENU_STATE
    global COMBINATIONS

    def create_grid():
        global GRID

        # Creates the grid by choosing a random item for each square in the grid
        GRID = [['' for x in range(ROW_COUNT)] for x in range(COLUMN_COUNT)]
        pieces = list(PIECES)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Removes item after it has been chosen
                choice = random.randint(0, len(pieces) - 1)
                GRID[r][c] = pieces[choice]
                pieces.pop(choice)

    SCREEN.blit(BG, (0, 0))

    # Draw title
    TITLE = textRect(text='PIRATE GAME', font=get_font(100), base_colour=GOLD, hover_colour=GOLD, pos=(640, 100))
    TITLE.draw(SCREEN)

    # Play button
    PLAY_BUTTON = rect(width=370, height=109, base_colour=GHOST_WHITE, hover_colour=GHOST_WHITE, alpha=70,
                       pos=(640, 250), align='centre')
    PLAY_TEXT = textRect(text='PLAY', font=get_font(75), base_colour=LIGHT_BROWN, hover_colour=DARK_BROWN,
                         pos=(640, 250))
    PLAY_BUTTON.draw(SCREEN)
    PLAY_TEXT.draw(SCREEN)

    # Options button
    OPTIONS_BUTTON = rect(width=585, height=109, base_colour=GHOST_WHITE, hover_colour=GHOST_WHITE, alpha=70,
                          pos=(640, 400), align='centre')
    OPTIONS_TEXT = textRect(text='OPTIONS', font=get_font(75), base_colour=LIGHT_BROWN, hover_colour=DARK_BROWN,
                            pos=(640, 400))
    OPTIONS_BUTTON.draw(SCREEN)
    OPTIONS_TEXT.draw(SCREEN)

    # Quit button
    QUIT_BUTTON = rect(width=354, height=109, base_colour=GHOST_WHITE, hover_colour=GHOST_WHITE, alpha=70,
                       pos=(640, 550), align='centre')
    QUIT_TEXT = textRect(text='QUIT', font=get_font(75), base_colour=LIGHT_BROWN, hover_colour=DARK_BROWN,
                         pos=(640, 550))
    QUIT_BUTTON.draw(SCREEN)
    QUIT_TEXT.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_TEXT.checkForInput():
                MENU_STATE = 'play'
                COMBINATIONS = ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '2A', '2B', '2C', '2D', '2E', '2F', '2G',
                                '3A', '3B', '3C', '3D', '3E', '3F', '3G', '4A', '4B', '4C', '4D', '4E', '4F', '4G',
                                '5A', '5B', '5C', '5D', '5E', '5F', '5G', '6A', '6B', '6C', '6D', '6E', '6F', '6G',
                                '7A', '7B', '7C', '7D', '7E', '7F', '7G']
                create_grid()
            if OPTIONS_TEXT.checkForInput():
                MENU_STATE = 'options'
            if QUIT_TEXT.checkForInput():
                pygame.quit()
                sys.exit()


def play():
    global MENU_STATE
    global INPUT_ACTIVE
    global POINTS
    global COORDINATE
    global INPUT_TEXT
    global STEAL_COLOUR
    global STEAL_HOVER
    global SWAP_COLOUR
    global CHOOSE_COLOUR
    global CHOOSE_HOVER
    global MESSAGE_ACTIVE
    global MESSAGE_COLOUR
    global CHOSEN
    global ELF_COLOUR
    global ELF_ALPHA
    global BAUBLE_COLOUR
    global BAUBLE_ALPHA

    def draw_grid():
        for c in range(COLUMN_COUNT + 1):
            pygame.draw.line(SCREEN, WHITE, (SX, SY + c * SQUARE_SIZE), (SX + GRID_WIDTH, SY + c * SQUARE_SIZE))
            for r in range(ROW_COUNT + 1):
                pygame.draw.line(SCREEN, WHITE, (SX + r * SQUARE_SIZE, SY), (SX + r * SQUARE_SIZE, SY + GRID_HEIGHT))

        for c in range(COLUMN_COUNT):
            X_AXIS_TEXT = get_font(45).render(LETTERS[c], True, WHITE)
            X_AXIS_RECT = X_AXIS_TEXT.get_rect(center=(SX + (SQUARE_SIZE // 2) + SQUARE_SIZE * c, SY - 25))
            SCREEN.blit(X_AXIS_TEXT, X_AXIS_RECT)

        for r in range(ROW_COUNT):
            Y_AXIS_TEXT = get_font(45).render(str(r + 1), True, WHITE)
            Y_AXIS_RECT = Y_AXIS_TEXT.get_rect(center=(SX - 25, SY + (SQUARE_SIZE // 2) + SQUARE_SIZE * r))
            SCREEN.blit(Y_AXIS_TEXT, Y_AXIS_RECT)

    def generate_coord():
        global COMBINATION
        global COORDINATE
        global CHOOSE_COLOUR
        global CHOOSE_HOVER
        global STEAL_COLOUR
        global STEAL_HOVER
        global SWAP_COLOUR
        global SWAP_HOVER
        global MESSAGE_ACTIVE

        MESSAGE_ACTIVE = False
        STEAL_COLOUR = WHITE
        STEAL_HOVER = GHOST_WHITE
        CHOOSE_COLOUR = WHITE
        CHOOSE_HOVER = GHOST_WHITE
        SWAP_COLOUR = WHITE
        SWAP_HOVER = GHOST_WHITE

        # Generate random combination e.g. '1G'
        if len(COMBINATIONS) < 1:
            print("Game Over")
            return False
        # Removes combination after it has been chosen
        CHOICE = random.randint(0, len(COMBINATIONS) - 1)
        COMBINATION = COMBINATIONS[CHOICE]
        COMBINATIONS.pop(CHOICE)
        CHOSEN.append(COMBINATION)

        # Format combination as a coordinate e.g. ['1', 'G']
        COORDINATE = list(COMBINATION)
        COORDINATE[0] = int(COORDINATE[0])
        COORDINATE[1] = LETTERS_DICT[COORDINATE[1]]
        print(f"Combination: {COMBINATION}  Coordinate: {COORDINATE}")
        print(CHOSEN)

        update_grid()
        update_points()

    def update_grid():
        global GRID_ITEMS

        ROW = COORDINATE[0] - 1
        COLUMN = COORDINATE[1] - 1
        POSITION = (SX + (SQUARE_SIZE // 2) + SQUARE_SIZE * COLUMN, SY + (SQUARE_SIZE // 2) + SQUARE_SIZE * ROW)

        CROSS = imageGridItem(image=exit_img, width=60, height=65, pos=POSITION)
        GRID_ITEMS.append(CROSS)

    def update_points():
        global POINTS
        global BANK
        global ELF_COLOUR
        global BAUBLE_COLOUR
        global STEAL_COLOUR
        global CHOOSE_COLOUR
        global SWAP_COLOUR
        global MESSAGE_COLOUR

        ROW = COORDINATE[0] - 1
        COLUMN = COORDINATE[1] - 1
        ITEM = GRID[ROW][COLUMN]

        if ITEM == 200:
            POINTS += 200
        elif ITEM == 1000:
            POINTS += 1000
        elif ITEM == 3000:
            POINTS += 3000
        elif ITEM == 5000:
            POINTS += 5000
        elif ITEM == 'CRACKER':
            POINTS *= 2
        elif ITEM == 'TURKEY':
            POINTS = 0
        elif ITEM == 'BANK':
            BANK = POINTS
            POINTS = 0
        elif ITEM == 'ELF':
            ELF_COLOUR = GREEN
            MESSAGE_COLOUR = None
            display_message(message="You can now BLOCK an attack", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'BAUBLE':
            BAUBLE_COLOUR = GREEN
            MESSAGE_COLOUR = None
            display_message(message="You can now REFLECT an attack", font=get_font(35), pos=(640, 680),
                            base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'GRINCH':
            STEAL_COLOUR = GREEN
            MESSAGE_COLOUR = None
            display_message(message="You can ROB someone", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'TREE':
            CHOOSE_COLOUR = GREEN
            MESSAGE_COLOUR = None
            display_message(message="CHOOSE the next square", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'MISTLETOE':
            SWAP_COLOUR = GREEN
            MESSAGE_COLOUR = None
            display_message(message="SWAP scores with someone", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'SNOWBALL':
            MESSAGE_COLOUR = None
            display_message(message="Wipe out a row's scores", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'PUDDING':
            MESSAGE_COLOUR = None
            display_message(message="KILL someone", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')
        elif ITEM == 'PRESENT':
            MESSAGE_COLOUR = None
            display_message(message="GIFT someone 1000 points", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                            hover_colour=GHOST_WHITE, font_colour=WHITE, align='centre')

    def steal_points():
        global INPUT_TEXT
        global INPUT_PURPOSE

        INPUT_TEXT = ''
        INPUT_PURPOSE = 'steal'
        get_input(question="How many points did you steal?", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                  font_colour=WHITE, focus_colour=BLACK, align='centre')

    def swap_points():
        global INPUT_TEXT
        global INPUT_PURPOSE

        INPUT_TEXT = ''
        INPUT_PURPOSE = 'swap'
        get_input(question="How many points do they have?", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                  font_colour=WHITE, focus_colour=BLACK, align='centre')

    def choose_coord():
        global INPUT_TEXT
        global INPUT_PURPOSE

        INPUT_TEXT = ''
        INPUT_PURPOSE = 'choose'
        get_input(question="Choose a coordinate", font=get_font(35), pos=(640, 680), base_colour=BLACK,
                  font_colour=WHITE, focus_colour=BLACK, align='centre')

    def receive_present():
        global POINTS

        POINTS += 1000

    def load_grid_items():
        global GRID_ITEMS

        if len(GRID_ITEMS) == 0:
            for COL in range(COLUMN_COUNT):
                for ROW in range(ROW_COUNT):
                    POSITION = (
                        SX + (SQUARE_SIZE // 2) + SQUARE_SIZE * COL, SY + (SQUARE_SIZE // 2) + SQUARE_SIZE * ROW)
                    # Places items in the grid
                    if GRID[ROW][COL] == 200:
                        POINTS_200 = textGridItem(text=200, font=get_font(30), colour=WHITE, pos=POSITION)
                        GRID_ITEMS.append(POINTS_200)
                    if GRID[ROW][COL] == 1000:
                        POINTS_1000 = textGridItem(text=1000, font=get_font(30), colour=WHITE, pos=POSITION)
                        GRID_ITEMS.append(POINTS_1000)
                    if GRID[ROW][COL] == 3000:
                        POINTS_3000 = textGridItem(text=3000, font=get_font(30), colour=WHITE, pos=POSITION)
                        GRID_ITEMS.append(POINTS_3000)
                    if GRID[ROW][COL] == 5000:
                        POINTS_5000 = textGridItem(text=5000, font=get_font(30), colour=WHITE, pos=POSITION)
                        GRID_ITEMS.append(POINTS_5000)
                    if GRID[ROW][COL] == 'GRINCH':
                        GRINCH = imageGridItem(image=grinch_img, width=60, height=65, pos=POSITION)
                        GRID_ITEMS.append(GRINCH)
                    if GRID[ROW][COL] == 'PUDDING':
                        PUDDING = imageGridItem(image=pudding_img, width=65, height=65, pos=POSITION)
                        GRID_ITEMS.append(PUDDING)
                    if GRID[ROW][COL] == 'PRESENT':
                        PRESENT = imageGridItem(image=present_img, width=60, height=65, pos=POSITION)
                        GRID_ITEMS.append(PRESENT)
                    if GRID[ROW][COL] == 'SNOWBALL':
                        SNOWBALL = imageGridItem(image=snowball_img, width=65, height=65, pos=POSITION)
                        GRID_ITEMS.append(SNOWBALL)
                    if GRID[ROW][COL] == 'MISTLETOE':
                        MISTLETOE = imageGridItem(image=mistletoe_img, width=65, height=65, pos=POSITION)
                        GRID_ITEMS.append(MISTLETOE)
                    if GRID[ROW][COL] == 'TREE':
                        TREE = imageGridItem(image=tree_img, width=55, height=65, pos=POSITION)
                        GRID_ITEMS.append(TREE)
                    if GRID[ROW][COL] == 'ELF':
                        ELF = imageGridItem(image=elf_img, width=40, height=65, pos=POSITION)
                        GRID_ITEMS.append(ELF)
                    if GRID[ROW][COL] == 'BAUBLE':
                        BAUBLE = imageGridItem(image=bauble_img, width=55, height=65, pos=POSITION)
                        GRID_ITEMS.append(BAUBLE)
                    if GRID[ROW][COL] == 'TURKEY':
                        TURKEY = imageGridItem(image=turkey_img, width=65, height=65, pos=POSITION)
                        GRID_ITEMS.append(TURKEY)
                    if GRID[ROW][COL] == 'CRACKER':
                        CRACKER = imageGridItem(image=cracker_img, width=65, height=65, pos=POSITION)
                        GRID_ITEMS.append(CRACKER)
                    if GRID[ROW][COL] == 'BANK':
                        HAT = imageGridItem(image=hat_img, width=65, height=65, pos=POSITION)
                        GRID_ITEMS.append(HAT)

        for ITEM in GRID_ITEMS:
            ITEM.update(SCREEN)

    def load_stats():
        global STATS_GROUP

        if len(STATS_GROUP) == 0:
            # Pirate Game Header
            HEADER_TEXT = textRect(text='PIRATE GAME', font=get_font(45), base_colour=GOLD, hover_colour=GOLD,
                                   pos=(640, 50))
            # Display points tracker
            POINTS_BG = rect(width=STATS_WIDTH // 2 - 30, height=350, base_colour=WHITE, hover_colour=WHITE, alpha=60,
                             pos=(GRID_WIDTH + SX + 20, SY), align='topleft')
            RESET_BG = rect(width=STATS_WIDTH // 2 - 30, height=70, base_colour=WHITE, hover_colour=WHITE, alpha=60,
                            pos=(GRID_WIDTH + SX + 20, SY + 280), align='topleft')
            # Display elf and bauble
            SHIELDS_BG = rect(width=STATS_WIDTH // 2 - 30, height=175, base_colour=WHITE, hover_colour=WHITE, alpha=60,
                              pos=(GRID_WIDTH + SX + 10 + STATS_WIDTH // 2, SY), align='topleft')
            ELF_TEXT = textRect(text='ELF', font=get_font(35), base_colour=WHITE, hover_colour=WHITE,
                                pos=(GRID_WIDTH + SX + 70 + STATS_WIDTH // 2, SY + 20), align='topleft')
            BAUBLE_TEXT = textRect(text='BAUBLE', font=get_font(35), base_colour=WHITE, hover_colour=WHITE,
                                   pos=(GRID_WIDTH + SX + 185 + STATS_WIDTH // 2, SY + 20), align='topleft')
            # Display bank
            BANK_BG = rect(width=STATS_WIDTH // 2 - 30, height=155, base_colour=WHITE, hover_colour=WHITE, alpha=60,
                           pos=(GRID_WIDTH + SX + 10 + STATS_WIDTH // 2, SY + 195), align='topleft')
            BANK_TEXT_BG = rect(width=STATS_WIDTH // 4 - 45, height=115, base_colour=WHITE, hover_colour=WHITE,
                                alpha=60, pos=(GRID_WIDTH + SX + 180 + STATS_WIDTH // 2, SY + 215), align='topleft')
            BANK_IMAGE = imgButton(image=bank_img, width=127, height=115,
                                   pos=(GRID_WIDTH + SX + 25 + STATS_WIDTH // 2, SY + 215), hover_transparency=255,
                                   align='topleft')
            # Display coordinates
            COORDS_BG = rect(width=STATS_WIDTH - 40, height=120, base_colour=WHITE, hover_colour=WHITE, alpha=60,
                             pos=(GRID_WIDTH + SX + 20, SY + 370), align='topleft')
            COORDS_TEXT_BG = rect(width=100, height=90, base_colour=WHITE, hover_colour=WHITE,
                                  alpha=60, pos=(GRID_WIDTH + SX + STATS_WIDTH // 2, SY + 430), align='centre')
            STATS_GROUP = [HEADER_TEXT, POINTS_BG, RESET_BG, SHIELDS_BG, ELF_TEXT, BAUBLE_TEXT, BANK_BG, BANK_TEXT_BG,
                           BANK_IMAGE, COORDS_BG, COORDS_TEXT_BG]

        for VAR in STATS_GROUP:
            VAR.draw(SCREEN)

    SCREEN.fill(BLACK)

    # Exit button
    EXIT_BUTTON = imgButton(image=exit_img, width=40, height=40, pos=(1230, 50), hover_transparency=128, align='centre')
    EXIT_BUTTON.draw(SCREEN)

    # Display points
    POINTS_TEXT = textRect(text=POINTS, font=get_font(45), base_colour=LIGHT_BROWN, hover_colour=WHITE,
                           pos=((WIDTH - GRID_WIDTH - SX) // 2 + GRID_WIDTH + SX, 100))
    POINTS_TEXT.draw(SCREEN)

    # Elf and Bauble status
    ELF_RECT = rect(width=100, height=100, base_colour=ELF_COLOUR, hover_colour=ELF_COLOUR, alpha=ELF_ALPHA,
                    pos=(GRID_WIDTH + SX + 45 + STATS_WIDTH // 2, SY + 60), align='topleft')
    ELF_RECT.draw(SCREEN)
    if ELF_RECT.checkForInput():
        ELF_ALPHA = 128
    else:
        ELF_ALPHA = 255
    BAUBLE_RECT = rect(width=100, height=100, base_colour=BAUBLE_COLOUR, hover_colour=BAUBLE_COLOUR, alpha=BAUBLE_ALPHA,
                       pos=(GRID_WIDTH + SX + 190 + STATS_WIDTH // 2, SY + 60), align='topleft')
    BAUBLE_RECT.draw(SCREEN)
    if BAUBLE_RECT.checkForInput():
        BAUBLE_ALPHA = 128
    else:
        BAUBLE_ALPHA = 255

    # Display bank points
    BANK_TEXT = textRect(text=BANK, font=get_font(35), base_colour=WHITE, hover_colour=WHITE,
                         pos=(GRID_WIDTH + SX + 243 + STATS_WIDTH // 2, SY + 195 + 155 // 2), align='centre')
    BANK_TEXT.draw(SCREEN)

    # Steal points button
    STEAL_POINTS = textRect(text='STEAL', font=get_font(30), base_colour=STEAL_COLOUR, hover_colour=STEAL_HOVER,
                            pos=(GRID_WIDTH + SX + 100, SY + 315), align='centre')
    STEAL_POINTS.draw(SCREEN)

    # Swap points button
    SWAP_POINTS = textRect(text='SWAP', font=get_font(30), base_colour=SWAP_COLOUR, hover_colour=SWAP_HOVER,
                           pos=(GRID_WIDTH + SX + 250, SY + 315), align='centre')
    SWAP_POINTS.draw(SCREEN)

    # Present button
    PRESENT_BUTTON = textRect(text='RECEIVE PRESENT', font=get_font(35), base_colour=RED, hover_colour=GREEN,
                              pos=(GRID_WIDTH + SX + STATS_WIDTH // 4 + 7, SY + 240), align='centre')
    PRESENT_BUTTON.draw(SCREEN)

    # Generate coordinate button
    COORD_GENERATOR = textRect(text='GENERATE', font=get_font(50), base_colour=WHITE, hover_colour=GHOST_WHITE,
                               pos=(GRID_WIDTH + SX + STATS_WIDTH // 4 - 10, SY + 430), align='centre')
    COORD_GENERATOR.draw(SCREEN)
    COORDS_TEXT = textRect(text=COMBINATION, font=get_font(70), base_colour=WHITE, hover_colour=WHITE,
                           pos=(GRID_WIDTH + SX + STATS_WIDTH // 2, SY + 430), align='centre')
    COORDS_TEXT.draw(SCREEN)

    # Choose coordinate button
    COORD_CHOOSE = textRect(text='CHOOSE', font=get_font(50), base_colour=CHOOSE_COLOUR, hover_colour=CHOOSE_HOVER,
                            pos=(GRID_WIDTH + SX + STATS_WIDTH // 2 + 185, SY + 430), align='centre')
    COORD_CHOOSE.draw(SCREEN)

    # Display grid
    draw_grid()
    load_grid_items()

    # Display stats
    load_stats()

    # Displays any active inputs
    if INPUT_ACTIVE and get_input(INPUT_QUESTION, INPUT_FONT, INPUT_BASE_COLOUR, INPUT_FOCUS_COLOUR, INPUT_FONT_COLOUR,
                                  INPUT_POS, INPUT_ALIGN):
        # Gets inputted text from finished inputs
        if INPUT_PURPOSE == 'swap':
            if INPUT_TEXT.isdigit():
                SWAP_COLOUR = WHITE
                POINTS = int(INPUT_TEXT)
            else:
                INPUT_TEXT = ''
                INPUT_ACTIVE = True
        elif INPUT_PURPOSE == 'steal':
            if INPUT_TEXT.isdigit():
                POINTS += int(INPUT_TEXT)
                STEAL_COLOUR = WHITE
                STEAL_HOVER = GHOST_WHITE
            else:
                INPUT_TEXT = ''
                INPUT_ACTIVE = True
        elif INPUT_PURPOSE == 'choose':
            if re.match('^[1-7][A-G]$', INPUT_TEXT) and INPUT_TEXT not in CHOSEN:
                # Format combination as a coordinate e.g. ['1', 'G']
                COORDINATE = list(INPUT_TEXT)
                COORDINATE[0] = int(COORDINATE[0])
                COORDINATE[1] = LETTERS_DICT[COORDINATE[1]]
                CHOSEN.append(INPUT_TEXT)
                print(f"Combination: {COMBINATION}  Coordinate: {COORDINATE}")
                print(CHOSEN)

                CHOOSE_COLOUR = WHITE
                CHOOSE_HOVER = GHOST_WHITE

                update_grid()
                update_points()
            else:
                INPUT_TEXT = ''
                INPUT_ACTIVE = True

    # Displays any active messages
    if MESSAGE_ACTIVE:
        display_message(MESSAGE_TEXT, MESSAGE_FONT, MESSAGE_BASE_COLOUR, MESSAGE_HOVER_COLOUR, MESSAGE_FONT_COLOUR,
                        MESSAGE_POS, 'topleft')
        # Checks if the user is hovering over the message
        if MESSAGE_POS[0] <= CURSOR[0] <= (MESSAGE_POS[0] + MESSAGE_RECT.width) and \
                MESSAGE_POS[1] <= CURSOR[1] <= (MESSAGE_POS[1] + MESSAGE_RECT.height):
            MESSAGE_COLOUR = MESSAGE_HOVER_COLOUR
        else:
            MESSAGE_COLOUR = MESSAGE_BASE_COLOUR

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # For displayed messages
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                MESSAGE_ACTIVE = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # For displayed messages
            if MESSAGE_ACTIVE:
                if MESSAGE_RECT.collidepoint(event.pos):
                    MESSAGE_ACTIVE = False
            if ELF_RECT.checkForInput() and ELF_COLOUR == GREEN:
                ELF_COLOUR = RED
            if BAUBLE_RECT.checkForInput() and BAUBLE_COLOUR == GREEN:
                BAUBLE_COLOUR = RED
            if COORD_GENERATOR.checkForInput() and not (CHOOSE_COLOUR == GREEN) and not (STEAL_COLOUR == GREEN) \
                    and not (SWAP_COLOUR == GREEN):
                MESSAGE_ACTIVE = False
                generate_coord()
            if COORD_CHOOSE.checkForInput() and not (STEAL_COLOUR == GREEN):
                choose_coord()
                MESSAGE_ACTIVE = False
            if STEAL_POINTS.checkForInput():
                steal_points()
                MESSAGE_ACTIVE = False
            if SWAP_POINTS.checkForInput():
                swap_points()
                MESSAGE_ACTIVE = False
            if PRESENT_BUTTON.checkForInput():
                receive_present()
                MESSAGE_ACTIVE = False
            if EXIT_BUTTON.checkForInput():
                MENU_STATE = 'main'
                MESSAGE_ACTIVE = False


def options():
    global MENU_STATE

    SCREEN.fill(WHITE)

    # Options text
    OPTIONS_TEXT = textRect(text='This is the OPTIONS screen', font=get_font(45), base_colour=BLACK, hover_colour=BLACK,
                            pos=(640, 260))
    OPTIONS_TEXT.draw(SCREEN)
    OPTIONS_BACK = textRect(text='BACK', font=get_font(75), base_colour=BLACK, hover_colour=GREEN, pos=(640, 460))
    if OPTIONS_BACK.draw(SCREEN):
        MENU_STATE = 'main'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if OPTIONS_BACK.checkForInput():
                MENU_STATE = 'main'


def main():
    global MENU_STATE
    global CURSOR

    run = True
    while run:
        clock.tick(FPS)

        CURSOR = pygame.mouse.get_pos()

        if MENU_STATE == 'main':
            main_menu()
        elif MENU_STATE == 'play':
            play()
        elif MENU_STATE == 'options':
            options()
        else:
            SCREEN.fill(BLACK)
            TITLE = textRect(text='PIRATE GAME', font=get_font(70), base_colour=GOLD, hover_colour=LIGHT_BROWN,
                             pos=(640, 360))
            if TITLE.draw(SCREEN):
                MENU_STATE = 'main'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
