import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile




class Level():
    def __init__(self, level_data, surface):
        #general setup
        self.display_surface = surface
        self.world_shift = 0                    #for scrolling
        self.obstacle_list = []

        #terrain setup      #für jedes tileset
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")        #terrain = welches tileset?


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    print(val)
                    if val != "0":
                        self.obstacle_list.append(val)
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                       terrain_tile_list = import_cut_graphics("jumper/graphics/assets/Pale Moon/Image Sheets/base_grass_tiles.png") #pfad vom tilesheet.png)
                       tile_surface = terrain_tile_list[int(val)]
                       sprite = StaticTile(tile_size, x, y, tile_surface)
                       sprite_group.add(sprite)
        ol = list(set(self.obstacle_list))
        print(ol)
               
        return sprite_group


    def run(self):
        #run the entire game/level
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

    def horizontal_movement_collision(self):
        pass
