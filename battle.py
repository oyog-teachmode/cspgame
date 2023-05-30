"""
RPG to do list:

OPTIMIZE CODE!!
The text scrolling function and main loop are easy to break\
the text scrolling can really be optimized


Bugs: 
# item still usable after reaching 0kk

Necessary:
# replace the placeholder dog


NOT Necessary but we should definetly do this:

# battle animations (can be as simple as shaking the screen when hurt or turning it red when he does the fire attack)
# more sounds
# character graphics for the Warrior, Healer, and Brute

"""
import sys, pygame
import random
from settings import *

pygame.display.set_caption('EARTH HOUND')

font = pygame.font.Font("Ubuntu.ttf", 21)  #text box text
font2 = pygame.font.Font("SYS.ttf", 18)  #description text
font3 = pygame.font.Font("courier.ttf", 18)  #used for status box text
font4 = pygame.font.Font("courier.ttf", 18)  #used for HP/PP counters
font5 = pygame.font.Font("SYS.ttf", 24)  #used for the YOU WIN! text

background = pygame.image.load("img/snow_biome.png").convert()
txt_box = pygame.image.load("img/txt_box.png").convert_alpha()
battle_box = pygame.image.load("img/battle_box.png").convert_alpha()
status_box = pygame.image.load("img/statusBox.png").convert_alpha()
boss_img = pygame.image.load("img/placeface.png").convert_alpha()
cur = pygame.image.load("img/cursor.png").convert_alpha()
cur2 = pygame.image.load("img/cursor2.png").convert_alpha()
cur3 = pygame.image.load("img/cursor3.png").convert_alpha()
attack_txt_bg = pygame.image.load("img/attack_window.png").convert()
context_menu = pygame.image.load("img/item_box.png").convert_alpha()
damage_indicator = pygame.image.load("img/damageIndicator.png").convert_alpha()
green_overlay = pygame.image.load("img/green_overlay.png")

death = pygame.image.load("img/effect_icons/death.png").convert_alpha()

BGM1 = pygame.mixer.Sound('music/02.wav')
BGM2 = pygame.mixer.Sound('music/03.wav')

screen = pygame.display.set_mode(size)
#draws an image to the screen
#these are static images

#variable initiation
current_line = 1
txt1 = ""
txt2 = ""
txt3 = ""
txt1_out = ""
txt2_out = ""
txt3_out = ""
txtScr = 0
last_message = ""
input_allowed = True
cursor_x = -16
cursor_y = 0
cursor2_x = -255
enemy_name = "SocksDog"
line_appender = 0
choices = []
menu_type = 0
"""
menu_type = -1: Unskippable Text
menu_type = 0: None, Text is scrolling
menu_type = 1: Main Battle Menu (Attack, Defend, Skills, etc.)
menu_type = 2: Attack Enemy Selection, Which is intended to select and attack multiple enemies
menu_type = 3: Skills Menu
menu_type = 4: Items Menu
"""
menu_row = 0
menu_col = 0

enemy0_x = 140
enemy0_y = 120

#booleans
text_has_finished = False
main_function_is_callable = False
winIsPlayed = False
member1_isActive = False

Warrior_action_completed = False
Healer_action_completed = False
Brute_action_completed = False
Enemy_action_completed = False

#bruh :(
WARR_LOGIC_DONE = False
HEAL_LOGIC_DONE = False
BRUT_LOGIC_DONE = False
ENEMY_LOGIC_DONE = False

Apress_after_intro = False

#main loop variables
BossHP = 2000
WAR_MAXHP = 300
HEA_MAXHP = 150
BRU_MAXHP = 500

HEA_MAXPP = 150

Warrior = WAR_MAXHP
Healer = HEA_MAXHP
Brute = BRU_MAXHP

PARTY_MEMBER_NAMES = ["Warrior", "Healer", "Brute"]
PARTY_MEMBER_EFFECTS = ["---", "---", "---"]

Warrior_TARGETHP = Warrior
Healer_TARGETHP = Healer
Brute_TARGETHP = Brute

Healer_PP = HEA_MAXPP

Healer_TARGETPP = Healer_PP

SKILLS = {
    1: ["Taunt", "Charge", "---"],
    2: ["Heal", "Mega Heal", "---"],
    3: ["BRUTE FORCE!", "---", "---"]
}
SKILLS_DESCRIPTION = {
    1: [[
        "Gives the hero a boost in stats.",
        "The enemy will become focused on the taunter."
    ],
        [
            "The Hero will rush toward the enemy waving their ",
            "sword wildly. Damage varies"
        ], ["Skill Locked", " "]],
    2: [["Restores the party to half of their health", "PP cost: 10"],
        ["Restores the party to full health", "PP cost: 37"],
        ["Skill Locked", " "]],
    3: [["Bum-rushes the enemy", " "], ["Skill Locked", " "],
        ["Skill Locked", " "]]
}

#item description images
mushroom = pygame.image.load("img/mushroom.png").convert()
skinny_mushroom = pygame.image.load("img/skinny_mushroom.png").convert()
one_up = pygame.image.load("img/1up.png").convert()
test = pygame.image.load("img/test.png").convert()
none = pygame.image.load("img/blank.png").convert_alpha()

