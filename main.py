import math
import pygame, sys
from random import randint

size = width, height = 800, 600
background_color = 255, 255, 255

def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    game_over = False
    ball = pygame.image.load('ball.png')
    ball_rect = ball.get_rect()

    x = y = 4

    rect_x = 0
    ball_rect.x = randint(0, 800-100)
    ball_rect.y = randint(0, 600-100)

    while not game_over:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                game_over = True

        screen.fill(background_color)

        if keys[pygame.K_d] and rect_x < 300:
            rect_x += 5
        if keys[pygame.K_a] and rect_x > -300:
            rect_x -= 5


        ball_rect.x += x
        ball_rect.y += y

        if ball_rect.x > width-100:
            x *= -1
        if ball_rect.x < 0:
            x *= -1
        if ball_rect.y > height-100:
            y *= -1
        if ball_rect.y < 0:
            y *= -1

        platform = pygame.draw.rect(screen, (0, 0, 0), (width // 2 - 100 + rect_x, height - 50, 200, 10))

        if platform.colliderect(ball_rect):
            # x *= -1
            y *= -1


        screen.blit(ball, ball_rect)


        pygame.time.wait(10)
        pygame.display.flip()
    sys.exit()

if __name__ == '__main__':
    main()

