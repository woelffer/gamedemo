import Player
import Bullet
import pygame

#Initialize Player 
player_model = Player.Player()
bullet_speed = -500
bullets = []


pygame.init()


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


while running:
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    #Clear Screen
    screen.fill((0,0,0))

    #Draw Player
    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))
    
    #Update and draw bullets
    for bullet in bullets:
        bullet.move(dt)
        screen.blit(bullet.bullet_img, (bullet.pos_x, bullet.pos_y))            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        key = pygame.key.get_pressed()
        
        if key[pygame.K_a]:
            player_model.movement('a', dt)

        if key[pygame.K_d]:
            player_model.movement('d', dt)

        if key[pygame.K_w]:
            player_model.movement('w', dt)

        if key[pygame.K_s]:
            player_model.movement('s', dt)
        
        if key[pygame.K_SPACE]:
            # Calculate the bullet positions relative to the player
            bullet_offset_1 = (98, 5)
            bullet_offset_2 = (22, 6)
            bullet_position_1 = [player_model.pos_x + bullet_offset_1[0], player_model.pos_y + bullet_offset_1[1]]
            bullet_position_2 = [player_model.pos_x + bullet_offset_2[0], player_model.pos_y + bullet_offset_2[1]]
            # Create new bullets and add them to the list
            new_bullet_1 = Bullet.Bullet(bullet_position_1, bullet_speed)
            new_bullet_2 = Bullet.Bullet(bullet_position_2, bullet_speed)
            bullets.append(new_bullet_1)
            bullets.append(new_bullet_2)
            if event.type == pygame.QUIT:
                running = False
            
        bullets = [bullet for bullet in bullets if bullet.pos_y >0]
    
    pygame.display.flip()

    clock.tick(120)

pygame.quit()
