import pygame
import math
from pygame import mixer 

class Bullet: 
    def __init__(self, position, speed, targetx, targety):
        self.bullet_img = pygame.image.load("assets/Bullet.png").convert_alpha()
        self.bullet_sound = mixer.Sound("audio/8-bit-machine-gun.aiff")
        self.bullet_sound.set_volume(0.1)
        self.pos_x, self.pos_y = position
        self.targetx = targetx
        self.targety = targety
        self.speed = speed
        self.angle = math.atan2(self.pos_y - self.targety, self.pos_x - self.targetx)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        print("Angle in degreese: ", int(self.angle*180/math.pi))


    
    def move(self, dt):
        self.pos_y += self.speed * dt
        
    
    def enemy_bullet_move(self, dt):
        self.pos_x = self.pos_x + int(self.dx) * dt
        self.pos_y = self.pos_y + int(self.dy) * dt
      
        

    def rect(self):
        return self.bullet_img.get_rect(center =(self.pos_x, self.pos_y))

    def play_sound(self):
        channel = pygame.mixer.Channel(2)
        channel.play(self.bullet_sound)

    
    def create_enemy_bullets(self, enemy_model, bullet_speed, targetx, targety):
        self.targetx = targetx
        self.targety = targety
        bullet_offset_1 = (54, 6)
        bullet_offset_2 = (4, 6)
        bullet_position_1 = [enemy_model.pos_x + bullet_offset_1[0], enemy_model.pos_y + bullet_offset_1[1]]
        bullet_position_2 = [enemy_model.pos_x + bullet_offset_2[0], enemy_model.pos_y + bullet_offset_2[1]]
        new_bullet_1 = Bullet(bullet_position_1, bullet_speed, self.targetx, self.targety)
        new_bullet_2 = Bullet(bullet_position_2, bullet_speed, self.targetx, self.targety)
        new_bullet_1.play_sound()
        new_bullet_2.play_sound()
        return [new_bullet_1, new_bullet_2]


    @staticmethod
    def create_bullets(player_model, bullet_speed):
        bullet_offset_1 = (54, 6)
        bullet_offset_2 = (4, 6)
        bullet_position_1 = [player_model.pos_x + bullet_offset_1[0], player_model.pos_y + bullet_offset_1[1]]
        bullet_position_2 = [player_model.pos_x + bullet_offset_2[0], player_model.pos_y + bullet_offset_2[1]]
        new_bullet_1 = Bullet(bullet_position_1, bullet_speed , 0, 0)
        new_bullet_2 = Bullet(bullet_position_2, bullet_speed, 0, 0)
        new_bullet_1.play_sound()
        new_bullet_2.play_sound()
        return [new_bullet_1, new_bullet_2]
    
    

    