Inventory = [
    "Mushroom", "Skinny Mushroom", "1-UP Shroom", "test", "---", "---", "---"
]
Inventory_amount = [5, 1, 1, 6, 0, 0, 0]
ITEM_DESCRIPTION = {
    "Mushroom": ["Soopah Mahreo in real loife.", "Restores 80 HP", mushroom],
    "Skinny Mushroom":
    ["Super Mario Maker reference??1?1", "Restores 160 HP", skinny_mushroom],
    "1-UP Shroom": ["Revives a dead team member", "Nice!", one_up],
    "test": [
        "Gives a lethal dose of poison to the user.",
        "...you can use it to revive the dead..", test
    ],
    "---": ["", "", none]
}

ITEM_ACTION = {
    "Mushroom": [
        80, 0,
        ["Don't do drugs kids, or you go to", "hell before you die", "BEANZ"],
        None, "add", "add"
    ],
    "1-UP Shroom": [1, 10, ["Waow ifone", " ", " "], "Death", "add", "add"],
    "Skinny Mushroom": [160, 0, [" ", " ", " "], None, "add", "add"],
    "test": [
        9999, 0,
        ["Don't do drugs kids, or you go to", "hell before you die", "BEANZ"],
        "Death", "sub", "add"
    ],
    "---": [None, None, None, None, None, None]
}
"""
ITEM_ACTION. The actions an item does. Argument Format:

0. hp amount to add/subtract
1. pp amount to add/subtract
2. what to say when the item is used. Must be a list of 3 strings with at least one character
3. What effect it can cure
4. "add" or "sub" HP?
5. "add" or "sub" PP?
"""

STATUSBAR_EFFECTCOLORS = {
    "Death": [(200, 20, 20), death],
    "Frozen": [(50, 20, 200)]
}
Wdefend = False
Hdefend = False
Bdefend = False
taunt = 0
TA = 0  #is this taunt aggrivation?
charge = False
CA = 0
special = 0
current_member = 1
item_cursor_list = [116, 237, 358]
"""
current_member = 1: Warrior
current_member = 2: Healer
current_member = 3: Brute
"""
pl_input = 0
main_output = 0
WIN = pygame.mixer.Sound('music/you_win!.wav')
MENU_CLICK = pygame.mixer.Sound('sound/click.wav')
MENU_OPEN = pygame.mixer.Sound('sound/open_select.wav')
MENU_CLOSE = pygame.mixer.Sound('sound/curshoriz_close.wav')
MENU_INVALID = pygame.mixer.Sound('sound/no.wav')

"""
printB() usage:
automatically formats text to be displayed in the text box
dont put printB or update_text in a loop
"""

div_clock = 0
div_clock2 = 0


def divide_clock(
):  #divides the 60Hz clock by div_clock amount and resets to 0
    global div_clock
    global div_clock2
    div_clock += 1
    div_clock2 += 1

    if div_clock >= 3:
        roll_hp()
        roll_pp()
        div_clock = 0


last_frame = 0


def quick_sleep(amount):  #used in the main() function to wait some time after the text box completes printing
    global last_frame
    last_frame = last_frame + 1
    if last_frame >= amount:
        last_frame = 0
        return True
    else:
        return False


def roll_hp():  #the HP roller. You lose life slowly
    global Warrior, Healer, Brute
    global WAR_MAXHP, HEA_MAXHP, BRU_MAXHP
    global Warrior_TARGETHP, Healer_TARGETHP, Brute_TARGETHP

    #Warrior's HP
    if Warrior_TARGETHP > Warrior and Warrior <= WAR_MAXHP:  #gaining life
        Warrior += 10
    elif Warrior_TARGETHP < Warrior and Warrior > -1:  #losing life
        Warrior -= 15

    #Healer's HP
    if Healer_TARGETHP > Healer and Healer <= HEA_MAXHP:  #gaining life
        Healer += 10
    elif Healer_TARGETHP < Healer and Healer > -1:  #losing life
        Healer -= 15

    #Brute's HP
    if Brute_TARGETHP > Brute and Brute <= BRU_MAXHP:  #gaining life
        Brute += 10
    elif Brute_TARGETHP < Brute and Brute > -1:  #losing life
        Brute -= 15

    #death effect giver
    if Warrior < 1:
        PARTY_MEMBER_EFFECTS[0] = "Death"
    if Healer < 1:
        PARTY_MEMBER_EFFECTS[1] = "Death"
    if Brute < 1:
        PARTY_MEMBER_EFFECTS[2] = "Death"

    #HP Visual Corrector
    if Warrior < 0:
        Warrior = 0
    if Healer < 0:
        Healer = 0
    if Brute < 0:
        Brute = 0


def roll_pp():
    global HEA_MAXHP
    global Healer_TARGETHP
    global Healer_PP

    #Healer's PP or Mana
    if Healer_TARGETPP > Healer_PP and Healer_PP <= HEA_MAXHP:  #gaining life
        Healer_PP += 10
    elif Healer_TARGETPP < Healer_PP and Healer_PP > -1:  #losing life
        Healer_PP -= 1


