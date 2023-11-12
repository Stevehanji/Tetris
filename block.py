from colors import *
import pygame
from postion import *

class Block:
    def __init__(self, id):
        self.id = id
        self.size = 35
        self.color = colors().color_list()
        self.cells = {}
        self.rotate = 0
        self.colum_offset = 0
        self.row_offset = 0

    def update_rotate(self):
        self.rotate += 1
        if self.rotate == len(self.cells):
            self.rotate = 0
    
    def undo_rotation(self):
        self.rotate -= 1

        if self.rotate == -1:
            self.rotate = len(self.cells) - 1
    
    def get_cell_postion(self):
        tiles = self.cells[self.rotate]
        moved_tiles = []
        for postion in tiles:
            postion = Position(postion.row + self.row_offset, postion.col + self.colum_offset)
            moved_tiles.append(postion)
        return moved_tiles

    def move(self,rows, cols):
        self.row_offset += rows
        self.colum_offset += cols

    def draw(self,screen, dicx = 0, dicy = 0):
        tiles = self.get_cell_postion()

        for tile in tiles:
            rect = pygame.Rect(dicx + tile.row * self.size,dicy + tile.col * self.size,
                               self.size - 1, self.size - 1)
            pygame.draw.rect(screen, self.color[self.id], rect)