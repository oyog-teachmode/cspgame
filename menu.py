import pygame
from settings import *

screen = pygame.display.set_mode(size)

context_menu = pygame.image.load("img/item_box.png").convert_alpha()
cur = pygame.image.load("img/cursor.png").convert_alpha()
cur2 = pygame.image.load("img/cursor2.png").convert_alpha()

MENU_CLICK = pygame.mixer.Sound('sound/click.wav')
MENU_OPEN = pygame.mixer.Sound('sound/open_select.wav')
MENU_CLOSE = pygame.mixer.Sound('sound/curshoriz_close.wav')
MENU_INVALID = pygame.mixer.Sound('sound/no.wav')

menu_type = 0
cursor_x = 30
cursor_y = 24
cursor2_x = -255
menu_row = 0
menu_col = 0

def menu_load(button):  #Button 0 is B. Button 1 is A
    #corrects menu_row and menu_col positions
    global menu_row, menu_col, menu_type
    global txt1_out, txt2_out, txt3_out
    global cursor_x, cursor_y


    if menu_type == 0 and button == 1:  #when on the items menu and the A button is pressed
      MENU_OPEN.play()



    #print("menurow = " + str(menu_row))
    #print("menucol = " + str(menu_col))
    #print("menutype = " + str(menu_type) + "\n")

def cursor_handler(dpad):  #0 is right. 1 is left. 2 is up. 3 is down
    global menu_row, menu_col, menu_type
    global cursor_x, cursor_y, cursor2_x

    if menu_type == 0:
        #cursor movers
        if dpad == 1:
            cursor2_x = cursor2_x - 121
            menu_col = menu_col - 1

        if dpad == 0:
            cursor2_x = cursor2_x + 121
            menu_col = menu_col + 1

        if dpad == 3:
            cursor_y = cursor_y + 26
            menu_row = menu_row + 1

        if dpad == 2:
            cursor_y = cursor_y - 26
            menu_row = menu_row - 1

        #cursor correction
        if menu_row < 0:
            menu_row = 6
            cursor_y = cursor_y + 26 * 7

        if menu_row > 6:
            menu_row = 0
            cursor_y = cursor_y - 26 * 7

        if menu_col < 0:
            menu_col = 0
            cursor2_x = cursor2_x + 121

        if menu_col > 2:
            menu_col = 2
            cursor2_x = cursor2_x - 121


def menu_load(input):
    global menu_type
    if input == 0:
        menu_type = menu_type - 1
    if input == 1:
        menu_type = menu_type + 1
    print(menu_type)
    

def menu_loop():
    global code_bank
    screen.blit(context_menu, (00, 00))
    screen.blit(cur, (cursor_x, cursor_y))
    screen.blit(cur2, (cursor2_x, 360))
    font = pygame.font.Font("Ubuntu.ttf", 21)
    textline = font.render("Press K or Z to proceed into the battle", False, (255, 255, 255))
    screen.blit(textline, (25, 410))  #BGLAYER0


#End of While Loop
