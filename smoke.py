# -*- coding: utf-8 -*-

"""

pygame smoke effect by Rounak Bhowmik
https://www.youtube.com/watch?v=onecEtoqdtg


Some speed tests by NerdyTurkey using lru caching to memoise the scaling of the smoke image.
lru caching of function `scale` gives ~30% speed-up on my laptop* (Dell XPS13 9350),
achieving frame rates of ~170 fps.

* Processor	Intel(R) Core(TM) i7-6600U CPU @ 2.60GHz   2.81 GHz
Installed RAM	8.00 GB (7.84 GB usable)

"""

import pygame
import random
import sys
from functools import lru_cache

FPS = 1000  # set high to see what max frame rate achievable is
SCREEN_WIDTH, SCREEN_HEIGHT = 750, 650

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
IMAGE = pygame.image.load("smoke.png").convert_alpha()
IMAGE_W, IMAGE_H = IMAGE.get_size()


@lru_cache  # comment out this decorator to compare speed with/without caching
def scale(factor: int):
    """
    For efficient caching, have converted `factor` to an int in range 0-100.
    Then convert back to float inside function.
    """
    factor /= 100
    return pygame.transform.scale(IMAGE, (int(IMAGE_W * factor), int(IMAGE_H * factor)))


class SmokeParticle:
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2):
        self.x = x
        self.y = y
        self.scale_k = 0.1
        self.img = scale(int(100 * self.scale_k))
        self.alpha = 255
        self.alpha_rate = 3
        self.alive = True
        self.vx = 0
        self.vy = 4 + random.randint(7, 10) / 10
        self.k = 0.01 * random.random() * random.choice([-1, 1])

    def update(self):
        self.x += self.vx
        self.vx += self.k
        self.y -= self.vy
        self.vy *= 0.99
        self.scale_k += 0.005
        self.alpha -= self.alpha_rate
        if self.alpha < 0:
            self.alpha = 0
            self.alive = False
        self.alpha_rate -= 0.1
        if self.alpha_rate < 1.5:
            self.alpha_rate = 1.5
        self.img = scale(int(100 * self.scale_k))
        self.img.set_alpha(self.alpha)

    def draw(self):
        screen.blit(self.img, self.img.get_rect(center=(self.x, self.y)))


class Smoke:
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 150):
        self.x = x
        self.y = y
        self.particles = []
        self.frames = 0

    def update(self):
        self.particles = [particle for particle in self.particles if particle.alive]
        self.frames += 1
        if self.frames % 2 == 0:
            self.frames = 0
            self.particles.append(SmokeParticle(self.x, self.y))
        for particle in self.particles:
            particle.update()

    def draw(self):
        # print(len(self.particles))
        for particle in self.particles:
            particle.draw()


def main():
    smoke = Smoke()

    # used to make a running average of fps
    fps_sum = 0
    counter = 0
    display_fps = 0
    n = 200

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
        screen.fill((0, 0, 0))
        smoke.update()
        smoke.draw()
        pygame.display.update()
        clock.tick(FPS)
        fps_sum += clock.get_fps()
        counter += 1
        if counter == n:
            display_fps = int(fps_sum / n)
            counter = 0
            fps_sum = 0
        # displays n-pt average of fps
        pygame.display.set_caption(f"FPS = {display_fps}")


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
