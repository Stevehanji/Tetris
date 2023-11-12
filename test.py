import pygame

pygame.init()
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

screen = pygame.display.set_mode((800,600))

running = True
while running:
    screen.fill("white")

    draw_rect_alpha(screen, (0,0,0,40), (0,0, 800,600))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()