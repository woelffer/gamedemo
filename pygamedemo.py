import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PygameDemo')

player = pygame.Rect((300, 250, 50, 50))
groundRect = pygame.Rect(0, 500, 800, 100)
clock = pygame.time.Clock()

x, y = 300, 400
xVelocity, yVelocity = 0, 0
red = (255, 0, 0)
blue = (0, 0, 255)

run = True
while run:
    clock.tick(30)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, red, player)
    pygame.draw.rect(screen, blue, groundRect)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-10, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(10, 0)
    elif key[pygame.K_w] == True:
        player.move_ip(0, -10)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()