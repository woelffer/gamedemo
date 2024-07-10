import pygame 
import math 

class Enemy:
    def __init__(self):
        self.enemy_img = pygame.image.load("assets/Enemy_Spaceship.png")
        self.pos_x, self.pos_y = 600, 0
        self.speed = 100
        self.enemy_img = pygame.transform.rotate(self.enemy_img, 180)

    def move_towards_player(self, player, dt):
        #Find direction vector (dx, dy) between enemy and player
        dx = player.pos_x - self.pos_x
        dy = player.pos_y - self.pos_y

        #Calculate distance
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            #Normalize the direction vector
            dx /= distance
            dy /= distance
        
        #Update the enemy position
        self.pos_x += dx * self.speed * dt
        self.pos_y += dy * self.speed * dt
    
    def draw(self, screen):
        screen.blit(self.enemy_img, (self.pos_x, self.pos_y))