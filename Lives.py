import pygame 

class Lives:
    def __init__(self):
        self.lives_img = pygame.image.load("assets/Spaceship.png")
        self.lives_img = pygame.transform.scale(self.lives_img, (50, 50))
        self.lives = 3  
    
    #def check_lives(lives):
        #write logic 