def music_change():  #changes out the music without stopping playback
    if BGM2.get_volume() < 1:
        BGM2.set_volume(1)
        BGM1.set_volume(0)
    elif BGM2.get_volume() > 0:
        BGM2.set_volume(0)
        BGM1.set_volume(1)


def printB(i1, i2, i3):  #used for printing text into the text boxes
    global txt1, txt2, txt3
    global current_line
    txt1 = i1
    txt2 = i2
    txt3 = i3
    current_line = 1


def item_handler(
        affected_player):  #item handling. This is the most complex function.
    global choices
    global Warrior_TARGETHP, Healer_TARGETHP, Brute_TARGETHP
    global Healer_TARGETPP

    inventory_index = int(choices[affected_player].split("@")
                          [1])  #take the encoded string and decode it
    for_whom = int(choices[affected_player].split("@")[2])
    item_name = Inventory[inventory_index]

    if for_whom == affected_player:
        printB(PARTY_MEMBER_NAMES[affected_player] + " used the " + item_name,
               " ", " ")
    else:
        printB(PARTY_MEMBER_NAMES[affected_player] + " used the " + item_name,
               "on " + PARTY_MEMBER_NAMES[for_whom], " ")

    #unpack everything for easier readability
    item_hp, item_pp, item_effect, HP_addsub, PP_addsub = ITEM_ACTION[
        item_name][0], ITEM_ACTION[item_name][1], ITEM_ACTION[item_name][
            3], ITEM_ACTION[item_name][4], ITEM_ACTION[item_name][5],

    if for_whom == 0:
        if HP_addsub == "add":
            Warrior_TARGETHP = Warrior_TARGETHP + item_hp
        if HP_addsub == "sub":
            Warrior_TARGETHP = Warrior_TARGETHP - item_hp

        #effect curing
        if item_effect == "Death" and PARTY_MEMBER_EFFECTS[
                0] == "Death":  #double check if they are actually dead
            Warrior_TARGETHP = WAR_MAXHP
            PARTY_MEMBER_EFFECTS[0] = "---"

    if for_whom == 1:

        if HP_addsub == "add":
            Healer_TARGETHP = Healer_TARGETHP + item_hp
        if HP_addsub == "sub":
            Healer_TARGETHP = Healer_TARGETHP - item_hp

        if PP_addsub == "add":
            Healer_TARGETPP = Healer_TARGETPP + item_pp
        if PP_addsub == "sub":
            Healer_TARGETPP = Healer_TARGETPP - item_pp

        #effect curing
        if item_effect == "Death" and PARTY_MEMBER_EFFECTS[1] == "Death":
            Healer_TARGETHP = HEA_MAXHP
            PARTY_MEMBER_EFFECTS[1] = "---"

    if for_whom == 2:

        if HP_addsub == "add":
            Brute_TARGETHP = Brute_TARGETHP + item_hp
        if HP_addsub == "sub":
            Brute_TARGETHP = Brute_TARGETHP - item_hp

        #effect curing
        if item_effect == "Death" and PARTY_MEMBER_EFFECTS[2] == "Death":
            Brute_TARGETHP = BRU_MAXHP
            PARTY_MEMBER_EFFECTS[2] = "---"

    Inventory_amount[inventory_index] = Inventory_amount[inventory_index] - 1


def update_text(
):  #does the scrolling text thing in RPGs, I am very sorry for the jankiness.
    global current_line, txtScr
    global txt1_out, txt2_out, txt3_out
    global txt1, txt2, txt3
    global text_has_finished

    if current_line == 1:
        txt1_out = (txt1[:txtScr])

        if txtScr == len(txt1):
            current_line = 2
            txtScr = 1
        else:
            txtScr = txtScr + 1

    elif current_line == 2:  #line2
        txt2_out = (txt2[:txtScr])

        if txtScr == len(txt2):
            current_line = 3
            txtScr = 1
        else:
            txtScr = txtScr + 1
    elif current_line == 3:  #line3
        txt3_out = (txt3[:txtScr])
        if txtScr == len(txt3):
            txtScr = 1
            current_line = 0
            text_has_finished = True
        else:
            txtScr = txtScr + 1

    line1 = font.render(txt1_out, True, (255, 255, 255))
    line2 = font.render(txt2_out, True, (255, 255, 255))
    line3 = font.render(txt3_out, True, (255, 255, 255))

    screen.blit(line1, (25, 20))  #BGLAYER0
    screen.blit(line2, (25, 45))  #BGLAYER0
    screen.blit(line3, (25, 70))  #BGLAYER0


