import pygame
import math


class Gun:
    def __init__(self, context):
        self.context = context

    def draw_gun(self):
        mouse_pos = pygame.mouse.get_pos()
        gun_point = (self.context.WIDTH / 2, self.context.HEIGHT - 200)
        lasers = ['red', 'purple', 'green']
        clicks = pygame.mouse.get_pressed()

        if mouse_pos[0] != gun_point[0]:
            slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
        else:
            slope = -100000

        angle = math.atan(slope)
        rotation = math.degrees(angle)

        if mouse_pos[0] < self.context.WIDTH / 2:
            gun = pygame.transform.flip(self.context.guns[self.context.level - 1], True, False)
            if mouse_pos[1] < 600:
                self.context.screen.blit(pygame.transform.rotate(gun, 90 - rotation),
                                         (self.context.WIDTH / 2 - 90, self.context.HEIGHT - 250))
                if clicks[0]:
                    pygame.draw.circle(self.context.screen, lasers[self.context.level - 1], mouse_pos, 5)
        else:
            gun = self.context.guns[self.context.level - 1]
            if mouse_pos[1] < 600:
                self.context.screen.blit(pygame.transform.rotate(gun, 270 - rotation),
                                         (self.context.WIDTH / 2 - 30, self.context.HEIGHT - 250))
                if clicks[0]:
                    pygame.draw.circle(self.context.screen, lasers[self.context.level - 1], mouse_pos, 5)

    def check_shot(self, targets, coords):
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(targets)):
            for j in range(len(targets[i])):
                if targets[i][j].collidepoint(mouse_pos):
                    coords[i].pop(j)
                    self.context.points += 10 + 10 * (i ** 2)
                    if self.context.level == 1:
                        self.context.bird_sound.play()
                    elif self.context.level == 2:
                        self.context.plate_sound.play()
                    elif self.context.level == 3:
                        self.context.laser_sound.play()
        return coords
