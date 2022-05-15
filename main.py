import pygame as py
import math
import random


class Game:
    def __init__(self, x, y):
        py.init()
        self.x = x
        self.y = y
        self.screen = py.display.set_mode((self.x, self.y))
        py.display.set_caption("Space Invaders")
        self.running = True
        self.background_img = py.image.load("spr_space_himmel.png")
        self.spaceship_character = Spaceship(self, 336, 545)
        self.clock = py.time.Clock()
        self.aliens_list = []
        self.score = 0

        # Random spawing points for the aliens
        for i in range(12):
            self.aliens_list.append(Enemy(self, random.randint(0, 736), random.randint(30, 130)))

        while self.running is True:
            self.clock.tick(60)
            self.screen.blit(self.background_img, (0, 0))
            self.spaceship_character.update()

            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False

                # Press Key
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RIGHT:
                        self.spaceship_character.move(10)
                    if event.key == py.K_LEFT:
                        self.spaceship_character.move(-10)
                    if event.key == py.K_SPACE:
                        self.spaceship_character.fire_bullet()

                # Release Key
                if event.type == py.KEYUP:
                    if event.key == py.K_RIGHT:
                        self.spaceship_character.move(-10)
                    if event.key == py.K_LEFT:
                        self.spaceship_character.move(10)

            # Creating/Removing of Bullets
            if len(self.spaceship_character.bullets_list) > 0:
                for bullet in self.spaceship_character.bullets_list:
                    if bullet.is_fired is True:
                        bullet.update()
                    else:
                        self.spaceship_character.bullets_list.remove(bullet)

            # Drawing the updated positions of the aliens while they move + collision check with bullets
            for enemy in self.aliens_list:
                enemy.update()
                enemy.check_collision()

                if enemy.y > 500:
                    for i in self.aliens_list:
                        i.y = 1000
                    self.game_over_screen()
                    break

            self.score_screen()
            py.display.update()

    def game_over_screen(self):
        go_font = py.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(go_text, (200, 250))

    def score_screen(self):
        score_font = py.font.Font("freesansbold.ttf", 24)
        score_text = score_font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (8, 8))


class Spaceship:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.spaceship_img = py.image.load("spr_spaceship.png")
        self.movement_speed = 0
        self.bullets_list = []

    def fire_bullet(self):
        self.bullets_list.append(Bullet(self.game, self.x, self.y))
        self.bullets_list[len(self.bullets_list) - 1].fire()

    def move(self, speed):
        self.movement_speed += speed

    def update(self):
        self.x += self.movement_speed
        self.game.screen.blit(self.spaceship_img, (self.x, self.y))
        # Movement limitation
        if self.x < 0:
            self.x = 0
        if self.x > 736:
            self.x = 736


class Bullet:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.is_fired = False
        self.bullet_img = py.image.load("spr_patrone.png")
        self.bullet_speed = 10

    def fire(self):
        self.is_fired = True

    def update(self):
        self.y -= self.bullet_speed
        if self.y <= 0:
            self.is_fired = False
        self.game.screen.blit(self.bullet_img, (self.x, self.y))


class Enemy:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.speed_x = 5
        self.speed_y = 60
        self.alien_img = py.image.load("spr_space_enemy.png")

    def check_collision(self):
        for bullet in self.game.spaceship_character.bullets_list:
            distance = math.sqrt(math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2))
            if distance < 35:
                bullet.is_fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)

    def update(self):
        self.x += self.speed_x
        if self.x >= 736 or self.x <= 0:
            self.y += self.speed_y
            self.speed_x *= -1
        self.game.screen.blit(self.alien_img, (self.x, self.y))


if __name__ == "__main__":
    game = Game(800, 600)