class WarriorMoves():

    def attack():
        global BossHP
        global TA
        if TA > 0:
            TA -= 1
        printB(PARTY_MEMBER_NAMES[0] + " attacked", " ", " ")
        BossHP -= 100
        print(f"Enemy health reduced to {BossHP}")

    def defend():
        global Wdefend
        global TA
        if TA > 0:
            TA -= 1
        printB(PARTY_MEMBER_NAMES[0] + "is defending", " ", " ")
        Wdefend = True

    def taunt():
        global TA
        if TA == 0:
            global taunt
            taunt = 3
            printB(PARTY_MEMBER_NAMES[0] + " taunted " + enemy_name, " ", " ")

            TA += 4

        else:
            print(
                f"Taunt is on cooldown, wait {TA} more turns until you can use it again"
            )

            TA -= 1

    def charge():
        global BossHP
        random_value = random.choice([20, 160, 160, 160])
        BossHP -= random_value
        if random_value == 20:
            printB(
                PARTY_MEMBER_NAMES[0] + " charged toward " + enemy_name +
                "                                ",
                "...but tripped and fell in the process.",
                str(random_value) + " damage to " + enemy_name)
        else:
            printB(PARTY_MEMBER_NAMES[0] + " charged toward " + enemy_name,
                   str(random_value) + " damage to " + enemy_name, " ")


class HealerMoves():

    def attack():
        global BossHP
        global Healer_TARGETPP
        Healer_TARGETPP += 10
        Max = 150
        if Healer_TARGETPP > Max:
            Healer_TARGETPP = 150
        printB(PARTY_MEMBER_NAMES[1] + " attacked", " ", " ")
        BossHP -= 25
        print(f"Enemy health reduced to {BossHP}")

    def defend():
        global Hdefend
        Hdefend = True
        printB(PARTY_MEMBER_NAMES[1] + " is defending", " ", " ")

    def mheal():
        global Warrior_TARGETHP
        global Healer_TARGETHP
        global Brute_TARGETHP
        global Healer_TARGETPP
        global WAR_MAXHP, HEA_MAXHP, BRU_MAXHP
        if Healer_TARGETPP < 37:
            printB("Not Enough Mana", "Attack to get more mana", " ")
        else:
            Healer_TARGETPP -= 37
            Warrior_TARGETHP = WAR_MAXHP
            Healer_TARGETHP = HEA_MAXHP
            Brute_TARGETHP = BRU_MAXHP
            printB(PARTY_MEMBER_NAMES[1] + " used Mega Heal", " ", " ")

    def heal():
        global Warrior_TARGETHP
        global Healer_TARGETHP
        global Brute_TARGETHP
        global WAR_MAXHP, HEA_MAXHP, BRU_MAXHP
        global Healer_TARGETPP
        if Healer_PP < 10:
            printB("Not Enough Mana", "Perhaps... ", "Attack to get more mana")
        else:
            Healer_TARGETPP -= 10
            Warrior_TARGETHP = Warrior_TARGETHP + (WAR_MAXHP / 2)
            Healer_TARGETHP = Healer_TARGETHP + (HEA_MAXHP / 2)
            Brute_TARGETHP = Brute_TARGETHP + (BRU_MAXHP / 2)
            printB(PARTY_MEMBER_NAMES[1] + " used Heal", " ", " ")


class BruteMoves():

    def attack():

        global BossHP
        global special
        if special > 0:
            special -= 1
        printB(PARTY_MEMBER_NAMES[2] + " attacked", " ", " ")
        BossHP -= 300
        print(f"Enemy health reduced to {BossHP}")

    def defend():
        global special
        global Bdefend
        if special > 0:
            special -= 1
        Bdefend = True
        printB(PARTY_MEMBER_NAMES[2] + " is defending", " ", " ")

    def HeavyAttack():
        global BossHP
        global special
        if special == 0:
            printB(PARTY_MEMBER_NAMES[2] + " used Heavy Attack", " ", " ")
            BossHP -= 1000
            special += 2
            print(f"Enemy health reduced to {BossHP}")

        else:
            print(
                f"Heavy Attack is on cooldown, wait {special} more turns until you can use it again "
            )


