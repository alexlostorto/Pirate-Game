import pygame, sys
import random
from Classes import *
from pygame.locals import *

pygame.init()

gold = "#FFD700"
buttonLight = '#E5AA70'
buttonDark = '#B87333'
white = '#FFFFFF'
green = '#00FF00'

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
lettersDict = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7
}

screenWidth = 1280
screenHeight = 720
gridWidth = 490
gridHeight = 490
squareSize = 70

topLeftX = 100
topLeftY = 150

grid = []
points = 0
chosen = []
combination = ''

SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/cute_font.ttf", size)


def play():
    ROW_COUNT = 7
    COLUMN_COUNT = 7
    PIECES = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
              200, 200, 200, 200, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 3000, 3000, 5000,
              'GRINCH', 'PUDDING', 'PRESENT', 'SNOWBALL', 'MISTLETOE', 'TREE', 'ELF_COLOUR', 'BAUBLE_COLOUR', 'TURKEY', 'CRACKER',
              'BANK']

    def create_grid():
        global grid

        # Creates the grid by choosing a random item for each square in the grid
        grid = [[['', 0] for x in range(ROW_COUNT)] for x in range(COLUMN_COUNT)]
        pieces = list(PIECES)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Removes item after it has been chosen
                choice = random.randint(0, len(pieces) - 1)
                grid[r][c][0] = pieces[choice]
                pieces.pop(choice)

        sx = topLeftX
        sy = topLeftY
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                position = (sx + (squareSize // 2) + squareSize * c, sy + (squareSize // 2) + squareSize * r)
                # Places items in the grid
                if grid[r][c][0] == 200:
                    textGridItem(text=200, font=get_font(30), colour=white, pos=position)
                if grid[r][c][0] == 1000:
                    textGridItem(text=1000, font=get_font(30), colour=white, pos=position)
                if grid[r][c][0] == 3000:
                    textGridItem(text=3000, font=get_font(30), colour=white, pos=position)
                if grid[r][c][0] == 5000:
                    textGridItem(text=5000, font=get_font(30), colour=white, pos=position)
                if grid[r][c][0] == 'GRINCH':
                    imageGridItem(image=pygame.image.load("assets/Grinch.png").convert_alpha(), width=60, height=65,
                                  pos=position)
                if grid[r][c][0] == 'PUDDING':
                    imageGridItem(image=pygame.image.load("assets/Pudding.png").convert_alpha(), width=65, height=65,
                                  pos=position)
                if grid[r][c][0] == 'PRESENT':
                    imageGridItem(image=pygame.image.load("assets/Present.png").convert_alpha(), width=60, height=65,
                                  pos=position)
                if grid[r][c][0] == 'SNOWBALL':
                    imageGridItem(image=pygame.image.load("assets/Snowball.png").convert_alpha(), width=65, height=65,
                                  pos=position)
                if grid[r][c][0] == 'MISTLETOE':
                    imageGridItem(image=pygame.image.load("assets/Mistletoe.png").convert_alpha(), width=65, height=65,
                                  pos=position)
                if grid[r][c][0] == 'TREE':
                    imageGridItem(image=pygame.image.load("assets/Christmas Tree.png").convert_alpha(), width=55, height=65,
                                  pos=position)
                if grid[r][c][0] == 'ELF_COLOUR':
                    imageGridItem(image=pygame.image.load("assets/Elf.png").convert_alpha(), width=40, height=65,
                                  pos=position)
                if grid[r][c][0] == 'BAUBLE_COLOUR':
                    imageGridItem(image=pygame.image.load("assets/Bauble.png").convert_alpha(), width=60, height=65,
                                  pos=position)
                if grid[r][c][0] == 'TURKEY':
                    imageGridItem(image=pygame.image.load("assets/Turkey.png").convert_alpha(), width=65, height=65,
                                  pos=position)
                if grid[r][c][0] == 'CRACKER':
                    imageGridItem(image=pygame.image.load("assets/Christmas Cracker.png").convert_alpha(), width=65, height=65,
                                  pos=position)
                if grid[r][c][0] == 'BANK':
                    imageGridItem(image=pygame.image.load("assets/Christmas Hat.png").convert_alpha(), width=65, height=65,
                                  pos=position)
                if grid[r][c][1] == 1:
                    imageGridItem(image=pygame.image.load("assets/Red_X.png").convert_alpha(), width=60, height=65,
                                  pos=position)

    def draw_grid():
        sx = topLeftX
        sy = topLeftY
        for c in range(COLUMN_COUNT + 1):
            pygame.draw.line(SCREEN, white, (sx, sy + c * squareSize), (sx + gridWidth, sy + c * squareSize))
            for r in range(ROW_COUNT + 1):
                pygame.draw.line(SCREEN, white, (sx + r * squareSize, sy), (sx + r * squareSize, sy + gridHeight))

        for c in range(COLUMN_COUNT):
            X_AXIS_TEXT = get_font(45).render(letters[c], True, white)
            X_AXIS_RECT = X_AXIS_TEXT.get_rect(center=(sx + (squareSize // 2) + squareSize * c, sy - 25))
            SCREEN.blit(X_AXIS_TEXT, X_AXIS_RECT)

        for r in range(ROW_COUNT):
            Y_AXIS_TEXT = get_font(45).render(str(r + 1), True, white)
            Y_AXIS_RECT = Y_AXIS_TEXT.get_rect(center=(sx - 25, sy + (squareSize // 2) + squareSize * r))
            SCREEN.blit(Y_AXIS_TEXT, Y_AXIS_RECT)

    def draw_items():
        sx = topLeftX
        sy = topLeftY

        def draw_item(text, fontSize, colour):
            ITEM_TEXT = get_font(int(fontSize)).render(str(text), True, colour)
            ITEM_RECT = ITEM_TEXT.get_rect(
                center=(sx + (squareSize // 2) + squareSize * c, sy + (squareSize // 2) + squareSize * r))
            SCREEN.blit(ITEM_TEXT, ITEM_RECT)

        def display_image(image, width, height):
            IMAGE = pygame.transform.scale(image, (width, height))
            IMAGE_RECT = IMAGE.get_rect(
                center=(sx + (squareSize // 2) + squareSize * c, sy + (squareSize // 2) + squareSize * r))
            SCREEN.blit(IMAGE, IMAGE_RECT)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Places items in the grid
                if grid[r][c][0] == 200:
                    draw_item(200, 30, white)
                if grid[r][c][0] == 1000:
                    draw_item(1000, 30, white)
                if grid[r][c][0] == 3000:
                    draw_item(3000, 30, white)
                if grid[r][c][0] == 5000:
                    draw_item(5000, 30, white)
                if grid[r][c][0] == 'GRINCH':
                    display_image(pygame.image.load("assets/Grinch.png").convert_alpha(), 65, 65)
                if grid[r][c][0] == 'PUDDING':
                    display_image(pygame.image.load("assets/Pudding.png").convert_alpha(), 65, 65)
                if grid[r][c][0] == 'PRESENT':
                    display_image(pygame.image.load("assets/Present.png").convert_alpha(), 60, 65)
                if grid[r][c][0] == 'SNOWBALL':
                    display_image(pygame.image.load("assets/Snowball.png").convert_alpha(), 65, 65)
                if grid[r][c][0] == 'MISTLETOE':
                    display_image(pygame.image.load("assets/Mistletoe.png").convert_alpha(), 65, 65)
                if grid[r][c][0] == 'TREE':
                    display_image(pygame.image.load("assets/Christmas Tree.png").convert_alpha(), 55, 65)
                if grid[r][c][0] == 'ELF_COLOUR':
                    display_image(pygame.image.load("assets/Elf.png").convert_alpha(), 40, 65)
                if grid[r][c][0] == 'BAUBLE_COLOUR':
                    display_image(pygame.image.load("assets/Bauble.png").convert_alpha(), 60, 65)
                if grid[r][c][0] == 'TURKEY':
                    display_image(pygame.image.load("assets/Turkey.png").convert_alpha(), 65, 65)
                if grid[r][c][0] == 'CRACKER':
                    display_image(pygame.image.load("assets/Christmas Cracker.png").convert_alpha(), 65, 65)
                if grid[r][c][0] == 'BANK':
                    display_image(pygame.image.load("assets/Christmas Hat.png").convert_alpha(), 65, 65)
                if grid[r][c][1] == 1:
                    display_image(pygame.image.load("assets/Red_X.png").convert_alpha(), 65, 65)

    def print_grid():
        # Prints the grid in the console
        for line in grid:
            print(line)

    def dict_grid():
        # Checks how many of each item there is
        result = {}
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                result[grid[r][c][0]] = result.get(grid[r][c][0], 0) + 1

        print(result)

    def generate_coord():
        global combination

        if len(chosen) >= 49:
            print("Game Over")
            return False
        combination = f"{random.randint(1, 7)}{random.choice(letters)}"
        while combination in chosen and len(chosen) < 49:
            combination = f"{random.randint(1, 7)}{random.choice(letters)}"
        chosen.append(combination)

        print(f"The coordinate is: {combination}")
        print(chosen)

    def cross_item(combination):
        combination = list(combination)
        row = int(combination[0])-1
        column = int(lettersDict[combination[1]])-1

        grid[row][column][1] = 1

    create_grid()
    print_grid()
    print()

    # Red Exit Button
    PLAY_BACK = imgButton(image=pygame.image.load("assets/Red_X.png").convert_alpha(), pos=(1230, 50),
                          width=40, height=40)
    # Pirate Game Header
    PLAY_TEXT = get_font(45).render("PIRATE GAME", True, gold)
    PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 50))
    # Points
    POINTS_TEXT = get_font(45).render(str(points), True, white)
    POINTS_RECT = POINTS_TEXT.get_rect(
        center=((screenWidth - gridWidth - topLeftX) // 2 + gridWidth + topLeftX, 120))
    # Generate coordinate button
    GENERATE = Button(image=None, pos=(750, 625),
                      text_input="GENERATE", font=get_font(50), base_color=white, hovering_color="Green")
    # Choose coordinate button
    CHOOSE = Button(image=None, pos=(1130, 625),
                    text_input="CHOOSE", font=get_font(50), base_color=white, hovering_color="Green")
    # Coordinate
    COORDINATE_TEXT = get_font(70).render(str(combination), True, gold)
    COORDINATE_RECT = COORDINATE_TEXT.get_rect(
        center=(915, 610))

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        SCREEN.blit(POINTS_TEXT, POINTS_RECT)

        GENERATE.changeColor(PLAY_MOUSE_POS)
        GENERATE.update(SCREEN)

        CHOOSE.changeColor(PLAY_MOUSE_POS)
        CHOOSE.update(SCREEN)

        pygame.draw.rect(SCREEN, white, pygame.Rect(902, 640, 100, 4))
        SCREEN.blit(COORDINATE_TEXT, COORDINATE_RECT)

        # Draws Grid
        draw_grid()
        # draw_items()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main()
                if GENERATE.checkForInput(PLAY_MOUSE_POS):
                    generate_coord()
                    cross_item(combination)
                    COORDINATE_TEXT = get_font(70).render(str(combination), True, gold)

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main()

        pygame.display.update()


def main():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("PIRATE GAME", True, gold)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color=buttonLight, hovering_color=buttonDark)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color=buttonLight,
                                hovering_color=buttonDark)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color=buttonLight, hovering_color=buttonDark)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
