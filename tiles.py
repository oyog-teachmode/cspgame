import pygame
from os import walk


def import_folder(path):
    surface_list = []

    for _,__,img_file in walk(path):
        for image in img_file:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_scroll):
        self.rect.x += x_scroll

#player
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)


        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed_x = 4
        self.speed_y = 4
        

    def get_input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0
        #Diagonal direction detecting
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] or keys[pygame.K_d] and keys[pygame.K_w]: #↗
            self.direction.x = 1
            self.direction.y = -1
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] or keys[pygame.K_d] and keys[pygame.K_s]: #↘
            self.direction.x = 1
            self.direction.y = 1
        
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP] or keys[pygame.K_a] and keys[pygame.K_w]: #↖
            self.direction.x = -1
            self.direction.y = -1
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN] or keys[pygame.K_a] and keys[pygame.K_s]: #↙
            self.direction.x = -1
            self.direction.y = 1

        #UDLR direction checking
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1

    def update(self):
        self.get_input()

    def import_character_assets(self):
        character_path = "./img/GFX/player/"
        self.animations = {"idle":[], "walkUp":[], "walkDown":[], "walkRight":[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)