class Boss:

    def Fire():
        global Warrior
        global Healer
        global Brute
        global Warrior_TARGETHP, Healer_TARGETHP, Brute_TARGETHP
        global Wdefend
        global Hdefend
        global Bdefend
        global taunt
        global CA
        if CA > 0:
            CA -= 1
        rng = random.randint(1, 3)
        if taunt > 0:
            if Wdefend == True:
                printB("Warrior blocked the attack", " ", " ")

            else:
                printB(
                    "Warrior was hit by a bolt of fire dealing 285 damage to him",
                    " ", " ")
                Warrior_TARGETHP -= 285

        else:
            if rng == 1:
                if Wdefend == True:
                    printB("Warrior blocked the attack", " ", " ")

                else:
                    printB("Warrior was hit by a fire ball causing him to",
                           "  take 135 damage", " ")
                    Warrior_TARGETHP -= 135

            elif rng == 2:
                if Hdefend == True:
                    printB("Healer blocked the attack", " ", " ")

                else:
                    printB("Healer was hit by a fire ball causing her to ",
                           "take 135 damage", " ")
                    Healer_TARGETHP -= 135

            else:
                if Bdefend == True:
                    printB("Brute blocked the attack", " ", " ")

                else:
                    printB("Brute was hit by a fire ball causing him to",
                           "  take 135 damage", " ")
                    Brute_TARGETHP -= 135

    def AOE():
        global CA
        global Warrior
        global Healer
        global Brute
        global Warrior_TARGETHP, Healer_TARGETHP, Brute_TARGETHP
        global Wdefend
        global Hdefend
        global Bdefend
        if CA > 0:
            CA -= 1
        printB("The Enemy summoned a rain of fire upon ", "the heroes", " ")
        Warrior_TARGETHP -= 135
        Healer_TARGETHP -= 135
        Brute_TARGETHP -= 135

    def RedSprite():
        global charge
        global CA
        global Brute
        global Warrior
        global Healer
        global Warrior_TARGETHP, Healer_TARGETHP, Brute_TARGETHP
        warrior_result_string = ""
        healer_result_string = ""
        brute_result_string = ""
        if charge == True:
            CA = 3
            charge = False
            if Wdefend == True:
                warrior_result_string = "Warrior blocked the attack"
            else:
                warrior_result_string = "Warrior was reduced to ashes"
                Warrior_TARGETHP = 0
            if Hdefend == True:
                healer_result_string = "Healer blocked the attack"
            else:
                healer_result_string = "Healer was reduced to ashes"
                Healer_TARGETHP = 0
            if Bdefend == True:
                brute_result_string = "Brute blocked the attack"
            else:
                brute_result_string = "Brute was reduced to ashes"
                Brute_TARGETHP = 0
            printB(warrior_result_string, healer_result_string,
                   brute_result_string)

        else:
            printB("The Enemy charges up an attack", " ", " ")
            charge = True


def BossAlgorithim():
    global CA
    global charge
    rng = random.randint(1, 3)
    if charge == True:
        #Do the attack that was charged
        Boss.RedSprite()
    elif rng == 1:
        #AOE Attack
        Boss.AOE()
    elif rng == 2 and CA == 0:
        #Charge
        Boss.RedSprite()
    else:
        #Basic Attack
        Boss.Fire()


def main(PLinput):  #the Main loop
    #pl is input for any person in the party. current_member is the current party member
    global current_member
    global choices
    global current_line
    global text_has_finished
    global Warrior_action_completed, Healer_action_completed, Brute_action_completed, Enemy_action_completed
    global WARR_LOGIC_DONE, HEAL_LOGIC_DONE, BRUT_LOGIC_DONE, ENEMY_LOGIC_DONE

    if BossHP < 1:  #after someone attacks it must check is the boss died or it will continue the cycle
        return 1

    if PARTY_MEMBER_EFFECTS[0] == "Death" and PARTY_MEMBER_EFFECTS[
            1] == "Death" and PARTY_MEMBER_EFFECTS[2] == "Death":
        pygame.quit()
    #print("W"+ str(Warrior_action_completed))
    #print("H"+ str(Healer_action_completed))
    #print("B" + str(Brute_action_completed))

    if WARR_LOGIC_DONE == False:
        if Warrior_action_completed == False:
            text_has_finished = False
            if PLinput[0] == "A":
                WarriorMoves.attack()
            elif PLinput[0] == "D":
                WarriorMoves.defend()
            elif PLinput[0] == "S0":
                WarriorMoves.taunt()
            elif PLinput[0] == "S1":
                WarriorMoves.charge()
            elif PLinput[0].split("@")[0] == "I":
                item_handler(0)
            elif PLinput[0] == "Ded":
                printB(PARTY_MEMBER_NAMES[0] + " is unconscious.", " ", " ")
            Warrior_action_completed = True

        if text_has_finished == False:
            return 0
        if quick_sleep(36) == False:
            return 0
        WARR_LOGIC_DONE = True

    if BossHP < 1:  #after someone attacks it must check is the boss died or it will continue the cycle
        return 1

    if HEAL_LOGIC_DONE == False:
        if Healer_action_completed == False:
            text_has_finished = False
            if PLinput[1] == "A":
                HealerMoves.attack()
            elif PLinput[1] == "D":
                HealerMoves.defend()
            elif PLinput[1] == "S0":
                HealerMoves.heal()
            elif PLinput[1] == "S1":
                HealerMoves.mheal()

            elif PLinput[1].split("@")[0] == "I":
                item_handler(1)
            elif PLinput[1] == "Ded":
                printB(PARTY_MEMBER_NAMES[1] + " is unconscious.", " ", " ")
            Healer_action_completed = True

        if text_has_finished == False:
            return 0
        if quick_sleep(36) == False:
            return 0
        HEAL_LOGIC_DONE = True

    if BossHP < 1:  #the if statement repeated
        return 1

    if BRUT_LOGIC_DONE == False:
        if Brute_action_completed == False:
            text_has_finished = False
            if PLinput[2] == "A":
                BruteMoves.attack()
            elif PLinput[2] == "D":
                BruteMoves.defend()
            elif PLinput[2] == "S0":
                BruteMoves.HeavyAttack()
            elif PLinput[2].split("@")[0] == "I":
                item_handler(2)
            elif PLinput[2] == "Ded":
                printB(PARTY_MEMBER_NAMES[2] + " is unconscious.", " ", " ")
            Brute_action_completed = True

        if text_has_finished == False:
            return 0
        if quick_sleep(36) == False:
            return 0
        BRUT_LOGIC_DONE = True

    if BossHP < 1:  #the if statement repeated
        return 1

    #This allows the enemy to attack
    if ENEMY_LOGIC_DONE == False:
        if Enemy_action_completed == False:
            text_has_finished = False
            BossAlgorithim()
            Enemy_action_completed = True

        if text_has_finished == False:
            return 0
        if quick_sleep(90) == False:
            return 0
        ENEMY_LOGIC_DONE = True

    global main_function_is_callable
    main_function_is_callable = False
    Warrior_action_completed = False
    Healer_action_completed = False
    Brute_action_completed = False
    Enemy_action_completed = False
    text_has_finished = True
    choices = []
    global menu_row, menu_col, menu_type
    global cursor_x, cursor_y
    menu_type = 1
    cursor_x = 30
    cursor_y = 24
    menu_col = 0
    menu_row = 0
    WARR_LOGIC_DONE = False
    HEAL_LOGIC_DONE = False
    BRUT_LOGIC_DONE = False
    ENEMY_LOGIC_DONE = False
    current_member = 1


