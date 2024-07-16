import pygame 

class Lives:
    def __init__(self):
        self.lives_img = pygame.image.load("assets/Spaceship.png")
        self.lives_img = pygame.transform.scale(self.lives_img, (50, 50))
        self.remaining_lives = 3  
        self.positions = [(0, 670), (50, 670), (100, 670)]  # Example positions for lives display
    

    def reset(self):
        self.remaining_lives = 3  # Reset remaining lives to initial value
        
    def draw(self, screen):
        for i in range(self.remaining_lives):
            pos_x, pos_y = self.positions[i]
            screen.blit(self.lives_img, (pos_x, pos_y))
    
    def remove_life(self):
        if self.remaining_lives > 0:
            self.remaining_lives -= 1

    def add_life(self):
        if self.remaining_lives < len(self.positions):
            self.remaining_lives += 1