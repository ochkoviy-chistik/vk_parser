from random import randint
import pygame
import sys
import math

size = width, height = 800, 600
background_color = 0, 0, 0


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
    # print(((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)**0.5)
    return True if ((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)**0.5 < circle1.radius+circle2.radius\
        else False


class Smile:
    radius = 50//2

    def __init__(self, screen, speed=2):
        self.screen = screen
        self.x, self.y = randint(self.radius, width - self.radius), randint(self.radius, height - self.radius)
        self.div = speed
        self.x_div = self.y_div = self.div
        self.color = Color()

    def moving(self, cords=None):
        if cords is not None:
            self.x_div = cords[0] / width * self.div
            self.y_div = cords[1] / height * self.div

            # if math.cos(angle)

        pygame.draw.circle(self.screen, self.color.get(), (self.x, self.y), self.radius)

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
        # circle2.x += 10
        # circle1.y += 10


def get_length(player, circle):
    return player.x - circle.x, player.y - circle.y


class Player (Smile):
    def __init__(self, screen):
        super().__init__(screen)
        self.radius = 15
        pygame.draw.circle(self.screen, self.color.get(), (self.x, self.y), self.radius)

    def moving(self, x=0, y=0):
        self.x += x
        self.y += y
        pygame.draw.circle(self.screen, self.color.get(), (self.x, self.y), self.radius)

    def get_cords(self):
        return self.x, self.y

    def dash(self, x=0, y=0):
        if self.x + x > width-self.radius:
            self.x = width-self.radius
        elif self.x + x < 0:
            self.x = self.radius
        else:
            self.x += x

        if self.y + y > height-self.radius:
            self.y = height-self.radius
        elif self.y + y < self.radius:
            self.y = self.radius
        else:
            self.y += y


class Life:
    def __init__(self, screen, x, y):
        self.screen = screen
        self. x = x
        self.y = y
        self.color = Color().red()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)

    def lose(self):
        self.color = Color().black()


class Stamina:
    def __init__(self, screen, x, y, size):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size

    def moving(self, time):
        pygame.draw.arc(self.screen, (0, 255, 0), (self.x, self.y, self.size[0], self.size[1]), 0, time, 100)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    game_over = False
    smiles = []
    n = 5
    for i in range(n):
        smiles.append(Smile(screen, randint(3, 4)))

    lifes = [
        Life(screen, 775, 25),
        Life(screen, 775, 50),
        Life(screen, 775, 75)
    ]

    count = 2
    flag = False
    player = Player(screen)

    time = 1500
    pygame.time.set_timer(pygame.USEREVENT, 1)
    
    timer = 0
    stamina = Stamina(screen, 770, 575, [20, 20])

    while not game_over:
        dash_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and timer >= time:
                    dash_flag = True
                    timer = 0
            if event.type == pygame.USEREVENT:
                timer += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and player.get_cords()[0] < 800-player.radius:
            player.moving(x=4)
            if dash_flag:
                player.dash(x=200)
                # dash_flag = False
        if keys[pygame.K_a] and player.get_cords()[0] > 0+player.radius:
            player.moving(x=-4)
            if dash_flag:
                player.dash(x=-200)
                # dash_flag = False
        if keys[pygame.K_s] and player.get_cords()[1] < 600-player.radius:
            player.moving(y=4)
            if dash_flag:
                player.dash(y=200)
                # dash_flag = False
        if keys[pygame.K_w] and player.get_cords()[1] > 0+player.radius:
            player.moving(y=-4)
            if dash_flag:
                player.dash(y=-200)
                # dash_flag = False
        dash_flag = False

        screen.fill(background_color)

        if timer < time:
            stamina.moving(timer / time * 2 * math.pi)
        if timer >= time:
            stamina.moving(2 * math.pi)

        for smile in smiles:
            smile.moving(get_length(player, smile))

        player.moving()
        # print(player.get_cords())

        for life in lifes:
            life.draw()

        for i in range(len(smiles)):
            for j in range(i+1, len(smiles)):
                if is_intersect(smiles[i], smiles[j]):
                    smiles.remove(smiles[i])
                    smiles.append(Smile(screen, randint(3, 4)))

        for smile in smiles:
            if is_intersect(smile, player) and not flag:
                lifes[count].lose()
                count -= 1
                flag = True
                start_ticks = pygame.time.get_ticks()

        if flag:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000

            if seconds > 1:
                flag = False

        if count <= -1:
            sys.exit()

        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
