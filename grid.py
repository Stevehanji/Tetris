import pygame
from colors import *

class Grid:
    def __init__(self):
        self.row = 20
        self.col = 10
        self.size = 35
        self.color = colors().color_list()
        self.grid_list = [[0 for _ in range(self.col)] for j in range(self.row)]
    
    def get_width(self):
        return self.col * self.size

    def get_height(self):
        return self.row * self.size

    def print_list_grid(self):
        for i in self.grid_list:
            for j in i:
                print(j, end = " ")
            
            print()
    
    def is_inside(self,row,col):
        if row >= 0 and row < self.row and \
        col >= 0 and col < self.col:
            return True
        
        return False

    def is_empty(self, col, row):
        if self.grid_list[col][row] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        for col in range(self.col):
            if self.grid_list[row][col] == 0:
                return False
        return True
    
    def clear_row(self, row):
        for col in range(self.col):
            self.grid_list[row][col] = 0
    
    def move_row_down(self, row, num_rows):
        for colum in range(self.col):
            self.grid_list[row + num_rows][colum] = self.grid_list[row][colum]
            self.grid_list[row][colum] = 0

    def clear_full_row(self,sound):
        completed = 0
        for row in range(self.row - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def draw(self, screen, dicx = 0, dicy = 0):
        for row in range(self.row):
            for col in range(self.col):
                rect = pygame.Rect(dicx + col * self.size,dicy + row * self.size, self.size - 1, self.size - 1)
                pygame.draw.rect(screen,self.color[self.grid_list[row][col]], rect)