def cursor_handler(dpad):  #0 is right. 1 is left. 2 is up. 3 is down
    global menu_row, menu_col, menu_type
    global cursor_x, cursor_y, cursor2_x

    if menu_type == 1:
        #cursor movers
        if dpad == 1:
            cursor_x = cursor_x - 86
            menu_col = menu_col - 1

        if dpad == 0:
            cursor_x = cursor_x + 86
            menu_col = menu_col + 1

        if dpad == 3:
            cursor_y = cursor_y + 26
            menu_row = menu_row + 1

        if dpad == 2:
            cursor_y = cursor_y - 26
            menu_row = menu_row - 1

        #cursor correction
        if menu_row < 0:
            menu_row = 1
            cursor_y = cursor_y + 26 * 2
        if menu_col < 0:
            menu_col = 2
            cursor_x = cursor_x + 86 * 3
        if menu_row > 1:
            menu_row = 0
            cursor_y = cursor_y - 26 * 2
        if menu_col > 2:
            menu_col = 0
            cursor_x = cursor_x - 86 * 3

    if menu_type == 4:
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

    if menu_type == 3:
        #cursor movers

        if dpad == 3:
            cursor_y = cursor_y + 26
            menu_row = menu_row + 1

        if dpad == 2:
            cursor_y = cursor_y - 26
            menu_row = menu_row - 1

        #cursor correction
        if menu_row < 0:
            menu_row = 2
            cursor_y = cursor_y + 26 * 3

        if menu_row > 2:
            menu_row = 0
            cursor_y = cursor_y - 26 * 3


def menu_load(button):  #Button 0 is B. Button 1 is A
    #corrects menu_row and menu_col positions
    global menu_row, menu_col, menu_type
    global txt1_out, txt2_out, txt3_out
    global current_line, current_member
    global choices
    global cursor_x, cursor_y
    global main_function_is_callable
    global Apress_after_intro
    global cursor2_x
    global PARTY_MEMBER_EFFECTS
    global item_cursor_list

    Apress_after_intro = True

    if menu_type == 0 and button == 1 and current_line < 1:  #When no menu is current, the A button is pressed, and text has finished
        current_line = 0
        menu_type = 1
        cursor_x = 30
        cursor_y = 24
        MENU_OPEN.play()
        main_function_is_callable = False

    elif menu_type == 1 and button == 1:  #when on the main menu and the A button is pressed
        if menu_row == 0:
            if menu_col == 0:  #bash
                menu_type = 2
                MENU_OPEN.play()
            elif menu_col == 1:  #defend
                choices.append("D")
                menu_type = 1
                cursor_x = 30
                cursor_y = 24
                menu_col = 0
                menu_row = 0
                current_member = current_member + 1
                MENU_OPEN.play()
            elif menu_col == 2:  #Run
                menu_type = 0
                cursor_x = -16
                cursor_y = 24
                menu_col = 0
                menu_row = 0
                txt2_out = ""
                printB("You can't run. This is a Boss Battle", " ", " ")
        if menu_row == 1:
            if menu_col == 0:  #Item
                menu_type = 4
                cursor_y = 24
                menu_col = current_member - 1
                cursor2_x = item_cursor_list[menu_col]
                menu_row = 0
                MENU_OPEN.play()

            elif menu_col == 1:  #skills
                menu_type = 3
                cursor_x = 30
                cursor_y = 24
                menu_col = 0
                menu_row = 0
                MENU_OPEN.play()

            elif menu_col == 2:  #spare
                pass

    elif menu_type == 1 and button == 0:  #when on the main menu and the B button is pressed
        current_member -= 1
        MENU_CLOSE.play()
        if len(choices) > 0:
            choices.pop()
        if PARTY_MEMBER_EFFECTS[current_member - 1] == "Death":
            current_member -= 1

    elif menu_type == 2 and button == 1:  #when on the attack enemy selection and the A button is pressed
        choices.append("A")
        menu_type = 1
        cursor_x = 30
        cursor_y = 24
        menu_col = 0
        menu_row = 0
        current_member = current_member + 1
        MENU_OPEN.play()

    elif menu_type == 3 and button == 1:  #when on the skills menu and the A button is pressed
        if SKILLS[current_member][menu_row] == "---":
            MENU_INVALID.play()
        else:
            choices.append("S" + str(menu_row))
            current_member = current_member + 1
            print(current_member)
            menu_type = 1
            cursor_x = 30
            cursor_y = 24
            menu_row = 0
            MENU_OPEN.play()

    elif menu_type == 4 and button == 1:  #when on the items menu and the A button is pressed
        if Inventory_amount[menu_row] < 1:  #if an item has been used up
            MENU_INVALID.play()
        elif PARTY_MEMBER_EFFECTS[menu_col] == "Death" or Inventory[
                menu_row] == "---":  #if the person you're trying to select is dead, do nothing and play a sound
            if ITEM_ACTION[Inventory[menu_row]][3] == "Death":
                choices.append("I@" + str(menu_row) + "@" + str(menu_col))
                current_member = current_member + 1
                MENU_OPEN.play()
                menu_type = 1
                cursor_x = 30
                cursor_y = 24
                cursor2_x = -255
                menu_col = 0
                menu_row = 0
            else:
                MENU_INVALID.play()

        else:
            choices.append("I@" + str(menu_row) + "@" + str(menu_col))
            current_member = current_member + 1
            MENU_OPEN.play()
            menu_type = 1
            cursor_x = 30
            cursor_y = 24
            cursor2_x = -255
            menu_col = 0
            menu_row = 0

    elif menu_type > 1 and button == 0:  #when on any menu that isn't text scrolling or the main menu and the B button is pressed
        menu_type = 1
        cursor_x = 30
        cursor_y = 24
        cursor2_x = -255
        menu_col = 0
        menu_row = 0
        MENU_CLOSE.play()

    if len(
            choices
    ) > 2 and menu_type != -1:  #if everyone has chosen what they want to do
        global text_has_finished
        main_function_is_callable = True
        text_has_finished = False
        menu_type = -1
        cursor_x = -16
        current_member = 3
        txt1_out, txt2_out, txt3_out = "", "", ""

    print(choices)
    if current_member < 1:
        current_member = 1

    #print("menurow = " + str(menu_row))
    #print("menucol = " + str(menu_col))
    #print("menutype = " + str(menu_type) + "\n")


