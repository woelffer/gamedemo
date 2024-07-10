import Player
import Bullet
import pygame
import Star
import random
import assets 

#Initialize Player 
player_model = Player.Player()
bullet_speed = -500
bullets = []

#Screen Dimensions
screen_width, screen_height = 1280, 720

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Initialize stars
star_img = pygame.image.load("assets/Star.png")  # Load the star image

num_stars = 35
stars = [Star.Star(star_img, screen_width, screen_height) for _ in range(num_stars)]

while running:
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    #Clear Screen
    screen.fill((0,0,0))

    # Update and draw stars
    for star in stars:
        star.move(dt)
        star.draw(screen)

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
        moved = False

        if key[pygame.K_a]:
            player_model.movement('a', dt)
            for star in stars:
                star.move_horizontal(player_model.vel_x * dt)
            moved = True
        if key[pygame.K_d]:
            player_model.movement('d', dt)
            for star in stars:
                star.move_horizontal(-player_model.vel_x * dt)
            moved = True
        if key[pygame.K_w]:
            player_model.movement('w', dt)
            # Move stars down as the plane moves up
            for star in stars:
                star.move_vertical(player_model.vel_y * dt)
            moved = True

        if key[pygame.K_s]:
            player_model.movement('s', dt)
            # Move stars up as the plane moves down
            for star in stars:
                star.move_vertical(-player_model.vel_y * dt)
            moved = True

        if key[pygame.K_SPACE]:
            # Calculate the bullet positions relative to the player
            bullet_offset_1 = (54, 6)
            bullet_offset_2 = (4, 6)
            bullet_position_1 = [player_model.pos_x + bullet_offset_1[0], player_model.pos_y + bullet_offset_1[1]]
            bullet_position_2 = [player_model.pos_x + bullet_offset_2[0], player_model.pos_y + bullet_offset_2[1]]
            # Create new bullets and add them to the list
            new_bullet_1 = Bullet.Bullet(bullet_position_1, bullet_speed)
            new_bullet_2 = Bullet.Bullet(bullet_position_2, bullet_speed)
            bullets.append(new_bullet_1)
            bullets.append(new_bullet_2)
            if event.type == pygame.QUIT:
                running = False

        for star in stars:
            star.draw(screen)    

        bullets = [bullet for bullet in bullets if bullet.pos_y >0]
    
    pygame.display.flip()

    clock.tick(120)

pygame.quit()
