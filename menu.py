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


def menu_loop():
    pygame.display.set_caption('There is no time to rest and manage items in the Pizza Tower')
    screen.blit(context_menu, (20, 30))
    screen.blit(cur, (cursor_x, cursor_y))
    screen.blit(cur2, (cursor2_x, 360))
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #for right now it's just a boss engine with more to be added
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:  #0 is right. 1 is left. 2 is up. 3 is down
                cursor_handler(2)
                MENU_CLICK.play()
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                cursor_handler(1)
                MENU_CLICK.play()

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                cursor_handler(3)
                MENU_CLICK.play()

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                cursor_handler(0)
                MENU_CLICK.play()

            if event.key == pygame.K_j or event.key == pygame.K_z:
                menu_load(0)

            if event.key == pygame.K_k or event.key == pygame.K_x:
                menu_load(1)

            if event.key == pygame.K_1:
                print("WARNING: THE WINDOW IS NO LONGER RUNNING \n\n ________DEBUG MENU_______ \n 1. Reset the Boss \n 2. Set Everyone's HP to MAX and restore PP\n")
                debug(int(input("Pick your number:")))


#End of While Loop
