import math
import pygame, sys
from random import randint

class Color:
    def __init__(self):
        self.r = randint(0, 255)
        self.g = randint(0, 255)
        self.b = randint(0, 255)

    def get(self):
        return (self.r, self.g, self.b)

size = width, height = 1200, 800
background_color = 0, 0, 0


def is_intersect(circle1=None, circle2=None):
    #print(((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)**0.5)
    return True if ((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)**0.5 < 2*Smile.radius else False


class Smile:
    radius = 50
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y = randint(self.radius, width - self.radius), randint(self.radius, height - self.radius)
        self.div = 5
        self.x_div = self.y_div = self.div
        self.color = Color()

    def mooving(self):
        pygame.draw.circle(self.screen, self.color.get(), (self.x, self.y), self.radius, 2)
        # pygame.draw.circle(self.screen, self.color.get(), (self.x + 45, self.y - 30), 15, 2)
        # pygame.draw.circle(self.screen, self.color.get(), (self.x - 45, self.y - 30), 15, 2)
        # pygame.draw.line(self.screen, self.color.get(), (self.x, self.y + 20), (self.x, self.y - 30), 2)
        # pygame.draw.arc(self.screen, self.color.get(), (self.x - 60, self.y + 10, 120, 50), math.pi, 2 * math.pi, 2)

        self.x += self.x_div
        self.y += self.y_div

        if self.x > width - self.radius:
            self.x_div = -1*self.div
            self.color = Color()

        if self.x < self.radius:
            self.x_div = self.div
            self.color = Color()

        if self.y > height - self.radius:
            self.y_div = -1*self.div
            self.color = Color()

        if self.y < self.radius:
            self.y_div = self.div
            self.color = Color()

def intersection(circle1=None, circle2=None):
    circle1.x_div, circle2.x_div = circle2.x_div, circle1.x_div
    circle1.y_div, circle2.y_div = circle2.y_div, circle1.y_div

    if circle1.x_div == circle2.x_div and circle1.y_div == circle2.y_div:
        circle1.x += 25
        #circle2.x += 10
        #circle1.y += 10



def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    game_over = False
    smiles = []
    n = 16
    for i in range(n):
        smiles.append(Smile(screen))

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        screen.fill(background_color)

        for smile in smiles:
            smile.mooving()

        for i in range(len(smiles)):
            for j in range(i+1, len(smiles)):
                if is_intersect(smiles[i], smiles[j]):
                    intersection(smiles[i], smiles[j])

        # pygame.draw.rect(screen, (0, 0, 0), (70, 70, 170, 100), 5)
        # pygame.draw.circle(screen, (0, 255, 0), (width//2, height//2), 100, 5)
        # pygame.draw.ellipse(screen, (0, 0, 255), (70, 70, 170, 100), 5)
        # pygame.draw.arc(screen, (0, 0, 255), (70, 70, 170, 100), 0, math.radians(270), 5)
        # pygame.draw.line(screen, (0,0,0), (70, 70), (270, 200), 1)

        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()

if __name__ == '__main__':
    main()