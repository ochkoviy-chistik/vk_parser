from random import randint
import pygame
import sys

size = width, height = 800, 600
background_color = 255, 255, 255

class Color:
    def __init__(self):
        self.r = randint(0, 255)
        self.g = randint(0, 255)
        self.b = randint(0, 255)

    def get(self):
        return self.r, self.g, self.b

    def red(self):
        return 255, 0, 0

    def black(self):
        return 0, 0, 0

def is_intersect(circle1=None, circle2=None):
    #print(((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)**0.5)
    return True if ((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)**0.5 < circle1.radius+circle2.radius else False


class Circle:
    def __init__(self, screen, radius, change_color=True, speed=3):
        self.screen = screen
        self.radius = radius
        self.x, self.y = randint(self.radius, width - self.radius), randint(self.radius, height - self.radius - 200)
        self.div = speed
        self.change_color = change_color
        self.x_div = self.y_div = self.div
        self.color = Color()

    def mooving(self):
        pygame.draw.circle(self.screen, self.color.get() if self.change_color else (0, 0, 0), (self.x, self.y), self.radius)
        # pygame.draw.circle(self.screen, self.color.get(), (self.x + 45, self.y - 30), 15, 2)
        # pygame.draw.circle(self.screen, self.color.get(), (self.x - 45, self.y - 30), 15, 2)
        # pygame.draw.line(self.screen, self.color.get(), (self.x, self.y + 20), (self.x, self.y - 30), 2)
        # pygame.draw.arc(self.screen, self.color.get(), (self.x - 60, self.y + 10, 120, 50), math.pi, 2 * math.pi, 2)

        self.x += self.x_div
        self.y += self.y_div

        if self.x > width - self.radius:
            self.x_div = -1*self.div
            if self.change_color:
                self.color = Color()

        if self.x < self.radius:
            self.x_div = self.div
            if self.change_color:
                self.color = Color()

        if self.y > height - self.radius:
            self.y_div = -1*self.div
            if self.change_color:
                self.color = Color()

        if self.y < self.radius:
            self.y_div = self.div
            if self.change_color:
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
    game_stop = False
    ball = Circle(screen, 15, False, speed=4)

    circles = [Circle(screen, 25) for i in range(30)]

    x = y = 4

    rect_x = 0

    font = pygame.font.SysFont("Comic Sans MS", 54, True)
    text_game_over = font.render("Game over!", True, (0, 0, 0))

    while not game_over:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                game_over = True

        if game_stop:
            start_ticks = pygame.time.get_ticks()
            while True:
                seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                if seconds > 2:
                    break
            sys.exit()

        screen.fill(background_color)

        if keys[pygame.K_d] and rect_x < 300 and not game_stop:
            rect_x += 5
        if keys[pygame.K_a] and rect_x > -300 and not game_stop:
            rect_x -= 5

        ball.mooving()

        for circle in circles:
            circle.mooving()
            if is_intersect(circle, ball):
                circles.remove(circle)

        if ball.y > height - ball.radius:
            y = 0
            x = 0
            screen.blit(text_game_over, (width // 3, height // 2))
            game_stop = True

        platform = pygame.draw.rect(screen, (0, 0, 0), (width // 2 - 100 + rect_x, height - 50, 200, 10))

        if platform.collidepoint(ball.x, ball.y + ball.radius):
            ball.y_div *= -1

        pygame.time.wait(10)
        pygame.display.flip()
    sys.exit()


if __name__ == '__main__':
    main()