"""
menu_load is a big piece of code so this comment marks the start of a new function
"""


def debug(a):
    if a == 1:
        global BossHP, choices
        BossHP = 2000
        choices = []
    elif a == 2:
        global Warrior, Healer, Brute
        global WAR_MAXHP, HEA_MAXHP, BRU_MAXHP
        Warrior = WAR_MAXHP
        Healer = HEA_MAXHP
        Brute = BRU_MAXHP
    else:
        print("What you entered was invalid")


def winner():
    global winIsPlayed

    if winIsPlayed == False:
        BGM2.stop()
        BGM1.fadeout(600)
        WIN.play()
        winIsPlayed = True

    screen.blit(font5.render("YOU WON!", True, (100, 100, 210)), (60, 60))


printB("The Dog shaped like a Sock snuck up from ", "behind.", "Goodluck")
#the graphics updating code

def battle_loop(): #this used to be a while loop but now its a function so every global variable must be imported
    # Limit to 60 frames
    global main_function_is_callable, main_output, menu_type, PARTY_MEMBER_EFFECTS, Inventory, current_member, SKILLS, SKILLS_DESCRIPTION, member1_isActive
    global txt1_out, txt2_out, txt3_out
    
    divide_clock()

    screen.blit(background, (0, 0))  #background image

    if main_function_is_callable:
        main_output = main(choices)

    if main_output == 1:
        winner()

    else:
        if menu_type == 0 or menu_type == -1:
            screen.blit(txt_box, (0, 0))
        if menu_type > 0:
            screen.blit(battle_box, (0, 0))
            screen.blit(font.render(str(PARTY_MEMBER_NAMES[current_member - 1]), True, (255, 255, 255)), (32, -4))
        if menu_type == 1:
            txt1_out = "   Bash   Defend   Run"
            txt2_out = "   Item   Action   Spare"
            txt3_out = ""

        screen.blit(boss_img, (enemy0_x, enemy0_x))  #Boss Sprite

        screen.blit(status_box, (78, 398))  #party member 1's box
        screen.blit(status_box, (198, 398))  #party member 2's box
        screen.blit(status_box, (318, 398))  #party member 3's box

        if PARTY_MEMBER_EFFECTS[0] != "---":
            pygame.draw.rect(screen, STATUSBAR_EFFECTCOLORS[PARTY_MEMBER_EFFECTS[0]][0], pygame.Rect(86, 406, 96, 28))
        if PARTY_MEMBER_EFFECTS[1] != "---":
            pygame.draw.rect(screen, STATUSBAR_EFFECTCOLORS[PARTY_MEMBER_EFFECTS[1]][0], pygame.Rect(206, 406, 96, 28))
        if PARTY_MEMBER_EFFECTS[2] != "---":
            pygame.draw.rect(screen, STATUSBAR_EFFECTCOLORS[PARTY_MEMBER_EFFECTS[2]][0], pygame.Rect(326, 406, 96, 28))

        screen.blit(font.render(PARTY_MEMBER_NAMES[0], True, (255, 255, 255)), (90, 408))  #the names in their boxes
        screen.blit(font.render(PARTY_MEMBER_NAMES[1], True, (255, 255, 255)), (210, 408))
        screen.blit(font.render(PARTY_MEMBER_NAMES[2], True, (255, 255, 255)), (330, 408))

        screen.blit(font.render(str(Warrior), True, (0, 0, 0)), (138, 438))
        screen.blit(font.render(str(Healer), True, (0, 0, 0)), (258, 438))
        screen.blit(font.render(str(Brute), True, (0, 0, 0)), (378, 438))

        screen.blit(font.render("---", True, (0, 0, 0)), (138, 462))
        screen.blit(font.render(str(Healer_PP), True, (0, 0, 0)), (258, 462))
        screen.blit(font.render("---", True, (0, 0, 0)), (378, 462))

        if menu_type == 3:
            screen.blit(context_menu, (0, 0))
            screen.blit(font.render("Skills", True, (40, 250, 250)), (32, -4))
            txt1_out = "   " + SKILLS[current_member][
                0]  #add some whitespace before the string
            txt2_out = "   " + SKILLS[current_member][1]
            txt3_out = "   " + SKILLS[current_member][2]
            screen.blit(font2.render(SKILLS_DESCRIPTION[current_member][menu_row][0], True, (0, 230, 0)), (32, 250))
            screen.blit(font2.render(SKILLS_DESCRIPTION[current_member][menu_row][1], True, (0, 230, 0)), (32, 275))

        if menu_type == 4:
            screen.blit(context_menu, (0, 0))
            screen.blit(font.render("Items", True, (250, 250, 40)), (32, -4))

            txt1_out = "   " + Inventory[0] + " (x" + str(Inventory_amount[0]) + ")"  #add some whitespace before the string
            txt2_out = "   " + Inventory[1] + " (x" + str(Inventory_amount[1]) + ")"
            txt3_out = "   " + Inventory[2] + " (x" + str(Inventory_amount[2]) + ")"
            screen.blit(
                font.render(
                    "   " + Inventory[3] + " (x" + str(Inventory_amount[3]) +
                    ")", True, (255, 255, 255)), (25, 96))
            screen.blit(
                font.render(
                    "   " + Inventory[4] + " (x" + str(Inventory_amount[4]) + ")", True, (255, 255, 255)), (25, 122))
            screen.blit(
                font.render(
                    "   " + Inventory[5] + " (x" + str(Inventory_amount[5]) + ")", True, (255, 255, 255)), (25, 148))
            screen.blit(
                font.render(
                    "   " + Inventory[6] + " (x" + str(Inventory_amount[6]) + ")", True, (255, 255, 255)), (25, 174))
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(12, 256, 50, 50))
            screen.blit(ITEM_DESCRIPTION[Inventory[menu_row]][2], (22, 260))  #the item image
            screen.blit(green_overlay, (6, 250))  #the crt tv
            screen.blit(font2.render(ITEM_DESCRIPTION[Inventory[menu_row]][0], True, (0, 230, 0)), (80, 250))
            screen.blit(font2.render(ITEM_DESCRIPTION[Inventory[menu_row]][1], True, (0, 230, 0)), (80, 275))

        update_text()  #<<<<<<<<<< VERY IMPORTANT

        if menu_type == 2:
            enemy_attack_txt = font.render("To: " + enemy_name, True, (255, 255, 255))
            screen.blit(attack_txt_bg, (200, 58))
            screen.blit(enemy_attack_txt, (220, 78))  #BGLAYER1
            screen.blit(cur3, (enemy0_x, enemy0_y))

        screen.blit(cur, (cursor_x, cursor_y))
        screen.blit(cur2, (cursor2_x, 360))

        #updates display every frame
        pygame.display.flip()

        if PARTY_MEMBER_EFFECTS[current_member - 1] == "Death":
            choices.append("Ded")
            print(choices)
            current_member += 1
            if current_member > 3:
                current_member = 3
                choices.pop()

            #detectors for whether the first party member is selecting something (it will change music whenever they are active or inactive)
        if current_member == 1 and member1_isActive == False and Apress_after_intro == True:
            member1_isActive = True
            music_change()
            print("music change")
            print(current_member)

        if current_member != 1 and member1_isActive == True:
            member1_isActive = False
            music_change()
            print("music change")
            print(current_member)

        #checks if keydown event happened or not and prevents the window from crashing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #for right now it's just a boss engine with more to be added
            if event.type == pygame.KEYDOWN and input_allowed == True:
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
                    print(
                        "WARNING: THE WINDOW IS NO LONGER RUNNING \n\n ________DEBUG MENU_______ \n 1. Reset the Boss \n 2. Set Everyone's HP to MAX and restore PP\n"
                    )
                    debug(int(input("Pick your number:")))

#End of While Loop