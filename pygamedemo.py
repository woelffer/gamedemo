import Player
import pygame


player_model = Player.Player()

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


while running:
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0
    screen.fill((0,0,0))
    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))
    for event in pygame.event.get():

        key = pygame.key.get_pressed()
        
        if key[pygame.K_a] == True:
            player_model.movement('a', dt)

        if key[pygame.K_d] == True:
            player_model.movement('d', dt)

        if key[pygame.K_w] == True:
            player_model.movement('w', dt)

        if key[pygame.K_s] == True:
            player_model.movement('s', dt)
            
        if event.type == pygame.QUIT:
            running = False
        

    
    pygame.display.flip()

    clock.tick(120)

pygame.quit()
