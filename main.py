import pygame
from colors import *
from grid import *
import random
from blocks import *
import json

# call file json
with open("asset/game.json", mode="r") as file_json_game:
    Game_json = json.load(file_json_game)

pygame.init()

class Game:
    def __init__(self):
        # Create Screen
        self.screen_width = 700
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.clock = pygame.time.Clock()
        self.FPS = Game_json["FPS"]
        self.game_over = False
        self.count = 0
        self.count1 = 0
        self.score = 0
        self.count2 = 0
        self.max_score = Game_json["max_score"]
        self.game_start = True
        self.game_pause = False
        
        # Caption and icon
        self.caption = Game_json["caption"]
        pygame.display.set_caption(self.caption)
        icon = pygame.image.load("asset/icon.png")
        pygame.display.set_icon(icon)

        # call class
        self.color = colors()
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        
        # call function self
        self.current_block = self.get_random_block(False)
        self.next_block, self.style = self.get_random_block()

        # get sound
        self.clear_sound = pygame.mixer.Sound("asset/clear.MP3")
        self.rotate_sound = pygame.mixer.Sound("asset/rotate.MP3")
        self.put_sound = pygame.mixer.Sound("asset/put.MP3")
    
    def font(self, TEXT, x, y, size = 50, color = (255,255,255)):
        font1 = pygame.font.SysFont(None, size)
        font1 = font1.render(TEXT, False, color)
        self.screen.blit(font1,(x,y))
    
    def get_random_block(self, re = True):
        if len(self.blocks) == 0:
            self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        style_dic = {
            0:"L",
            1:"J",
            2:"I",
            3:"O",
            4:"S",
            5:"T",
            6:"Z"
        }

        style = style_dic[self.blocks.index(block)]

        self.blocks.remove(block)

        if re:
            return block, style
        
        else:
            return block
    
    def update_score(self, line):
        self.score += line * 2

    def draw_font(self):
        # Score
        self.font(TEXT = "SCORE",x = self.screen_width - 200, y = 50)
        pygame.draw.rect(self.screen, colors.dark_blue,(self.screen_width - 200,95, 115,65),border_radius=50)
        self.font(str(self.score),self.screen_width - 150 - ((len(str(self.score)) - 1) * 10), 110)
        
        # Max Score
        self.font("MAX SCORE",self.screen_width - 230, 200, 50)
        pygame.draw.rect(self.screen, colors.dark_blue,(self.screen_width - 200,245, 115,65),border_radius=50)
        self.font(str(self.max_score),self.screen_width - 150 - ((len(str(self.max_score)) - 1) * 10), 260)

        # Next Block
        self.font("NEXT BLOCK", self.screen_width - 250, y = 500)
        pygame.draw.rect(self.screen, colors.dark_blue,(self.screen_width - 240,545, 200,165),border_radius=50)
        
        if self.style == "I":
            self.next_block.draw(self.screen,self.screen_width - 315, 605)

        elif self.style == "O":
            self.next_block.draw(self.screen,self.screen_width - 315, 585)
        
        else:
            self.next_block.draw(self.screen,self.screen_width - 290, 565)
    
    def draw_rect_alpha(self, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self.screen.blit(shape_surf, rect)

    def screen_game_over(self):
        self.draw_rect_alpha((0,0,0,150),(0,0,self.screen_width, self.screen_height))
        self.font("GAME OVER", self.screen_width // 2 - 200, self.screen_height // 2 - 100, 100)
        self.font(f"SCORE: {self.score}", self.screen_width // 2 - 100, self.screen_height // 2, 50)
        self.font(f"MAX SCORE: {self.max_score}", self.screen_width // 2 - 100, self.screen_height // 2 + 50, 50)
        self.font("PRESS SPACE TO PLAY AGAIN", self.screen_width // 2 - 250, self.screen_height // 2 + 300, 50)

    def screen_game_start(self):
        self.draw_rect_alpha((0,0,0,150),(0,0,self.screen_width, self.screen_height))
        self.font("PRESS SPACE TO PLAY", self.screen_width // 2 - 290, self.screen_height // 2 - 50, 75)

    def screen_game_pause(self):
        self.draw_rect_alpha((0,0,0,150),(0,0,self.screen_width, self.screen_height))
        self.font("GAME PAUSE", self.screen_width // 2 - 210, self.screen_height // 2 - 100, 100)
        self.font("PRESS SPACE TO UNPAUSE", self.screen_width // 2 - 300, self.screen_height // 2 + 300, 65)
    
    def make_file_json(self):
        dic = {
        "FPS":self.FPS,
        "max_score":self.max_score,
        "caption":self.caption
        }

        dic = json.dumps(dic)

        with open("asset/game.json", mode="w") as file_json_game:
            file_json_game.write(dic)

    def draw(self):
        # compact
        screen, color = self.screen, self.color
        screen_width, screen_height = self.screen_width, self.screen_height
        grid = self.grid

        # draw screen
        screen.fill(color.light_blue)

        # pos
        x = screen_width // 2 - grid.get_width() // 2 - 100
        y = screen_height // 2 - grid.get_height() // 2

        # draw grid
        grid.draw(screen, x, y)
        
        # Draw Block
        self.current_block.draw(screen, x,y)

        # Draw font
        self.draw_font()

        # game over
        if self.game_over:
            self.screen_game_over()
        
        if self.game_pause:
            self.screen_game_pause()

        if self.game_start:
            self.screen_game_start()

        pygame.display.update()
    
    def move_left(self):
        self.current_block.move(-1, 0)
        if self.block_inside() == False or self.lock_fits() == False:
            self.current_block.move(1,0)

    def move_right(self):
        self.current_block.move(1,0)
        if self.block_inside() == False or self.lock_fits() == False:
            self.current_block.move(-1,0)
    
    def move_down(self):
        self.current_block.move(0,1)
        if self.block_inside() == False or self.lock_fits() == False:
            self.current_block.move(0,-1)
            self.lock_block()
            self.put_sound.play()
    
    def block_inside(self):
        tiles = self.current_block.get_cell_postion()
        for tile in tiles:
            if self.grid.is_inside(tile.col, tile.row) == False:
                return False
        
        return True

    def rotate(self):
        self.current_block.update_rotate()
        self.rotate_sound.play()
        if self.block_inside() == False or self.lock_fits() == False:
            self.current_block.undo_rotation()

    def lock_block(self):
        tiles = self.current_block.get_cell_postion()
        for postion in tiles:
            self.grid.grid_list[postion.col][postion.row] = self.current_block.id
        
        self.current_block = self.next_block
        self.next_block, self.style = self.get_random_block()
        row_clear = self.grid.clear_full_row(self.clear_sound)

        if row_clear > 0:
            self.clear_sound.play()
            self.update_score(row_clear)

        if self.lock_fits() == False:
            self.game_over = True

    def lock_fits(self):
        tiles = self.current_block.get_cell_postion()
        
        for tile in tiles:
            if self.grid.is_empty(tile.col, tile.row) == False:
                return False
        return True
    
    def speed_move(self,speed):
        limit_count = speed

        if self.count >= limit_count:
            self.count = 0
            return True
        
        self.count += 1

    def get_key(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.speed_move(5):
            self.move_left()
        
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.speed_move(5):
            self.move_right()
        
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.speed_move(1):
            self.move_down()
    
    def play_music(self):
        if self.count1 == 0:
            pygame.mixer.music.load("asset/music.mp3")
            pygame.mixer.music.play(-1)
            self.count1 += 1
        
        pygame.mixer.music.set_volume(0.3)
        
    def run(self):
        running = True

        limit_down = 25
        count_down = 0

        while running:
            self.play_music()
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.game_over == False:
                        self.rotate()
                    
                    if event.key == pygame.K_ESCAPE and (self.game_start == False and self.game_over == False):
                        self.game_pause = True
                    
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.game_over = False
                        self.grid.grid_list = [[0 for _ in range(self.grid.col)] for j in range(self.grid.row)]
                        self.count1 = 0
                        if self.max_score < self.score:
                            self.max_score = self.score
                        
                        self.score = 0

                    if event.key == pygame.K_SPACE and self.game_start:
                        self.game_start = False
                        self.count1 = 0
                    
                    if event.key == pygame.K_SPACE and self.game_pause:
                        self.game_pause = False
                        self.count1 = 0
                        self.count2 = 0
                    
                    if event.key == pygame.K_ESCAPE and (self.game_over or self.game_start):
                        running = False
                    
                    if event.key == pygame.K_ESCAPE and self.game_pause and self.count2 > 1:
                        running = False
            
            if self.game_over == False and self.game_start == False and self.game_pause == False:

                if count_down >= limit_down:
                    self.move_down()
                    count_down = 0
                
                self.get_key()
            
            count_down += 1
            self.draw()

            if self.game_pause:
                self.count2 += 1

            if self.game_over or self.game_pause or self.game_start:
                pygame.mixer.music.stop()
                self.make_file_json()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()