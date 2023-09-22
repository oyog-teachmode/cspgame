import pygame
from tiles import Tile, Player
from settings import tile_size, screen_width

#the level updater

class Level:
    def __init__(self,level_data,surface):

        #level setup
        self.surface = surface
        self.setup_level(level_data)

        self.ow_scroll = 0 

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if col == "X":
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if col == "P":
                    player_sprite = Player((x,y))
                    self.tiles.add(tile)
                    self.player.add(player_sprite)

    def run(self):

        #level tiles
        self.tiles.update(self.ow_scroll)
        self.tiles.draw(self.surface)
        self.scroll_x()

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.surface)
        

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 3 and direction_x < 0:
            self.ow_scroll = 4
            player.speed_x = 0
        elif player_x > screen_width - (screen_width / 3) and direction_x > 0:
            self.ow_scroll = -4
            player.speed_x = 0
        else:
            self.ow_scroll = 0
            player.speed_x = 4

    def horizontal_movement_collision(self):
        player = self.player.sprite

        player.rect.x += player.direction.x * player.speed_x

        #collision detection
        for sprite in self.tiles.sprites(): #check for all tiles the player can possibly collide with
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: #make a blind reckoning and figure the player is colliding on the left
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:  #The player is colliding on the right
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite


        player.rect.y += player.direction.y * player.speed_y

        #collision detection
        for sprite in self.tiles.sprites(): #check for all tiles the player can possibly collide with
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: #figure the player is colliding underneath
                    player.rect.bottom = sprite.rect.top
                elif player.direction.y < 0:  #figure the player is colliding above
                    player.rect.top = sprite.rect.bottom

