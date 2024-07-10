import pygame 
import math 

class Enemy:
    def __init__(self, posx, posy):
        self.enemy_img = pygame.image.load("assets/Enemy_Spaceship.png")
        self.dmg_img = pygame.image.load("assets/Inv_Spaceship.png")
        self.pos_x, self.pos_y = posx, posy
        self.speed = 100
        self.health = 20
        self.enemy_img = pygame.transform.rotate(self.enemy_img, 180)
        self.damaged = False
        self.damaged_time = 0 # Time when the enemy was last damaged

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
        if self.damaged:
            screen.blit(self.dmg_img, (self.pos_x, self.pos_y))
        else:
            screen.blit(self.enemy_img, (self.pos_x, self.pos_y))
    
    def draw_dmg(self, screen):
    # Temporarily set the damaged flag and draw the damaged image
        self.damaged = True
        self.draw(screen)
        self.damaged = False

    def take_dmg(self):
        self.health -= 1
        self.damaged = True
        # Optionally, set a timer to switch back to normal image after some time
        self.damaged_time = pygame.time.get_ticks() # Get current time

    def update(self):
        #Check if the damged stae should be reset
        if self.damaged and pygame.time.get_ticks() - self.damaged_time > 300: #500 ms
            self.damaged = False
    
    def is_alive(self):
        return self.health > 0
    
    def rect(self):
        return self.enemy_img.get_rect(topleft = (self.pos_x, self.pos_y))