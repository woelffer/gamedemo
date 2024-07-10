import Player
import Bullet
import pygame
import Star
import Enemy
import Lives
import random


#Initialize Player 
player_model = Player.Player()
enemies = [Enemy.Enemy(0, 0), Enemy.Enemy(400, 0), Enemy.Enemy(600, 0)]  # List of enemies
lives_model = Lives.Lives()

#Bullet initialize
bullet_speed = -500
bullets = []

#Can ADJUST THIS WHEN WE Introduce levels and powerups
BULLET_COOLDOWN = 0.05


# Track the time since the last bullet was fired
time_since_last_shot = 0

#Screen Dimensions
screen_width, screen_height = 1280, 720
pygame.display.set_caption("Galaga Clone")

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Initialize stars
star_img = pygame.image.load("assets/Star.png")  # Load the star image
num_stars = 50
stars = [Star.Star(star_img, screen_width, screen_height) for _ in range(num_stars)]

while running:
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    time_since_last_shot += dt  # Update the cooldown timer

    #Clear Screen
    screen.fill((0,0,0))

    # Update and draw stars
    for star in stars:
        star.move(dt)
        star.draw(screen)

    #Draw Players
    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))


    #screen.blit(enemy_model.enemy_img, (enemy_model.pos_x, enemy_model.pos_y))

    #Draw Player lives
    lives_model.draw(screen)


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
            player_model.movement('a', dt, screen_width, screen_height)

    if key[pygame.K_d]:
            player_model.movement('d', dt, screen_width, screen_height)

    if key[pygame.K_w]:
            player_model.movement('w', dt, screen_width, screen_height)


    if key[pygame.K_s]:
            player_model.movement('s', dt, screen_width, screen_height)


    if key[pygame.K_SPACE] and time_since_last_shot >= BULLET_COOLDOWN:
            
 

            # Reset the cooldown timer
            time_since_last_shot = 0

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

    #Draw stars
    for star in stars:
       star.draw(screen) 

    # Move bullets
    for bullet in bullets:
        bullet.move(dt)

    # Check for bullet collisions with enemies
    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect().colliderect(enemy.rect()):
                enemy.take_dmg()
                bullets.remove(bullet)  # Remove bullet after collision
                if not enemy.is_alive():
                    enemies.remove(enemy)  # Remove enemy if health is zero
                break  # Exit the inner loop to avoid modifying the list during iteration           

    # Move and update enemies
    for enemy in enemies:
        enemy.move_towards_player(player_model, dt)
        enemy.update()

    # Draw game objects
    for enemy in enemies:
        enemy.draw(screen)

    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))
    
    lives_model.draw(screen)
    
    for bullet in bullets:
        screen.blit(bullet.bullet_img, (bullet.pos_x, bullet.pos_y))             


    
    pygame.display.flip()
    
    clock.tick(0)

pygame.quit()
